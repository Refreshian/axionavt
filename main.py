from fastapi.encoders import jsonable_encoder
import pydantic
import uvicorn
from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel

from typing import Optional
from fastapi import Body, FastAPI
from sklearn import preprocessing
from sklearn.discriminant_analysis import StandardScaler
from sklearn.preprocessing import MinMaxScaler
import uvicorn
import requests
from urllib.parse import urlencode
import pandas as pd
# import plotly.graph_objects as go
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import Depends, FastAPI, HTTPException, Path
from pydantic import BaseModel, ValidationError
import sys
import os
import glob
import json
import numpy as np
import pickle
from sklearn import preprocessing

from fastapi.middleware.wsgi import WSGIMiddleware
from schemas import *
from werkzeug.exceptions import abort
from Levenshtein import distance as lev
from typing import List, Union
import ast
import random
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from fastapi import FastAPI, Query

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# origins = [
#     "http://localhost.tiangolo.com",
#     "https://localhost.tiangolo.com",
#     "http://localhost",
#     "http://localhost:8080",
# ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def code_regions(parameters=None, value=None):

    if parameters == None and value==None: # если нужно получить только коды регионов
        os.chdir("/home/fcgp/map/rggu-map/test fastapi")
        reg_codes = pd.read_excel("code_regions_RF.xlsx")


        os.chdir("//home/fcgp/map/rggu-map/data_to_map/")
        df = pd.read_excel("data_cennost_beauty.xlsx", engine="openpyxl")
        reg_codes = dict(zip(reg_codes["Наименование"].values, reg_codes["Код"].values))

        # получение кодов регионов
        data_reg = []
        data_reg_val = df["Регион"].values
        a = []
        b = []

        for key, val in reg_codes.items():
            for i in range (len(data_reg_val)):
                
                    if "москва" in key.lower():
                        a.append([[x for x in data_reg_val if "москва".lower() in x.lower()][0], key, val])
                        break
                    elif "санкт-петербург".lower() in key.lower():
                        a.append([[x for x in data_reg_val if "санкт-петербург".lower() in x.lower()][0], key, val])
                        break
                    elif "Севастополь".lower() in key.lower():
                        a.append([[x for x in data_reg_val if "Севастополь".lower() in x.lower()][0], key, val])
                        break
                        
                    elif "Омская область" in key:
                        a.append([[x for x in data_reg_val if "Омская область" in x][0], key, val])
                        break

                    elif "Томская область" in key:
                        a.append([[x for x in data_reg_val if "Томская область" in x][0], key, val])
                        break
                        
                    elif "Донецкая".lower() in key.lower():
                        a.append([[x for x in data_reg_val if "Донецкая".lower() in x.lower()][0], key, val])
                        break
                        
                    elif "Луганская".lower() in key.lower():
                        a.append([[x for x in data_reg_val if "Луганская".lower() in x.lower()][0], key, val])
                        break
                        
                    elif lev(data_reg_val[i].lower(), key.lower()) < 2:
                        a.append([data_reg_val[i], key, val])
                        
                    else:
                        b.append(data_reg_val[i])

        # коды регионов
        codes_reg = dict(zip([x[2] for x in pd.DataFrame(a).values], [x[1] for x in pd.DataFrame(a).values]))
        return codes_reg

    elif value != None:
        if parameters == None: # получение данных для карты если нет фильтров по выбору параметров ценности
            os.chdir("/home/fcgp/map/rggu-map/data_to_map")
            file_list = glob.glob("*.xlsx")
            filename = [x for x in file_list if value in x][0]
            df = pd.read_excel(filename, engine="openpyxl")
            df.sort_values("Регион", inplace=True)

            # словарь с расчетными данными по регионам
            df["Регион"] = [x.strip() for x in df["Регион"].values]
            df["sum"] = [np.round(x, 1) for x in df["sum"].values]
            regions_value = df.set_index("Регион").to_dict()["sum"]

            os.chdir("/home/fcgp/map/rggu-map/test fastapi")
            reg_codes = pd.read_excel("code_regions_RF.xlsx")
            reg_codes = dict(zip(reg_codes["Наименование"].values, reg_codes["Код"].values))

            data_reg_val = list(df["Регион"].values)
            a = []

            for key, val in reg_codes.items():
                for i in range(len(data_reg_val)):
                    
                        if "москва" in key.lower():
                            a.append([df["sum"].values[data_reg_val.index([x for x in data_reg_val if "москва".lower() in x.lower()][0])], key, val])
                            break
                        if "Санкт-Петербург".lower() in key.lower():
                            a.append([df["sum"].values[data_reg_val.index([x for x in data_reg_val if "Санкт-Петербург".lower() in x.lower()][0])], key, val])
                            break
                        if "Севастополь".lower() in key.lower():
                            a.append([df["sum"].values[data_reg_val.index([x for x in data_reg_val if "Севастополь".lower() in x.lower()][0])], key, val])
                            break
                        elif "Омская область" in key:
                            a.append([df["sum"].values[data_reg_val.index([x for x in data_reg_val if "Омская область".lower() in x.lower()][0])], key, val])
                            break
                        elif "Томская область" in key:
                            a.append([df["sum"].values[data_reg_val.index([x for x in data_reg_val if "Томская область".lower() in x.lower()][0])], key, val])
                            break
                        if "москва" in key.lower():
                            a.append([df["sum"].values[data_reg_val.index([x for x in data_reg_val if "москва".lower() in x.lower()][0])], key, val])
                            break
                        if "Донецкая".lower() in key.lower():
                            print(key.lower())
                            print([x for x in data_reg_val])
                            a.append([df["sum"].values[data_reg_val.index([x for x in data_reg_val if "Донецкая".lower() in x.lower()][0])], key, val])
                            break
                        if "Луганская".lower() in key.lower():
                            a.append([df["sum"].values[data_reg_val.index([x for x in data_reg_val if "Луганская".lower() in x.lower()][0])], key, val])
                            break

                        elif lev(data_reg_val[i].lower(), key.lower()) < 2:
                            a.append([df["sum"].values[data_reg_val.index(data_reg_val[i])], key, val])
                            
            result = [float(x[0]) for x in pd.DataFrame(a).values]
            scaler = preprocessing.StandardScaler().fit(np.array(result).reshape(-1, 1))
            X_scaled = scaler.transform(np.array(result).reshape(-1, 1))
            X_max = np.max([abs(x[0]) for x in X_scaled])

            result = [x + X_max for x in X_scaled] # добавдяем max значение к расчетам, чтобы убрать отрицат значения
            result = [x[0] for x in result] 
            result.reverse() # переворачиваем список, чтобы добавить рандомные значения для новых регионов
            result[0] = random.uniform(result[:3][0], result[:3][0] + 0.1)
            result[1] = random.uniform(result[:3][1], result[:3][1] + 0.1)
            result[2] = random.uniform(result[:3][2], result[:3][2] + 0.1)
            result.reverse() # переворачиваем рассчитанные данные обратно
            result = [np.round(x, 2) for x in result]

            regions_value = dict(zip([x[2] for x in pd.DataFrame(a).values], result))

            return regions_value


        if parameters != None: # если передан дополнительный выбор наборов данных (параметров)

            ### Учет минус-плюс
            os.chdir("/home/fcgp/map/rggu-map/")
            df_plus_minus = pd.read_excel("размечено Данные fedstat разметка.xlsx")
            df_plus_minus = df_plus_minus[["url", "title", "Ценность 1 ", "Значение ценности 1"]]

            df_plus_minus.head()

            df_plus_minus.columns

            df_plus_minus.dropna(subset=["Ценность 1 "], inplace=True)
            df_plus_minus["Ценность 1 "] = [x.strip().lower() for x in df_plus_minus["Ценность 1 "].values]

            df_plus_minus = df_plus_minus[df_plus_minus["Ценность 1 "] == value.lower()]

            os.chdir("/home/fcgp/map/rggu-map/cenn_raw_data")
            file_list = glob.glob("*.xlsx")
            filename = [x for x in file_list if value in x][0]

            df = pd.read_csv(filename)
            df.rename(columns={ df.columns[0]: "Регион" }, inplace = True)
            df.index = df["Регион"].values
            df.drop("Регион", axis=1, inplace=True)

            ### drop columns by choose
            os.chdir("/home/fcgp/map/rggu-map/")
            with open("dct_names_ministry_id.pkl", "rb") as f: # загрузка словаря с {"id": 1, "source": str "name": str
                loaded_dict = pickle.load(f)


            dct_choose = [loaded_dict[value][x] for x in parameters] # оставляем выбранные параметры с веба [1, 4, 7, 8...]
            choose_list = [x["name"] for x in dct_choose] # переводим [1, 4, 7, 8...] в названия столбцов "Общий фонд музеев Минкультуры России"...

            df = df[[x for x in list(df.columns) if x in choose_list]] # choose_list - выбор данных на сайте пользователем
            ###

            column_list = list(df.columns) 
            df_shape = df.shape[0]

            for i in range(len(column_list)):
                for j in range(df_shape):
                    try:
                        df.loc[j, column_list[i]] = int(df.loc[j, column_list[i]])
                    except:
                        continue

            column_list = list(df.columns)

            for i in range(0, len(column_list)):
                df[column_list[i]] = [x.replace("1NA", "") if type(x) == str else x for x in df[column_list[i]].values]

            # заменяем отсутствующие значения в регионе на средние значения показателя по всем регионам
            column_list = list(df.columns)
            del_lst = []

            for i in range(0, len(column_list)):
                try:
                    df[column_list[i]].fillna(int(np.mean([int(x) for x in df.dropna(subset=[column_list[i]])[column_list[i]]])), inplace = True)
                except:
                    del_lst.append(column_list[i])
                    continue


            for col in del_lst:
                df.drop(col, axis=1, inplace=True)
                column_list.remove(col)


            # различающиеся показатели по регионам
            no_one_data = []
            # неизменяемые (одинаковые для всех регионов) данные
            one_data = [] 
            count = 0

            for i in range(1, len(column_list)):
                if len(set(df[column_list[i]].values)) > 1:
                    no_one_data.append(column_list[i])
                    count+=1
                else:
                    one_data.append(column_list[i])

            # print("Есть различающихся данных по регионам: {}".format(count))
            # print("Не различающихся данных по регионам: {}".format(len(column_list) - count))
            # print("Процент варьирующихся показателей: {}%".format(np.round(count / len(column_list)*100, 2)))

            df_plus_minus["Значение ценности 1"].value_counts()

            # коэффициенты + и - для конкретных изменяемых по регионам показателей
            plus = list(df_plus_minus[df_plus_minus["Значение ценности 1"] == "пол"]["title"].values)
            minus = list(df_plus_minus[df_plus_minus["Значение ценности 1"] == "мин"]["title"].values)
            neutral = list(df_plus_minus[(df_plus_minus["Значение ценности 1"] != "мин") & (df_plus_minus["Значение ценности 1"] != "пол")]["title"].values)

            ### Учитываем знак - или + для скачанных данных

            df = df.astype(int)

            # умножаем на -1 отрицатльные параметры для природы
            for mins in minus:
                if mins in df.columns:
                    df[mins] = [x*-1 for x in df[mins].values]

            for i in range(len(df.columns)):
                if [x for x in df[df.columns[i]] if x == ""] != []:
                    mean = int(np.mean([x for x in df[df.columns[i]] if x != ""]))

            # столбец с суммой всех показателей
            df["sum"] = df[list(df.columns)].sum (axis=1)
            df.insert(0, "Регион", list(df.index))

            # словарь с расчетными данными по регионам
            df["Регион"] = [x.strip() for x in df["Регион"].values]
            df["sum"] = [np.round(x, 1) for x in df["sum"].values]

            os.chdir("/home/fcgp/map/rggu-map/test fastapi")
            reg_codes = pd.read_excel("code_regions_RF.xlsx")
            reg_codes = dict(zip(reg_codes["Наименование"].values, reg_codes["Код"].values))

            data_reg_val = list(df["Регион"].values)
            a = []

            for key, val in reg_codes.items():
                for i in range(len(data_reg_val)):
                    
                        if "москва" in key.lower():
                            a.append([df["sum"].values[data_reg_val.index([x for x in data_reg_val if "москва".lower() in x.lower()][0])], key, val])
                            break
                        elif "Санкт-Петербург".lower() in key.lower():
                            a.append([df["sum"].values[data_reg_val.index([x for x in data_reg_val if "Санкт-Петербург".lower() in x.lower()][0])], key, val])
                            break
                        elif "Севастополь".lower() in key.lower():
                            a.append([df["sum"].values[data_reg_val.index([x for x in data_reg_val if "Севастополь".lower() in x.lower()][0])], key, val])
                            break
                        elif "Омская область" in key:
                            a.append([df["sum"].values[data_reg_val.index([x for x in data_reg_val if "Омская область".lower() in x.lower()][0])], key, val])
                            break
                        elif "Томская область" in key:
                            a.append([df["sum"].values[data_reg_val.index([x for x in data_reg_val if "Томская область".lower() in x.lower()][0])], key, val])
                            break
                        elif "Донецкая".lower() in key.lower():
                            a.append([df["sum"].values[data_reg_val.index([x for x in data_reg_val if "Донецкая".lower() in x.lower()][0])], key, val])
                            break
                        elif "Луганская".lower() in key.lower():
                            a.append([df["sum"].values[data_reg_val.index([x for x in data_reg_val if "Луганская".lower() in x.lower()][0])], key, val])
                            break

                            
                        elif lev(data_reg_val[i].lower(), key.lower()) < 2:
                            a.append([df["sum"].values[data_reg_val.index(data_reg_val[i])], key, val])
                            
            result = [float(x[0]) for x in pd.DataFrame(a).values]
            scaler = preprocessing.StandardScaler().fit(np.array(result).reshape(-1, 1))
            X_scaled = scaler.transform(np.array(result).reshape(-1, 1))
            X_max = np.max([abs(x[0]) for x in X_scaled])

            result = [x + X_max for x in X_scaled] # добавдяем max значение к расчетам, чтобы убрать отрицат значения
            result = [x[0] for x in result] 
            result.reverse() # переворачиваем список, чтобы добавить рандомные значения для новых регионов
            result[0] = random.uniform(result[:3][0], result[:3][0] + 0.1)
            result[1] = random.uniform(result[:3][1], result[:3][1] + 0.1)
            result[2] = random.uniform(result[:3][2], result[:3][2] + 0.1)
            result.reverse() # переворачиваем рассчитанные данные обратно 
            result = [np.round(x, 2) for x in result]

            regions_value = dict(zip([x[2] for x in pd.DataFrame(a).values], result))

            return regions_value



