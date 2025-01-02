from fastapi import FastAPI, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Dict, Optional
import uuid
import random
from sqlalchemy.orm import Session
from . import database
from .database import get_db

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


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
async def create_session(db: Session = Depends(get_db)):
    session_id = str(uuid.uuid4())
    db_session = database.Session(id=session_id, compared_pairs=[])
    db.add(db_session)
    db.commit()
    return {"session_id": session_id}

@app.post("/add-name/{session_id}")
async def add_name(session_id: str, name: str = Form(...), db: Session = Depends(get_db)):
    db_session = db.query(database.Session).filter(database.Session.id == session_id).first()
    if not db_session:
        return {"error": "Session not found"}
    
    name_id = f"{session_id}_{name}"
    db_name = database.Name(id=name_id, name=name, session_id=session_id)
    db.add(db_name)
    db.commit()
    return {"success": True}

@app.get("/names/{session_id}")
async def get_names(session_id: str, db: Session = Depends(get_db)):
    db_session = db.query(database.Session).filter(database.Session.id == session_id).first()
    if not db_session:
        return {"error": "Session not found"}
    
    names_with_votes = []
    for name in db_session.names:
        names_with_votes.append({
            "name": name.name,
            "votes": len(name.votes),
            "voters": [{"voter_name": vote.voter_name, "voter_age": vote.voter_age} for vote in name.votes]
        })
    return {"names": names_with_votes}

@app.get("/get-comparison/{session_id}")
async def get_comparison(session_id: str, db: Session = Depends(get_db)):
    db_session = db.query(database.Session).filter(database.Session.id == session_id).first()
    if not db_session or len(db_session.names) < 2:
        return {"error": "Not enough names for comparison"}
    
    compared_pairs = db_session.compared_pairs or []
    
    # Get all possible pairs
    all_names = [name.name for name in db_session.names]
    possible_pairs = []
    for i in range(len(all_names)):
        for j in range(i + 1, len(all_names)):
            pair = sorted([all_names[i], all_names[j]])
            if pair not in compared_pairs:
                possible_pairs.append([all_names[i], all_names[j]])
    
    if not possible_pairs:
        return {"error": "All pairs have been compared"}
    
    # Return a random pair
    selected_pair = random.choice(possible_pairs)
    return {"names": selected_pair}

@app.post("/compare-vote/{session_id}/{name}")
async def compare_vote(session_id: str, name: str, voter_info: VoterInfo, db: Session = Depends(get_db)):
    db_session = db.query(database.Session).filter(database.Session.id == session_id).first()
    if not db_session:
        return {"error": "Session not found"}
    
    name_id = f"{session_id}_{name}"
    db_name = db.query(database.Name).filter(database.Name.id == name_id).first()
    if not db_name:
        return {"error": "Name not found"}
    
    # Store vote with voter information
    vote = database.Vote(
        name_id=name_id,
        voter_name=voter_info.name,
        voter_age=voter_info.age
    )
    db.add(vote)
    
    # Update compared pairs
    names = [n.name for n in db_session.names]
    current_comparison = [n for n in names if f"{session_id}_{n}" != name_id]
    if current_comparison:
        pair = sorted([name, current_comparison[0]])
        compared_pairs = db_session.compared_pairs or []
        if pair not in compared_pairs:
            compared_pairs.append(pair)
            db_session.compared_pairs = compared_pairs
    
    db.commit()
    return {"success": True}
