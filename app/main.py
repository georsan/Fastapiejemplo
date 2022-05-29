from urllib import request
from urllib.request import Request
from fastapi import FastAPI, HTTPException,Request,status
from datetime import datetime
from fastapi import FastAPI
from service.deviceServicio import crearDevice
from utils.settings import db
import json,os  
app = FastAPI()


@app.post("/device")
async def saveDevice(device:Request):
   request=await device.json()

   if not isinstance(request,list):
       raise HTTPException(status_code=422, detail="Unprocessable Entity")
   else:
       for i in request:
           json={
               "_id":datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "firmware":i['firmware'],
                "estado":i['estado'],
                "bucket":i['bucket'],
                "env":i['env']
                }
           crearDevice(json,i['id'])
       raise HTTPException(status_code=200, detail="Registro con éxito")


@app.get("/device/{id}")
def readDevice(id:str):
    sum=0
    item=[]
    for i in  db[id].find():
        item.append(i)
    if len(item)==0:
        raise HTTPException(status_code=404, detail="Device not found")
    else:
        return item.pop()


@app.put("/device/{id}")
async def saveDevice(id,estado:Request):
   #estado=estado.json()
   #device=readDevice(id)
   print("hola")
   '''json={
        "_id":datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "firmware":device['firmware'],
        "estado":estado['estado']}
   crearDevice(json,id)
   return json'''   
   raise HTTPException(status_code=200, detail="sin actualizaciones")
@app.post("/initUpdate/{id}")
async def initUpdate(id:str):
    dispositivo=readDevice(id)
    estado=dispositivo['estado']
    firmware=dispositivo['firmware']
    bucket=dispositivo['bucket']
    env=dispositivo['env']
    if  estado== "Actualización Pendiente":
        
        ruta="/home/georsan/nuevo/Update_devices/runApp.sh"
        os.system("sh {} UP_001 firmware-file-test firmware.bin esp32dev 22-05-29".format(ruta))
        #os.system("node /home/georsan/trabajo/Update_devices/Typescriptjs/Hellomundo.js")
    else:
        json={
            "_id":datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "firmware":dispositivo['firmware'],
            "estado":"sin actualizaciones"}

        crearDevice(json,id)
        raise HTTPException(status_code=200, detail="sin actualizaciones")
    