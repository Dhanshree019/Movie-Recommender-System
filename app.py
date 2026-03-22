import pickle
import streamlit as st
import requests
import pandas as pd 
import os 
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.environ.get("API_KEY")

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"

    try:
        response = requests.get(url, timeout=5)

        # Check status
        if response.status_code != 200:
            return 'no_image_available.jpg'

        data = response.json()

        poster_path = data.get('poster_path')

        if not poster_path:
            return 'no_image_available.jpg'  # no poster available

        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path

    except requests.exceptions.RequestException as e:
        return 'no_image_available.jpg'

def recommend(movie):
    index = movie_df[movie_df['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movie_df.iloc[i[0]].id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movie_df.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters


st.header('Movie Recommender System')
movies = pickle.load(open('movies.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

movie_df = pd.DataFrame(movies)
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_df['title'].values
)

if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie)
    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.text(recommended_movie_names[i])
            st.image(recommended_movie_posters[i])
           