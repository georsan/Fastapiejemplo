from multiprocessing.connection import wait
from urllib import request
from urllib.request import Request
from fastapi import FastAPI, HTTPException,Request,status
from datetime import datetime
from fastapi import FastAPI
from app.service.deviceServicio import crearDevice
from app.utils.settings import db
import time
import json,os
import requests

app = FastAPI()


@app.post("/device")
async def saveDevice(device:Request):
   request=await device.json()

   if not isinstance(request,list):
       raise HTTPException(status_code=422, detail="Unprocessable Entity")
   else:
       for i in request:

            _json={
                "_id":time.time_ns(),
                "firmware":i['firmware'],
                "estado":i['estado'],
                "bucket":i['bucket'],
                "env":i['env']
                }
            crearDevice(_json,i['id'])
            id_device = i['id']
            header_ = {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiJPVEEiLCJzdnIiOiJtYWtlc2Vucy5hd3MudGhpbmdlci5pbyIsInVzciI6Ik1ha2VTZW5zIn0.xbbjNXgCLX00LZZ7SM-eKYq9cN2xfesTWH__BOD7rZk"
                }
            _property_=json.dumps({
            "value": {
                "val": True
            }
            })

            response = requests.put(    url=f"https://makesens.aws.thinger.io/v3/users/MakeSens/devices/{id_device}/properties/is_update",
                                    data=_property_, headers=header_   ) 



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


'''
@app.put("/device/{id}")
async def saveDevice(id,estado:Request):
   #estado=estado.json()
   #device=readDevice(id)
   print("hola")
   json={
        "_id":datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "firmware":device['firmware'],
        "estado":estado['estado']}
   crearDevice(json,id)
   return json   
   raise HTTPException(status_code=200, detail="sin actualizaciones")
'''
'''@app.post("/initUpdate")
async def initUpdate():
    for i in db.list_collections():
        id=i['name']
        dispositivo=readDevice(id)
        estado=dispositivo['estado']
        firmware=dispositivo['firmware']
        bucket=dispositivo['bucket']
        env=dispositivo['env']
        fecha=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if  estado!="success":
            
            ruta="/home/georsan/nuevo/Update_devices/runApp.sh"
            os.system("sh {} {} {} {} {} {}".format(ruta,id,bucket,firmware,env,fecha))
            #os.system("node /home/georsan/trabajo/Update_devices/Typescriptjs/Hellomundo.js")
        else:
            json={
                "_id":fecha,
                "firmware":firmware,
                "estado":estado,
                "bucket":bucket,
                "env":env}

            crearDevice(json,id)

    raise HTTPException(status_code=200, detail="ok")'''
    
@app.post("/initUpdate")
async def initUpdate(id:Request):
    body=await id.json()
    id=body['id']
    dispositivo=readDevice(id)
    estado=dispositivo['estado']
    firmware=dispositivo['firmware']
    bucket=dispositivo['bucket']
    env=dispositivo['env']
    fecha=time.time_ns()
    
    if  estado!="success":
        json={
            "_id":fecha,
            "firmware":firmware,
            "estado":"Actualizando",
            "bucket":bucket,
            "env":env}
        crearDevice(json,id)
        ruta="/home/georsan/nuevo/Update_devices/runApp.sh"
        os.system("sh {} {} {} {} {} {} ".format(ruta,id,bucket,firmware,env,fecha,id,fecha))
        #os.system("node /home/georsan/trabajo/Update_devices/Typescriptjs/Hellomundo.js")
    else:
        json={
            "_id":fecha,
            "firmware":firmware,
            "estado":estado,
            "bucket":bucket,
            "env":env}

        crearDevice(json,id)
        
        raise HTTPException(status_code=200, detail="sin actualizaciones")
        