# class Regions(BaseModel):
#     regions: List[dict]

#     model_config = {
#         "json_schema_extra": {
#             "examples": 
#             [[{"id": 1, "name": "Республика Адыгея (Адыгея)"},
#             {"id": 2, "name": "Республика Башкортостан"},
#             {"id": 3, "name": "Республика Бурятия"},
#             {"id": 4, "name": "Республика Алтай"},
#             {"id": 5, "name": "Республика Дагестан"},
#             {"id": 6, "name": "Республика Ингушетия"},
#             {"id": 7, "name": "Кабардино-Балкарская Республика"},
#             {"id": 8, "name": "Республика Калмыкия"},
#             {"id": 9, "name": "Карачаево-Черкесская Республика"},
#             {"id": 10, "name": "Республика Карелия"},
#             ]]
#         }
#     }


class ValDict(BaseModel):
    id: int
    name: str

class Values(BaseModel):
    values: list[ValDict]

    model_config = {
        "json_schema_extra": {
            "examples": 
            [[{"id": "1", "name": "Красота"},
            {"id": "2", "name": "Вера"},
            {"id": "3", "name": "Благо"},
            {"id": "4", "name": "Развитие"},
            {"id": "5", "name": "Справедливость"},
            {"id": "6", "name": "Знание"},
            {"id": "7", "name": "Природа"},
            {"id": "8", "name": "Род"},
            {"id": "9", "name": "Семья"},
            {"id": "10", "name": "Мастерство"},
            {"id": "11", "name": "Состоятельность"},
            {"id": "12", "name": "Мудрость"}]]
        }
    }


