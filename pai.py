import pandas as pd
import os

path = r'E:\UT'
f = 'pai.xlsx'

df = pd.read_excel(os.path.join(path,f),'raw')
df.rename(columns{'拍卖时间':'date','投放数量':'number',\
                   '警示价':'start','最低成交价':'low',
                   '平均成交价':'mean','投标人数':'enrollment'

})
print(df)