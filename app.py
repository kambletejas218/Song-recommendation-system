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

# Placeholder image for missing images
MISSING_IMAGE_URL = "path_to_your_missing_image.jpg"

# Add custom CSS for styling
st.markdown(
    """
    <style>
    body {
        font-family: "Times New Roman", Times, serif;
        color: var(--text-color);
        background-color: var(--background-color);
    }
    h1 {
        font-size: 3em;
        font-weight: bold;
        color: var(--title-color);
        text-align: center;
    }
    p {
        font-size: 1.2em;
        color: var(--description-color);
        text-align: center;
    }
    .stButton>button {
        font-family: "Times New Roman", Times, serif;
        font-size: 1em;
        background-color: var(--button-background);
        color: var(--button-text);
        border-radius: 5px;
        padding: 10px 20px;
        border: none;
    }
    .stButton>button:hover {
        background-color: var(--button-hover-background);
    }
    .stSelectbox>div>div {
        font-family: "Times New Roman", Times, serif;
        font-size: 1em;
    }
    .spotify-box {
        margin-top: 10px;
        padding: 10px;
        background-color: var(--button-background);
        color: var(--button-text);
        text-align: center;
        border-radius: 5px;
        font-weight: bold;
        display: inline-block;
    }
    .spotify-box a {
        color: white;
        text-decoration: none;
    }
    :root {
        --background-color: #fafafa; /* Lightened background */
        --text-color: #555; /* Lighter text color */
        --title-color: #e74c3c; /* Red color for title */
        --description-color: #7f8c8d; /* Subtle gray for description */
        --button-background: #3498db; /* Light blue button background */
        --button-text: white;
        --button-hover-background: #2980b9; /* Slightly darker blue for hover */
    }

    @media (prefers-color-scheme: dark) {
        :root {
            --background-color: #2c3e50; /* Darker background for dark mode */
            --text-color: #ecf0f1; /* Lighter text for dark mode */
            --title-color: #ecf0f1;
            --description-color: #bdc3c7;
            --button-background: #3498db; /* Light blue button background */
            --button-text: white;
            --button-hover-background: #2980b9;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Set the title of the app
st.markdown("<h1>TuneMate: Unleash Your Vibe🎶</h1>", unsafe_allow_html=True)

# Add a brief description
st.markdown(
    "<p><b>Receive tailored music recommendations based on your listening habits and preferences</b></p>",
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

                    if song_image:
                        st.image(song_image, width=150)  # Display image with fixed size
                    st.markdown(f"**{recommended_song}**")  # Song name below the image
                    if song_link:
                        st.markdown(f"<div class='spotify-box'><a href='{song_link}' target='_blank'>Play on Spotify</a></div>", unsafe_allow_html=True)
                else:
                    st.image("https://via.placeholder.com/150?text=No+Image+Available+🎵", width=150)  # Custom missing image
                    st.markdown(f"**{recommended_song}**")
                    st.markdown(f"<div class='spotify-box'>No Spotify link available</div>", unsafe_allow_html=True)

        # Add spacing between rows
        st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)