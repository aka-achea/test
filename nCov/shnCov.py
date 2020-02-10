#!/usr/bin/python3
#coding:utf-8

import json
import os
import datetime,random

from pyecharts.options import AreaStyleOpts,TitleOpts,TooltipOpts,InitOpts,DataZoomOpts,\
    LineStyleOpts,VisualMapOpts,LegendOpts,TextStyleOpts,LabelOpts,GraphicShapeOpts,\
    GraphicGroup,GraphicItem,GraphicText,GraphicTextStyleOpts,GraphicBasicStyleOpts,GraphicRect,\
    CalendarOpts,ItemStyleOpts,AxisOpts,AxisTickOpts,GridOpts,BrushOpts,\
    AxisLineOpts,SplitLineOpts
from pyecharts.charts import Line, Bar, Graph, Map, Page, Calendar,Grid
# from pyecharts.faker import Faker
from pyecharts.globals import ChartType, SymbolType
from pyecharts.commons.utils import JsCode


from cos import outfile




def new_trend(day,newconfirmed,newpending) -> Line:
    line = (
        Line(init_opts=InitOpts())
        .add_xaxis(day)
        .add_yaxis(
            '新确诊',newconfirmed,symbol_size=1,
            # symbol='diamond',color='red',
            # is_symbol_show = False,
            itemstyle_opts=ItemStyleOpts(color='red'),
            label_opts=LabelOpts(font_size=15,color='darkred',position='inside'),
            linestyle_opts=LineStyleOpts(width=2,color='red'),
            is_connect_nones=True,is_smooth=True,
            )
        .add_yaxis(
            '新疑似',newpending,symbol_size=1,
            # symbol='triangle',color='blue',
            itemstyle_opts=ItemStyleOpts(color='blue'),
            label_opts=LabelOpts(font_size=15,color='darkblue',position='inside'),
            linestyle_opts=LineStyleOpts(width=2,color='blue'),
            is_connect_nones=True,is_smooth=True,
            )
        .set_global_opts(
            xaxis_opts=AxisOpts(
                # type_="category",
                axislabel_opts=LabelOpts(is_show=False),
            ),
            yaxis_opts=AxisOpts(
                # grid_index=1,
                # is_scale=True,
                # split_number=2,
                axislabel_opts=LabelOpts(is_show=False),
                # axisline_opts=AxisLineOpts(is_show=False),
                axistick_opts=AxisTickOpts(is_show=False),
                # splitline_opts=SplitLineOpts(is_show=False),
            ),
            legend_opts=LegendOpts(
                pos_top='top',pos_left='55%',
                textstyle_opts=TextStyleOpts(font_size=30),
                orient='horizontal',legend_icon='rect'
            ),
        )
    )
    return line


def total_trend(day,shdeath,shcured,shsum,shpending) -> Line:
    line = (
        Line(init_opts=InitOpts())
        .add_xaxis(day)
        # .add_yaxis("全国死亡",y_axis=death,is_connect_nones=True,is_smooth=True)
   
        .add_yaxis(
            '死亡',shdeath,symbol_size=10,color='black',
            itemstyle_opts=ItemStyleOpts(color='black'),
            label_opts=LabelOpts(is_show=False),
            areastyle_opts=AreaStyleOpts(opacity=0.5,color='black'),
            stack=1,is_connect_nones=True,is_smooth=True
            )
        .add_yaxis(
            '治愈',shcured,symbol_size=10,color='LimeGreen',
            itemstyle_opts=ItemStyleOpts(color='LimeGreen'),
            label_opts=LabelOpts(font_size=15,color='ForestGreen'),
            areastyle_opts=AreaStyleOpts(opacity=0.5,color='LimeGreen'),
            stack=1,is_connect_nones=True,is_smooth=True
            )
        .add_yaxis(
            '确诊',shsum,symbol_size=10,color='Orange',
            itemstyle_opts=ItemStyleOpts(color='Orange'),
            label_opts=LabelOpts(font_size=15,color='DarkOrange',font_weight='bold'),
            areastyle_opts=AreaStyleOpts(opacity=0.5,color='Orange'),
            stack=1,is_connect_nones=True,is_smooth=True
            )
        .add_yaxis(
            '疑似',shpending,symbol_size=10,color='LightSkyBlue',
            itemstyle_opts=ItemStyleOpts(color='LightSkyBlue'),
            label_opts=LabelOpts(font_size=15,color='DarkBlue'),
            areastyle_opts=AreaStyleOpts(opacity=0.5,color='LightSkyBlue'),
            stack=1,is_connect_nones=True,is_smooth=True
            )
        .set_global_opts(
            title_opts=TitleOpts(
                # title=title,
                # pos_left='10%',
                # pos_top='-10%',
                ),
            # tooltip_opts=TooltipOpts(formatter="{b} {a}\n {c}人"),
            datazoom_opts=[
                DataZoomOpts(range_start=40,range_end=100,xaxis_index=[0, 1],),
                DataZoomOpts(range_start=40,range_end=100,xaxis_index=[0, 1],type_='inside'),
                ],
            xaxis_opts=AxisOpts(name_gap=50),
            legend_opts=LegendOpts(
                pos_top='top',pos_left='10%',
                textstyle_opts=TextStyleOpts(font_size=30),
                orient='horizontal',legend_icon='rect'
                ),
            tooltip_opts=TooltipOpts(textstyle_opts=TextStyleOpts(font_size=30)),
            graphic_opts=GraphicGroup(
                graphic_item=GraphicItem(left="12%",top="11%"),
                children=[
                    GraphicRect(
                        graphic_item=GraphicItem(z=0,left="center",top="middle"),
                        graphic_shape_opts=GraphicShapeOpts(width=150, height=90),
                        graphic_basicstyle_opts=GraphicBasicStyleOpts(
                            fill="#fff",
                            stroke="black",
                            line_width=3,
                            )
                        ),                                        
                    GraphicText(
                        graphic_item=GraphicItem(left="center",top="middle",z=0),
                        graphic_textstyle_opts=GraphicTextStyleOpts(
                            text=f"确诊{shsum[-1]}人\n\n疑似{shpending[-1]}人",
                            font="bolder 20px sans-serif",
                            graphic_basicstyle_opts=GraphicBasicStyleOpts(fill="#333")
                            )
                        )
                    ]
                )
            )
        )
        # line.overlap(bar)
    return line


