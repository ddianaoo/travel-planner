from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date


class PlaceCreate(BaseModel):
    external_id: int


class PlaceUpdate(BaseModel):
    notes: Optional[str] = None
    visited: Optional[bool] = None


class PlaceResponse(BaseModel):
    id: int
    external_id: int
    title: str
    notes: Optional[str]
    visited: bool

    class Config:
        orm_mode = True


class ProjectCreate(BaseModel):
    name: str = Field(..., min_length=1)
    description: Optional[str] = None
    start_date: Optional[date] = None
    places: List[PlaceCreate] = []


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[date] = None


class ProjectResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    start_date: Optional[date]
    completed: bool
    places: List[PlaceResponse]

    class Config:
        orm_mode = True