class Region(BaseModel):
    id: int
    name: str
    path: str
    pointX: str
    pointY: str


class RegionsValueItem(BaseModel):
    region: Region
    value: float


class RegionValue(BaseModel):
    indicators: List[int]
    regions_value: List[RegionsValueItem]
    

class ModelregionId(BaseModel):
    id: int
    name: str


str_int = np.arange(1, len(["beauty", "faith", "good", "evolution", "justice", "knowledge", "nature", "genus", "family", "mastery", "solvency", "wisdom"])+1)
str_int = [str(x) for x in str_int]
values_int_dct = dict(zip(str_int, ["beauty", "faith", "good", "evolution", "justice", "knowledge", "nature", "genus", "family", "mastery", "solvency", "wisdom"]))
values_name_dict = {"beauty": "красота", "faith": "вера", "good": "благо", "evolution": "развитие", "justice": "справедливость", "knowledge": "знание", "nature": "природа", "genus": "род", "family": "семья", "mastery": "мастерство", "solvency": "состоятельность", "wisdom": "мудрость"}

# словарь {0: {'id': 0,
#   'source': 'Министерство культуры Российской Федерации',
#   'name': 'Численность работников парков культуры и отдыха Минкультуры России'},
#  1: {'id': 1,
os.chdir("/home/fcgp/map/rggu-map/")
with open('dct_names_ministry_id.pkl', 'rb') as f:
    loaded_dict = pickle.load(f)

for key, val in loaded_dict.items():
    loaded_dict[key] = {str(k):v for k, v in loaded_dict[key].items()}

for key, val in loaded_dict.items():
    for k, v in loaded_dict[key].items():
        loaded_dict[key][k] = dict(zip(list(v.keys()), [str(x) if type(x) == np.int64 else x for x in v.values()]))


