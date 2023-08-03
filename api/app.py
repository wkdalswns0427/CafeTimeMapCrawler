import uvicorn
import os
from pydantic import BaseModel
from typing import Optional,List
from fastapi import FastAPI, status,HTTPException,Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles 
from starlette.middleware.cors import CORSMiddleware

from utils.crawler import *
import router.router_naver

app = FastAPI()
# templates = Jinja2Templates(directory=os.path.abspath(os.path.expanduser('templates')))
# app.mount("/static", StaticFiles(directory=os.path.abspath(os.path.expanduser('static'))), name="static") 
app.include_router(router)

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
