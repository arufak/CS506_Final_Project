import matplotlib.pyplot as plt
from wordcloud import WordCloud
import seaborn as sns
import plotly.express as px
from final_model import WeatherRecommender
import matplotlib.pyplot as plt
import seaborn as sns


def plot_top_genres(final_df):
    """
    Plot the top genre per weather condition.
    """
    # Calculate the top genre per weather condition
    top_genres = final_df.explode('Genres').groupby(['Weather', 'Genres']).size().reset_index(name='Frequency')
    top_genre_per_weather = top_genres.loc[top_genres.groupby('Weather')['Frequency'].idxmax()]
    
    plt.figure(figsize=(10, 6))
    bars = plt.bar(
        top_genre_per_weather['Weather'], 
        top_genre_per_weather['Frequency'], 
        color="skyblue", 
        alpha=0.8
    )

    for bar, genre in zip(bars, top_genre_per_weather['Genres']):
        plt.text(
            bar.get_x() + bar.get_width() / 2, 
            bar.get_height() + 0.01, 
            genre, 
            ha="center", 
            va="bottom", 
            fontsize=10, 
            color="darkblue"
        )

    plt.title("Predicted Top Genre per Weather Condition", fontsize=14)
    plt.xlabel("Weather", fontsize=12)
    plt.ylabel("Frequency", fontsize=12)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig("images/predicted/predicted_genre_per_weather.png", dpi=300, bbox_inches='tight')
    plt.show()

