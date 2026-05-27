from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..dependencies import get_db
from ..models import TravelProject, ProjectPlace
from ..schemas import (
    PlaceCreate,
    PlaceResponse,
    PlaceUpdate
)
from ..services.artic_api import fetch_artwork
from ..crud import (
    validate_duplicate_place,
    validate_place_limit,
    check_project_completion
)

router = APIRouter(
    prefix="/projects/{project_id}/places",
    tags=["Places"]
)


@router.post("/", response_model=PlaceResponse)
async def add_place(
    project_id: int,
    payload: PlaceCreate,
    db: Session = Depends(get_db)
):
    project = db.query(TravelProject).filter(
        TravelProject.id == project_id
    ).first()

    if not project:
        raise HTTPException(404, "Project not found")

    validate_place_limit(project)
    validate_duplicate_place(project, payload.external_id)

    artwork = await fetch_artwork(payload.external_id)

    place = ProjectPlace(
        project_id=project.id,
        external_id=artwork["external_id"],
        title=artwork["title"]
    )

    db.add(place)
    db.commit()
    db.refresh(place)

    return place


@router.get("/", response_model=list[PlaceResponse])
def list_places(
    project_id: int,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 10,
    visited: bool | None = None,
    title: str | None = None,
    external_id: int | None = None
):
    query = db.query(ProjectPlace).filter(
        ProjectPlace.project_id == project_id
    )

    if visited is not None:
        query = query.filter(ProjectPlace.visited == visited)

    if title:
        query = query.filter(ProjectPlace.title.contains(title))

    if external_id is not None:
        query = query.filter(ProjectPlace.external_id == external_id)

    return query.offset(skip).limit(limit).all()


@router.get("/{place_id}", response_model=PlaceResponse)
def get_place(
    project_id: int,
    place_id: int,
    db: Session = Depends(get_db)
):
    place = db.query(ProjectPlace).filter(
        ProjectPlace.project_id == project_id,
        ProjectPlace.id == place_id
    ).first()

    if not place:
        raise HTTPException(404, "Place not found")

    return place


@router.patch("/{place_id}", response_model=PlaceResponse)
def update_place(
    project_id: int,
    place_id: int,
    payload: PlaceUpdate,
    db: Session = Depends(get_db)
):
    place = db.query(ProjectPlace).filter(
        ProjectPlace.project_id == project_id,
        ProjectPlace.id == place_id
    ).first()

    if not place:
        raise HTTPException(404, "Place not found")

    if payload.notes is not None:
        place.notes = payload.notes

    if payload.visited is not None:
        place.visited = payload.visited

    project = place.project

    check_project_completion(project)

    db.commit()
    db.refresh(place)

    return place
