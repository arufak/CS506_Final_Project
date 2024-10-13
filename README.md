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

## Data Cleaning
The collected data will be pre-processed to handle missing values, inconsistencies, and irrelevant information. The weather data will be standardized to ensure uniformity, and only relevant movie information (genre, ratings) will be extracted and cleaned from TMDB API responses.

## Feature Extraction
- **Weather Features**: Weather conditions such as "rainy", "sunny", "snowy", "cloudy", and temperature ranges will be extracted and categorized for use in the recommendation model.
- **Movie Features**: Movies will be grouped based on genre, popularity, and viewer ratings to associate specific movies with weather conditions.

## Data Visualization
- **Bar Charts**: A key visual will show the distribution of recommended movie genres for different weather conditions, highlighting patterns (e.g., comedy for sunny weather, drama for rainy weather).
- **Time-Series Plots**: Weather patterns over time will be plotted alongside trends in movie recommendations to analyze how seasonal or long-term weather changes influence the type of movies recommended.

## Modeling
The recommendation system will be built using scikit-learn. It will be trained on historical weather and movie data to map specific weather conditions to appropriate movie genres (e.g., cozy movies for rainy days, action-packed movies for sunny days). We may explore clustering or decision tree models to analyze patterns in the data.

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

