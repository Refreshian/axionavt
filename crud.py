# import glob
# import pandas as pd
# from pydantic import BaseModel, Field
# import os
# import schemas

# def get_data_map(value: schemas.GetMapData):

#     if value in ['beauty', 'faith', 'good', 'evolution', 'justice', 'knowledge', 'nature', 'genus', 'family', 'mastery', 'solvency', 'wisdom']:

#         os.chdir('/home/admin-rggu/rggu-map/data_to_map')
#         file_list = glob.glob('*.xlsx')
#         print(file_list)
#         filename = [x for x in file_list if value in x][0]
#         print(filename)
#         df = pd.read_excel(filename, engine='openpyxl')
#         df.sort_values('Регион', inplace=True)

#         # словарь с расчетными данными по регионам
#         df['Регион'] = [x.strip() for x in df['Регион'].values]
#         dict_val = df.set_index('Регион').to_dict()['sum']
#         return dict_val