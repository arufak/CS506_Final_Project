import pandas as pd
from sklearn.cluster import KMeans
from sklearn.neighbors import NearestNeighbors
from sklearn.decomposition import NMF, PCA
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.feature_selection import VarianceThreshold


class WeatherRecommender:
    def __init__(self, file_path):
        """
        Initialize the Weather Recommender with a dataset.
        """
        self.data = pd.read_csv(file_path)
        self.scaler = StandardScaler()
        self.min_max_scaler = MinMaxScaler()
        self.n_clusters = 9
        self.weather_cluster_mapping = None
        self.integrated_mapping = None
        self.reduced_features = None

    def reduce_features(self, variance_threshold, n_components):
        """
        Reduce features using VarianceThreshold and PCA.
        """
        selector = VarianceThreshold(threshold=variance_threshold)
        reduced_data = selector.fit_transform(self.data)
        pca = PCA(n_components=n_components, random_state=42)
        reduced_data = pca.fit_transform(reduced_data)
        self.reduced_features = reduced_data
        return reduced_data

    def train_kmeans(self):
        """
        Train KMeans clustering model.
        """
        kmeans = KMeans(n_clusters=self.n_clusters, random_state=42, n_init=10)
        clusters = kmeans.fit_predict(self.reduced_features)
        self.data['Cluster'] = clusters
        self.kmeans = kmeans

    def train_nearest_neighbors(self):
        """
        Train Nearest Neighbors model.
        """
        nn_model = NearestNeighbors(n_neighbors=10, metric='cosine')
        nn_model.fit(self.reduced_features)
        self.nn_model = nn_model

    def train_nmf(self):
        """
        Train Non-Negative Matrix Factorization (NMF) model.
        """
        non_negative_data = self.min_max_scaler.fit_transform(self.reduced_features)
        nmf = NMF(n_components=self.n_clusters, random_state=42, max_iter=300)
        self.weather_factors = nmf.fit_transform(non_negative_data)
        self.nmf = nmf

    def assign_weather_to_clusters(self, weather_columns):
        """
        Assign weather types to clusters based on frequency within clusters.
        """
        cluster_weather = pd.DataFrame(index=range(self.n_clusters), columns=weather_columns, data=0)
        for cluster in range(self.n_clusters):
            cluster_data = self.data[self.data['Cluster'] == cluster]
            for weather in weather_columns:
                cluster_weather.loc[cluster, weather] = cluster_data[weather].sum()

        weather_cluster_mapping = {}
        assigned_clusters = set()
        assigned_weather = set()

        for cluster in cluster_weather.index:
            most_common_weather = cluster_weather.loc[cluster].idxmax()
            if most_common_weather not in assigned_weather:
                weather_cluster_mapping[cluster] = most_common_weather
                assigned_clusters.add(cluster)
                assigned_weather.add(most_common_weather)

        self.weather_cluster_mapping = weather_cluster_mapping

    def integrate_models(self, weather_columns):
        """
        Integrate results from KMeans, Nearest Neighbors, and NMF to refine the mapping.
        """
        cluster_scores = {cluster: {weather: 0 for weather in weather_columns} for cluster in range(self.n_clusters)}

        for cluster, weather in self.weather_cluster_mapping.items():
            cluster_scores[cluster][weather] += 2

        self.integrated_mapping = {}
        for cluster in range(self.n_clusters):
            sorted_weather = sorted(cluster_scores[cluster].items(), key=lambda x: x[1], reverse=True)
            self.integrated_mapping[cluster] = sorted_weather[0][0]

    def run_pipeline(self, weather_columns):
        """
        Full pipeline: reduce features, train models, map weather to clusters.
        """
        reduced_features = self.reduce_features(0.005, 70)
        self.reduced_features = self.scaler.fit_transform(reduced_features)
        self.train_kmeans()
        self.train_nearest_neighbors()
        self.train_nmf()
        self.assign_weather_to_clusters(weather_columns)
        self.integrate_models(weather_columns)

        genre_columns = [
            'Action', 'Adventure', 'Animation', 'Comedy', 'Crime', 'Documentary',
            'Drama', 'Family', 'Fantasy', 'History', 'Horror', 'Music', 'Mystery',
            'Romance', 'Science Fiction', 'TV Movie', 'Thriller', 'War', 'Western', 'Unknown'
        ]
        final_df = self.data[genre_columns].copy()
        final_df['Genres'] = final_df.apply(lambda row: [genre for genre in genre_columns if row[genre] > 0], axis=1)
        final_df = final_df[['Genres']].copy()
        final_df['Weather'] = self.data['Cluster'].map(self.integrated_mapping)
        self.final_df = final_df  # Save for later use


# optional, merge the weather clusters with df with movie information to create a dataset for recommendation
def final_output(original_data_path, final_df, output_path, weather_columns):
    """
    Merge the final weather-cluster mapping with the original dataset and save it.

    Parameters:
    - original_data_path: str, path to the original dataset.
    - final_df: pd.DataFrame, the dataframe with the weather-cluster mapping.
    - output_path: str, path to save the merged dataset.
    - weather_columns: list, columns representing weather types to be dropped.
    """
    print("Loading original dataset...")
    original_data = pd.read_csv(original_data_path)

    print("Merging datasets...")
    merged_df = pd.merge(original_data, final_df['Weather'], how='left', left_index=True, right_index=True)
    merged_df.drop(columns=weather_columns, inplace=True)

    print(f"Saving merged dataset to {output_path}...")
    merged_df.to_csv(output_path, index=False)
    print("Final dataset saved successfully!")


# Main script execution
if __name__ == "__main__":
    file_path = 'reduced_cleaned.csv'
    original_data_path = 'MovieWithWeatherV3.csv'
    output_path = 'data_weather_mapped.csv'
    weather_columns = [
        "Clear Sky", "Few Clouds", "Scattered Clouds", "Broken Clouds",
        "Shower Rain", "Rain", "Thunderstorm", "Snow", "Mist"
    ]

    # Instantiate and run the recommender pipeline
    recommender = WeatherRecommender(file_path)
    recommender.run_pipeline(weather_columns)

    # Call the external function to merge and save the final output
    final_output(original_data_path, recommender.final_df, output_path, weather_columns)