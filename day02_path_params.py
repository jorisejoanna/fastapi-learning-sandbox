from fastapi import FastAPI

app = FastAPI()

#1
#@app.get("/items/{item_id}")
#async def read_item(item_id): #output: string (e.g. "8008")
#async def read_item(item_id: int): #declare the type of item_id as int #output: int (e.g. 8008)
#    return {"item_id": item_id, "status": "active"}

#2
#put fixed paths above dynamic paths to avoid conflicts
#Python reads code from top to bottom, so if you put a dynamic path first, it will catch all requests that match the pattern, including those that should go to the fixed path.
"""
@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the_current_user"}

@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}
"""

#3
#from enum import Enum

#create an enumeration class to define a set of named values for the model names
"""
class ModelName(str, Enum):
    alexnet = "alexnet"
    restnet = "restnet"
    lenet = "lenet"
    randomforest = "randomforest"
    """

#app = FastAPI()

#@app.get("/models/{model_name}")
#async def get_model(model_name: ModelName): #declare the type of model_name as ModelName
#    if model_name is ModelName.alexnet: #check if model_name is alexnet
#        return {"model_name": model_name, "message": "Deep Learning"}
#
#    if model_name.value == "lenet": #check if model_name is lenet
#        return {"model_name": model_name, "message": "LeCNN all the images"}

#    return {"model_name": model_name, "message": "Have some residuals"}

#4
#path parameters can also capture the entire path
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}