
"""
This script is the main entry point for the FastAPI application
It sets up the application, includes routers for different modules, and defines a root endpoint.
"""
from fastapi import FastAPI
from routers import items, users #import the routers module from the routers folder
app = FastAPI()

# Include the routers for users and items
app.include_router(users.router)
app.include_router(items.router)

# Define a root endpoint that returns a welcome message
@app.get("/")
async def root():
    return {"message": "Welcome to my Bigger Application structure!"}