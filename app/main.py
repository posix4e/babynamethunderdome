from fastapi import FastAPI, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Dict, Optional
import uuid
import random
from sqlalchemy.orm import Session
from . import database

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Initialize database
database.init_db()


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
async def create_session(db: Session = Depends(database.get_db)):
    session_id = str(uuid.uuid4())
    db_session = database.Session(id=session_id)
    db.add(db_session)
    db.commit()
    return {"session_id": session_id}


@app.post("/add-name/{session_id}")
async def add_name(session_id: str, name: str = Form(...), db: Session = Depends(database.get_db)):
    db_session = db.query(database.Session).filter(database.Session.id == session_id).first()
    if not db_session:
        return {"error": "Session not found"}
    
    name_id = f"{session_id}_{name}"
    db_name = database.Name(id=name_id, session_id=session_id, name=name)
    db.add(db_name)
    db.commit()
    return {"success": True}


@app.get("/names/{session_id}")
async def get_names(session_id: str, db: Session = Depends(database.get_db)):
    db_session = db.query(database.Session).filter(database.Session.id == session_id).first()
    if not db_session:
        return {"error": "Session not found"}
    
    names_with_votes = []
    db_names = db.query(database.Name).filter(database.Name.session_id == session_id).all()
    
    for db_name in db_names:
        votes = db.query(database.Vote).filter(database.Vote.name_id == db_name.id).all()
        names_with_votes.append({
            "name": db_name.name,
            "votes": len(votes),
            "voters": [vote.voter_info for vote in votes]
        })
    
    return {"names": names_with_votes}


@app.get("/get-comparison/{session_id}")
async def get_comparison(session_id: str, db: Session = Depends(database.get_db)):
    db_names = db.query(database.Name).filter(database.Name.session_id == session_id).all()
    if len(db_names) < 2:
        return {"error": "Not enough names for comparison"}
    
    # Get all compared pairs
    compared = db.query(database.ComparedPair).filter(
        database.ComparedPair.session_id == session_id
    ).all()
    compared_set = {(pair.name1, pair.name2) for pair in compared}
    
    # Get all possible pairs
    all_names = [n.name for n in db_names]
    possible_pairs = []
    for i in range(len(all_names)):
        for j in range(i + 1, len(all_names)):
            pair = tuple(sorted([all_names[i], all_names[j]]))
            if pair not in compared_set:
                possible_pairs.append([all_names[i], all_names[j]])
    
    if not possible_pairs:
        return {"error": "All pairs have been compared"}
    
    # Return a random pair
    selected_pair = random.choice(possible_pairs)
    return {"names": selected_pair}


@app.post("/compare-vote/{session_id}/{name}")
async def compare_vote(
    session_id: str, name: str, voter_info: VoterInfo, db: Session = Depends(database.get_db)
):
    db_session = db.query(database.Session).filter(database.Session.id == session_id).first()
    if not db_session:
        return {"error": "Session not found"}
    
    name_id = f"{session_id}_{name}"
    
    # Store vote with voter information
    vote = database.Vote(
        name_id=name_id,
        voter_info={"voter_name": voter_info.name, "voter_age": voter_info.age}
    )
    db.add(vote)
    
    # Get the other name in the comparison
    other_name = db.query(database.Name).filter(
        database.Name.session_id == session_id,
        database.Name.id != name_id
    ).first()
    
    if other_name:
        # Store the compared pair
        name1, name2 = sorted([name, other_name.name])
        compared = database.ComparedPair(
            session_id=session_id,
            name1=name1,
            name2=name2
        )
        db.add(compared)
    
    db.commit()
    return {"success": True}