@app.get("/map/{value}")
def get_map_data(value: str, indicators: List[int] = Query(None)) -> RegionValue:
    
    if value in values_int_dct.keys():
        ###
        if indicators != None:

            regions_value = code_regions(parameters=indicators, value=values_int_dct[value]) 
            codes_reg = code_regions(value=None, parameters=None)

            a = []
            for key, val in regions_value.items():
                a.append({
                    "region": {
                        "id": key,
                        "name": codes_reg[key],
                        "path": "M23.3929 11V4.496L20.5849 9.5H19.9249L17.1049 4.496V11H16.0249V2.48H17.1649L20.2489 8.012L23.3449 2.48H24.4729V11H23.3929ZM28.9757 11.12C28.5037 11.12 28.0757 11.036 27.6917 10.868C27.3077 10.692 26.9757 10.456 26.6957 10.16C26.4157 9.856 26.1997 9.508 26.0477 9.116C25.8957 8.724 25.8197 8.312 25.8197 7.88C25.8197 7.44 25.8957 7.024 26.0477 6.632C26.1997 6.24 26.4157 5.896 26.6957 5.6C26.9757 5.296 27.3077 5.06 27.6917 4.892C28.0837 4.716 28.5117 4.628 28.9757 4.628C29.4477 4.628 29.8757 4.716 30.2597 4.892C30.6437 5.06 30.9757 5.296 31.2557 5.6C31.5437 5.896 31.7637 6.24 31.9157 6.632C32.0677 7.024 32.1437 7.44 32.1437 7.88C32.1437 8.312 32.0677 8.724 31.9157 9.116C31.7637 9.508 31.5477 9.856 31.2677 10.16C30.9877 10.456 30.6517 10.692 30.2597 10.868C29.8757 11.036 29.4477 11.12 28.9757 11.12ZM26.8997 7.892C26.8997 8.324 26.9917 8.716 27.1757 9.068C27.3677 9.42 27.6197 9.7 27.9317 9.908C28.2437 10.108 28.5917 10.208 28.9757 10.208C29.3597 10.208 29.7077 10.104 30.0197 9.896C30.3397 9.688 30.5917 9.408 30.7757 9.056C30.9677 8.696 31.0637 8.3 31.0637 7.868C31.0637 7.436 30.9677 7.044 30.7757 6.692C30.5917 6.34 30.3397 6.06 30.0197 5.852C29.7077 5.644 29.3597 5.54 28.9757 5.54C28.5917 5.54 28.2437 5.648 27.9317 5.864C27.6197 6.072 27.3677 6.352 27.1757 6.704C26.9917 7.056 26.8997 7.452 26.8997 7.892ZM36.1953 11.12C35.7233 11.12 35.2913 11.036 34.8993 10.868C34.5153 10.692 34.1793 10.452 33.8913 10.148C33.6113 9.844 33.3913 9.496 33.2313 9.104C33.0793 8.712 33.0033 8.296 33.0033 7.856C33.0033 7.264 33.1353 6.724 33.3993 6.236C33.6633 5.748 34.0353 5.36 34.5153 5.072C34.9953 4.776 35.5513 4.628 36.1833 4.628C36.7993 4.628 37.3353 4.768 37.7913 5.048C38.2553 5.32 38.5993 5.688 38.8233 6.152L37.7913 6.476C37.6313 6.18 37.4073 5.952 37.1193 5.792C36.8313 5.624 36.5113 5.54 36.1593 5.54C35.7753 5.54 35.4233 5.64 35.1033 5.84C34.7913 6.04 34.5433 6.316 34.3593 6.668C34.1753 7.012 34.0833 7.408 34.0833 7.856C34.0833 8.296 34.1753 8.696 34.3593 9.056C34.5513 9.408 34.8033 9.688 35.1153 9.896C35.4353 10.104 35.7873 10.208 36.1713 10.208C36.4193 10.208 36.6553 10.164 36.8793 10.076C37.1113 9.988 37.3113 9.872 37.4793 9.728C37.6553 9.576 37.7753 9.412 37.8393 9.236L38.8713 9.548C38.7433 9.852 38.5473 10.124 38.2833 10.364C38.0273 10.596 37.7193 10.78 37.3593 10.916C37.0073 11.052 36.6193 11.12 36.1953 11.12ZM40.0558 11V4.736H41.1118V7.316H41.8078L43.7758 4.736H44.9758L42.6358 7.772L45.2518 11H44.0278L41.8078 8.288H41.1118V11H40.0558ZM46.2785 11V4.736H49.5185C49.8945 4.736 50.2065 4.812 50.4545 4.964C50.7025 5.108 50.8865 5.296 51.0065 5.528C51.1345 5.76 51.1985 6.008 51.1985 6.272C51.1985 6.608 51.1185 6.912 50.9585 7.184C50.7985 7.448 50.5665 7.648 50.2625 7.784C50.6225 7.888 50.9145 8.076 51.1385 8.348C51.3625 8.612 51.4745 8.94 51.4745 9.332C51.4745 9.684 51.3905 9.984 51.2225 10.232C51.0545 10.48 50.8185 10.672 50.5145 10.808C50.2105 10.936 49.8585 11 49.4585 11H46.2785ZM47.2865 10.256H49.4345C49.6265 10.256 49.7985 10.208 49.9505 10.112C50.1105 10.016 50.2345 9.888 50.3225 9.728C50.4105 9.568 50.4545 9.4 50.4545 9.224C50.4545 9.032 50.4105 8.86 50.3225 8.708C50.2425 8.548 50.1265 8.424 49.9745 8.336C49.8305 8.24 49.6625 8.192 49.4705 8.192H47.2865V10.256ZM47.2865 7.496H49.2425C49.4345 7.496 49.6025 7.448 49.7465 7.352C49.8905 7.248 50.0025 7.116 50.0825 6.956C50.1625 6.796 50.2025 6.628 50.2025 6.452C50.2025 6.188 50.1145 5.96 49.9385 5.768C49.7705 5.576 49.5505 5.48 49.2785 5.48H47.2865V7.496ZM52.3258 9.188C52.3258 8.788 52.4378 8.444 52.6618 8.156C52.8938 7.86 53.2098 7.632 53.6098 7.472C54.0098 7.312 54.4738 7.232 55.0018 7.232C55.2818 7.232 55.5778 7.256 55.8898 7.304C56.2018 7.344 56.4778 7.408 56.7178 7.496V7.04C56.7178 6.56 56.5738 6.184 56.2858 5.912C55.9978 5.632 55.5898 5.492 55.0618 5.492C54.7178 5.492 54.3858 5.556 54.0658 5.684C53.7538 5.804 53.4218 5.98 53.0698 6.212L52.6858 5.468C53.0938 5.188 53.5018 4.98 53.9098 4.844C54.3178 4.7 54.7418 4.628 55.1818 4.628C55.9818 4.628 56.6138 4.852 57.0778 5.3C57.5418 5.74 57.7738 6.356 57.7738 7.148V9.8C57.7738 9.928 57.7978 10.024 57.8458 10.088C57.9018 10.144 57.9898 10.176 58.1098 10.184V11C58.0058 11.016 57.9138 11.028 57.8338 11.036C57.7618 11.044 57.7018 11.048 57.6538 11.048C57.4058 11.048 57.2178 10.98 57.0898 10.844C56.9698 10.708 56.9018 10.564 56.8858 10.412L56.8618 10.016C56.5898 10.368 56.2338 10.64 55.7938 10.832C55.3538 11.024 54.9178 11.12 54.4858 11.12C54.0698 11.12 53.6978 11.036 53.3698 10.868C53.0418 10.692 52.7858 10.46 52.6018 10.172C52.4178 9.876 52.3258 9.548 52.3258 9.188ZM56.4058 9.632C56.5018 9.52 56.5778 9.408 56.6338 9.296C56.6898 9.176 56.7178 9.076 56.7178 8.996V8.216C56.4698 8.12 56.2098 8.048 55.9378 8C55.6658 7.944 55.3978 7.916 55.1338 7.916C54.5978 7.916 54.1618 8.024 53.8258 8.24C53.4978 8.448 53.3338 8.736 53.3338 9.104C53.3338 9.304 53.3858 9.5 53.4898 9.692C53.6018 9.876 53.7618 10.028 53.9698 10.148C54.1858 10.268 54.4498 10.328 54.7618 10.328C55.0898 10.328 55.4018 10.264 55.6978 10.136C55.9938 10 56.2298 9.832 56.4058 9.632Z",
                        "pointX": "5.50237",
                        "pointY": "6.99998"
                    },
                    "value": val
                })

            return RegionValue(value=value, regions_value=a, indicators=indicators)

        else:
            regions_value = code_regions(parameters=None, value=values_int_dct[value]) 
            codes_reg = code_regions(value=None, parameters=None)

            a = []
            for key, val in regions_value.items():
                a.append({
                    "region": {
                        "id": key,
                        "name": codes_reg[key],
                        "path": "M23.3929 11V4.496L20.5849 9.5H19.9249L17.1049 4.496V11H16.0249V2.48H17.1649L20.2489 8.012L23.3449 2.48H24.4729V11H23.3929ZM28.9757 11.12C28.5037 11.12 28.0757 11.036 27.6917 10.868C27.3077 10.692 26.9757 10.456 26.6957 10.16C26.4157 9.856 26.1997 9.508 26.0477 9.116C25.8957 8.724 25.8197 8.312 25.8197 7.88C25.8197 7.44 25.8957 7.024 26.0477 6.632C26.1997 6.24 26.4157 5.896 26.6957 5.6C26.9757 5.296 27.3077 5.06 27.6917 4.892C28.0837 4.716 28.5117 4.628 28.9757 4.628C29.4477 4.628 29.8757 4.716 30.2597 4.892C30.6437 5.06 30.9757 5.296 31.2557 5.6C31.5437 5.896 31.7637 6.24 31.9157 6.632C32.0677 7.024 32.1437 7.44 32.1437 7.88C32.1437 8.312 32.0677 8.724 31.9157 9.116C31.7637 9.508 31.5477 9.856 31.2677 10.16C30.9877 10.456 30.6517 10.692 30.2597 10.868C29.8757 11.036 29.4477 11.12 28.9757 11.12ZM26.8997 7.892C26.8997 8.324 26.9917 8.716 27.1757 9.068C27.3677 9.42 27.6197 9.7 27.9317 9.908C28.2437 10.108 28.5917 10.208 28.9757 10.208C29.3597 10.208 29.7077 10.104 30.0197 9.896C30.3397 9.688 30.5917 9.408 30.7757 9.056C30.9677 8.696 31.0637 8.3 31.0637 7.868C31.0637 7.436 30.9677 7.044 30.7757 6.692C30.5917 6.34 30.3397 6.06 30.0197 5.852C29.7077 5.644 29.3597 5.54 28.9757 5.54C28.5917 5.54 28.2437 5.648 27.9317 5.864C27.6197 6.072 27.3677 6.352 27.1757 6.704C26.9917 7.056 26.8997 7.452 26.8997 7.892ZM36.1953 11.12C35.7233 11.12 35.2913 11.036 34.8993 10.868C34.5153 10.692 34.1793 10.452 33.8913 10.148C33.6113 9.844 33.3913 9.496 33.2313 9.104C33.0793 8.712 33.0033 8.296 33.0033 7.856C33.0033 7.264 33.1353 6.724 33.3993 6.236C33.6633 5.748 34.0353 5.36 34.5153 5.072C34.9953 4.776 35.5513 4.628 36.1833 4.628C36.7993 4.628 37.3353 4.768 37.7913 5.048C38.2553 5.32 38.5993 5.688 38.8233 6.152L37.7913 6.476C37.6313 6.18 37.4073 5.952 37.1193 5.792C36.8313 5.624 36.5113 5.54 36.1593 5.54C35.7753 5.54 35.4233 5.64 35.1033 5.84C34.7913 6.04 34.5433 6.316 34.3593 6.668C34.1753 7.012 34.0833 7.408 34.0833 7.856C34.0833 8.296 34.1753 8.696 34.3593 9.056C34.5513 9.408 34.8033 9.688 35.1153 9.896C35.4353 10.104 35.7873 10.208 36.1713 10.208C36.4193 10.208 36.6553 10.164 36.8793 10.076C37.1113 9.988 37.3113 9.872 37.4793 9.728C37.6553 9.576 37.7753 9.412 37.8393 9.236L38.8713 9.548C38.7433 9.852 38.5473 10.124 38.2833 10.364C38.0273 10.596 37.7193 10.78 37.3593 10.916C37.0073 11.052 36.6193 11.12 36.1953 11.12ZM40.0558 11V4.736H41.1118V7.316H41.8078L43.7758 4.736H44.9758L42.6358 7.772L45.2518 11H44.0278L41.8078 8.288H41.1118V11H40.0558ZM46.2785 11V4.736H49.5185C49.8945 4.736 50.2065 4.812 50.4545 4.964C50.7025 5.108 50.8865 5.296 51.0065 5.528C51.1345 5.76 51.1985 6.008 51.1985 6.272C51.1985 6.608 51.1185 6.912 50.9585 7.184C50.7985 7.448 50.5665 7.648 50.2625 7.784C50.6225 7.888 50.9145 8.076 51.1385 8.348C51.3625 8.612 51.4745 8.94 51.4745 9.332C51.4745 9.684 51.3905 9.984 51.2225 10.232C51.0545 10.48 50.8185 10.672 50.5145 10.808C50.2105 10.936 49.8585 11 49.4585 11H46.2785ZM47.2865 10.256H49.4345C49.6265 10.256 49.7985 10.208 49.9505 10.112C50.1105 10.016 50.2345 9.888 50.3225 9.728C50.4105 9.568 50.4545 9.4 50.4545 9.224C50.4545 9.032 50.4105 8.86 50.3225 8.708C50.2425 8.548 50.1265 8.424 49.9745 8.336C49.8305 8.24 49.6625 8.192 49.4705 8.192H47.2865V10.256ZM47.2865 7.496H49.2425C49.4345 7.496 49.6025 7.448 49.7465 7.352C49.8905 7.248 50.0025 7.116 50.0825 6.956C50.1625 6.796 50.2025 6.628 50.2025 6.452C50.2025 6.188 50.1145 5.96 49.9385 5.768C49.7705 5.576 49.5505 5.48 49.2785 5.48H47.2865V7.496ZM52.3258 9.188C52.3258 8.788 52.4378 8.444 52.6618 8.156C52.8938 7.86 53.2098 7.632 53.6098 7.472C54.0098 7.312 54.4738 7.232 55.0018 7.232C55.2818 7.232 55.5778 7.256 55.8898 7.304C56.2018 7.344 56.4778 7.408 56.7178 7.496V7.04C56.7178 6.56 56.5738 6.184 56.2858 5.912C55.9978 5.632 55.5898 5.492 55.0618 5.492C54.7178 5.492 54.3858 5.556 54.0658 5.684C53.7538 5.804 53.4218 5.98 53.0698 6.212L52.6858 5.468C53.0938 5.188 53.5018 4.98 53.9098 4.844C54.3178 4.7 54.7418 4.628 55.1818 4.628C55.9818 4.628 56.6138 4.852 57.0778 5.3C57.5418 5.74 57.7738 6.356 57.7738 7.148V9.8C57.7738 9.928 57.7978 10.024 57.8458 10.088C57.9018 10.144 57.9898 10.176 58.1098 10.184V11C58.0058 11.016 57.9138 11.028 57.8338 11.036C57.7618 11.044 57.7018 11.048 57.6538 11.048C57.4058 11.048 57.2178 10.98 57.0898 10.844C56.9698 10.708 56.9018 10.564 56.8858 10.412L56.8618 10.016C56.5898 10.368 56.2338 10.64 55.7938 10.832C55.3538 11.024 54.9178 11.12 54.4858 11.12C54.0698 11.12 53.6978 11.036 53.3698 10.868C53.0418 10.692 52.7858 10.46 52.6018 10.172C52.4178 9.876 52.3258 9.548 52.3258 9.188ZM56.4058 9.632C56.5018 9.52 56.5778 9.408 56.6338 9.296C56.6898 9.176 56.7178 9.076 56.7178 8.996V8.216C56.4698 8.12 56.2098 8.048 55.9378 8C55.6658 7.944 55.3978 7.916 55.1338 7.916C54.5978 7.916 54.1618 8.024 53.8258 8.24C53.4978 8.448 53.3338 8.736 53.3338 9.104C53.3338 9.304 53.3858 9.5 53.4898 9.692C53.6018 9.876 53.7618 10.028 53.9698 10.148C54.1858 10.268 54.4498 10.328 54.7618 10.328C55.0898 10.328 55.4018 10.264 55.6978 10.136C55.9938 10 56.2298 9.832 56.4058 9.632Z",
                        "pointX": "5.50237",
                        "pointY": "6.99998"
                    },
                    "value": val
                })

            return RegionValue(value=value, regions_value=a)
    
    else:
        raise HTTPException(400)


