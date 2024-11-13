import streamlit as st
import pandas as pd
import random

# Load and filter the Spotify song data
df = pd.read_csv('spotify_songs.csv')[['title', 'artist', 'cluster', 'popularity_score', 'track_id','final genre']].drop_duplicates()

# Function to search songs by title or artist
def search_songs(df, search_term, search_by='title'):
    if search_by == 'title':
        return df[df['title'].str.contains(search_term, case=False)]
    else:
        return df[df['artist'].str.contains(search_term, case=False)]

# Function to get 3 song recommendations based on cluster, popularity, genre
def get_recommendations(df, selected_song):
    song_details = df[df['title'] == selected_song]
    if not song_details.empty:
        song_details = song_details.iloc[0]
        selected_cluster = song_details['cluster']
        selected_popularity = song_details['popularity_score']
        selected_genre = song_details['final genre']

        # Filter songs by the same cluster
        cluster_recs = df[(df['cluster'] == selected_cluster) & (df['title'] != selected_song)]
        cluster_recs = cluster_recs.sample(min(1, len(cluster_recs))) if not cluster_recs.empty else pd.DataFrame()

        # Filter songs by the same genre
        genre_recs = df[(df['final genre'] == selected_genre) & (df['title'] != selected_song)]
        genre_recs = genre_recs.sample(min(1, len(genre_recs))) if not genre_recs.empty else pd.DataFrame()

        # Filter songs by the same popularity score
        popularity_recs = df[(df['popularity_score'] == selected_popularity) & (df['title'] != selected_song)]
        popularity_recs = popularity_recs.sample(min(1, len(popularity_recs))) if not popularity_recs.empty else pd.DataFrame()

        return cluster_recs, genre_recs, popularity_recs
    else:
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

# Function to display song details
def display_song_details(song_details):
    st.write(f'🎵Title: {song_details["title"]} ')
    st.write(f"👤Artist: {song_details['artist']}")
    st.write(f"🎨Genre: {song_details['final genre']}")
    st.markdown(f"[🔗 Listen on Spotify](https://open.spotify.com/track/{song_details['track_id']})")

# Function to display recommendations
def display_recommendations(cluster_recs, genre_recs, popularity_recs):
    st.header("Recommendations")

    if not cluster_recs.empty:
        st.subheader("Similar Song:")
        for _, rec in cluster_recs.iterrows():
            st.write(f'🎵Title: {rec["title"]} ')
            st.write(f"👤Artist: {rec['artist']}")
            st.markdown(f"[🔗 Listen on Spotify](https://open.spotify.com/track/{rec['track_id']})")
            st.write("***")
    else:
        st.write("No songs found in the same cluster.")

    if not genre_recs.empty:
        st.subheader("Song in the same Genre:")
        for _, rec in genre_recs.iterrows():
            st.write(f'🎵Title: {rec["title"]} ')
            st.write(f"👤Artist: {rec['artist']}")
            st.markdown(f"[🔗 Listen on Spotify](https://open.spotify.com/track/{rec['track_id']})")
            st.write("***")
    else:
        st.write("No songs found in the same genre.")

    if not popularity_recs.empty:
        st.subheader("Similarly Popular Song:")
        for _, rec in popularity_recs.iterrows():
            st.write(f'🎵Title: {rec["title"]} ')
            st.write(f"👤Artist: {rec['artist']}")
            st.markdown(f"[🔗 Listen on Spotify](https://open.spotify.com/track/{rec['track_id']})")
            st.write("***")
    else:
        st.write("No songs found with similar popularity.")

# Main function
def main():
    st.title("Song Recommender")

    # Select method for choosing a song
    selection_method = st.radio("How would you like to select a song?", ["Choose from list", "Search by title/artist", "Random song"])
    
    selected_song = None
    if selection_method == "Choose from list":
        selected_song = st.selectbox("Choose a song title from the list:", df['title'].tolist())
    elif selection_method == "Search by title/artist":
        search_term = st.text_input("Enter search term:")
        search_by = st.radio("Search by:", ["Title", "Artist"])
        if search_term:
            matches = search_songs(df, search_term, search_by.lower())
            if not matches.empty:
                selected_song = st.selectbox("Select a song:", matches['title'].tolist())
            else:
                st.write("No matches found.")
    else:  # Random song
        selected_song = random.choice(df['title'].tolist())

    # If a song is selected, display details and recommendations
    if selected_song:
        song_details = df[df['title'] == selected_song]
        if not song_details.empty:
            song_details = song_details.iloc[0]
            display_song_details(song_details)

            cluster_recs, genre_recs, popularity_recs = get_recommendations(df, selected_song)
            display_recommendations(cluster_recs, genre_recs, popularity_recs)
        else:
            st.write("Selected song not found in the dataset.")

if __name__ == "__main__":
    main()