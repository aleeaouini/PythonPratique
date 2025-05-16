
# PythonPratique

## Setup Instructions

### 1. Cloner le dépôt

```bash
git clone https://github.com/aleeaouini/PythonPratique.git
cd PythonPratique
```

### 2. Créer un environnement virtuel

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

---
###  lancer backend
```bash
uvicorn main_fastapi:app --reload
```

---
###  lancer frontend
```bash
python -m streamlit run main_streamlit.py
```

## Questions

### Question 1 :
It's necessary to commit the primary record (Movies) first because the related records (Actors) require a valid movie_id foreign key, which is generated upon insertion. Without committing, the Movie wouldn't have an ID to reference.

### Question 2 :
Lazy loading fetches related data only when explicitly accessed, generating additional queries. Eager loading (like joinedload) retrieves everything in a single query upfront, improving performance by reducing database roundtrips.

### Question 3 :
```python
actor_list = ", ".join([actor.actor_name for actor in movie.actors])
```
For a more natural output, you could use ", ".join() for all but the last actor and add "and" before the final name.
