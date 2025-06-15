import streamlit as st
import pickle
import pandas as pd
import requests
import time
import base64

def fetch_movie_data(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=en-US"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3YTJjNGQwYzM4Yzc0MjdmZjQwMDk2MjQ5NTIyYWY4MyIsIm5iZiI6MTc1MDAwMjQxNi4zNTksInN1YiI6IjY4NGVlYWYwN2ExZGI5YzIxYTI5NGVjMCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.KuXwbnvA4qcb4jVErRBTHg0M9opeo2KccC74Ae39UOM"
    }
    try:
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            poster_url = "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            poster_url = "assets/more_info.jpg"  # Local fallback image
        return {
            "movie_id": data.get("id", movie_id),
            "title": data.get("title", "N/A"),
            "overview": data.get("overview", "No overview available."),
            "release_date": data.get("release_date", "N/A"),
            "vote_average": data.get("vote_average", "N/A"),
            "poster_url": poster_url,
            "genres": ", ".join([g["name"] for g in data.get("genres", [])]),
            "runtime": data.get("runtime", "N/A")
        }
    except Exception as e:
        return {
            "movie_id": movie_id,
            "title": "N/A",
            "overview": "No overview available.",
            "release_date": "N/A",
            "vote_average": "N/A",
            "poster_url": "assets/more_info.jpg",  # Local fallback image
            "genres": "N/A",
            "runtime": "N/A"
        }

movies_dict = pickle.load(open('models/movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('models/similarity.pkl', 'rb'))

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies_data = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        local_title = movies.iloc[i[0]].title
        movie_data = fetch_movie_data(movie_id)
        movie_data['title'] = local_title  # Always use local title
        recommended_movies_data.append(movie_data)
        time.sleep(0.5)  # To avoid rate limiting
    return recommended_movies_data

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

st.markdown(
    """
    <style>
    .main-title {
        font-size: 3em !important;
        color: #FF4B4B;
        font-weight: bold;
        text-align: center;
        margin-bottom: 0.5em;
    }
    .movie-card {
        background-color: #f9f9f9;
        border-radius: 12px;
        padding: 1em;
        box-shadow: 0 2px 8px rgba(0,0,0,0.07);
        margin-bottom: 1em;
        height: 100%;
    }
    .movie-title {
        font-size: 1.2em;
        font-weight: bold;
        color: #333;
        margin-bottom: 0.3em;
    }
    .movie-meta {
        color: #888;
        font-size: 0.9em;
        margin-bottom: 0.5em;
    }
    .movie-overview {
        font-size: 1em;
        color: #444;
        margin-bottom: 0.5em;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="main-title">🍿 Popcorn Picks</div>', unsafe_allow_html=True)
st.markdown("##### Select a movie you like and get recommendations with details:")

selected_movie_name = st.selectbox(
    "Select Movie",
    (movies['title'].values),
)

if st.button('Recommend'):
    recommended_movies = recommend(selected_movie_name)
    local_img_b64 = get_base64_image("assets/more_info.jpg")
    for movie in recommended_movies:
        tmdb_url = f"https://www.themoviedb.org/movie/{movie['movie_id']}"
        if movie['poster_url'] == "assets/more_info.jpg":
            img_src = f"data:image/jpeg;base64,{local_img_b64}"
        else:
            img_src = movie['poster_url']
        st.markdown(
            f"""
            <a href="{tmdb_url}" target="_blank" style="text-decoration: none; color: inherit;">
                <div class="movie-card" style="transition: box-shadow 0.2s; cursor: pointer;">
                    <div style="display: flex; gap: 2em; align-items: flex-start;">
                        <img src="{img_src}" width="180" style="border-radius:8px; box-shadow:0 2px 8px rgba(0,0,0,0.10);">
                        <div style="flex:1;">
                            <div class="movie-title">{movie['title']}</div>
                            <div class="movie-meta">⭐ {movie['vote_average']} | {movie['release_date']}<br>
                            {movie['genres']} | {movie['runtime']} min</div>
                            <div class="movie-overview">{movie['overview']}</div>
                        </div>
                    </div>
                </div>
            </a>
            """,
            unsafe_allow_html=True
        )

