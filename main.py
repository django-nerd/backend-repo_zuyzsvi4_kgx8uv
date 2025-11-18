import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from database import db, create_document, get_documents
from schemas import Team, Member, Office, Session, TeamLocation, HelpTicket

app = FastAPI(title="Naithika Foundations Education Tracker API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Naithika Foundations Backend Running"}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Connected & Working"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = os.getenv("DATABASE_NAME") or "❌ Not Set"
            response["connection_status"] = "Connected"
            response["collections"] = db.list_collection_names()
        else:
            response["database"] = "❌ Not Available"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:120]}"
    return response

# ---------- Public Schemas endpoint (for admin viewers) ----------
class SchemaInfo(BaseModel):
    name: str
    fields: List[str]

@app.get("/schema", response_model=List[SchemaInfo])
async def get_schema():
    models = [Team, Member, Office, Session, TeamLocation, HelpTicket]
    output = []
    for m in models:
        output.append(SchemaInfo(name=m.__name__.lower(), fields=list(m.model_fields.keys())))
    return output

# ---------- Team & Member Directory ----------
@app.post("/teams")
async def create_team(team: Team):
    team_id = create_document("team", team)
    return {"id": team_id}

@app.get("/teams")
async def list_teams():
    return get_documents("team")

@app.post("/members")
async def create_member(member: Member):
    member_id = create_document("member", member)
    return {"id": member_id}

@app.get("/members")
async def list_members():
    return get_documents("member")

# ---------- Offices ----------
@app.post("/offices")
async def create_office(office: Office):
    office_id = create_document("office", office)
    return {"id": office_id}

@app.get("/offices")
async def list_offices():
    return get_documents("office")

# ---------- Sessions (teaching visits) ----------
@app.post("/sessions")
async def create_session(session: Session):
    sess_id = create_document("session", session)
    return {"id": sess_id}

@app.get("/sessions")
async def list_sessions(mandal: Optional[str] = None, village: Optional[str] = None):
    filt = {}
    if mandal:
        filt["mandal"] = mandal
    if village:
        filt["village"] = village
    return get_documents("session", filt)

# ---------- Live Team Tracking ----------
@app.post("/track")
async def update_location(loc: TeamLocation):
    loc_id = create_document("teamlocation", loc)
    return {"id": loc_id}

@app.get("/track")
async def get_locations(team_id: Optional[str] = None, limit: int = 20):
    filt = {"team_id": team_id} if team_id else {}
    return get_documents("teamlocation", filt, limit)

# ---------- Help Desk ----------
@app.post("/help")
async def create_ticket(ticket: HelpTicket):
    ticket_id = create_document("helpticket", ticket)
    return {"id": ticket_id}

@app.get("/help")
async def list_tickets(limit: int = 50):
    return get_documents("helpticket", {}, limit)

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
