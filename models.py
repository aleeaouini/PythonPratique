from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Movies(Base):
    __tablename__ = 'movies'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    year = Column(Integer)
    director = Column(String)
    
    actors = relationship("Actors", back_populates="movie")

class Actors(Base):
    __tablename__ = 'actors'
    
    id = Column(Integer, primary_key=True, index=True)
    actor_name = Column(String)
    movie_id = Column(Integer, ForeignKey("movies.id"))
    
    movie = relationship("Movies", back_populates="actors")
