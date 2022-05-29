from app.modelo.deviceModelo import Modelo
from app.utils.settings import db

def crearDevice(model:Modelo,dispositivo):
    collection_name=db[dispositivo]
    collection_name.insert_one(dict(model))


