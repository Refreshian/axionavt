import glob
import pandas as pd
from pydantic import BaseModel, Field
import os
import crud

class Map(BaseModel):

    value: str

class GetMapData(Map):

    dict_val: dict 