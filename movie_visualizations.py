#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns


# In[3]:


df = pd.read_csv('data/TMDB_cleaned.csv')


# In[16]:


df.head(10)


# In[23]:


# Ensure 'release_date' is in datetime format
df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')

# Drop rows with invalid release_date values
df = df.dropna(subset=['release_date'])

# Filter the DataFrame to only include rows between the years 1900 and 2024
df = df[(df['release_date'].dt.year >= 1900) & (df['release_date'].dt.year <= 2024)]

# Create a new column for the release month
df['release_month'] = df['release_date'].dt.month


# Confirm the filtering was successful
print(df['release_date'].describe())


# Bar Graph of Genre Count per Month

# This graph shows the number of movies that were released in each month for each genre. This tells us the when each genre perfers to release thier movies. While release date doesn't tell us when users are actually watching those movies (outside of the theater), it does tell us when studios beleive each genre should be released and when they beleive poeple would perfer to watch that genre. It also tells us when the movie is in theaters which gives us information into what type of genre users go to the threaters for each month. 
# 
# Looking at this graph all the months generally have the same amount of released movies, besides for Janurary (which may be an error in the data). We also see that the genres comedy, romance and drama are consistintly the most realesed movies.  

# In[24]:


# Group data by release month and genres
genre_columns = ['genre_action', 'genre_animation', 'genre_horror', 'genre_family',
                 'genre_drama', 'genre_romance', 'genre_documentary', 'genre_science_fiction',
                 'genre_western', 'genre_fantasy', 'genre_mystery', 'genre_music',
                 'genre_adventure', 'genre_war', 'genre_thriller', 'genre_comedy',
                 'genre_crime', 'genre_tv_movie', 'genre_history']

# Summarize by month and genre
genre_counts_per_month = df.groupby('release_month')[genre_columns].sum()

