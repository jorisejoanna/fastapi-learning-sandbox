"""
this file defines a set of routes related to user operations in the FastAPI application
e.g., reading all users, reading the current user, and reading a specific user by username
"""
from fastapi import APIRouter

#create an APIRouter instance to define a set of routes related to user operations
router = APIRouter(
    prefix="/users", #1. prefix = "/users": all routes routes in this file automatically have the prefix "/users" in their URL path
    tags=["users"], #2. tags = ["users"]: groups these endpoints under the "users" tag in the /docs documentation

)

# Define a route to read users
@router.get("/")
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]

# Define a route to read the current user
@router.get("/me")
async def read_user_me():
    return {"username": "currentuser"}

# Define a route to read a specific user by username
@router.get("/{username}")
async def read_user(username: str):
    return {"username": username}
