import streamlit as st
import pandas as pd
import pickle

# Function to recommend songs
def recommend(song):
    song_index = Songs[Songs['Song'] == song].index[0]
    distances = similarity[song_index]
    song_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]

    recommended_songs = []
    for i in song_list:
        recommended_songs.append(Songs.iloc[i[0]].Song)
    return recommended_songs


# Load first dataset (recommender dataset)
Songs_dict = pickle.load(open('Song_dict.pkl', 'rb'))
Songs = pd.DataFrame(Songs_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

# Load second dataset (contains song links and images)
links_images_data = pd.read_csv('Poster_Img.csv')

# Normalize the 'Song' column in the second dataset
links_images_data['Song'] = links_images_data['Song'].str.strip().str.lower()

# Set the title of the app
st.markdown("<h1>TuneMate: Unleash Your Vibe 🎶</h1>", unsafe_allow_html=True)

# Add a brief description
st.markdown(
    "<p><b>Receive tailored music recommendations based on your listening habits and preferences.</b></p>",
    unsafe_allow_html=True,
)

# Song selection from the recommender system
selected_song_name = st.selectbox("Which song do you need?", Songs['Song'].values)

# Recommend and display songs when the button is clicked
if st.button('Recommend'):
    recommendations = recommend(selected_song_name)

    # Divide recommendations into rows of 5
    for row in range(0, len(recommendations), 5):
        cols = st.columns(5)  # Create 5 columns for each row
        for idx, recommended_song in enumerate(recommendations[row:row + 5]):
            col = cols[idx]  # Assign each song to a column
            
            # Normalize the recommended song name for comparison
            normalized_song = recommended_song.strip().lower()
            
            # Fetch corresponding data from the second dataset
            song_data = links_images_data[links_images_data['Song'] == normalized_song]

            with col:
                if not song_data.empty:
                    song_link = song_data['Spotify Link'].values[0] if 'Spotify Link' in song_data else None
                    song_image = song_data['Song Image'].values[0] if 'Song Image' in song_data else None

                    st.markdown(f"**{recommended_song}**")  # Song name
                    if song_image:
                        st.image(song_image, use_column_width=True)  # Song image
                    if song_link:
                        st.markdown(f"[Play on Spotify]({song_link})")  # Spotify link
                else:
                    st.markdown(f"**{recommended_song}**")
                    st.error("No additional data available.")

        # Add spacing between rows
        st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)
