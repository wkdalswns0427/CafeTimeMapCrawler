import os
from fastapi import APIRouter, Request, status, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from typing import Optional, List
from utils.crawler import CrawlerNaverMap
from utils.utils import utils

router = APIRouter()
crawler = CrawlerNaverMap()
util = utils()


# get time
@router.get('/get_cafe_list/{search_key}', tags=['search_key'], status_code=status.HTTP_200_OK)
def search_by_keyword(search_key : Optional[str]):
    res = crawler.main(search_keyword=search_key)
    cur_time = util.get_time()

    temp = []

    for key, values in res.items():
        close_time = values["time"]
        if util.compare_time(cur_time=cur_time, close_time=close_time):
            temp.append(key)
        else:
            pass
    
    return res
