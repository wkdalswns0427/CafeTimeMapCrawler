import uvicorn
import os
from pydantic import BaseModel
from typing import Optional,List
from fastapi import FastAPI, status,HTTPException,Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles 
from starlette.middleware.cors import CORSMiddleware

from utils.dbutils.database import SessionLocal

app = FastAPI()
db=SessionLocal()
# templates = Jinja2Templates(directory=os.path.abspath(os.path.expanduser('templates')))
# app.mount("/static", StaticFiles(directory=os.path.abspath(os.path.expanduser('static'))), name="static") 
app.include_router(route_admin.router)
app.include_router(route_login.router)
app.include_router(route_sensordata.router)
# app.include_router(route_mqtt.router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=["*"]
)

@app.get("/")
def init(request: Request):
    init = "initial page.. wait"
    return init
    # return templates.TemplateResponse("initial.html", {"request": request})