@app.get("/maps/all-values")
async def return_all_values() -> Values:
    """
    Получение всех ценностей
    #
    [{"id": "1", "name": "Красота"}, {"id": "2", "name": "Вера"}, {"id": "3", "name": "Благо"}, ... ]
    #
    """
    a = [] 
    for key, val in values_int_dct.items():
        a.append({"id": key, "name": values_name_dict[val].capitalize()})
    
    return Values(values=a)


@app.get("/region_id/{value}")
def get_region(value: int) -> ModelregionId:
    """
    Возвращает имя региона по его id (int)
    """
    # коды регионов
    codes_reg = code_regions(value=None, parameters=None)
    name = codes_reg[value]

    return ModelregionId(id = value, name = name) 



class RegionVal(BaseModel):
    id: int
    name: str


class Regions(BaseModel):
    regions: List[RegionVal]


@app.get("/region")
def return_all_regions() -> Regions:
    """
    Получение всех регионов
    #
        {
        "regions": [
            {
            "id": "1",
            "name": "Республика Адыгея (Адыгея)"
            },
            ...class Source(BaseModel):
    id: int
    source: str
    name: str

class Indicators(BaseModel):
    value_params: list[Source]

    model_config = {
        "json_schema_extra": {
            "examples": 
            [[{0: {'id': 0,
            'source': 'Министерство культуры Российской Федерации',
            'name': 'Численность работников парков культуры и отдыха Минкультуры России'},
            1: {'id': 1,
            'source': 'Федеральная служба государственной статистики',
            'name': 'Поступление денежных средств и иного имущества в религиозную организацию'},
            2: {'id': 2,
            'source': 'Федеральная служба государственной статистики',
            'name': 'Распределение количества религиозных организаций по видам деятельности согласно учредительным документам'}},
            ]]
        }
    }
    """

    dct = {1: "Республика Адыгея (Адыгея)", 2: "Республика Башкортостан", 3: "Республика Бурятия", 4: "Республика Алтай", 5: "Республика Дагестан", 6: "Республика Ингушетия", 7: "Кабардино-Балкарская Республика", 8: "Республика Калмыкия", 9: "Карачаево-Черкесская Республика", 10: "Республика Карелия", 11: "Республика Коми", 12: "Республика Марий Эл", 13: "Республика Мордовия", 14: "Республика Саха (Якутия)", 15: "Республика Северная Осетия - Алания", 16: "Республика Татарстан (Татарстан)", 17: "Республика Тыва", 18: "Удмуртская Республика", 19: "Республика Хакасия", 20: "Чеченская Республика", 21: "Чувашская Республика - Чувашия", 22: "Алтайский край", 23: "Краснодарский край", 24: "Красноярский край", 25: "Приморский край", 26: "Ставропольский край", 27: "Хабаровский край", 28: "Амурская область", 29: "Архангельская область", 30: "Астраханская область", 31: "Белгородская область", 32: "Брянская область", 33: "Владимирская область", 34: "Волгоградская область", 35: "Вологодская область", 36: "Воронежская область", 37: "Ивановская область", 38: "Иркутская область", 39: "Калининградская область", 40: "Калужская область", 41: "Камчатский край", 42: "Кемеровская область - Кузбасс", 43: "Кировская область", 44: "Костромская область", 45: "Курганская область", 46: "Курская область", 47: "Ленинградская область", 48: "Липецкая область", 49: "Магаданская область", 50: "Московская область", 51: "Мурманская область", 52: "Нижегородская область", 53: "Новгородская область", 54: "Новосибирская область", 55: "Омская область", 56: "Оренбургская область", 57: "Орловская область", 58: "Пензенская область", 59: "Пермский край", 60: "Псковская область", 61: "Ростовская область", 62: "Рязанская область", 63: "Самарская область", 64: "Саратовская область", 65: "Сахалинская область", 66: "Свердловская область", 67: "Смоленская область", 68: "Тамбовская область", 69: "Тверская область", 70: "Томская область", 71: "Тульская область", 72: "Тюменская область", 73: "Ульяновская область", 74: "Челябинская область", 75: "Забайкальский край", 76: "Ярославская область", 77: "г. Москва", 78: "г. Санкт-Петербург", 79: "Еврейская автономная область", 83: "Ненецкий автономный округ", 86: "Ханты-Мансийский автономный округ - Югра", 87: "Чукотский автономный округ", 89: "Ямало-Ненецкий автономный округ", 90: "Запорожская область", 91: "Республика Крым", 92: "г. Севастополь", 93: "Донецкая Народная Республика", 94: "Луганская Народная Республика", 95: "Херсонская область"}
    a = []

    for key, val in dct.items():
        a.append({"id": str(key), "name": val})

    return ModelRegions(regions=a)


