from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

app=FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Libro(BaseModel):
    id: int = None
    titulo: str
    autor: str
    anio: int
    genero: str

libros_db = []
contador_id = 1


### CREAR LIBRO
@app.post("/",response_model=Libro)
def crear_libro(nuevo_libro:Libro,):
    global contador_id
    nuevo_libro.id = contador_id
    contador_id += 1
    libros_db.append(nuevo_libro)
    return nuevo_libro
###

### OBTENER TODOS LOS LIBROS
@app.get("/",response_model=list[Libro], status_code=201)
def obtener_libros():
    return libros_db
###

### OBTENER LIBRO POR ID
@app.get("/{libro_id}",response_model=Libro)
def obtener_libro(libro_id: int):
    for x in libros_db:
        if x.id == libro_id:
            return x
    raise HTTPException(status_code=404, detail="Libro no encontrado")
###

### BORRAR LIBRO
@app.delete("/{libro_id}")
def eliminar_libro(libro_id: int):
    for x in libros_db:
        if x.id == libro_id:
            libros_db.remove(x)
            return {"Mensaje" : "Libro eliminado"}
    raise HTTPException(status_code=404, detail="Libro no encontrado")  
###
