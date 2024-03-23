import os
from fastapi import APIRouter, Request, status, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse, JSONResponse
from typing import Optional, List
from utils.crawler import CrawlerKakaoMap
from utils.utils import utils
from models.response_model import OpenCafe

router = APIRouter()
crawler = CrawlerKakaoMap()
util = utils()

@router.get('/get_full_cafe_list/{search_key}', tags=['search_key'], status_code=status.HTTP_200_OK) # response_model=OpenCafe
def search_by_keyword(search_key : Optional[list]):
    temp = {}
    return JSONResponse(content=jsonable_encoder(temp))

@router.get('/get_open_cafe_list/{search_key}', tags=['search_key'], status_code=status.HTTP_200_OK) # response_model=OpenCafe
def search_by_keyword(search_key : Optional[list]):
    temp = {}
    return JSONResponse(content=jsonable_encoder(temp))
