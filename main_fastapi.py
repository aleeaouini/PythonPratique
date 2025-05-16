from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import SessionLocal, engine
import schemas
from sqlalchemy.orm import joinedload
import random
import models

from langchain.prompts import PromptTemplate

from langchain_groq import ChatGroq

from langchain.chains import LLMChain
from dotenv import load_dotenv
import os
from pydantic import BaseModel
from schemas import SummaryRequest, SummaryResponse

from fastapi.responses import JSONResponse



# Charger les variables d'environnement
load_dotenv()  # charge .env dans les variables d'environnement
groq_api_key = os.getenv("GROQ_API_KEY")

print("GROQ_API_KEY =", groq_api_key)

if not groq_api_key:
    raise RuntimeError("La clé GROQ_API_KEY n'est pas définie")



# Initialiser le LLM avec Groq
llm = ChatGroq(api_key=groq_api_key, model_name="llama3-8b-8192")




models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/movies/", response_model=schemas.MoviePublic)
def create_movie(movie: schemas.MovieBase, db: Session = Depends(get_db)):
    db_movie = models.Movies(title=movie.title, year=movie.year, director=movie.director)
    db.add(db_movie)
    db.commit()          # Nécessaire pour générer un ID
    db.refresh(db_movie) # Récupère l'ID généré

    for actor in movie.actors:
        db_actor = models.Actors(actor_name=actor.actor_name, movie_id=db_movie.id)
        db.add(db_actor)

    db.commit()
    db.refresh(db_movie)
    return db_movie

@app.get("/movies/random/", response_model=schemas.MoviePublic)
def get_random_movie(db: Session = Depends(get_db)):
    movie = db.query(models.Movies).options(joinedload(models.Movies.actors)).order_by(func.random()).first()
    if not movie:
        raise HTTPException(status_code=404, detail="No movies found")
    return movie

def format_actor_list(actors):
    names = [actor.actor_name for actor in actors]
    if not names:
        return "acteurs inconnus"
    elif len(names) == 1:
        return names[0]
    else:
        return ", ".join(names[:-1]) + " et " + names[-1]


@app.post("/generate_summary/", response_model=SummaryResponse)
def generate_summary(request: SummaryRequest, db: Session = Depends(get_db)):
    movie = db.query(models.Movies).options(joinedload(models.Movies.actors)).filter(models.Movies.id == request.movie_id).first()

    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found.")

    actor_list_str = format_actor_list(movie.actors)

    prompt_template = PromptTemplate(
        input_variables=["title", "year", "director", "actor_list"],
        template="Generate a short, engaging summary for the movie '{title}' ({year}), directed by {director} and starring {actor_list}."
    )

    chain = prompt_template | llm

    try:
        result = chain.invoke({
            "title": movie.title,
            "year": movie.year,
            "director": movie.director,
            "actor_list": actor_list_str
        })
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": f"Error generating summary: {str(e)}"})

    return SummaryResponse(summary_text=result)

