"""
this script defines a set of routes related to item operations using FastAPI's APIRouter.
It includes a route to read items, which returns a list of items in JSON format.
"""

from fastapi import APIRouter

#create an APIRouter instance to define a set of routes related to item operations
router = APIRouter(
    prefix="/items",
    tags=["items"],
)

# Define a route to read items
@router.get("/")
async def read_items():
    return [{"item_name": "Plumbus"}, {"item_name": "Portal Gun"}]
