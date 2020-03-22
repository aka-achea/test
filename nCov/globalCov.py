import requests
import pyecharts
from pyecharts.charts import *
from pyecharts import options as opts
from pyecharts.commons.utils import JsCode
from datetime import date, datetime
import datetime
from pprint import pprint

url = 'https://lab.isaaclin.cn/nCoV/api/area'
data = requests.get(url).json()

# 生成更新日期
update_date = date.today()

pprint(data)

oversea_confirm = []
for item in data['results']:
    if item['countryEnglishName']:
        oversea_confirm.append((item['countryEnglishName']
                                .replace('United States of America', 'United States')
                                .replace('United Kiongdom', 'United Kingdom'), 
                                item['confirmedCount']))


_map = (
        Map(init_opts=opts.InitOpts(theme='dark', width='400'))
        .add("累计确诊人数", oversea_confirm, "world",is_map_symbol_show=False,  is_roam=False)
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(
            title_opts=opts.TitleOpts(title="新型冠状病毒全球疫情地图",
                                     subtitle="更新日期：{}".format(update_date)),
            legend_opts=opts.LegendOpts(is_show=False),
            visualmap_opts=opts.VisualMapOpts(is_show=True, max_=50, 
                                              is_piecewise=False, 
                                              range_color=['#FFFFE0', '#FFFFE0', '#FFA07A', '#CD5C5C', '#8B0000']),
            graphic_opts=[
                    opts.GraphicGroup(
                        graphic_item=opts.GraphicItem(
                            bounding="raw",
                            right=150,
                            bottom=50,
                            z=100,
                        ),
                        children=[
                            opts.GraphicRect(
                                graphic_item=opts.GraphicItem(
                                    left="center", top="center", z=100
                                ),
                                graphic_shape_opts=opts.GraphicShapeOpts(
                                    width=200, height=50
                                ),
                                graphic_basicstyle_opts=opts.GraphicBasicStyleOpts(
                                    fill="rgba(0,0,0,0.3)"
                                ),
                            ),
                            opts.GraphicText(
                                graphic_item=opts.GraphicItem(
                                    left="center", top="center", z=100
                                ),
                                graphic_textstyle_opts=opts.GraphicTextStyleOpts(
                                    text=JsCode("['钻石号邮轮', '累计确诊人数：{}人'].join('\\n')"
                                                .format(dict(oversea_confirm)['Diamond Princess Cruise Ship'])),
                                    font="bold 16px Microsoft YaHei",
                                    graphic_basicstyle_opts=opts.GraphicBasicStyleOpts(
                                        fill="#fff"
                                    ),
                                ),
                            ),
                        ],
                    )
                ],
        )
    )

_map.render_notebook()