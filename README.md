# CS506_Final_Project

# Movie Recommendation System Based on Weather

## Our Team
- **Arufa Khanom** - Product Manager (arufak@bu.edu)
- **Arien Amin** - Front-End Developer (aramin@bu.edu)
- **Justin Liao** - Data Engineer (liaoju@bu.edu)
- **Kaiyue Shen** - Data Scientist (kaiyue18@bu.edu)
- **Temima Muskin** - Data Visualization Specialist (tsmuskin@bu.edu)

## Project Goals
The goal of this project is to develop a movie recommendation system that dynamically suggests movies based on current weather conditions. The recommendation system will combine weather data from OpenWeather API with movie data from The Movie Database (TMDB) API to generate movie recommendations tailored to weather patterns. The project will practice the full data science lifecycle, incorporating data collection, data cleaning, feature extraction, visualization, and model training, while also maintaining a well-organized GitHub repository with proper documentation and testing workflow.

## Data Collection
- **Weather Data**: Collected from the OpenWeather API, which provides real-time weather information such as temperature, humidity, and weather conditions (e.g., rainy, sunny, cloudy).
- **Movie Data**: Collected from the TMDB API, providing information on genres, ratings, release dates, and user reviews of movies. This data will be used to create movie recommendations based on the current weather.

## Data Cleaning and Processing
- **Loading and Initial Inspection**: The dataset was loaded and reviewed for duplicates, missing values, and invalid entries, which helped identify the scope of cleaning required.

- **Duplicate Removal**: Duplicate entries based on the `id` column were removed to ensure each movie entry was unique.

- **Numerical Data Cleaning**:
  - Columns like `vote_average`, `vote_count`, `revenue`, `runtime`, and `popularity` were converted to numeric types. Missing or non-numeric entries were set to `NaN` and filled based on data distribution (e.g., median).
  - A custom `vote_score` was calculated using a weighted rating formula, considering the average votes and a threshold on vote count for accuracy.

- **Date Processing**:
  - The `release_date` column was standardized to a datetime format, with invalid dates set to `NaN`.
  - New columns were created: `release_year` and `release_month`, which helped categorize movies by release year and month. Missing years were filled as `-1`.

- **Text Field Cleaning**:
  - Columns like `title`, `overview`, `tagline`, and `original_title` were stripped of leading/trailing spaces, and missing values were replaced with empty strings to standardize text data.

- **Genre Extraction and Encoding**:
  - A new `genres_list` column was created by splitting genre strings into lists for easier access.
  - Genre-specific dummy variables were generated for each unique genre, making genres compatible with modeling.

- **Production Companies and Languages**:
  - Counts for production companies and languages were added, allowing insights into the diversity of production and language scope for each movie.
  - A binary `is_english` column was created to flag English-language films, while `is_hollywood` indicated whether a movie was produced in the United States.

- **Revenue and Budget Levels**:
  - Revenue values were categorized into custom budget levels (e.g., `very_low`, `low`, `medium`, `high`, `very_high`), enabling budget-based analysis. Missing values were filled as zero.

- **Additional Features**:
  - Calculated `movie_age` as the difference between the current year and the `release_year`, aiding in understanding the dataset's time-based trends.
  - Count columns were added for keywords, genres, production companies, and languages, giving numerical representation to these categorical fields.
  - A `is_released` flag marked movies as released or not, standardizing the dataset based on release status.

- **Filtering for Clean Data**:
  - Entries marked as `adult` were removed, ensuring the dataset was family-friendly.
  - The final cleaning report highlighted data metrics post-cleaning, such as average vote score, median runtime, and movies count by decade.

## Feature Extraction
- **Weather Features**: Weather conditions such as "rainy", "sunny", "snowy", "cloudy", and temperature ranges will be extracted and categorized for use in the recommendation model.
- **Movie Features**: Movies will be grouped based on genre, popularity, and viewer ratings to associate specific movies with weather conditions.

## Preliminary Visualizations of Data
### Weather Influence on Genre Choice  
- **Visualization**: This pie chart answers the question, “Does the weather affect what genre of movie you watch?” The chart provides a clear breakdown, showing the percentage of individuals who consider weather when choosing a movie genre versus those who do not.  
- **Insight**: Preliminary responses reveal a trend where weather appears to influence movie-watching habits, providing a basis for analyzing genre preferences across different weather conditions.  

