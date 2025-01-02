from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Dict, Optional
import uuid
import random

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# In-memory storage (replace with database in production)
baby_names = {}  # session_id -> list of names
votes = {}  # name_id -> list of votes
compared_pairs = {}  # session_id -> set of compared name pairs


class NameSession(BaseModel):
    session_id: str
    names: List[str]

class VoterInfo(BaseModel):
    name: str
    age: int


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/vote-page")
async def vote_page(request: Request):
    return templates.TemplateResponse("vote.html", {"request": request})


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
    votes[name_id] = []
    return {"success": True}


@app.get("/names/{session_id}")
async def get_names(session_id: str):
    if session_id not in baby_names:
        return {"error": "Session not found"}
    names_with_votes = []
    for name in baby_names[session_id]:
        name_id = f"{session_id}_{name}"
        vote_list = votes.get(name_id, [])
        names_with_votes.append({
            "name": name,
            "votes": len(vote_list),
            "voters": vote_list
        })
    return {"names": names_with_votes}


@app.get("/get-comparison/{session_id}")
async def get_comparison(session_id: str):
    if session_id not in baby_names or len(baby_names[session_id]) < 2:
        return {"error": "Not enough names for comparison"}
    
    if session_id not in compared_pairs:
        compared_pairs[session_id] = set()
    
    # Get all possible pairs
    all_names = baby_names[session_id]
    possible_pairs = []
    for i in range(len(all_names)):
        for j in range(i + 1, len(all_names)):
            pair = tuple(sorted([all_names[i], all_names[j]]))
            if pair not in compared_pairs[session_id]:
                possible_pairs.append([all_names[i], all_names[j]])
    
    if not possible_pairs:
        return {"error": "All pairs have been compared"}
    
    # Return a random pair
    selected_pair = random.choice(possible_pairs)
    return {"names": selected_pair}

@app.post("/compare-vote/{session_id}/{name}")
async def compare_vote(session_id: str, name: str, voter_info: VoterInfo):
    if session_id not in baby_names:
        return {"error": "Session not found"}
    
    name_id = f"{session_id}_{name}"
    if name_id not in votes:
        votes[name_id] = []
    
    # Store vote with voter information
    votes[name_id].append({
        "voter_name": voter_info.name,
        "voter_age": voter_info.age
    })
    
    # Update compared pairs
    names = baby_names[session_id]
    current_comparison = [n for n in names if f"{session_id}_{n}" != name_id]
    if current_comparison:
        pair = tuple(sorted([name, current_comparison[0]]))
        compared_pairs[session_id].add(pair)
    
    return {"success": True}
