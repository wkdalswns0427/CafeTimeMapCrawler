import os
from fastapi import APIRouter, Request, status, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse, JSONResponse
from typing import Optional, List
from utils.crawler import CrawlerNaverMap
from utils.utils import utils
from models.response_model import OpenCafe

router = APIRouter()
crawler = CrawlerNaverMap()
util = utils()

@router.get('/get_cafe_list/{search_key}', tags=['search_key'], status_code=status.HTTP_200_OK) # response_model=OpenCafe
def search_by_keyword(search_key : Optional[str]):
    res = crawler.main(search_keyword=search_key)
    cur_time = util.get_time()

    temp = {}

    for key, values in res.items():
        close_time = values["time"]
        # print(f"{key} -> cur : {cur_time} , cls : {close_time}")
        time_comp = util.compare_time(cur_time=cur_time, close_time=close_time)
        if time_comp:
            temp[key] = close_time
            # temp["Closing"]
        else:   
            pass
    
    return JSONResponse(content=jsonable_encoder(temp))
