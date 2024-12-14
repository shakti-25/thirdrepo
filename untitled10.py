import streamlit as st
import pickle
import pandas as pd
import requests

import ast

# ... (fetch_poster function remains the same) ...

# Data Loading and Preprocessing
movies = pd.read_csv('tmdb_5000_movies.csv')
credits = pd.read_csv('tmdb_5000_movies.csv')
credits.rename(columns={'movie_id': 'id'}, inplace=True)
merged_data = pd.merge(movies, credits, on='id')

selected_columns = merged_data[['genres_x', 'id', 'keywords_x', 'original_title_x', 'overview_x']]
selected_columns = selected_columns.rename(columns={'original_title_x': 'title', 'genres_x': 'genres', 'keywords_x': 'keywords', 'overview_x': 'overview'})

selected_columns['combined_features'] = selected_columns['genres'].apply(lambda x: ' '.join(x)) + ' ' + \
                                         selected_columns['overview'] + ' ' + \
                                         selected_columns['keywords'].apply(lambda x: ' '.join(x))

# Impute or remove any NaN values
selected_columns['combined_features'] = selected_columns['combined_features'].fillna('')
# Ensure 'combined_features' column is of type str
selected_columns['combined_features'] = selected_columns['combined_features'].astype(str)

# ... (your existing code) ...
# Streamlit Integration
st.title('A Movie Recommendation System')
selected_movie_name = st.selectbox(
    'Which movie u want to search?',
    selected_columns['title'].values  # Use selected_columns here
)
# same commands is being used which u used in the jupyter-Notebook
def recommend_func(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movie_list:
        # movie_id = movies['movie_id'][i[0]]  # -> your command
        movie_id = movies.iloc[i[0]].movie_id  # -> tutorial command
        recommended_movies.append(movies['title'][i[0]])
        # fetching poster from API
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters


if st.button('Recommend'):
    # st.write('Selected movie name: ', selected_movie_name)
    recommendations_five_movies, posters = recommend_func(selected_movie_name)

    st.write("      ")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(recommendations_five_movies[0])
        st.image(posters[0])

    with col2:
        st.text(recommendations_five_movies[1])
        st.image(posters[1])

    with col3:
        st.text(recommendations_five_movies[2])
        st.image(posters[2])

    with col4:
        st.text(recommendations_five_movies[3])
        st.image(posters[3])

    with col5:
        st.text(recommendations_five_movies[4])
        st.image(posters[4])