### Genre Preferences by Weather Condition  
- **Visualization**: Multiple bar charts illustrate the distribution of popular movie genres (e.g., action, comedy, drama) watched under specific weather conditions:  
    - **Sunny (Summer)**: Displays genre preferences in sunny or warm weather.  
    - **Rainy**: Highlights genres chosen when it’s raining, suggesting certain movies might be preferred in rainy conditions.  
    - **Snowy (Winter)**: Shows genres preferred during winter or snowy weather, potentially aligning with holiday or seasonal themes.  
    - **Cloudy/Overcast**: Explores genre choices during cloudy weather, revealing preferences for neutral weather conditions.  
    - **Storm/Lightning**: Observes genre selection during stormy weather, identifying potential patterns for more intense weather scenarios.  
- **Insight**: These visualizations suggest that weather conditions may correlate with certain genre preferences, helping identify trends that could support a recommendation model based on real-time weather.  

### Genre Count by Release Month  
- **Visualization**: A bar graph shows the count of movie releases by genre for each month, providing insight into seasonal trends. For example, family movies may peak in December, aligning with holiday releases, or summer action blockbusters might see more releases around mid-year.  
- **Insight**: This visualization indicates that certain genres are associated with specific times of the year, showing potential seasonality in movie releases. Understanding these trends can support models that recommend movies based on time-of-year preferences.  

### Release Date Analysis  
- **Data Filtering**: To ensure data accuracy, release dates are converted to a standardized datetime format, and invalid dates are removed. The data is filtered to include releases between 1900 and 2024.  
- **Visualization**: A breakdown by month of release reveals historical trends, allowing for a more granular look at genre popularity across different times.  
- **Insight**: Data filtering and date analysis ensure clean, relevant data, enabling an exploration of time-based trends in movie genres. This can help in predicting popular genres throughout the year.  

## Data Modeling Methods
### Clustering Model: K-Means
- **Purpose**: To group movies into clusters that align with specific weather conditions (e.g., adventure movies for sunny days, dramas for rainy days).
- **Method**: Using selected features (such as `vote_average`, `popularity`, `runtime`, and genre dummy variables), a K-Means algorithm was trained with five clusters to represent different weather categories.
- **Weather Mapping**: Each weather type is mapped to certain clusters:
  - *Sunny*: Clusters with movies that are upbeat or adventurous.
  - *Rainy*: Clusters featuring dramatic or introspective films.
  - *Stormy*: Clusters with intense, thrilling genres.
- **Outcome**: This clustering provides recommendations by associating specific clusters with weather conditions.

### Collaborative Filtering Model: Nearest Neighbors
- **Purpose**: To recommend similar movies based on feature similarity, leveraging collaborative filtering to provide recommendations for each weather type.
- **Method**: The Nearest Neighbors model (with cosine similarity) was trained using the feature matrix. This model finds movies that are similar to a representative movie chosen based on each weather condition.
- **Representative Movie Selection**: A seed movie representing each weather condition is selected based on relevant genre tags (e.g., *comedy* for sunny weather, *drama* for rainy weather).
- **Outcome**: The model generates recommendations by finding movies with similar attributes to the seed movie, based on the target weather.

### Matrix Factorization Model: Non-negative Matrix Factorization (NMF)
- **Purpose**: To uncover latent features within the genre matrix, identifying underlying patterns that correspond to different weather conditions.
- **Method**: Using genre columns, NMF was applied to extract 10 latent components. Each component represents a blend of genres or attributes that correlate with specific weather preferences.
- **Weather Components**: Each weather type is mapped to relevant components:
  - *Sunny*: Components associated with upbeat or light-hearted genres.
  - *Rainy*: Components tied to dramatic or emotional genres.
  - *Stormy*: Components reflecting intense or thriller genres.
- **Outcome**: This model provides recommendations by analyzing these latent components and scoring movies based on their alignment with weather-related patterns.

### Ensemble Recommendation Approach
- **Purpose**: To enhance recommendation robustness by combining outputs from the clustering, collaborative filtering, and matrix factorization models.
- **Method**: Recommendations from each model are aggregated, with movies appearing in multiple model outputs given higher priority.
- **Outcome**: This ensemble method ensures that recommendations align more closely with each weather condition by synthesizing insights across multiple models.

