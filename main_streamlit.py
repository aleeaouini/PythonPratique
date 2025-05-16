import streamlit as st
import requests

st.title("Movie Explorer")

if st.button("Show Random Movie"):
    try:
        response = requests.get("http://localhost:8000/movies/random/")
        response.raise_for_status()
        movie = response.json()

        st.session_state.movie = movie
        st.session_state.summary = None

    except requests.RequestException as e:
        st.error(f"Error fetching movie: {e}")

if "movie" in st.session_state:
    movie = st.session_state.movie
    st.header(f"{movie['title']} ({movie['year']})")
    st.write(f"Director: {movie['director']}")

    st.subheader("Actors:")
    for actor in movie.get("actors", []):
        st.write(actor["actor_name"])

if "movie" in st.session_state:
    movie = st.session_state.movie
    st.header(f"{movie['title']} ({movie['year']})")
    st.write(f"Director: {movie['director']}")

    st.subheader("Actors:")
    for actor in movie.get("actors", []):
        st.write(actor["actor_name"])

    # Bouton pour obtenir le résumé
    movie_id = movie["id"]
    if st.button("Get Summary"):
        try:
            payload = {"movie_id": movie_id}
            response = requests.post("http://localhost:8000/generate_summary/", json=payload)
            response.raise_for_status()
            summary_data = response.json()
            st.session_state.summary = summary_data.get("summary", "No summary returned.")
        except requests.RequestException as e:
            st.error(f"Error fetching summary: {e}")
else:
    st.button("Get Summary", disabled=True)

# Afficher le résumé s'il existe
if "summary" in st.session_state and st.session_state.summary:
    st.info(st.session_state.summary)
