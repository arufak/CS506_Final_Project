import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
import os

# Load the CSV file
df = pd.read_csv("data/Movie Genre based on Weather (Responses) - Form Responses 1.csv")

# Weather categories
weather_columns = ["Sunny (summer)", "Rainy ", "Snowy (winter)", "Cloudy/Overcast", "Storm / Lightning"]

# Create necessary directories for output if they don't exist
os.makedirs("images/form", exist_ok=True)
os.makedirs("html", exist_ok=True)

# Helper Functions
def plot_pie_chart(data, title, filename):
    """Creates a pie chart."""
    plt.figure(figsize=(8, 8))
    colors = plt.cm.tab20c(range(len(data)))
    plt.pie(data.values, labels=data.index, autopct='%1.1f%%', startangle=140, colors=colors)
    plt.title(title, fontsize=14, fontweight='bold')
    plt.savefig(f"images/form/{filename}", dpi=300)
    plt.show()

def plot_bar_chart(data, title, xlabel, ylabel, filename, rotation=45):
    """Creates a bar chart."""
    plt.figure(figsize=(10, 6))
    data.plot(kind='bar', color='skyblue', figsize=(10, 6))
    plt.title(title, fontsize=14, fontweight='bold')
    plt.xlabel(xlabel, fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.xticks(rotation=rotation)
    plt.tight_layout()
    plt.savefig(f"images/form/{filename}", dpi=300)
    plt.show()

def plot_heatmap(data, title, filename):
    """Creates a heatmap."""
    plt.figure(figsize=(10, 6))
    sns.heatmap(data, annot=True, fmt='d', cmap="YlGnBu", cbar_kws={'label': 'Genre Frequency'})
    plt.title(title, fontsize=14, fontweight='bold')
    plt.xlabel("Genres", fontsize=12, fontweight='bold')
    plt.ylabel("Weather Conditions", fontsize=12, fontweight='bold')
    plt.tight_layout()
    plt.savefig(f"images/form/{filename}", dpi=300)
    plt.show()

def plot_stacked_bar(data, title, filename):
    """Creates a stacked bar chart."""
    data.plot(kind="bar", stacked=True, figsize=(10, 6), colormap="tab20c")
    plt.xlabel("Weather Conditions", fontsize=12, fontweight='bold')
    plt.ylabel("Genre Frequency", fontsize=12, fontweight='bold')
    plt.title(title, fontsize=14, fontweight='bold')
    plt.xticks(rotation=45, fontsize=10, ha="right")
    plt.legend(title="Genres", bbox_to_anchor=(1.05, 1), loc="upper left", fontsize=10)
    plt.tight_layout()
    plt.savefig(f"images/form/{filename}", dpi=300)
    plt.show()

def plot_interactive_radar(data, title, filename):
    """Creates an interactive radar chart."""
    categories = data.columns.tolist()
    traces = []
    for genre in data.index:
        values = data.loc[genre].tolist() + [data.loc[genre].iloc[0]]
        traces.append(go.Scatterpolar(r=values, theta=categories + [categories[0]], fill='toself', name=genre))

    fig = go.Figure(data=traces, layout=go.Layout(title=title, polar=dict(radialaxis=dict(visible=True)), showlegend=True))
    # plt.savefig("images/form/form_interactive_radar_chart.png", dpi=300)
    fig.write_html(f"html/{filename}")
    fig.show()

# 1. Pie chart: Does weather affect movie genre?
weather_affect_counts = df["Does the weather affect what genre of movie you watch?"].value_counts()
plot_pie_chart(weather_affect_counts, "Does the weather affect what genre of movie you watch?", "pie_weather_affect_genere_answers.png")

# 2. Bar chart: Genre popularity during each weather condition
for weather in weather_columns:
    genre_counts = df[weather].str.split(', ').explode().value_counts()
    plot_bar_chart(genre_counts, f"Popular Genres During {weather}", "Genres", "Count", f"popular_genres_during_{weather.replace(' ', '_').replace('/', '_')}.png")

# 3. Combined genre counts for all weather conditions (heatmap and stacked bar)
genre_counts = {weather: Counter() for weather in weather_columns}
for weather in weather_columns:
    for genres in df[weather]:
        if pd.notna(genres):
            genre_counts[weather].update([genre.strip() for genre in genres.split(',')])

genre_df = pd.DataFrame(genre_counts).fillna(0).astype(int).T
plot_heatmap(genre_df, "Genre Popularity Across Weather Conditions", "genre_popularity_heatmap.png")
plot_stacked_bar(genre_df, "Stacked Bar: Genre Popularity Across Weather Conditions", "stacked_bar_chart.png")

# 4. Radar chart: Genre popularity
plot_interactive_radar(genre_df.T, "Interactive Radar Chart: Genre Popularity", "form_interactive_radar_chart.html")

# 5. Sunburst chart: Weather, genre, and movie preferences
sunburst_data = []
for weather in weather_columns:
    for _, row in df.iterrows():
        if pd.notna(row[weather]):
            genres = row[weather].split(', ')
            for genre in genres:
                sunburst_data.append({'Weather': weather, 'Genre': genre.strip(), 'Response': row["Does the weather affect what genre of movie you watch?"]})

sunburst_df = pd.DataFrame(sunburst_data)
fig = px.sunburst(sunburst_df, path=['Weather', 'Genre', 'Response'], title="Sunburst Chart: Weather, Genre, and Movie Preferences", color='Response')
fig.write_html("html/form_answers_sunburst_chart.html")
# plt.savefig("images/form/form_answers_sunburst_chart.png", dpi=300)
fig.show()

# 6. Sankey diagram: Genre preferences across weather conditions
sankey_data = []
for _, row in df.iterrows():
    for weather in weather_columns:
        if pd.notna(row[weather]):
            genres = row[weather].split(', ')
            for genre in genres:
                sankey_data.append({'Source': weather, 'Target': genre.strip(), 'Value': 1})

sankey_df = pd.DataFrame(sankey_data)
sankey_aggregated = sankey_df.groupby(['Source', 'Target'], as_index=False).sum()

all_nodes = list(set(sankey_aggregated['Source']).union(set(sankey_aggregated['Target'])))
source_indices = [all_nodes.index(source) for source in sankey_aggregated['Source']]
target_indices = [all_nodes.index(target) for target in sankey_aggregated['Target']]

sankey_fig = go.Figure(data=[go.Sankey(
    node=dict(pad=15, thickness=20, line=dict(color="black", width=0.5), label=all_nodes),
    link=dict(source=source_indices, target=target_indices, value=sankey_aggregated['Value'])
)])
sankey_fig.update_layout(title_text="Sankey Diagram: Genre Preferences Across Weather Conditions", font_size=12)
# plt.savefig("images/form/form_genre_prefrences_sankey_diagram.png", dpi=300)
sankey_fig.write_html("html/form_genre_prefrences_sankey_diagram.html")
sankey_fig.show()

def plot_bubble_chart(df):
    """Plot a bubble chart of genre frequency by weather conditions."""
    transformed_data = []
    for _, row in df.iterrows():
        for weather in weather_columns:
            if pd.notna(row[weather]):  # Avoid NaN values
                genres = row[weather].split(', ')  # Split genres by comma
                for genre in genres:
                    transformed_data.append({
                        'Weather': weather,
                        'Genre': genre.strip(),  # Remove any extra spaces
                        'Frequency': 1  # Count each occurrence
                    })

    # Create a new DataFrame with aggregated data
    transformed_df = pd.DataFrame(transformed_data)
    bubble_data = transformed_df.groupby(['Weather', 'Genre'], as_index=False).count()
    bubble_data['Avg_Rating'] = 4.0  # Example static value, replace with actual metric if available

    # Create the bubble chart
    fig = px.scatter(
        bubble_data,
        x='Weather',                # X-axis: Weather
        y='Genre',                  # Y-axis: Genre
        size='Frequency',           # Bubble size: Frequency of the genre
        color='Avg_Rating',         # Bubble color: Average rating (replace with your metric)
        hover_name='Genre',         # Add genre info on hover
        title="Bubble Chart: Genre Frequency by Weather",
        labels={'Frequency': 'Bubble Size'},
        size_max=40                 # Max bubble size
    )

    # Save the bubble chart
    # plt.savefig("images/form/genre_frequency_bubble_chart.png", dpi=300)
    fig.write_html("html/form_answers_genre_frequency_bubble_chart.html")
    fig.show()

def plot_bar_chart(genre_counts):
    """Plot a bar chart of genre popularity across weather conditions."""
    genre_df = pd.DataFrame(genre_counts).fillna(0).astype(int)

    plt.figure(figsize=(12, 6))
    genre_df.plot(kind='bar', figsize=(14, 8), width=0.8)
    plt.title("Genre Popularity Across Weather Conditions", fontsize=16, fontweight='bold')
    plt.xlabel("Genres", fontsize=14)
    plt.ylabel("Frequency", fontsize=14)
    plt.xticks(rotation=45, fontsize=12)
    plt.legend(title="Weather Conditions", fontsize=12)
    plt.tight_layout()
    plt.savefig("images/form/genre_popularity_bar_chart.png", dpi=300)
    plt.show()


def plot_pie_charts(df):
    """Plot pie charts for genre proportions in each weather condition."""
    for weather_condition in weather_columns:
        genre_counter = Counter()
        for genres in df[weather_condition].dropna():
            genre_counter.update([genre.strip() for genre in genres.split(',')])

        labels = genre_counter.keys()
        sizes = genre_counter.values()

        plt.figure(figsize=(8, 8))
        colors = plt.cm.tab20c(range(len(labels)))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors)
        plt.title(f"Genre Popularity for {weather_condition}", fontsize=14, fontweight='bold')
        plt.savefig(f"images/form/pie_chart_{weather_condition.replace(' ', '_').replace('/', '_')}.png", dpi=300)
        plt.show()


all_genres = set()
genre_matrix = {weather: Counter() for weather in weather_columns}
for weather in weather_columns:
    for genres in df[weather].dropna():
        genre_list = [g.strip() for g in genres.split(',')]
        all_genres.update(genre_list)
        genre_matrix[weather].update(genre_list)

plot_bar_chart(genre_matrix)  # Bar Chart
plot_pie_charts(df)  # Pie Charts
plot_bubble_chart(df)  # Bubble Chart
