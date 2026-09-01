"""
complete in-memory CRUD API (Create, Read, Update, Delete) 
with proper HTTP status codes
-200 OK -> Standard response for successful HTTP requests
-201 Created -> Resource has been successfully created (POST)
-204 No Content -> Resource has been successfully deleted (DELETE)
-400 Bad Request -> Invalid request data (e.g., duplicate item ID)
-404 Not Found -> Requested resource ID does not exist (GET, PUT, DELETE)
-422 Unprocessable Entity -> Data type validation error (Pydantic validation error)

raise HTTPException when backend logic encounters an error (e.g., item not found, duplicate item ID)
using HTTPException immediately stops execution and returns an error response with the specified status code and detail message
"""

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

#1. Define your data model as a class that inherits from BaseModel
class Item(BaseModel):
    name: str
    price: float
    description: str | None = None

#2. Create an in-memory database (a dictionary) to store items
#using standard Python dictionary to store items in memory
items_db: dict[int, Item] = {
    1: Item(
        name = "Razer Orochi V2",
        price = 377.00,
        description = "Razer Orochi V2 is a wireless gaming mouse with a lightweight design and long battery life.",
    ),

    2: Item(
        name = "Keychron V1",
        price = 379.00,
        description = "Keychron V1 is a mechanical keyboard with a compact design and customizable RGB lighting.",
    ),
}

#3. Create (POST) with 201 Created status code
@app.post("/items/{item_id}",
          status_code = status.HTTP_201_CREATED) #sets the default response status code to 201 Created

async def create_item(item_id: int, item: Item):
    if item_id in items_db: #check if item_id already exists in our dictionary/in-memory database
        
        #HTTPExecption is raised when the item_id already exists in the items_db dictionary
        #it immediately stops execution and returns error response
        #this prevents duplicate items from being created
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Item with ID {item_id} already exists.",
        )
    
    #save the new item in the items_db dictionary with the provided item_id as the key
    items_db[item_id] = item
    return {"message": "Item created successfully", "item": item}

#4. Read all items (GET) with 200 OK status code
@app.get("/items/")
async def read_all_items():
    return items_db

#5. Read one item (GET) with 404 Not Found status code if item not found
@app.get("/items/{item_id}")
async def read_item(item_id: int):

    #if the item_id is not found in the items_db dictionary
    #raise an HTTPException with a 404 Not Found status code 
    #and a message indicating that the item was not found
    if item_id not in items_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID {item_id} was not found.",
        )
    return items_db[item_id]

#6. Update (PUT) with 404 Not Found status code if item not found
@app.put("/items/{item_id}")
async def update_item(item_id: int, updated_item: Item):
    if item_id not in items_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cannot update item with ID {item_id} because it does not exist.",
        )

    #If the item_id exists in the items_db dictionary, update the item with the provided updated_item data
    items_db[item_id] = updated_item
    return {"message": "Item updated successfully", "item": updated_item}

#7. Delete (DELETE) with 204 No Content status code if item found, 
#but returns no content in the response body 
#404 Not Found if not found
@app.delete("/items/{item_id}",
            status_code=status.HTTP_204_NO_CONTENT) #sets the default response status code to 204 No Content

async def delete_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cannot delete item with ID {item_id} because it does not exist.",
        )
    
    #Delete key-value pair from the items_db dictionary using the del statement
    del items_db[item_id]

    #Return None to indicate that the response body is empty 
    #for a 204 No Content response
    return None