## Preliminary Results
- **Clustering Model (K-Means)**: The K-Means clustering model successfully grouped movies into clusters that align with different weather conditions. Each cluster shows distinct genre preferences:
  - *Sunny* clusters contain upbeat and adventure genres.
  - *Rainy* clusters show a higher concentration of drama and romance movies.
  - *Stormy* clusters primarily include thrillers and intense genres.
  - **Result**: This pattern supports our hypothesis that different weather conditions influence genre preferences, validating the effectiveness of clustering for weather-based recommendations.

- **Collaborative Filtering (Nearest Neighbors)**: The collaborative filtering model effectively identified movies similar to weather-representative movies using cosine similarity.
  - *Sunny*: Similar movies to popular comedies and family films.
  - *Rainy*: Recommendations tend to focus on dramas and romantic movies.
  - *Stormy*: Recommendations include thrillers and sci-fi movies, suitable for stormy weather.
  - **Result**: This approach confirms the value of using collaborative filtering to provide recommendations based on weather-related moods.

- **Matrix Factorization (NMF)**: By extracting latent factors from the genre matrix, the NMF model identified underlying patterns that align with weather types.
  - *Sunny*: Latent factors associated with genres like comedy and family.
  - *Rainy*: Factors linked with more emotional or dramatic genres.
  - *Stormy*: Factors representing thrillers and darker themes.
  - **Result**: The NMF model successfully highlights genre associations that correspond with different weather patterns, providing a new layer of insights for tailored recommendations.

- **Ensemble Approach**: The ensemble method, combining outputs from all three models, provides robust recommendations that align well with each weather condition.
  - **Result**: This blended approach ensures high-quality recommendations by leveraging the strengths of each individual model.

## Test Plan
We plan to split our dataset into training (80%) and test (20%) sets. This approach will allow us to test the recommendation system's performance on unseen data and tune the model based on the results. The model will be evaluated using accuracy metrics and user feedback (if applicable) on movie recommendations for varying weather conditions.

## Technologies & Tools
- **Python**: The primary programming language for implementing data collection, model training, and visualization.
- **APIs**: 
  - OpenWeather API for real-time weather data collection.
  - TMDB API for movie data (genres, popularity, ratings).
- **scikit-learn**: Used for building the recommendation system.
- **Matplotlib/Plotly**: Visualization tools for creating bar charts and time-series plots.
- **GitHub Actions**: For maintaining a testing workflow and ensuring code quality.
- **GitHub**: A well-organized GitHub repository will house the project, including detailed documentation, code, and visualizations.

## Role Description

### Product Manager
- **Responsibilities**: The project manager will oversee the overall project timeline, coordinate team meetings, manage task delegation, and ensure alignment between team members. They will also ensure the timely submission of deliverables such as the midterm report and final report, and maintain project documentation in the GitHub repository.

### Data Engineer
- **Responsibilities**: The data engineer will design and implement the data pipeline for collecting both weather and movie data. They will handle the API integrations, ensure clean and structured data is available for the rest of the team, and provide regular updates on the pipeline’s functionality. They will also work on data cleaning and standardization.

### Data Scientist
- **Responsibilities**: The data scientist will develop the core recommendation model, which involves analyzing the relationship between weather conditions and movie genres. They will work on feature extraction, model selection (e.g., clustering, decision trees), and evaluate model performance through testing. They will also ensure the model adapts to changes in weather and movie data.

### Data Visualization Specialist
- **Responsibilities**: The data visualization specialist will create visual representations of key insights. They will generate bar charts to illustrate the relationship between weather conditions and movie genres, and time-series plots to show how weather patterns influence movie recommendations over time. Their visuals will be integrated into both reports and the front-end UI.

### Front-End Developer
- **Responsibilities**: The front-end developer will design and build a user-friendly interface that fetches real-time weather data and presents relevant movie recommendations. They will integrate the recommendation model into the app, ensure a smooth user experience, and collaborate closely with the data visualization specialist to include insightful visual representations in the UI.

## Project Timeline
- **October 1**: Form groups, submit proposals, and create a GitHub repository.
- **November 5**: Submit midterm report, including data collection progress, preliminary results from the recommendation model, and initial visualizations.
- **December 10**: Submit final report, complete with final results, polished visualizations, detailed project documentation, and a functional recommendation system hosted online.

## Conclusion
This project will provide a complete walkthrough of the data science lifecycle, allowing the team to gain practical experience in data collection, modeling, visualization, and front-end development. The Movie Recommendation System will not only generate relevant movie suggestions based on weather conditions but also showcase the power of combining data from different sources to enhance user experience.

