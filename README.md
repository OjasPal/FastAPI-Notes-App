# FastAPI Notes App

A simple notes app built with **FastAPI**, **MongoDB** and **Jinja2**. I made it to learn the FastAPI basics: routing, forms, templates and database CRUD.


## Features

- Add, edit and delete notes
- Mark notes as important with a star toggle
- Search notes by title or description
- Filter to show important notes only
- Created date on every note
- Dark theme with a cyan accent

## Tech Stack

- **Backend:** Python, FastAPI, Uvicorn
- **Database:** MongoDB Atlas (PyMongo)
- **Frontend:** Jinja2 templates, HTML, CSS
- **Validation:** Pydantic

## Project Structure

```
FastAPI-Notes-App/
├── index.py            # App entry point
├── config/db.py        # MongoDB connection
├── models/note.py      # Pydantic note model
├── schemas/note.py     # Converts Mongo documents to clean dicts
├── routes/note.py      # All routes (create, read, update, delete)
├── templates/          # index.html, edit.html
├── static/style.css    # Styling
└── requirements.txt
```

## Getting Started

1. **Clone the repo**
   ```bash
   git clone https://github.com/OjasPal/FastAPI-Notes-App.git
   cd FastAPI-Notes-App
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate        # Windows
   source .venv/bin/activate     # macOS / Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Add your MongoDB connection string**

   Create a .env file and add your own URI (a free [MongoDB Atlas](https://www.mongodb.com/atlas) cluster works):
   ```
   MONGO_URI=your_mongodb_connection_string_here
   ```

5. **Run the app**
   ```bash
   fastapi dev index.py
   ```
   Open [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Routes

| Method | Route | Description |
|---|---|---|
| GET | `/` | List notes (supports `?q=` search and `?important=true`) |
| POST | `/` | Create a note |
| GET / POST | `/edit/{id}` | Edit page / save changes |
| POST | `/toggle/{id}` | Toggle important |
| POST | `/delete/{id}` | Delete a note |

## What I Learned

- Structuring a FastAPI project with routers, models and schemas
- Handling HTML forms and Jinja2 templates
- CRUD operations with MongoDB and PyMongo
