import os
from fastapi import APIRouter, Request, status, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from typing import Optional, List
from utils.crawler import CrawlerNaverMap

router = APIRouter()
crawler = CrawlerNaverMap()


# get time
@router.get('/get_cafe_list', status_code=status.HTTP_200_OK)
def search_by_keyword(search_key : Optional[str]):
    res = crawler.main(search_keyword=search_key)

    for key, values in res:
