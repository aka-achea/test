#!/usr/bin/python3
#coding:utf-8

import json
import os
import datetime,random
from pyecharts.options import (
    AreaStyleOpts,AxisOpts,AxisTickOpts,AxisLineOpts,
    BrushOpts,CalendarOpts,DataZoomOpts,
    InitOpts,ItemStyleOpts,
    TitleOpts,TooltipOpts,TextStyleOpts,
    LineStyleOpts,LegendOpts,LabelOpts,
    GraphicGroup,GraphicItem,GraphicText,GraphicTextStyleOpts,
    GraphicBasicStyleOpts,GraphicRect,GridOpts,GraphicShapeOpts,
    VisualMapOpts,SplitLineOpts,
    )
from pyecharts.charts import Line,Bar,Graph,Map,Calendar,Grid,BMap,Tab
from pyecharts.globals import ChartType,SymbolType
# from pyecharts.commons.utils import JsCode


from crawler import get_detail
from conf import data,ak_web,geofile,outfile,ak_dev



def data_process(data):
    day = [ day[5:] for day in data.keys() ]
    death = [ a[0] if a != () else 0 for a in data.values() ]
    shsum = [ a[1] if a != () else 0 for a in data.values() ]
    shpending = [ a[2] if a != () else 0 for a in data.values() ]
    shcured = [ a[3] if a != () else 0 for a in data.values() ]
    shdeath = [ a[4] if a != () else 0 for a in data.values() ]
    shsum_date = [ (a,data[a][1]) for a in data.keys() ] 
    new_date = [ (shsum_date[n][0],shsum_date[n][1]-shsum_date[n-1][1] ) if n>0 else (shsum_date[n][0],shsum_date[n][1]) for n in range(len(shsum_date)) ]
    newconfirmed = [ shsum[n]-shsum[n-1] if n>0 else shsum[n] for n in range(len(shsum)) ]
    # print(new)
    newpending = [ shpending[n]-shpending[n-1] if n>0 else shpending[n] for n in range(len(shpending)) ]
    return day,shsum,shpending,shcured,shdeath,shsum_date,new_date,newconfirmed,newpending


def bmap_base(geofile=geofile,BAIDU_AK=ak_web) -> BMap:
    with open(geofile,'r',encoding='utf-8') as f:
        j = json.loads(f.read())
    location = [[k,1] for k in j.keys()]
    c = (
        BMap()
        .add_schema(
            baidu_ak=BAIDU_AK,
            center=[121.497739,31.242029],
            zoom=11
        )
        .add_coordinate_json(json_file=geofile)
        .add(
            '',location,
            # type_='heatmap',
            label_opts=LabelOpts(is_show=False)
        )
        .set_global_opts(title_opts=TitleOpts())
    )
    return c


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
                max_=70,
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


def makechart(data):
    day,shsum,shpending,shcured,shdeath,shsum_date,new_date,newconfirmed,newpending = data_process(data)
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
    sumary = get_detail()
    tab = Tab(page_title=title)
    tab.add(grid_chart, "趋势")
    tab.add(map_visualmap(sumary), "分布")
    tab.add(bmap_base(),'详细地图')
    tab.render(outfile) 


if __name__ == "__main__":
    # from conf import sumarysample
    makechart(data)
