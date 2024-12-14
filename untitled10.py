# ... (your imports and data loading code) ...

# Preprocessing
selected_columns = merged_data[['genres_x', 'id', 'keywords_x', 'original_title_x', 'overview_x']]
selected_columns = selected_columns.rename(columns={'original_title_x': 'title', 'genres_x': 'genres', 'keywords_x': 'keywords', 'overview_x': 'overview'})

from ast import literal_eval

# Convert 'genres' and 'keywords' to strings
selected_columns['genres'] = selected_columns['genres'].apply(literal_eval).apply(lambda x: ' '.join([d['name'] for d in x]))
selected_columns['keywords'] = selected_columns['keywords'].apply(literal_eval).apply(lambda x: ' '.join([d['name'] for d in x]))

selected_columns['combined_features'] = selected_columns['genres'] + ' ' + selected_columns['overview'] + ' ' + selected_columns['keywords']

# ... (TfidfVectorizer and cosine_similarity code) ...

# Streamlit Integration
st.title('A Movie Recommendation System')
selected_movie_name = st.selectbox('Which movie u want to search?', selected_columns['title'].values)

# Recommendation Function
def recommend_func(movie):
    movie_index = selected_columns[selected_columns['title'] == movie].index[0]  # Use selected_columns
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movie_posters = []
    for i in movie_list:
        movie_id = selected_columns.iloc[i[0]].id  # Access id from selected_columns
        recommended_movies.append(selected_columns.iloc[i[0]].title)  # Access title from selected_columns
        recommended_movie_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movie_posters


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
