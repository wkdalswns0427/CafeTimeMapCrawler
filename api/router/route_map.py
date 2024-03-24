import os
from fastapi import APIRouter, Request, status, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse, JSONResponse
from typing import Optional, List
import json
from utils.crawler import CrawlerKakaoMap
from utils.utils import utils
from models.response_model import OpenCafe

router = APIRouter()
crawler = CrawlerKakaoMap()
util = utils()

@router.post('/get_full_cafe_list/', status_code=status.HTTP_200_OK) # response_model=OpenCafe
def search_by_keyword(keyword : Optional[str]):

    if not crawler.is_exist(keyword):
        print("vacant")
        crawler.make_file(keyword)
        print("file made")
        crawler.crawlMap(keyword)
        
    temp = crawler.findAll(keyword)
    # print(temp)
    return json.dumps(temp, ensure_ascii = False)

@router.post('/get_open_cafe_list/', status_code=status.HTTP_200_OK) # response_model=OpenCafe
def search_by_keyword(keyword : Optional[str]):
    if not crawler.is_exist(keyword):
        print("vacant")
        crawler.make_file(keyword)
        print("file made")
        crawler.crawlMap(keyword)
        
    temp = crawler.findOpen(keyword)
    return json.dumps(temp, ensure_ascii = False)