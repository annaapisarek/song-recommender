
# Song Recommender

https://annaapisarek-song-recommender-streamlit-app-l0x1lx.streamlit.app/

This project is a song recommendation app built with Python and Streamlit, designed to provide song suggestions based on user preferences. 

## Features

- **Clustering-Based Recommendations**: Utilizes K-Means clustering to group songs into clusters, providing recommendations from similar clusters.
- **Genre-Based Recommendations**: Provides recommendations of songs in the similar genre.
- **Popularity-Based Recommendations**: Provides recommendations of songs in the similar popularity range.
- **Interactive UI**: Built with Streamlit for a simple, intuitive user experience.

## Methodology

The recommendation system is based on K-Means clustering with the following setup:

- **Spotify Data**: 5,000 popular songs from the Spotify API with detailed acoustic attributes, including energy, danceability, tempo, and genre.
- **Number of Clusters**: 4
- **Clustering Model**: KMeans with PCA.
  
Songs were clustered based on various acoustic features and genres, enabling the app to suggest similar songs from the same cluster.

## More details

https://docs.google.com/presentation/d/1mFU5HXllsNJHqzC5fsKceKfH1t-uTa2gDaj76bKh66o/edit?usp=sharing
