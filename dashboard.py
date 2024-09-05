# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# Load your data 
df = pd.read_csv('final_cleaned_version.csv')  # Adjust path as needed

# Streamlit app layout
st.set_page_config(page_title="Spotify Dashboard", layout="wide")

# Title and description
st.title("Spotify Dashboard")
st.markdown("""
This interactive dashboard allows you to explore Spotify playlist data, including the most popular artists, albums, and tracks.
""")

# Sidebar filters
st.sidebar.header("Filters")
artist_filter = st.sidebar.multiselect("Select Artists", options=df['artist_name'].unique(), default=df['artist_name'].unique())
collaborative_filter = st.sidebar.radio("Collaborative Playlists", options=["All", "Collaborative", "Non-Collaborative"])

# Filter data based on sidebar inputs
if collaborative_filter != "All":
    df = df[df['collaborative'] == ("True" if collaborative_filter == "Collaborative" else "False")]

df_filtered = df[df['artist_name'].isin(artist_filter)]

# Display filtered data
st.dataframe(df_filtered)

# Visualization - Top 10 Artists by Track Count
st.subheader("Top 10 Artists by Track Count")
top_artists = df_filtered.groupby('artist_name')['track_name'].count().sort_values(ascending=False).head(10)
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x=top_artists.values, y=top_artists.index, palette='viridis', ax=ax)
ax.set_xlabel("Number of Tracks")
ax.set_ylabel("Artist")
ax.set_title("Top 10 Artists by Track Count")
st.pyplot(fig)

# Visualization - Distribution of Playlist Length
st.subheader("Distribution of Playlist Length (Number of Tracks)")
average_tracks = df_filtered['num_tracks'].mean()
fig, ax = plt.subplots(figsize=(10, 5))
sns.histplot(df_filtered['num_tracks'], bins=10, color='purple', kde=False, ax=ax)
ax.axvline(average_tracks, color='red', linestyle='--', label='Average Number of Tracks')
ax.set_xlabel('Number of Tracks')
ax.set_ylabel('Number of Playlists')
ax.legend()
st.pyplot(fig)

# Visualization - Correlation Matrix
st.subheader("Correlation Matrix")
correlation_matrix = df_filtered[['num_tracks', 'num_followers', 'num_edits', 'num_albums', 'num_artists']].corr()
fig, ax = plt.subplots(figsize=(8, 8))
sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap='coolwarm', ax=ax)
st.pyplot(fig)

# Additional sections can be added as needed...
