"""
Database Schemas for Naithika Foundations Education Tracker

Each Pydantic model maps to a MongoDB collection (lowercased class name).
"""
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime

class Team(BaseModel):
    name: str = Field(..., description="Team name")
    mandal: str = Field(..., description="Operational mandal")
    email: EmailStr = Field(..., description="Team contact email")

class Member(BaseModel):
    name: str = Field(..., description="Member full name")
    role: str = Field(..., description="Role in organization")
    email: EmailStr
    phone: Optional[str] = None

class Office(BaseModel):
    mandal: str = Field(..., description="Mandal name")
    address: str
    lat: float
    lng: float
    email: EmailStr

class Session(BaseModel):
    team_id: str = Field(..., description="Team identifier or name")
    date: datetime = Field(default_factory=datetime.utcnow)
    mandal: str = Field(..., description="Mandal of the village")
    village: str = Field(..., description="Village name")
    school: Optional[str] = Field(None, description="School name if applicable")
    topic: str = Field(..., description="Topic taught")
    attendees_children: int = Field(..., ge=0)
    attendees_adults: int = Field(..., ge=0)
    video_urls: List[str] = Field(default_factory=list)

class TeamLocation(BaseModel):
    team_id: str
    lat: float
    lng: float
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class HelpTicket(BaseModel):
    name: str
    email: EmailStr
    subject: str
    message: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
