#!/usr/bin/env python
# coding: utf-8

# In[1]:


from google.colab import drive
drive.mount('/content/drive')


# In[2]:


import pandas as pd

file_path = '/content/drive/MyDrive/Fall\'24/CS506/FinalProject/TMDB_movie_dataset_v11.csv'
data = pd.read_csv(file_path)
print(data.head())


# In[3]:


import pandas as pd
import numpy as np
from datetime import datetime
import ast
import re

def clean_tmdb_dataset(df):
    """
    Clean TMDB movie dataset with specific handling for each column type.
    """
    # Create a copy to avoid modifying the original
    cleaned = df.copy()

    # Basic cleaning operations
    cleaned = cleaned.drop_duplicates(subset=['id'])

    # Clean numeric columns
    cleaned['vote_average'] = pd.to_numeric(cleaned['vote_average'], errors='coerce')
    cleaned['vote_count'] = pd.to_numeric(cleaned['vote_count'], errors='coerce')
    cleaned['revenue'] = pd.to_numeric(cleaned['revenue'], errors='coerce')
    cleaned['runtime'] = pd.to_numeric(cleaned['runtime'], errors='coerce')
    cleaned['popularity'] = pd.to_numeric(cleaned['popularity'], errors='coerce')

    # Calculate vote score
    vote_count_threshold = cleaned['vote_count'].quantile(0.1)
    mean_vote = cleaned['vote_average'].mean()
    cleaned['vote_score'] = cleaned.apply(
        lambda x: calculate_weighted_rating(x['vote_average'], x['vote_count'], mean_vote, vote_count_threshold)
        if pd.notnull(x['vote_average']) and pd.notnull(x['vote_count'])
        else np.nan, axis=1
    )

    # Clean dates
    cleaned['release_date'] = pd.to_datetime(cleaned['release_date'], errors='coerce')
    cleaned['release_year'] = cleaned['release_date'].dt.year
    cleaned['release_month'] = cleaned['release_date'].dt.month

    # Handle missing release years
    cleaned['release_year'] = cleaned['release_year'].fillna(-1).astype(int)

    # Clean text fields
    text_columns = ['title', 'overview', 'tagline', 'original_title']
    for col in text_columns:
        cleaned[col] = cleaned[col].fillna('')
        cleaned[col] = cleaned[col].str.strip()

    # Clean genres
    cleaned['genres'] = cleaned['genres'].fillna('')
    cleaned['genres_list'] = cleaned['genres'].apply(lambda x: [genre.strip() for genre in str(x).split(',')])
    cleaned['genre_count'] = cleaned['genres_list'].apply(len)

    # Create genre dummy variables
    all_genres = set([genre for genres in cleaned['genres_list'] for genre in genres if genre])
    for genre in all_genres:
        cleaned[f'genre_{genre.lower().replace(" ", "_")}'] = cleaned['genres_list'].apply(
            lambda x: 1 if genre in x else 0)

    # Clean production companies
    cleaned['production_companies'] = cleaned['production_companies'].fillna('')
    cleaned['production_company_count'] = cleaned['production_companies'].str.count(',') + 1

    # Clean countries and languages
    cleaned['production_countries'] = cleaned['production_countries'].fillna('')
    cleaned['spoken_languages'] = cleaned['spoken_languages'].fillna('')
    cleaned['language_count'] = cleaned['spoken_languages'].str.count(',') + 1

    # Create binary flags
    cleaned['is_english'] = cleaned['spoken_languages'].str.contains('English', case=False, na=False).astype(int)
    cleaned['is_hollywood'] = cleaned['production_countries'].str.contains('United States', case=False, na=False).astype(int)

    # Handle revenue categories
    cleaned['revenue'] = cleaned['revenue'].fillna(0)

    # Create budget levels using custom bins
    revenue_bins = [0, 1000000, 10000000, 50000000, 100000000, float('inf')]
    revenue_labels = ['very_low', 'low', 'medium', 'high', 'very_high']
    cleaned['budget_level'] = pd.cut(
        cleaned['revenue'],
        bins=revenue_bins,
        labels=revenue_labels,
        include_lowest=True
    )

    # Calculate movie age (handle missing years)
    current_year = datetime.now().year
    cleaned['movie_age'] = np.where(
        cleaned['release_year'] != -1,
        current_year - cleaned['release_year'],
        np.nan
    )

    # Handle missing values
    cleaned['runtime'] = cleaned['runtime'].fillna(cleaned['runtime'].median())
    cleaned['popularity'] = cleaned['popularity'].fillna(cleaned['popularity'].median())

    # Clean keywords
    cleaned['keywords'] = cleaned['keywords'].fillna('')
    cleaned['keyword_count'] = cleaned['keywords'].str.count(',') + 1

    # Create status dummy variables
    cleaned['is_released'] = (cleaned['status'] == 'Released').astype(int)

    # Remove adult content
    cleaned = cleaned[cleaned['adult'] == False]

    # Generate cleaning report
    decade_counts = cleaned[cleaned['release_year'] != -1]['release_year'].apply(
        lambda x: int(x//10)*10
    ).value_counts().to_dict()

    report = {
        'original_rows': len(df),
        'cleaned_rows': len(cleaned),
        'removed_rows': len(df) - len(cleaned),
        'missing_values': cleaned.isnull().sum().to_dict(),
        'unique_genres': len(all_genres),
        'avg_vote_score': cleaned['vote_score'].mean(),
        'median_runtime': cleaned['runtime'].median(),
        'total_movies_by_decade': decade_counts
    }

    return cleaned, report

def calculate_weighted_rating(vote_average, vote_count, mean_vote, min_votes):
    """
    Calculate weighted rating using IMDB's weighted rating formula
    """
    if pd.isnull(vote_average) or pd.isnull(vote_count) or vote_count + min_votes == 0:
        return np.nan

    return (vote_count / (vote_count + min_votes) * vote_average) + \
           (min_votes / (vote_count + min_votes) * mean_vote)


# In[4]:


# Clean the data
cleaned_data, report = clean_tmdb_dataset(data)
print("Cleaning Report:")
for key, value in report.items():
    print(f"{key}: {value}")

# Save the cleaned data
cleaned_file_path = '/content/drive/MyDrive/Fall\'24/CS506/FinalProject/TMDB_cleaned.csv'
cleaned_data.to_csv(cleaned_file_path, index=False)
print(f"\nCleaned data saved to: {cleaned_file_path}")

# Verify the categories
print("\nBudget level distribution:")
print(cleaned_data['budget_level'].value_counts())

