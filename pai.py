import pandas as pd
import os

path = r'E:\UT'
f = 'pai.xlsx'

df = pd.read_excel(os.path.join(path,f),'raw')

print(df)