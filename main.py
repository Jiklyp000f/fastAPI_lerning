from fastapi import FastAPI
from typing import Union
from pydantic import BaseModel


app = FastAPI()

class Item(BaseModel):  
    name: str
    price: float
    is_offer: Union[bool, None] = None

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.put("/items/{item_id}")
def save_item(item_id: int, item: Item):
    return {"item_name": item.price, "item_id": item_id}