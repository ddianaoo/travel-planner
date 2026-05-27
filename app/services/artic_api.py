import httpx
from fastapi import HTTPException

from .cache import get_from_cache, set_cache

ARTIC_BASE_URL = "https://api.artic.edu/api/v1/artworks"


async def fetch_artwork(external_id: int):
    cached = get_from_cache(external_id)
    if cached:
        return cached

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{ARTIC_BASE_URL}/{external_id}")

    if response.status_code != 200:
        raise HTTPException(404, "Artwork not found")

    data = response.json()["data"]

    result = {
        "external_id": data["id"],
        "title": data.get("title", "Unknown")
    }

    set_cache(external_id, result)

    return result