def plot_top_k_genres(final_df, k=3):
    """
    Plot top-k genres per weather as a stacked bar chart. Can change k. 
    """
    top_genres = final_df.explode('Genres').groupby(['Weather', 'Genres']).size().reset_index(name='Frequency')
    # top_k = top_genres.groupby('Weather').apply(lambda x: x.nlargest(k, 'Frequency')).reset_index(drop=True)
    top_k = (
        top_genres.groupby('Weather', group_keys=False)
        .apply(lambda x: x.nlargest(k, 'Frequency'))
        .reset_index(drop=True)
    )

    pivot_data = top_k.pivot(index='Weather', columns='Genres', values='Frequency').fillna(0)
    pivot_data.plot(kind='bar', stacked=True, figsize=(12, 6), colormap='tab20')

    plt.title(f"Top {k} Predicted Genres per Weather Condition", fontsize=16)
    plt.xlabel("Weather", fontsize=14)
    plt.ylabel("Frequency", fontsize=14)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.legend(title="Genres", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.savefig("images/predicted/top_k_predicted_genres_per_weather.png", dpi=300, bbox_inches='tight')
    plt.show()



def plot_wordclouds(final_df):
    """
    Generate and display a word cloud for each weather condition.
    """
    genre_counts_by_weather = final_df.explode('Genres').groupby(['Weather', 'Genres']).size().reset_index(name='Frequency')
    
    for weather in genre_counts_by_weather['Weather'].unique():
        weather_data = genre_counts_by_weather[genre_counts_by_weather['Weather'] == weather]
        wordcloud_data = dict(zip(weather_data['Genres'], weather_data['Frequency']))

        wordcloud = WordCloud(width=800, height=300, background_color='white').generate_from_frequencies(wordcloud_data)

        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title(f"Word Cloud for '{weather}'", fontsize=16)
        plt.savefig("images/predicted/wordclouds/word_cloud_" +weather+ ".png", dpi=300, bbox_inches='tight')
        plt.show()


def plot_heatmap(final_df):
    """
    Generate a heatmap of genre frequencies by weather.
    """
    genre_counts_by_weather = final_df.explode('Genres').groupby(['Weather', 'Genres']).size().unstack(fill_value=0)

    plt.figure(figsize=(12, 6))
    sns.heatmap(genre_counts_by_weather, annot=True, fmt=".0f", cmap="Blues", cbar_kws={'label': 'Frequency'})
    plt.title("Heatmap of Genre Frequencies by Weather", fontsize=16)
    plt.ylabel("Weather")
    plt.xlabel("Genres")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig("images/predicted/genre_frequencies_heatmap.png", dpi=300, bbox_inches='tight')
    plt.show()


def plot_avg_popularity_bar(final_df):
    """
    Plot the average popularity of genres by weather as a grouped bar plot.

    Parameters:
    - final_df: pd.DataFrame, DataFrame with columns ["Weather", "Genres"] and optionally "Popularity".
    - save_path: str, optional path to save the plot as an image.
    """
    # Explode the genres list into individual rows
    exploded_df = final_df.explode("Genres")

    # Generate dummy "Popularity" column for visualization if not provided
    if "Popularity" not in exploded_df.columns:
        exploded_df["Popularity"] = 1  # Set popularity to 1 for equal weighting

    # Calculate average popularity
    avg_popularity = exploded_df.groupby(["Weather", "Genres"])["Popularity"].mean().reset_index()

    # Plot grouped bar chart
    plt.figure(figsize=(12, 6))
    sns.barplot(data=avg_popularity, x="Weather", y="Popularity", hue="Genres", errorbar=None)
    plt.title("Average Popularity by Genre for Each Weather", fontsize=16)
    plt.xlabel("Weather", fontsize=14)
    plt.ylabel("Average Popularity", fontsize=14)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.legend(title="Genre", bbox_to_anchor=(1.05, 0.5), loc='center left')

    # Save or display the plot
    plt.savefig("images/predicted/avg_popularity.png", dpi=300, bbox_inches='tight')
    plt.show()


def plot_avg_popularity_stacked_bar(final_df):
    """
    Plot the average popularity of genres by weather as a stacked bar chart.

    Parameters:
    - final_df: pd.DataFrame, DataFrame with columns ["Weather", "Genres"] and optionally "Popularity".
    - save_path: str, optional path to save the plot as an image.
    """
    # Explode the genres list into individual rows
    exploded_df = final_df.explode("Genres")

    # Generate dummy "Popularity" column for visualization if not provided
    if "Popularity" not in exploded_df.columns:
        exploded_df["Popularity"] = 1  # Set popularity to 1 for equal weighting

    # Calculate average popularity
    avg_popularity = exploded_df.groupby(["Weather", "Genres"])["Popularity"].mean().reset_index()

    # Pivot data for stacked bar chart
    pivot_table = avg_popularity.pivot(index="Weather", columns="Genres", values="Popularity").fillna(0)

    # Plot stacked bar chart
    pivot_table.plot(kind="bar", stacked=True, figsize=(12, 6), colormap='tab20', width=0.7)
    plt.title("Average Popularity by Genre for Each Weather", fontsize=16)
    plt.xlabel("Weather", fontsize=14)
    plt.ylabel("Average Popularity", fontsize=14)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.legend(title="Genre", bbox_to_anchor=(1.05, 0.5), loc='center left')

    plt.savefig("images/predicted/avg_popularity_stacked.png", dpi=300, bbox_inches='tight')
    plt.show()


def plot_radar_chart(final_df):
    """
    Generate a radar chart for genre frequencies across weather conditions.
    """
    genre_counts_by_weather = final_df.explode('Genres').groupby(['Weather', 'Genres']).size().unstack(fill_value=0).reset_index()
    radar_data = genre_counts_by_weather.melt(id_vars=['Weather'], var_name="Genre", value_name="Frequency")

    fig = px.line_polar(
        radar_data,
        r="Frequency",
        theta="Genre",
        color="Weather",
        line_close=True,
        title="Radar Chart of Genre Frequencies Across Weather Conditions"
    )

    fig.update_traces(fill='toself', hoverinfo="all")
    fig.write_html("html/predicted_interactive_genre_popularity_radar_chart.html")
    fig.show()


def plot_sunburst_chart(final_df):
    """
    Generate a sunburst chart of genre frequencies by weather.
    """
    genre_counts_by_weather = final_df.explode('Genres').groupby(['Weather', 'Genres']).size().reset_index(name='Frequency')

    fig = px.sunburst(
        genre_counts_by_weather,
        path=['Weather', 'Genres'],
        values='Frequency',
        color='Weather',
        title="Sunburst Chart of Genres by Weather"
    )

    fig.write_html("html/predicted_sunburst_chart.html")
    fig.show()


file_path = 'data/reduced_cleaned.csv'
original_data_path = 'data/MovieWithWeatherV3.csv'
output_path = 'data/data_weather_mapped.csv.gz'
weather_columns = [
    "Clear Sky", "Few Clouds", "Scattered Clouds", "Broken Clouds",
    "Shower Rain", "Rain", "Thunderstorm", "Snow", "Mist"
]

# Instantiate and run the recommender pipeline
recommender = WeatherRecommender(file_path)
recommender.run_pipeline(weather_columns)

# Use the processed DataFrame for visualizations
final_df = recommender.final_df

# Call visualization functions
plot_top_genres(final_df)
plot_top_k_genres(final_df, k=3)
plot_wordclouds(final_df)
plot_heatmap(final_df)
plot_radar_chart(final_df)
plot_sunburst_chart(final_df)
plot_avg_popularity_bar(final_df)
plot_avg_popularity_stacked_bar(final_df)
