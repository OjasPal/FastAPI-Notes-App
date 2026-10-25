import re

from bson import ObjectId
from bson.errors import InvalidId
from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from config.db import conn
from models.note import Note
from schemas.note import noteEntity, notesEntity

note = APIRouter()
templates = Jinja2Templates(directory="templates")
collection = conn.notes.notes


def get_object_id(note_id: str) -> ObjectId:
    """Convert the id from the URL into a MongoDB ObjectId, or return a 404."""
    try:
        return ObjectId(note_id)
    except InvalidId:
        raise HTTPException(status_code=404, detail="Note not found")


def redirect_home() -> RedirectResponse:
    return RedirectResponse(url="/", status_code=303)


# ---------- READ (with search + filter) ----------
@note.get("/", response_class=HTMLResponse)
def home(request: Request, q: str = "", important: bool = False):
    query = {}

    if q:
        pattern = {"$regex": re.escape(q), "$options": "i"}  # case-insensitive
        query["$or"] = [{"title": pattern}, {"desc": pattern}]

    if important:
        query["important"] = True

    docs = collection.find(query).sort("_id", -1)  # newest first
    return templates.TemplateResponse(
        request,
        "index.html",
        {"notes": notesEntity(docs), "q": q, "only_important": important},
    )


# ---------- CREATE ----------
@note.post("/")
def create_note(
    title: str = Form(...),
    desc: str = Form(...),
    important: bool = Form(False),
):
    new_note = Note(title=title.strip(), desc=desc.strip(), important=important)
    collection.insert_one(new_note.model_dump())
    return redirect_home()


# ---------- UPDATE: toggle important ----------
@note.post("/toggle/{note_id}")
def toggle_important(note_id: str):
    oid = get_object_id(note_id)
    doc = collection.find_one({"_id": oid})
    if not doc:
        raise HTTPException(status_code=404, detail="Note not found")

    collection.update_one(
        {"_id": oid},
        {"$set": {"important": not doc.get("important", False)}},
    )
    return redirect_home()


# ---------- UPDATE: edit title/description ----------
@note.get("/edit/{note_id}", response_class=HTMLResponse)
def edit_page(request: Request, note_id: str):
    doc = collection.find_one({"_id": get_object_id(note_id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Note not found")
    return templates.TemplateResponse(request, "edit.html", {"note": noteEntity(doc)})


@note.post("/edit/{note_id}")
def update_note(note_id: str, title: str = Form(...), desc: str = Form(...)):
    result = collection.update_one(
        {"_id": get_object_id(note_id)},
        {"$set": {"title": title.strip(), "desc": desc.strip()}},
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Note not found")
    return redirect_home()


# ---------- DELETE ----------
@note.post("/delete/{note_id}")
def delete_note(note_id: str):
    result = collection.delete_one({"_id": get_object_id(note_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Note not found")
    return redirect_home()