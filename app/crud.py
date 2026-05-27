from fastapi import HTTPException

from .models import TravelProject, ProjectPlace


MAX_PLACES = 10


def check_project_completion(project: TravelProject):
    if project.places and all(place.visited for place in project.places):
        project.completed = True
    else:
        project.completed = False


def validate_place_limit(project: TravelProject):
    if len(project.places) >= MAX_PLACES:
        raise HTTPException(
            status_code=400,
            detail="Maximum 10 places allowed per project"
        )


def validate_duplicate_place(project: TravelProject, external_id: int):
    existing = next(
        (
            p for p in project.places
            if p.external_id == external_id
        ),
        None
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Place already exists in project"
        )
