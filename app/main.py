from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Dict
import uuid

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# In-memory storage (replace with database in production)
baby_names = {}  # session_id -> list of names
votes = {}  # name_id -> vote count


class NameSession(BaseModel):
    session_id: str
    names: List[str]


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/create-session")
async def create_session():
    session_id = str(uuid.uuid4())
    baby_names[session_id] = []
    return {"session_id": session_id}


@app.post("/add-name/{session_id}")
async def add_name(session_id: str, name: str = Form(...)):
    if session_id not in baby_names:
        return {"error": "Session not found"}
    name_id = f"{session_id}_{name}"
    baby_names[session_id].append(name)
    votes[name_id] = 0
    return {"success": True}


@app.get("/names/{session_id}")
async def get_names(session_id: str):
    if session_id not in baby_names:
        return {"error": "Session not found"}
    names_with_votes = []
    for name in baby_names[session_id]:
        name_id = f"{session_id}_{name}"
        names_with_votes.append({"name": name, "votes": votes.get(name_id, 0)})
    return {"names": names_with_votes}


@app.post("/vote/{session_id}/{name}")
async def vote(session_id: str, name: str):
    name_id = f"{session_id}_{name}"
    if name_id not in votes:
        return {"error": "Name not found"}
    votes[name_id] += 1
    return {"success": True}
