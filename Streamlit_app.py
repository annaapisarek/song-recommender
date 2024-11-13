import streamlit as st
import pandas as pd
import numpy as np
import random

# Load Spotify song data into a DataFrame
df = pd.read_csv('spotify_songs.csv')

#Filter the df
df = df[['title', 'artist', 'cluster', 'popularity_score','track_id']]



def search_songs(df, search_term, search_by='title'):
    """
    Search for songs by title or artist
    """
    if search_by == 'title':
        matches = df[df['title'].str.contains(search_term, case=False)]
    else:  # search_by == 'artist'
        matches = df[df['artist'].str.contains(search_term, case=False)]
    return matches


def get_recommendations(df, selected_song, n_recommendations=1):
    """
    Get song recommendations based on cluster and popularity score
    """
    # Create a copy of the DataFrame to avoid modifying the original
    df = df.copy()
    
    # Define popularity score ordering
    popularity_order = {'Low': 0, 'Medium': 1, 'High': 2, 'Highest': 3}
    
    # Get selected song details
    song_details = df[df['title'] == selected_song].iloc[0]
    selected_cluster = song_details['cluster']
    selected_popularity = song_details['popularity_score']
    
    # Get recommendation from same cluster
    cluster_matches = df[
        (df['cluster'] == selected_cluster) & 
        (df['title'] != selected_song)
    ]
    
    if not cluster_matches.empty:
        random_indices = random.sample(list(cluster_matches.index), 
                                    min(n_recommendations, len(cluster_matches)))
        cluster_recommendations = cluster_matches.loc[random_indices]
    else:
        cluster_recommendations = pd.DataFrame()
    
    # Get recommendation with same popularity score
    popularity_matches = df[
        (df['popularity_score'] == selected_popularity) & 
        (df['title'] != selected_song)
    ]
    
    if not popularity_matches.empty:
        random_indices = random.sample(list(popularity_matches.index), 
                                    min(n_recommendations, len(popularity_matches)))
        popularity_recommendations = popularity_matches.loc[random_indices]
    else:
        # If no exact matches, get closest popularity level
        df['popularity_numeric'] = df['popularity_score'].map(popularity_order)
        selected_popularity_numeric = popularity_order[selected_popularity]
        
        # Calculate absolute difference in popularity levels
        df['popularity_diff'] = abs(df['popularity_numeric'] - selected_popularity_numeric)
        min_diff = df[df['title'] != selected_song]['popularity_diff'].min()
        
        closest_matches = df[
            (df['popularity_diff'] == min_diff) & 
            (df['title'] != selected_song)
        ]
        
        random_indices = random.sample(list(closest_matches.index), 
                                     min(n_recommendations, len(closest_matches)))
        popularity_recommendations = closest_matches.loc[random_indices]
    
    return cluster_recommendations, popularity_recommendations

def display_song_details(song_details, container):
    """
    Display song details in the given container
    """
    with container:
        st.write("Selected Song Details:")
        st.write(f"🎵 **{song_details['title']}**")
        st.write(f"👤 Artist: {song_details['artist']}")
        spotify_link = f"https://open.spotify.com/track/{song_details['track_id']}"
        st.markdown(f"[🔗 Spotify link]({spotify_link})")

def display_recommendations(cluster_recs, popularity_recs, song_details):
    """
    Display recommendations in a formatted way
    """
    st.subheader("Recommendations")
    
    rec_col1, rec_col2 = st.columns(2)
    
    with rec_col1:
        st.write("🎵 Similar Song:")
        if not cluster_recs.empty:
            for _, rec in cluster_recs.iterrows():
                st.write(f"**{rec['title']}**")
                st.write(f"👤 by {rec['artist']}")
                spotify_link = f"https://open.spotify.com/track/{song_details['track_id']}"
                st.markdown(f"[🔗 Spotify link]({spotify_link})")
        else:
            st.write("No songs found in the same cluster.")
    
    with rec_col2:
        st.write("🎵 Equally popular song:")
        if not popularity_recs.empty:
            for _, rec in popularity_recs.iterrows():
                st.write(f"**{rec['title']}**")
                st.write(f"👤 by {rec['artist']}")
                spotify_link = f"https://open.spotify.com/track/{rec['track_id']}"
                st.markdown(f"[🔗 Spotify link]({spotify_link})")
        else:
            st.write("No songs found with similar popularity.")

def main():
    st.title("Song Recommender")
    
    # Set random seed for reproducibility
    random.seed(42)
    
    # Initialize session state for random song
    if 'random_song' not in st.session_state:
        st.session_state.random_song = None
    
    # Selection method
    selection_method = st.radio(
        "How would you like to select a song?",
        ["Choose from list", "Search by title/artist", "Random song"]
    )
    
    selected_song = None
    
    if selection_method == "Choose from list":
        selected_song = st.selectbox(
            "Choose a song from the list:",
            options=df['title'].tolist()
        )
    
    elif selection_method == "Search by title/artist":
        search_by = st.radio("Search by:", ["Title", "Artist"])
        search_term = st.text_input("Enter search term:")
        
        if search_term:
            matches = search_songs(df, search_term, search_by.lower())
            if not matches.empty:
                st.write(f"Found {len(matches)} matches:")
                selected_song = st.selectbox(
                    "Select a song:",
                    options=matches['title'].tolist()
                )
            else:
                st.write("No matches found.")
    
    else:  # Random song
        if st.button("Get Random Song"):
            st.session_state.random_song = random.choice(df['title'].tolist())
        selected_song = st.session_state.random_song
    
    # Only proceed if we have a selected song
    if selected_song:
        # Get and display song details
        song_details = df[df['title'] == selected_song].iloc[0]
        
        # Create columns for layout
        col1, col2 = st.columns(2)
        display_song_details(song_details, col1)
        
        # Get and display recommendations
        cluster_recs, popularity_recs = get_recommendations(df, selected_song)
        display_recommendations(cluster_recs, popularity_recs, song_details)

if __name__ == "__main__":
    main()
