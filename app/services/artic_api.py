import httpx
from fastapi import HTTPException

ARTIC_BASE_URL = "https://api.artic.edu/api/v1/artworks"


async def fetch_artwork(external_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{ARTIC_BASE_URL}/{external_id}")

    if response.status_code != 200:
        raise HTTPException(
            status_code=404,
            detail="Artwork not found in Art Institute API"
        )

    data = response.json()

    artwork = data.get("data")

    if not artwork:
        raise HTTPException(
            status_code=404,
            detail="Artwork not found"
        )

    return {
        "external_id": artwork["id"],
        "title": artwork.get("title", "Unknown")
    }
