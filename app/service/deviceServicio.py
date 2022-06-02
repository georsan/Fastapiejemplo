from app.modelo.deviceModelo import Modelo
from pymongo import MongoClient

def crearDevice(model:Modelo,dispositivo):
    cli = MongoClient("mongodb+srv://georsan:root@cluster0.rozni.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = cli.MakeSens23
    collection_name=db[dispositivo]
    collection_name.insert_one(dict(model))
    cli.close()

