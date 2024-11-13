
# Song Recommender

[![Streamlit App](https://img.shields.io/badge/Streamlit-Live%20App-brightgreen)](https://annaapisarek-song-recommender-streamlit-app-l0x1lx.streamlit.app/) [![GitHub](https://img.shields.io/github/license/annaapisarek/song-recommender)](https://github.com/annaapisarek/song-recommender/blob/main/LICENSE)

This project is a song recommendation app built with Python and Streamlit, designed to provide song suggestions based on user preferences. 

## Features

- **Clustering-Based Recommendations**: Utilizes K-Means clustering to group songs into clusters, providing recommendations from similar clusters based on user-selected attributes.
- **Spotify Data**: 5,000 songs from the Spotify API with detailed acoustic attributes, including energy, danceability, tempo, and genre.
- **Interactive UI**: Built with Streamlit for a simple, intuitive user experience.

## Methodology

The recommendation system is based on K-Means clustering with the following setup:

- **Number of Clusters**: 4
- **Clustering Model**: KMeans with `k-means++` initialization and `random_state=42`
  
Songs were clustered based on various acoustic features and genres, enabling the app to suggest similar songs from the same cluster.



