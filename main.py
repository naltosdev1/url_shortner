from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
import sqlite3
import datetime
import string
import random
app = FastAPI()

def get_conn():
    return sqlite3.connect("database.db")

def init_db():
    with get_conn() as conn:
        cursor = conn.cursor()

        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS urls
                       (
                           id          INTEGER PRIMARY KEY AUTOINCREMENT,
                           url         TEXT    NOT NULL,
                           shortCode   TEXT    NOT NULL,
                           createdAt   INTEGER NOT NULL,
                           updatedAt   INTEGER NOT NULL,
                           accessCount INTEGER NOT NULL
                       )
                       """)
        conn.commit()
        conn.close()

class URL(BaseModel):
    url: str

init_db()

@app.get("/shorten/{code}")
async def shorten(code: str):
    with get_conn() as conn:
        row = conn.execute(
            "SELECT url FROM urls WHERE shortCode = ?",
            (code,)
        ).fetchone()

        if not row:
            raise HTTPException(status_code=404, detail="URL not found.")

    conn.execute(
        "UPDATE urls SET accessCount = accessCount + 1 WHERE shortCode = ?",
        (code,)
    )

    return {"url": row[0]}

@app.get("/shorten/{code}/stats")
async def stats(code: str):
    with get_conn() as conn:
        row = conn.execute(
            "SELECT accessCount FROM urls WHERE shortCode = ?",
            (code,)
        ).fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Not found.")

    return {"accessCount": row[0]}

@app.post("/shorten")
async def create_short_url(url: URL):
    short_code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    created_at = datetime.datetime.now().timestamp()

    with get_conn() as conn:
        conn.execute(
            "INSERT INTO urls (url, shortCode, createdAt, updatedAt) VALUES (?, ?, ?, ?)",
            (url, short_code, created_at, created_at)
        )

    return {"shortCode": short_code}

@app.put("/shorten/modify/{code}")
async def update_url_by_short_code(code: str, url: URL):
    with get_conn() as conn:
        row = conn.execute(
            "UPDATE urls SET url = ? WHERE shortCode = ?",
            (url, code)
        )

        if not row:
            raise HTTPException(status_code=404, detail="URL not found.")

    return {"success": True}

@app.delete("/shorten/delete/{code}")
async def delete_short_url(code: str):
    with get_conn() as conn:
        conn.execute(
            "DELETE FROM urls WHERE shortCode = ?",
            (code,)
        )

    return {"success": True}