def map_visualmap(sumary) -> Map:
    c = (
        Map(
            init_opts=InitOpts(
            width="750px",
            height='1000px')
        )
        .add(
            "确诊",sumary,"上海",
            is_map_symbol_show=False,
            label_opts=None
            )
        .set_global_opts(
            title_opts=TitleOpts(
                title="分布统计（不含外地来沪和待确认）",
                subtitle='    市卫健局每日两次发布信息，如未更新，请尝试刷新页面',
                pos_left='10%',pos_top='top',
                title_textstyle_opts=TextStyleOpts(font_size=40),
                subtitle_textstyle_opts=TextStyleOpts(font_size=20),
                
                ),
            visualmap_opts=VisualMapOpts(
                max_=50,
                range_color=['lightblue','yellow','red'],
                pos_top='15%',pos_left='12%',
                item_height='200px',item_width='30px',
                textstyle_opts=TextStyleOpts(font_size=15)
                # split_number=50
                ),
            legend_opts=LegendOpts(is_show=False),
            tooltip_opts=TooltipOpts(textstyle_opts=TextStyleOpts(font_size=30)),
        )
    )
    return c


def calendar_base() -> Calendar:
    # begin = datetime.date(2020,1,19)
    # end = datetime.date(2020,3,1)
    # data = [
    #     [str(begin + datetime.timedelta(days=i)), random.randint(1000, 25000)]
    #     for i in range((end - begin).days + 1)
    # al
    # print(data)
    c = (
        Calendar(init_opts=InitOpts( width="100%"))
        .add(
            "", new_date, 
            calendar_opts=CalendarOpts(
                range_=['2020-1-15', '2020-3-1'],
                orient="vertical",
                pos_left=None,
                pos_right=None,
                pos_bottom=None,
                pos_top=None

                # daylabel_opts=LabelOpts(
                #     font_size=10
                # )

                )
            )
        .set_global_opts(
            title_opts=TitleOpts(
                title="新增病例时间分布图",
                pos_left='center',pos_top='bottom',
                title_textstyle_opts=TextStyleOpts(font_size=40),
                ),
            visualmap_opts=VisualMapOpts(
                max_=40,min_=1,
                orient="vertical",
                range_color=['white','yellow','red'],
                # is_piecewise=True,
                pos_top="230px",
                pos_left="100px",
                item_height='200px',item_width='30px',
            ),
        )
    )
    return c


def makechart(sumary,day,shdeath,shcured,shsum,shpending,newconfirmed,newpending):
    title = "上海新型冠状病毒统计"
    grid_chart = Grid()
    grid_chart.add(
        total_trend(day,shdeath,shcured,shsum,shpending),
        grid_opts=GridOpts(height="57%")
    )
    grid_chart.add(
        new_trend(day,newconfirmed,newpending),
        grid_opts=GridOpts(pos_top="75%",)
    )
    page = Page(page_title=title)
    page.add(
        grid_chart,        
        # calendar_base(),
        map_visualmap(sumary),
        )
    page.render(outfile)


if __name__ == "__main__":
    sumary = [('浦东新区', 32), ('静安区', 8),('宝山区', 8), ('闵行区', 7), ('长宁区', 7), ('徐汇区', 7),('金山区', 1),
 ('虹口区', 5), ('黄浦区', 5), ('奉贤区', 5), ('松江区', 3),('青浦区', 2), ('杨浦区', 2), ('嘉定区', 2), ('普陀区', 2) ]
    makechart(sumary)
