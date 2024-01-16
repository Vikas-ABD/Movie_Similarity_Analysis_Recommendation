import pickle
import streamlit as st
import requests

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=b2f8bcbb12061d5fb168509a13ec4bc4&language=en-US"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for errors in the HTTP response
        
        data = response.json()
        
        # Check if 'poster_path' is present in the response
        if 'poster_path' in data:
            poster_path = data['poster_path']
            full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
            return full_path
        else:
            return "No poster available"
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return "Poster not found"
        else:
            return f"Error fetching poster: {e}"
    except requests.exceptions.RequestException as e:
        return f"Error fetching poster: {e}"

def recommend(movie):
    try:
        index = movies[movies['title'] == movie].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        recommended_movie_names = []
        recommended_movie_posters = []

        for i in distances[1:6]:
            # Fetch the movie poster
            movie_id = movies.iloc[i[0]].imdb_id
            recommended_movie_poster = fetch_poster(movie_id)

            # Check if the poster was successfully fetched before adding to the list
            if recommended_movie_poster not in ["No poster available", "Poster not found"]:
                recommended_movie_posters.append(recommended_movie_poster)
                recommended_movie_names.append(movies.iloc[i[0]].title)

        return recommended_movie_names, recommended_movie_posters
    except IndexError:
        return "Movie not found in the dataset", []

st.header('Movie Recommender System')

# Load movie data and similarity matrix
movies = pickle.load(open('data_frame.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Display a dropdown to select a movie
movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

# Display recommendations when the button is clicked
if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    
    # Display recommendations in columns
    cols = st.columns(5)
    
    for i, col in enumerate(cols):
        if i < len(recommended_movie_names):
            col.text(recommended_movie_names[i])
            
            if recommended_movie_posters[i] not in ["No poster available", "Poster not found"]:
                col.image(recommended_movie_posters[i])
            else:
                col.write(recommended_movie_posters[i])