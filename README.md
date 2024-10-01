# CS506_Final_Project

# Analyzing the Influence of Social Media Sentiment on Stock Price Movements for Popular Student Stocks

## Our Team
- **Arufa Khanom** - Product Manager ([arufak@bu.edu](mailto:arufak@bu.edu))
- **Arien Amin** - Front-End Developer ([aramin@bu.edu](mailto:aramin@bu.edu))
- **Justin Liao** - Data Engineer ([liaoju@bu.edu](mailto:liaoju@bu.edu))
- **Kaiyue Shen** - Data Scientist ([kaiyue18@bu.edu](mailto:kaiyue18@bu.edu))
- **Temima Muskin** - Data Visualization Specialist ([tsmuskin@bu.edu](mailto:tsmuskin@bu.edu))

## Project Description
This project aims to analyze the correlation between social media sentiment (specifically from Twitter) and stock price movements for popular stocks among college students, such as those in the tech and retail sectors. Our goal is to explore whether social media sentiment can help explain or predict trends in stock prices over time.

### Goals
- Investigate the correlation between Twitter sentiment and stock price movements for selected popular stocks among college students.
- Identify patterns rather than focus on making precise predictions.
  
### Secondary Goals
- Implement basic analysis on collected Twitter data.
- Visualize the relationship between trends and stock price movements.
- Build an interactive dashboard for exploration.

## Data Collection
- **Twitter Data**: We will collect tweets related to specific stocks using the Twitter API. Keywords will include stock ticker symbols, company names, and relevant hashtags for each stock.
- **Stock Price Data**: Historical stock price data will be gathered from Yahoo Finance for the same time period, covering at least one month of activity.

## Data Cleaning
- **Twitter Data**: Preprocess the tweets by removing irrelevant information (e.g., URLs, mentions, stopwords) and normalizing the text (e.g., lowercasing, removing punctuation).
- **Stock Data**: Ensure consistency in date ranges and handle outliers or missing values in the stock price data.

## Feature Extraction
- **Sentiment Scores**: Perform sentiment analysis on the collected tweets using VADER or TextBlob, assigning sentiment scores (positive, neutral, or negative) to each tweet.
- **Stock Features**: Extract stock features such as daily closing price, daily volume, and price changes to analyze their relationship with sentiment trends.

## Data Visualization
- **Correlation Plots**: Create scatter plots and line charts to visualize sentiment scores alongside stock price movements.
- **Word Clouds**: Generate word clouds to show the most common keywords associated with each stock.
- **Interactive Dashboard**: Build an interactive dashboard using Plotly or Dash for real-time exploration of sentiment and stock data.

## Modeling
- **Basic Correlation Analysis**: Correlate the average daily sentiment score with daily stock price changes to identify significant patterns.
- **Time Series Models**: If time permits, explore time series modeling (e.g., ARIMA) to assess how sentiment scores influence future stock price movements.

## Test Plan
- **Data Split**: Hold out 20% of stock data for testing. Training will be performed on the data collected over one month.
- **Validation**: Validate model performance using correlation metrics or other appropriate evaluation techniques based on the modeling approach.

## Role Descriptions

- **Product Manager**: Manages project goals, timelines, and deliverables. Acts as the main point of contact for stakeholders, ensuring team collaboration and smooth execution. Oversees quality assurance, GitHub documentation, and the final presentation.
  
- **Data Engineer**: Responsible for collecting and cleaning data from Twitter and Yahoo Finance, ensuring the data is structured for analysis. Sets up the Twitter API, cleans stock price data, and normalizes both datasets.

- **Data Scientist**: Handles sentiment analysis and correlation analysis. Explores potential time series models and identifies key insights from the data.

- **Data Visualization Specialist**: Creates visualizations such as correlation plots, word clouds, and the interactive dashboard. Collaborates with the Data Scientist to ensure effective representation of analysis results.

- **Front-End Developer**: Builds and maintains the interactive dashboard using Plotly or Dash. Ensures the dashboard is user-friendly and enables interactive data exploration.

## Team Expectations
- **Data Engineer** & **Data Scientist**: Collaborate on data collection and cleaning. Once the data is prepared, they will work together on sentiment analysis and correlation studies.
  
- **Data Visualization Specialist** & **Front-End Developer**: Work closely with the Data Scientist to visualize the analysis. The Visualization Specialist will start preparing charts while the Front-End Developer sets up the dashboard framework.

- **Product Manager**: Coordinates efforts, aligns tasks with the overall timeline, and ensures smooth communication across the team.
