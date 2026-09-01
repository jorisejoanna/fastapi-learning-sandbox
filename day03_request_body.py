"""
using Pydantic to receive and validate JSON bodies in FastAPI
when a user submits a form or sends data to create/update an item,
they send data in the HTTP Request body (as JSON) 
using POST, PUT, or PATCH request
"""

from fastapi import FastAPI
from pydantic import BaseModel

#1. Define your data model as a class that inherits from BaseModel
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

app = FastAPI()

#2. Declare it as a parameter in a POST route
@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.model_dump() #model_dump() convert the Pydantic object into a regular Python dictionary
    
    #3. You can also add additional logic to process the data, such as calculating the price with tax
    #If tax is provided by the user, calculate total price with tax
    if item.tax is not None:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})

    return item_dict

#4. Combining path parameters, query parameters, and request bodies in a single route
#FastAPI will recognise the path parameter, query parameter, and request body parameter based on their types and names
@app.put("/items/{item_id}")

#-item_id -> path parameter (because it matches {item_id} in the URL path)
#-item -> request body parameter (because it is a Pydantic model)
#-q -> query parameter (because it is not part of the URL path and is not a Pydantic model)
async def update_item(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.model_dump()}
    if q:
        result.update({"q": q})
    return result

"""
FastAPI read the body of the request as JSON
convert the corresponding types (if needed)
validate the data against the Pydantic model
give the received data in the parameter item
"""