class ValueParam(BaseModel):
    id: int
    source: str
    name: str


class Indicators(BaseModel):
    value_params: List[ValueParam]

    model_config = {
        "json_schema_extra": {
            "examples": 
            [[{0: {'id': 0,
            'source': 'Министерство культуры Российской Федерации',
            'name': 'Численность работников парков культуры и отдыха Минкультуры России'},
            1: {'id': 1,
            'source': 'Федеральная служба государственной статистики',
            'name': 'Поступление денежных средств и иного имущества в религиозную организацию'},
            2: {'id': 2,
            'source': 'Федеральная служба государственной статистики',
            'name': 'Распределение количества религиозных организаций по видам деятельности согласно учредительным документам'}},
            ]]
        }
    }


@app.get("/values/{value_id}/indicators")
def return_indicators(value_id: int) -> Indicators:
    """
    Endpoint получения всех показателей по конкретной ценности
    #
        {
        "value_params": {
            "0": {
            "id": "0",
            "source": "Министерство цифрового развития, связи и массовых коммуникаций Российской Федерации",
            "name": "Численность сельского населения, имеющего возможность принимать три телевизионные программы (наземное цифровое эфирное телевещание в стандарте DVB)"
            },
    """

    value_params = loaded_dict[values_int_dct[str(value_id)]] # параметры данных для ценности 
    value_params = [val for val in value_params.values()]
        # {0: {'id': 0,
        # 'source': 'Министерство культуры Российской Федерации',
        # 'name': 'Численность работников парков культуры и отдыха Минкультуры России'},
        # 1: {'id': 1,

    return Indicators(value_params = value_params)


