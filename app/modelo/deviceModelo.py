from datetime import date

from pydantic import BaseModel, Json

class Modelo(BaseModel):
    _id:str
    id:str
    bucket:str
    firmware:str
    env:str
    estado:str