# Plot each genre's count for each month
genre_counts_per_month.plot(kind='bar', stacked=True, figsize=(15, 7))
plt.title('Number of Movies by Genre and Release Month')
plt.xlabel('Release Month')
plt.ylabel('Number of Movies')
plt.xticks(ticks=range(0, 12), labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()


# Total Revenue vs. Release Date
# (both by year and by month - 2 plots)

# These graphs show the total revenue of all the movie per year and per month of when it was released. This tells us when users perfer to go to theaters to watch movies and what months are more popular to go to a theater to watch a movie. This again doesn't tell us information about watching movies at home since we only have the release date. 
# 
# In the second graph we can see that total reveunue for months May, June, July, adn December and higher than the rest. This makes sense since May, June July is the summer and users like to go out summer nights since the nights are loner, there's no school, and poeple take time off during that time. December also makes sence since again people have off from work or school and they are speanding it with thier family and this is a good family activity. 

# In[25]:


# Ensure 'release_date' is in datetime format
df['release_date'] = pd.to_datetime(df['release_date'])

# Sort by release date and plot
df_sorted = df.sort_values('release_date')
plt.figure(figsize=(15, 7))
plt.plot(df_sorted['release_date'], df_sorted['revenue'], color='green')
plt.title('Total Revenue Over Time')
plt.xlabel('Release Date')
plt.ylabel('Revenue (in dollars)')
# plt.xlim(left=1900,right=2024)
plt.grid(True)
plt.show()


# Summarize total revenue by month
revenue_per_month = df.groupby('release_month')['revenue'].sum()

# Plot
plt.figure(figsize=(15, 7))
sns.barplot(x=revenue_per_month.index, y=revenue_per_month.values, palette='viridis')
plt.title('Total Revenue by Release Month')
plt.xlabel('Release Month')
plt.ylabel('Total Revenue')
plt.xticks(ticks=range(0, 12), labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
plt.show()



# Vote Average/Vote Count vs. Release Date (year)
# 

# In these graphs we see the vote averge and vote count per each movie compared to the realese year and month. Although, the vote avg and vote count does not tell us when the user voted for the movie and it doesn't nessesarily mean they voted for it when it was released, it makes sense that a good portion of the votes were when the movie was released since that it when it is being talked about and when poeple are more likely to watch it. 

# In[ ]:


# Plot vote average
plt.figure(figsize=(15, 7))
plt.plot(df_sorted['release_date'], df_sorted['vote_average'], label='Vote Average', color='blue')
plt.title('Vote Average Over Time')
plt.xlabel('Release Date')
plt.ylabel('Vote Average')
plt.grid(True)
plt.legend()
plt.show()

# Plot vote count
plt.figure(figsize=(15, 7))
plt.plot(df_sorted['release_date'], df_sorted['vote_count'], label='Vote Count', color='orange')
plt.title('Vote Count Over Time')
plt.xlabel('Release Date')
plt.ylabel('Vote Count')
plt.grid(True)
plt.legend()
plt.show()



# Vote Average/Vote Count vs. Release Date (monthly)
# 

# While the same from the above graphs apply here, that the vote counts may not be from when the movie is released, we see here the amount of votes per each month (for when it was released). While the averge vote there is not much difference between the months, we see in the total vote count that the same months as the most released months, May, June, July, and December have the most about of total vote counts, which makes sense since porpotionally they have the most movies. 

# In[26]:


# Average vote average and vote count by release month
vote_avg_per_month = df.groupby('release_month')['vote_average'].mean()
vote_count_per_month = df.groupby('release_month')['vote_count'].mean()

# Plot vote average
plt.figure(figsize=(15, 7))
sns.barplot(x=vote_avg_per_month.index, y=vote_avg_per_month.values, color='skyblue')
plt.title('Average Vote Average by Release Month')
plt.xlabel('Release Month')
plt.ylabel('Vote Average')
plt.xticks(ticks=range(0, 12), labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
plt.show()

# Plot vote count
plt.figure(figsize=(15, 7))
sns.barplot(x=vote_count_per_month.index, y=vote_count_per_month.values, color='lightgreen')
plt.title('Average Vote Count by Release Month')
plt.xlabel('Release Month')
plt.ylabel('Vote Count')
plt.xticks(ticks=range(0, 12), labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
plt.show()


# Vote Average/Vote Count vs. Genre (year)
# 

# This shows us the total amount of votes per genre and shows us which genres are more popular, although no one gnere is that much more than the rest in the averge count, but in the total count we see a couple of genres that are much more popular and a couple that are not very popular. 

# In[22]:


# Melt the data for genres to facilitate grouped plotting
genres_melted = df.melt(id_vars=['vote_average', 'vote_count'], value_vars=genre_columns, 
                        var_name='genre', value_name='is_genre')

# Filter to keep only rows where the genre is present
genres_melted = genres_melted[genres_melted['is_genre'] == 1]

# Plot vote average by genre
plt.figure(figsize=(15, 7))
sns.boxplot(data=genres_melted, x='genre', y='vote_average')
plt.title('Vote Average by Genre')
plt.xticks(rotation=90)
plt.show()

# Plot vote count by genre
plt.figure(figsize=(15, 7))
sns.boxplot(data=genres_melted, x='genre', y='vote_count')
plt.title('Vote Count by Genre')
plt.xticks(rotation=90)
plt.show()


# Vote Average/Vote Count vs. Genre (monthly)
# 

# This shows us the vote avg per month for each genre so that we can see when it is more popular for users to watch each genre. 

# In[27]:


# Melt data for easier grouping
genres_melted = df.melt(id_vars=['release_month', 'vote_average', 'vote_count'], value_vars=genre_columns, 
                        var_name='genre', value_name='is_genre')

# Filter to keep only rows where the genre is present
genres_melted = genres_melted[genres_melted['is_genre'] == 1]

# Plot vote average by genre and release month
plt.figure(figsize=(20, 10))
sns.boxplot(data=genres_melted, x='release_month', y='vote_average', hue='genre')
plt.title('Vote Average by Genre and Release Month')
plt.xlabel('Release Month')
plt.ylabel('Vote Average')
plt.xticks(ticks=range(0, 12), labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()


# In[ ]:




