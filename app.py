import streamlit as st
import pickle
import requests
import base64
# variables:

movies = pickle.load(open('movies_list (2).mkl', 'rb'))
match_values = pickle.load(open('cosine_similarities_2.mkl', 'rb'))
movie_titles = movies['original_title'].values
API_KEY = "923bbf64ad6e19d116d14c796d098fd4"


# functions:

def get_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"
    try:
        data = requests.get(url).json()
        print(data)
        poster_path = data['poster_path']
        return "https://image.tmdb.org/t/p/w500" + poster_path
    except ConnectionError:
        print("Connection Error")
        return "Connection Error!!"
    except KeyError:
        print("Poster not found")
        return "Poster not found!!"


def get_movies(movie_name, no_of_movies, is_similar):
    recommended_movies = []
    recommended_movie_posters = []
    recommended_movies_homepage = []
    idx = movies[movies['original_title'] == movie_name].index[0]
    distance = sorted(list(enumerate(match_values[idx])), reverse=is_similar, key=lambda vector: vector[1])
    for i in distance[1:no_of_movies + 1]:
        recommended_movies.append(movies.iloc[i[0]]['original_title'])
        try:
            recommended_movie_posters.append(get_poster(movies.iloc[i[0]]['id']))
            recommended_movies_homepage.append(movies.iloc[i[0]]['homepage'])
        except ConnectionError:
            recommended_movie_posters.append("Poster unavailable")
            recommended_movies_homepage.append("Homepage_unavailable")
    return recommended_movies, recommended_movie_posters, recommended_movies_homepage


# interface:

st.set_page_config(layout='wide')


def set_background(png_file):
    # Read image and encode to base64
    with open(png_file, "rb") as f:
        encoded_string = base64.b64encode(f.read()).decode()

    # Inject into Streamlit app with CSS
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded_string}");
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


# Set background using an image file path
set_background('img.png')

st.markdown("<h1 style='text-align:center; color: green;background:black;'>Movie Recommendation System</h1>", unsafe_allow_html=True)

st.markdown(
    """
    <style>
    .stSelectbox label {
        color: green;
        width: 50%; 
        margin: 0 auto; 
        background:black;
        display: flex;
        justify-content: center;
    }
    .stSelectbox div[data-baseweb="select"] {
        width: 50%; 
        margin: 0 auto; 
    }
    </style>
    """,
    unsafe_allow_html=True
)

selected_movie = st.selectbox(label="PICK A MOVIE", options=movie_titles)
no_of_recommendations = st.selectbox(label="PICK NUMBER OF RECOMMENDATIONS", options=range(1, 6))

st.markdown(
    """
    <style>
    .stButton {
        display: flex;
        justify-content: center;
    }
    .stButton button {
        background-color: #45a049;
        color: white; 
        padding: 10px 24px; 
        font-size: 16px; 
        border-radius: 12px; 
        border: 2px solid #909090; 
    }
    .stButton button:hover {
        background-color: #45a049;
        color: white;
        border: 4px solid #4CAF50; 
    }
    </style>
    """,
    unsafe_allow_html=True
)

button_1 = st.button("Show Similar Movies:")
button_2 = st.button("Show Different Movies:")

display_similar = not button_2

if button_1 or button_2:
    res_movie, res_poster, res_homepage = get_movies(selected_movie, no_of_recommendations, display_similar)

    if no_of_recommendations == 1:
        col1, col2, col3 = st.columns([2, 2, 2])
        with col2:
            st.subheader(res_movie[0])
            st.markdown(f"[![Foo]({res_poster[0]})]({res_homepage[0]})")

    else:
        cols = st.columns(no_of_recommendations)
        pointer = 0

        for each in cols:
            with each:
                st.subheader(res_movie[pointer])
                st.markdown(f"[![Foo]({res_poster[pointer]})]({res_homepage[pointer]})")
                pointer += 1
