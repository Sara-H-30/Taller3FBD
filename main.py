from fastapi import FastAPI
from pymongo import MongoClient
import datetime
from bson.objectid import ObjectId


app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configuración de CORS para permitir a APEX
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite a cualquier sitio (incluyendo Oracle APEX)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MONGO_URI = "mongodb+srv://admin_sara:30112006@cluster0.rrzrclg.mongodb.net/ISIS2304A07202610?retryWrites=true&w=majority"


client = MongoClient(MONGO_URI)
db = client['ISIS2304A07202610'] 

# ==========================================
# ENDPOINTS PARA COMENTARIOS (Parte 1 - Puntos 6 y 7)
# ==========================================

# 6. GET /bares/{bar_id}/comentarios (5 Puntos)
@app.get("/bares/{bar_id}/comentarios")
def get_comentarios(bar_id: int):
    # Buscar en la colección comentarios_bares filtrando por bar_id
    comentarios = list(db.comentarios_bares.find({"bar_id": bar_id}))
    
    # Convertir el ObjectId a string para que FastAPI lo pueda retornar como JSON
    for comentario in comentarios:
        comentario["_id"] = str(comentario["_id"])
        
    return comentarios

# 7. POST /bares/{bar_id}/comentarios (5 Puntos)
@app.post("/bares/{bar_id}/comentarios")
def crear_comentario(bar_id: int, datos: dict):
    # El enunciado indica: "El bar_id y la fecha ya están agregados al documento antes del TODO."
    # Si tú misma estás creando el API, debes agregar esos datos aquí antes de insertar:
    datos["bar_id"] = bar_id
    datos["fecha"] = datetime.datetime.utcnow()
    
    # Insertar el documento en la colección
    resultado = db.comentarios_bares.insert_one(datos)
    
    return {"mensaje": "Comentario guardado exitosamente", "id": str(resultado.inserted_id)}


# ==========================================
# ENDPOINTS PARA EVENTOS (Parte 1 - Puntos 8 y 9)
# ==========================================

# 8. GET /bares/{bar_id}/eventos (7 Puntos)
@app.get("/bares/{bar_id}/eventos")
def get_eventos(bar_id: int):
    # Buscar en la colección eventos filtrando por bar_id
    eventos = list(db.eventos.find({"bar_id": bar_id}))
    
    # Convertir el ObjectId a string
    for evento in eventos:
        evento["_id"] = str(evento["_id"])
        
    return eventos

# 9. POST /bares/{bar_id}/eventos (8 Puntos)
@app.post("/bares/{bar_id}/eventos")
def crear_evento(bar_id: int, evento: dict):
    # Recibe un documento con la información del evento, le agrega el bar_id y la fecha_creacion
    evento["bar_id"] = bar_id
    evento["fecha_creacion"] = datetime.datetime.utcnow()
    
    # Insertarlo en la colección eventos
    resultado = db.eventos.insert_one(evento)
    
    return {"mensaje": "Evento creado exitosamente", "id": str(resultado.inserted_id)}

# 11. GET /bares/{bar_id}/eventos (5 Puntos)
@app.get("/bares/{bar_id}/eventos")
def get_eventos(bar_id: int):
    # Buscar en la colección 'eventos' filtrando por bar_id
    eventos = list(db["eventos"].find({"bar_id": bar_id}))
    for e in eventos:
        e["_id"] = str(e["_id"])  # Convertir el ID de Mongo a texto
    return eventos
