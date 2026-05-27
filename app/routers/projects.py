from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..dependencies import get_db
from ..models import TravelProject, ProjectPlace
from ..schemas import (
    ProjectCreate,
    ProjectResponse,
    ProjectUpdate
)
from ..services.artic_api import fetch_artwork
from ..core.security import get_current_user


router = APIRouter(
    prefix="/projects",
    tags=["Projects"]
)


@router.post("/", response_model=ProjectResponse, dependencies=[Depends(get_current_user)])
async def create_project(
    payload: ProjectCreate,
    db: Session = Depends(get_db)
):
    # max 10 places validation
    if len(payload.places) > 10:
        raise HTTPException(
            status_code=400,
            detail="Maximum 10 places allowed"
        )

    project = TravelProject(
        name=payload.name,
        description=payload.description,
        start_date=payload.start_date
    )

    db.add(project)
    db.flush()

    used_external_ids = set()

    for place in payload.places:

        # duplicate validation in same request
        if place.external_id in used_external_ids:
            raise HTTPException(
                status_code=400,
                detail="Duplicate place in request"
            )

        used_external_ids.add(place.external_id)

        # validate external API
        artwork = await fetch_artwork(place.external_id)

        project_place = ProjectPlace(
            project_id=project.id,
            external_id=artwork["external_id"],
            title=artwork["title"]
        )

        db.add(project_place)

    db.commit()
    db.refresh(project)

    return project


@router.get("/", response_model=list[ProjectResponse], dependencies=[Depends(get_current_user)])
def list_projects(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 10,
    name: str | None = None,
    completed: bool | None = None,
    start_date_from: date | None = None,
    start_date_to: date | None = None
):
    query = db.query(TravelProject)

    if name:
        query = query.filter(TravelProject.name.contains(name))

    if completed is not None:
        query = query.filter(TravelProject.completed == completed)

    if start_date_from:
        query = query.filter(TravelProject.start_date >= start_date_from)

    if start_date_to:
        query = query.filter(TravelProject.start_date <= start_date_to)

    return query.offset(skip).limit(limit).all()


@router.get("/{project_id}", response_model=ProjectResponse, dependencies=[Depends(get_current_user)])
def get_project(
    project_id: int,
    db: Session = Depends(get_db)
):
    project = db.query(TravelProject).filter(
        TravelProject.id == project_id
    ).first()

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    return project


@router.put("/{project_id}", response_model=ProjectResponse, dependencies=[Depends(get_current_user)])
def update_project(
    project_id: int,
    payload: ProjectUpdate,
    db: Session = Depends(get_db)
):
    project = db.query(TravelProject).filter(
        TravelProject.id == project_id
    ).first()

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    if payload.name is not None:
        project.name = payload.name

    if payload.description is not None:
        project.description = payload.description

    if payload.start_date is not None:
        project.start_date = payload.start_date

    db.commit()
    db.refresh(project)

    return project


@router.delete("/{project_id}", dependencies=[Depends(get_current_user)])
def delete_project(
    project_id: int,
    db: Session = Depends(get_db)
):
    project = db.query(TravelProject).filter(
        TravelProject.id == project_id
    ).first()

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    visited_exists = any(
        place.visited for place in project.places
    )

    if visited_exists:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete project with visited places"
        )

    db.delete(project)
    db.commit()

    return {
        "message": "Project deleted successfully"
    }
