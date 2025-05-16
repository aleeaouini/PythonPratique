Question1:
It's necessary to commit the primary record (Movies) first because the related records (Actors) require a valid movie_id foreign key, which is generated upon insertion. Without committing, the Movie wouldn't have an ID to reference

Question2:
Lazy loading fetches related data only when explicitly accessed, generating additional queries. Eager loading (like joinedload) retrieves everything in a single query upfront, improving performance by reducing database roundtrips.

Question3:
actor_list = ", ".join([actor.actor_name for actor in movie.actors])  
For a more natural output, you could use ", ".join() for all but the last actor and add "and" before the final name.



