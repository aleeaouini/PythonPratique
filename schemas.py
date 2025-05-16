from pydantic import BaseModel
from typing import List

class ActorBase(BaseModel):
    actor_name: str

class MovieBase(BaseModel):
    title: str
    year: int
    director: str
    actors: List[ActorBase]

class ActorPublic(ActorBase):
    id: int

    class Config:
        from_attributes = True

class MoviePublic(MovieBase):
    id: int
    actors: List[ActorPublic]

    class Config:
        from_attributes = True

class SummaryRequest(BaseModel):
    movie_id: int

class SummaryResponse(BaseModel):
    summary_text: str

