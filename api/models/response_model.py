from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from dataclasses import dataclass

@dataclass
class OpenCafe(BaseModel):
    name : str
    closing_time : str