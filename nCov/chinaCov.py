import requests
import pyecharts
from pyecharts.charts import *
from pyecharts import options as opts
from pyecharts.commons.utils import JsCode
from datetime import date, datetime
import datetime
from pprint import pprint

# 获取时间序列数据
# 细分到城市
area_data_timeline = requests.get('https://lab.isaaclin.cn/nCoV/api/area?latest=0').json()

# 全国数据
all_data_timeline = requests.get('http://lab.isaaclin.cn/nCoV/api/overall?latest=0').json()

# 生成更新日期
update_date = date.today()


def get_value(dic, key):
    try:
        return dic[key]
    except KeyError:
        return 0

def insert_data(to_update_date, to_update_area, dic, is_city):
    if to_update_date in format_data:
        if to_update_area in format_data[to_update_date]:
            pass
        else:
            format_data[to_update_date][to_update_area] = {}
    else:
        format_data[to_update_date] = {}
        format_data[to_update_date][to_update_area] = {}
    format_data[to_update_date][to_update_area]['currentConfirmedCount'] = get_value(dic, 'currentConfirmedCount')
    format_data[to_update_date][to_update_area]['confirmedCount'] = get_value(dic, 'confirmedCount')
    format_data[to_update_date][to_update_area]['deadCount'] = get_value(dic, 'deadCount')
    format_data[to_update_date][to_update_area]['suspectedCount'] = get_value(dic, 'suspectedCount')
    format_data[to_update_date][to_update_area]['curedCount'] = get_value(dic, 'curedCount')
    format_data[to_update_date][to_update_area]['countryName'] = get_value(dic, 'countryName')
    # 用于区分区域层级
    if is_city:
        format_data[to_update_date][to_update_area]['is_city'] = 1 
    else:
        format_data[to_update_date][to_update_area]['is_city'] = 0

format_data = {}
for item in area_data_timeline['results'][::-1]:
    to_update_date = date.fromtimestamp(item['updateTime']/1000)
    to_update_area = item['provinceShortName']
    insert_data(to_update_date, to_update_area, item, 0)
    if 'cities' in item:
        if item['cities']:
            for city_data in item['cities']:
                insert_data(to_update_date, city_data['cityName'], city_data, 1)

for item in all_data_timeline['results'][::-1]:
    to_update_date = date.fromtimestamp(item['updateTime']/1000)
    insert_data(to_update_date, '全国', item, 0)

time_range = list(format_data.keys())



def area_data(area_name='湖北', type_='confirmedCount', get_total=True, date_list=time_range):
    # 用于pyecharts获取时间序列数据
    data_array = []
    for day in date_list:
        try:
            data_array.append(format_data[day][area_name][type_])
        except KeyError:
            if day + datetime.timedelta(days=-1) in format_data:
                if area_name in format_data[day + datetime.timedelta(days=-1)]:
                    # 当天未更新数据情况时，取前一天数据填充
                    data_array.append(format_data[day + datetime.timedelta(days=-1)][area_name][type_])
                else:
                    data_array.append(0)
            else:
                data_array.append(0)
    # 返回每日新增数据
    if not get_total:
        data_array = [data_array[i+1] - data_array[i] for i in range(len(data_array)-1)]
    return data_array







cities_data = []
for item in data['results']:
    if item['countryName'] == '中国':
        cities_data.extend((item['cities']))

geo = (
        Geo(init_opts=opts.InitOpts(theme='dark', width='400'))
        .add_schema(maptype="china", zoom=3, center=[114.31,30.52])
        .add("累计确诊人数", 
             [(i['cityName'], i['currentConfirmedCount']) for i in cities_data 
              if i['cityName'] in pyecharts.datasets.COORDINATES.keys()], 
             type_='heatmap',
             symbol_size=3,
             progressive=50)
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(
            title_opts=opts.TitleOpts(title="新型冠状病毒全国疫情热力图",
                                     subtitle="更新日期：{}".format(update_date),
                                     pos_left='right'),
            legend_opts=opts.LegendOpts(is_show=False),
            visualmap_opts=opts.VisualMapOpts(is_show=True, 
                                              is_piecewise=False, 
                                              range_color=['blue', 'green', 'yellow', 'yellow', 'red'])
        )
)

geo.render_notebook()