from fastapi import FastAPI
from typing import Union
from pydantic import BaseModel
import sqlite3

# Создание API
app = FastAPI()

# Модель данных
class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None

# Подключение к базе данных
def get_db_connection():
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row
    return conn

# Создание таблицы при старте приложения (если ее нет)
def init_db():
    with get_db_connection() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            is_offer BOOLEAN
        )
        """)
        conn.commit()

init_db()  # Инициализация базы данных

@app.post("/items/")
async def create_item(item: Item):
    # Сохранение данных в базу
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO items (name, price, is_offer) VALUES (?, ?, ?)
        """, (item.name, item.price, item.is_offer))
        conn.commit()
        item_id = cursor.lastrowid
    return {"id": item_id, "name": item.name, "price": item.price, "is_offer": item.is_offer}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    # Получение данных из базы
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM items WHERE id = ?", (item_id,))
        row = cursor.fetchone()
        if row:
            return {"id": row["id"], "name": row["name"], "price": row["price"], "is_offer": row["is_offer"]}
        return {"error": "Item not found"}

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    # Обновление данных в базе
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        UPDATE items SET name = ?, price = ?, is_offer = ? WHERE id = ?
        """, (item.name, item.price, item.is_offer, item_id))
        conn.commit()
    return {"id": item_id, "name": item.name, "price": item.price, "is_offer": item.is_offer}

@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    # Удаление данных из базы
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        DELETE FROM items WHERE id = ?
        """, (item_id,))
        conn.commit()
    return {"id": item_id}