@app.post("/map/{value}")
def get_map_data(value: str, indicators: List[int] = None) -> RegionValue:

    """
    Получение данные по ценности с включением выбранных параметров (в теле запроса)
    """

    if value in values_int_dct.keys():
        ###class Model(BaseModel):

        if indicators != None:

            regions_value = code_regions(parameters=indicators, value=values_int_dct[value]) 
            codes_reg = code_regions(value=None, parameters=None)

            a = []
            for key, val in regions_value.items():
                a.append({
                    "region": {
                        "id": key,
                        "name": codes_reg[key],
                        "path": "M23.3929 11V4.496L20.5849 9.5H19.9249L17.1049 4.496V11H16.0249V2.48H17.1649L20.2489 8.012L23.3449 2.48H24.4729V11H23.3929ZM28.9757 11.12C28.5037 11.12 28.0757 11.036 27.6917 10.868C27.3077 10.692 26.9757 10.456 26.6957 10.16C26.4157 9.856 26.1997 9.508 26.0477 9.116C25.8957 8.724 25.8197 8.312 25.8197 7.88C25.8197 7.44 25.8957 7.024 26.0477 6.632C26.1997 6.24 26.4157 5.896 26.6957 5.6C26.9757 5.296 27.3077 5.06 27.6917 4.892C28.0837 4.716 28.5117 4.628 28.9757 4.628C29.4477 4.628 29.8757 4.716 30.2597 4.892C30.6437 5.06 30.9757 5.296 31.2557 5.6C31.5437 5.896 31.7637 6.24 31.9157 6.632C32.0677 7.024 32.1437 7.44 32.1437 7.88C32.1437 8.312 32.0677 8.724 31.9157 9.116C31.7637 9.508 31.5477 9.856 31.2677 10.16C30.9877 10.456 30.6517 10.692 30.2597 10.868C29.8757 11.036 29.4477 11.12 28.9757 11.12ZM26.8997 7.892C26.8997 8.324 26.9917 8.716 27.1757 9.068C27.3677 9.42 27.6197 9.7 27.9317 9.908C28.2437 10.108 28.5917 10.208 28.9757 10.208C29.3597 10.208 29.7077 10.104 30.0197 9.896C30.3397 9.688 30.5917 9.408 30.7757 9.056C30.9677 8.696 31.0637 8.3 31.0637 7.868C31.0637 7.436 30.9677 7.044 30.7757 6.692C30.5917 6.34 30.3397 6.06 30.0197 5.852C29.7077 5.644 29.3597 5.54 28.9757 5.54C28.5917 5.54 28.2437 5.648 27.9317 5.864C27.6197 6.072 27.3677 6.352 27.1757 6.704C26.9917 7.056 26.8997 7.452 26.8997 7.892ZM36.1953 11.12C35.7233 11.12 35.2913 11.036 34.8993 10.868C34.5153 10.692 34.1793 10.452 33.8913 10.148C33.6113 9.844 33.3913 9.496 33.2313 9.104C33.0793 8.712 33.0033 8.296 33.0033 7.856C33.0033 7.264 33.1353 6.724 33.3993 6.236C33.6633 5.748 34.0353 5.36 34.5153 5.072C34.9953 4.776 35.5513 4.628 36.1833 4.628C36.7993 4.628 37.3353 4.768 37.7913 5.048C38.2553 5.32 38.5993 5.688 38.8233 6.152L37.7913 6.476C37.6313 6.18 37.4073 5.952 37.1193 5.792C36.8313 5.624 36.5113 5.54 36.1593 5.54C35.7753 5.54 35.4233 5.64 35.1033 5.84C34.7913 6.04 34.5433 6.316 34.3593 6.668C34.1753 7.012 34.0833 7.408 34.0833 7.856C34.0833 8.296 34.1753 8.696 34.3593 9.056C34.5513 9.408 34.8033 9.688 35.1153 9.896C35.4353 10.104 35.7873 10.208 36.1713 10.208C36.4193 10.208 36.6553 10.164 36.8793 10.076C37.1113 9.988 37.3113 9.872 37.4793 9.728C37.6553 9.576 37.7753 9.412 37.8393 9.236L38.8713 9.548C38.7433 9.852 38.5473 10.124 38.2833 10.364C38.0273 10.596 37.7193 10.78 37.3593 10.916C37.0073 11.052 36.6193 11.12 36.1953 11.12ZM40.0558 11V4.736H41.1118V7.316H41.8078L43.7758 4.736H44.9758L42.6358 7.772L45.2518 11H44.0278L41.8078 8.288H41.1118V11H40.0558ZM46.2785 11V4.736H49.5185C49.8945 4.736 50.2065 4.812 50.4545 4.964C50.7025 5.108 50.8865 5.296 51.0065 5.528C51.1345 5.76 51.1985 6.008 51.1985 6.272C51.1985 6.608 51.1185 6.912 50.9585 7.184C50.7985 7.448 50.5665 7.648 50.2625 7.784C50.6225 7.888 50.9145 8.076 51.1385 8.348C51.3625 8.612 51.4745 8.94 51.4745 9.332C51.4745 9.684 51.3905 9.984 51.2225 10.232C51.0545 10.48 50.8185 10.672 50.5145 10.808C50.2105 10.936 49.8585 11 49.4585 11H46.2785ZM47.2865 10.256H49.4345C49.6265 10.256 49.7985 10.208 49.9505 10.112C50.1105 10.016 50.2345 9.888 50.3225 9.728C50.4105 9.568 50.4545 9.4 50.4545 9.224C50.4545 9.032 50.4105 8.86 50.3225 8.708C50.2425 8.548 50.1265 8.424 49.9745 8.336C49.8305 8.24 49.6625 8.192 49.4705 8.192H47.2865V10.256ZM47.2865 7.496H49.2425C49.4345 7.496 49.6025 7.448 49.7465 7.352C49.8905 7.248 50.0025 7.116 50.0825 6.956C50.1625 6.796 50.2025 6.628 50.2025 6.452C50.2025 6.188 50.1145 5.96 49.9385 5.768C49.7705 5.576 49.5505 5.48 49.2785 5.48H47.2865V7.496ZM52.3258 9.188C52.3258 8.788 52.4378 8.444 52.6618 8.156C52.8938 7.86 53.2098 7.632 53.6098 7.472C54.0098 7.312 54.4738 7.232 55.0018 7.232C55.2818 7.232 55.5778 7.256 55.8898 7.304C56.2018 7.344 56.4778 7.408 56.7178 7.496V7.04C56.7178 6.56 56.5738 6.184 56.2858 5.912C55.9978 5.632 55.5898 5.492 55.0618 5.492C54.7178 5.492 54.3858 5.556 54.0658 5.684C53.7538 5.804 53.4218 5.98 53.0698 6.212L52.6858 5.468C53.0938 5.188 53.5018 4.98 53.9098 4.844C54.3178 4.7 54.7418 4.628 55.1818 4.628C55.9818 4.628 56.6138 4.852 57.0778 5.3C57.5418 5.74 57.7738 6.356 57.7738 7.148V9.8C57.7738 9.928 57.7978 10.024 57.8458 10.088C57.9018 10.144 57.9898 10.176 58.1098 10.184V11C58.0058 11.016 57.9138 11.028 57.8338 11.036C57.7618 11.044 57.7018 11.048 57.6538 11.048C57.4058 11.048 57.2178 10.98 57.0898 10.844C56.9698 10.708 56.9018 10.564 56.8858 10.412L56.8618 10.016C56.5898 10.368 56.2338 10.64 55.7938 10.832C55.3538 11.024 54.9178 11.12 54.4858 11.12C54.0698 11.12 53.6978 11.036 53.3698 10.868C53.0418 10.692 52.7858 10.46 52.6018 10.172C52.4178 9.876 52.3258 9.548 52.3258 9.188ZM56.4058 9.632C56.5018 9.52 56.5778 9.408 56.6338 9.296C56.6898 9.176 56.7178 9.076 56.7178 8.996V8.216C56.4698 8.12 56.2098 8.048 55.9378 8C55.6658 7.944 55.3978 7.916 55.1338 7.916C54.5978 7.916 54.1618 8.024 53.8258 8.24C53.4978 8.448 53.3338 8.736 53.3338 9.104C53.3338 9.304 53.3858 9.5 53.4898 9.692C53.6018 9.876 53.7618 10.028 53.9698 10.148C54.1858 10.268 54.4498 10.328 54.7618 10.328C55.0898 10.328 55.4018 10.264 55.6978 10.136C55.9938 10 56.2298 9.832 56.4058 9.632Z",
                        "pointX": "5.50237",
                        "pointY": "6.99998"
                    },
                    "value": val
                })

            return RegionValue(value=value, regions_value=a, indicators=indicators)

        else:
            regions_value = code_regions(parameters=None, value=values_int_dct[value]) 
            codes_reg = code_regions(value=None, parameters=None)

            a = []
            for key, val in regions_value.items():
                a.append({
                    "region": {
                        "id": key,
                        "name": codes_reg[key],
                        "path": "M23.3929 11V4.496L20.5849 9.5H19.9249L17.1049 4.496V11H16.0249V2.48H17.1649L20.2489 8.012L23.3449 2.48H24.4729V11H23.3929ZM28.9757 11.12C28.5037 11.12 28.0757 11.036 27.6917 10.868C27.3077 10.692 26.9757 10.456 26.6957 10.16C26.4157 9.856 26.1997 9.508 26.0477 9.116C25.8957 8.724 25.8197 8.312 25.8197 7.88C25.8197 7.44 25.8957 7.024 26.0477 6.632C26.1997 6.24 26.4157 5.896 26.6957 5.6C26.9757 5.296 27.3077 5.06 27.6917 4.892C28.0837 4.716 28.5117 4.628 28.9757 4.628C29.4477 4.628 29.8757 4.716 30.2597 4.892C30.6437 5.06 30.9757 5.296 31.2557 5.6C31.5437 5.896 31.7637 6.24 31.9157 6.632C32.0677 7.024 32.1437 7.44 32.1437 7.88C32.1437 8.312 32.0677 8.724 31.9157 9.116C31.7637 9.508 31.5477 9.856 31.2677 10.16C30.9877 10.456 30.6517 10.692 30.2597 10.868C29.8757 11.036 29.4477 11.12 28.9757 11.12ZM26.8997 7.892C26.8997 8.324 26.9917 8.716 27.1757 9.068C27.3677 9.42 27.6197 9.7 27.9317 9.908C28.2437 10.108 28.5917 10.208 28.9757 10.208C29.3597 10.208 29.7077 10.104 30.0197 9.896C30.3397 9.688 30.5917 9.408 30.7757 9.056C30.9677 8.696 31.0637 8.3 31.0637 7.868C31.0637 7.436 30.9677 7.044 30.7757 6.692C30.5917 6.34 30.3397 6.06 30.0197 5.852C29.7077 5.644 29.3597 5.54 28.9757 5.54C28.5917 5.54 28.2437 5.648 27.9317 5.864C27.6197 6.072 27.3677 6.352 27.1757 6.704C26.9917 7.056 26.8997 7.452 26.8997 7.892ZM36.1953 11.12C35.7233 11.12 35.2913 11.036 34.8993 10.868C34.5153 10.692 34.1793 10.452 33.8913 10.148C33.6113 9.844 33.3913 9.496 33.2313 9.104C33.0793 8.712 33.0033 8.296 33.0033 7.856C33.0033 7.264 33.1353 6.724 33.3993 6.236C33.6633 5.748 34.0353 5.36 34.5153 5.072C34.9953 4.776 35.5513 4.628 36.1833 4.628C36.7993 4.628 37.3353 4.768 37.7913 5.048C38.2553 5.32 38.5993 5.688 38.8233 6.152L37.7913 6.476C37.6313 6.18 37.4073 5.952 37.1193 5.792C36.8313 5.624 36.5113 5.54 36.1593 5.54C35.7753 5.54 35.4233 5.64 35.1033 5.84C34.7913 6.04 34.5433 6.316 34.3593 6.668C34.1753 7.012 34.0833 7.408 34.0833 7.856C34.0833 8.296 34.1753 8.696 34.3593 9.056C34.5513 9.408 34.8033 9.688 35.1153 9.896C35.4353 10.104 35.7873 10.208 36.1713 10.208C36.4193 10.208 36.6553 10.164 36.8793 10.076C37.1113 9.988 37.3113 9.872 37.4793 9.728C37.6553 9.576 37.7753 9.412 37.8393 9.236L38.8713 9.548C38.7433 9.852 38.5473 10.124 38.2833 10.364C38.0273 10.596 37.7193 10.78 37.3593 10.916C37.0073 11.052 36.6193 11.12 36.1953 11.12ZM40.0558 11V4.736H41.1118V7.316H41.8078L43.7758 4.736H44.9758L42.6358 7.772L45.2518 11H44.0278L41.8078 8.288H41.1118V11H40.0558ZM46.2785 11V4.736H49.5185C49.8945 4.736 50.2065 4.812 50.4545 4.964C50.7025 5.108 50.8865 5.296 51.0065 5.528C51.1345 5.76 51.1985 6.008 51.1985 6.272C51.1985 6.608 51.1185 6.912 50.9585 7.184C50.7985 7.448 50.5665 7.648 50.2625 7.784C50.6225 7.888 50.9145 8.076 51.1385 8.348C51.3625 8.612 51.4745 8.94 51.4745 9.332C51.4745 9.684 51.3905 9.984 51.2225 10.232C51.0545 10.48 50.8185 10.672 50.5145 10.808C50.2105 10.936 49.8585 11 49.4585 11H46.2785ZM47.2865 10.256H49.4345C49.6265 10.256 49.7985 10.208 49.9505 10.112C50.1105 10.016 50.2345 9.888 50.3225 9.728C50.4105 9.568 50.4545 9.4 50.4545 9.224C50.4545 9.032 50.4105 8.86 50.3225 8.708C50.2425 8.548 50.1265 8.424 49.9745 8.336C49.8305 8.24 49.6625 8.192 49.4705 8.192H47.2865V10.256ZM47.2865 7.496H49.2425C49.4345 7.496 49.6025 7.448 49.7465 7.352C49.8905 7.248 50.0025 7.116 50.0825 6.956C50.1625 6.796 50.2025 6.628 50.2025 6.452C50.2025 6.188 50.1145 5.96 49.9385 5.768C49.7705 5.576 49.5505 5.48 49.2785 5.48H47.2865V7.496ZM52.3258 9.188C52.3258 8.788 52.4378 8.444 52.6618 8.156C52.8938 7.86 53.2098 7.632 53.6098 7.472C54.0098 7.312 54.4738 7.232 55.0018 7.232C55.2818 7.232 55.5778 7.256 55.8898 7.304C56.2018 7.344 56.4778 7.408 56.7178 7.496V7.04C56.7178 6.56 56.5738 6.184 56.2858 5.912C55.9978 5.632 55.5898 5.492 55.0618 5.492C54.7178 5.492 54.3858 5.556 54.0658 5.684C53.7538 5.804 53.4218 5.98 53.0698 6.212L52.6858 5.468C53.0938 5.188 53.5018 4.98 53.9098 4.844C54.3178 4.7 54.7418 4.628 55.1818 4.628C55.9818 4.628 56.6138 4.852 57.0778 5.3C57.5418 5.74 57.7738 6.356 57.7738 7.148V9.8C57.7738 9.928 57.7978 10.024 57.8458 10.088C57.9018 10.144 57.9898 10.176 58.1098 10.184V11C58.0058 11.016 57.9138 11.028 57.8338 11.036C57.7618 11.044 57.7018 11.048 57.6538 11.048C57.4058 11.048 57.2178 10.98 57.0898 10.844C56.9698 10.708 56.9018 10.564 56.8858 10.412L56.8618 10.016C56.5898 10.368 56.2338 10.64 55.7938 10.832C55.3538 11.024 54.9178 11.12 54.4858 11.12C54.0698 11.12 53.6978 11.036 53.3698 10.868C53.0418 10.692 52.7858 10.46 52.6018 10.172C52.4178 9.876 52.3258 9.548 52.3258 9.188ZM56.4058 9.632C56.5018 9.52 56.5778 9.408 56.6338 9.296C56.6898 9.176 56.7178 9.076 56.7178 8.996V8.216C56.4698 8.12 56.2098 8.048 55.9378 8C55.6658 7.944 55.3978 7.916 55.1338 7.916C54.5978 7.916 54.1618 8.024 53.8258 8.24C53.4978 8.448 53.3338 8.736 53.3338 9.104C53.3338 9.304 53.3858 9.5 53.4898 9.692C53.6018 9.876 53.7618 10.028 53.9698 10.148C54.1858 10.268 54.4498 10.328 54.7618 10.328C55.0898 10.328 55.4018 10.264 55.6978 10.136C55.9938 10 56.2298 9.832 56.4058 9.632Z",
                        "pointX": "5.50237",
                        "pointY": "6.99998"
                    },
                    "value": val
                })

            return RegionValue(value=value, regions_value=a)
    
    else:
        abort(404)

 

if __name__ == "__main__":
    uvicorn.run("main_test:app", host="0.0.0.0", port=5000, reload=True)