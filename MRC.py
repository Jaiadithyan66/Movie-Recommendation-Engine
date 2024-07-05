import streamlit as st
import pickle
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en=US".format(movie_id)
    retries = Retry(total=3, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
    session = requests.Session()
    session.mount('http://', HTTPAdapter(max_retries=retries))
    session.mount('https://', HTTPAdapter(max_retries=retries))
    
    try:
        data = session.get(url).json()
        poster_path = data['poster_path']
        full_path = "http://image.tmdb.org/t/p/w500" + poster_path
        return full_path
    except requests.RequestException as e:
        st.error(f"Error fetching poster: {e}")
        return None

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse= True, key = lambda x:x[1])
    recommended_movies_name = []
    recommended_movies_poster = []
    for i in distances[1:7]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies_poster.append(fetch_poster(movie_id))
        recommended_movies_name.append(movies.iloc[i[0]].title)
    return recommended_movies_name, recommended_movies_poster

st.title("MOVIE RECOMMENDATION ENGINE")
st.subheader("Discover your next favorite movie with this Smart Recommendation Tool")

movies = pickle.load(open('Fosters/MOVIE_LIST.pkl','rb'))
similarity = pickle.load(open('Fosters/SIMILARITY.pkl','rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    'Select or Type your favorite movie',
    movie_list
)

if st.button('SHOW RECOMMENDATIONS'):
    recommended_movies_name, recommended_movies_poster = recommend(selected_movie)
    col1, col2, col3, col4, col5, col6, = st.columns(6)
    with col1:
        st.text(recommended_movies_name[0])
        st.image(recommended_movies_poster[0])

    with col2:
        st.text(recommended_movies_name[1])
        st.image(recommended_movies_poster[1])

    with col3:
        st.text(recommended_movies_name[2])
        st.image(recommended_movies_poster[2])

    with col4:
        st.text(recommended_movies_name[3])
        st.image(recommended_movies_poster[3])

    with col5:
        st.text(recommended_movies_name[4])
        st.image(recommended_movies_poster[4])

    with col6:
        st.text(recommended_movies_name[5])
        st.image(recommended_movies_poster[5])