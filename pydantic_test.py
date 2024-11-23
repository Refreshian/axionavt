from ast import List
import json
from typing import Optional
from pydantic import BaseModel
# from future import annotations

from typing import List

from pydantic import BaseModel


# Define student_details dictionary
model_config = [{'name': 'Красота', 'value': 5706},
 {'name': 'Вера', 'value': 24825},
 {'name': 'Благо', 'value': 41251},
 {'name': 'Развитие', 'value': 45579},
 {'name': 'Справедливость', 'value': 68791},
 {'name': 'Знание', 'value': 7765},
 {'name': 'Природа', 'value': 4443},
 {'name': 'Род', 'value': 55692},
 {'name': 'Семья', 'value': 111006},
 {'name': 'Мастерство', 'value': 20886},
 {'name': 'Состоятельность', 'value': 14246},
 {'name': 'Мудрость', 'value': 28230}]

dj = json.dumps(model_config)

import datamodel_code_generator
cg = datamodel_code_generator
print(cg.generate(dj))
