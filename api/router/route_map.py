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

@router.post('/get_full_cafe_list/', status_code=status.HTTP_200_OK) # response_model=OpenCafe
def search_by_keyword(keywords : Optional[list]):
    for idx, keyword in enumerate(keywords):
        print(keyword)
        if not crawler.is_exist(keyword):
            print("vacant")
            crawler.make_file(keyword)
            print("file made")
            crawler.crawlMap(keyword)
        
    temp = crawler.findAll(keywords[0])
    print(temp)
    return JSONResponse(content=jsonable_encoder(temp))

@router.get('/get_open_cafe_list/{search_key}', tags=['search_key'], status_code=status.HTTP_200_OK) # response_model=OpenCafe
def search_by_keyword(keywords : Optional[list]):
    for idx, keyword in enumerate(keywords):
        vacant = []
        if not crawler.is_exist(keyword):
            crawler.make_file(keyword)
            vacant.append(keyword)
        crawler.crawlMap(vacant)
    temp = {}
    return JSONResponse(content=jsonable_encoder(temp))
