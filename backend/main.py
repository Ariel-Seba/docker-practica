from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2
import os
import redis
import json

app = FastAPI()
cache = redis.Redis(host="redis", port=6379, decode_responses=True)


def get_conn():
    return psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host="db"
    )

class Contacto(BaseModel):
    nombre: str
    apellido: str
    telefono: str

@app.get("/contactos")
def listar():
    cached = cache.get("contactos")
    if cached:
        return json.loads(cached)
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, nombre, apellido, telefono FROM contactos")
    rows = cur.fetchall()
    conn.close()
    result = [{"id": r[0], "nombre": r[1], "apellido": r[2], "telefono": r[3]} for r in rows]
    cache.set("contactos", json.dumps(result), ex=30)
    return result


@app.post("/contactos")
def crear(contacto: Contacto):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO contactos (nombre, apellido, telefono) VALUES (%s, %s, %s)",
        (contacto.nombre, contacto.apellido, contacto.telefono)
    )
    conn.commit()
    conn.close()
    cache.delete("contactos")
    return {"ok": True}
