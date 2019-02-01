
import openpyxl,math,re,os,configparser
import PIL
from PIL import ImageFont, Image, ImageDraw




# kq = 'baseline.xlsx'
# workpath = r'e:\daka'
# # workpath = os.path.dirname(os.path.realpath(__file__))
# fontfile = 'STHUPO.TTF'
# background = 't.jpg'
# outwsum = 'wsum.jpg'
# outwon = 'won.jpg'
# outwoff = 'woff.jpg'
# color = (239,232,23)
# size = 30

confile = 'daka.ini'
workpath = os.path.dirname(os.path.realpath(__file__))
confilepath = os.path.join(workpath,confile)
config = configparser.ConfigParser()
config.read(confilepath)
kq = config['setting']['kq']
fontfile = config['setting']['fontfile']
background = config['setting']['background']
outwsum = config['setting']['outwsum']
outwon = config['setting']['outwon']
outwoff = config['setting']['outwoff']
size = int(config['setting']['size'])
# workpath = config['setting']['workpath']


color = config['setting']['color']
c = color.split(',')
color = ( int(c[0]),int(c[1]),int(c[2]) )

fontfilepath = os.path.join(workpath,fontfile)
font = ImageFont.truetype(fontfile,size,encoding='utf-8')
imageFile = os.path.join(workpath,background)
wb = openpyxl.load_workbook(os.path.join(workpath,kq))

# def buildtongji(wb):
#     tjrow = {}
#     sheet2 = wb['统计']
#     for i in range(2,sheet2.max_row+1):
#         name = sheet2.cell(row=i,column=1).value
#         d = sheet2.cell(row=i,column=2).value
#         tjrow[name+d] = i
#     # print(tjrow)
#     return tjrow

def tj(wb):
    tjdic ={}
    sheet1 = wb['原始记录']  
    for i in range(4,sheet1.max_row+1):
        status = sheet1.cell(row=i,column=6).value
        # print(status)
        if  re.search('打卡无效',status):
            print('打卡无效')
            continue

        name = sheet1.cell(row=i,column=1).value
        if name not in tjdic:
            tjdic[name] = {}

        dk = sheet1.cell(row=i,column=3).value # 打卡日期时间
        day = dk.split(' ')[0].split('-')[-1].replace('0','') 
        if day not in tjdic[name]:
            tjdic[name][day] = {}
        ti = dk.split(' ')[-1] # 打卡时间
        h = int(ti.split(':')[0])
        m = int(ti.split(':')[1])
        hm = h+m/60
        # print(name+' '+day+' '+dk)
        if hm > 12: # 下班
            tjdic[name][day]['off'] = hm
            tjdic[name][day]['rawoff'] = ti
            # print(tjdic)
        else:   # 上班
            tjdic[name][day]['on'] = hm
            tjdic[name][day]['rawon'] = ti
            # print(tjdic)
    # print(tjdic)
    return tjdic

def fillempty(tjdic):
    for i in tjdic:
        name = i
        for d in tjdic[i]:
            day = d
            if 'on' not in tjdic[i][d]:
                tjdic[name][day]['on'] = 9
                tjdic[name][day]['rawon'] = '9:00'
            if 'off' not in tjdic[i][d]:
                tjdic[name][day]['off'] = 18
                tjdic[name][day]['rawoff'] = '18:00'
    # print(tjdic)     
    return tjdic

def cal(tjdic):
    result = {}
    for i in tjdic:
        name = i
        result[name] = {}    
        maxt = 0
        avgt = 0
        sumt = 0
        maxoff = ''
        for d in tjdic[i]:
            day = d
            off = tjdic[name][day]['off']
            rawoff = tjdic[name][day]['rawoff']
            on = tjdic[name][day]['on']
            sumt = sumt + off - on
            avgt = avgt + on
            if off > maxt: 
                maxt = off
                maxoff = rawoff
        avgt = avgt / len(tjdic[i])
        # print(name,maxt,avgt,sumt)
        result[name]['max'] = maxoff
        result[name]['avg'] = avgt
        result[name]['sum'] = sumt
    # print(result)
    return result

def s2hm(i): # convert string to Hour:Minute
    h = int(i)
    h = '0'+str(h) if h <10 else str(h)
    m = round((i - int(i))*60)
    m = '0'+str(m) if m <10 else str(m)
    hm = h+':'+m
    return hm

def winneroff(result):
    print('='*15)
    print('最晚下班排行榜')
    print('='*15)
    maxwinner = {}
    count = 0
    for i in result:
        maxwinner[result[i]['max']] = i
    woff = {}
    for i in sorted(maxwinner,reverse=True):
        count += 1
        print('%s %s %s' % (count,maxwinner[i],i) )
        woff[count] = (maxwinner[i],i)        
        if count == 10: break
    return woff

def winneron(result):
    print('='*15)
    print('平均早鸟排行榜')
    print('='*15)
    avgwinner = {}
    count = 0
    for i in result:
        avgwinner[result[i]['avg']] = i
    won = {}
    for i in sorted(avgwinner):
        hm = s2hm(i)
        count += 1
        print('%s %s %s' % (count,avgwinner[i],hm) )
        won[count] = (avgwinner[i],hm)        
        if count == 10: break
    return won

def winnersum(result):
    print('='*15)
    print('最拼命榜')
    print('='*15)
    sumwinner = {}
    count = 0
    for i in result:
        sumwinner[result[i]['sum']] = i    
    wsum = {}
    for i in sorted(sumwinner,reverse=True):
        hm = s2hm(i)
        count += 1
        print('%s %s %s' % (count , sumwinner[i],hm) )
        wsum[count] = (sumwinner[i],hm)
        if count == 10: break
    return wsum
            
# wdic = {position:(name,value)...}
def windraw(wdic,imout,title):
    im = Image.open(imageFile)
    draw = ImageDraw.Draw(im)
    x,y = (70,50) #初始左上角的坐标
    xstep = 100
    ystep = 40
    texttile = title[0]
    draw.text( (x+xstep*2,y),texttile,color,font=font )
    x,y = (x, y+ystep*2)
    draw.text( (x,y),title[1],color,font=font )
    draw.text( (x+xstep*2,y),title[2],color,font=font )
    draw.text( (x+xstep*3.5,y),title[3],color,font=font )
    x,y = (x, y+ystep)
    for i in range(10):
        textposition = str(i+1)
        textname = wdic[i+1][0]
        textvalue = wdic[i+1][1]
        # print(textposition,textname,textvalue)
        draw.text( (x,y),textposition,color,font=font )
        draw.text( (x+xstep*2,y),textname,color,font=font )
        draw.text( (x+xstep*4.2,y),textvalue,color,font=font )
        x,y = (x,y+ystep)
    draw = ImageDraw.Draw(im)
    im.save(imout)


try:
    tjdic = tj(wb)
    tjdic = fillempty(tjdic)
    result = cal(tjdic)
    won =  winneron(result)
    woff = winneroff(result)
    wsum = winnersum(result)
except PermissionError as e:
    print(e)
    print('Is file being opened?')


title = ['办公室达人','排名','名字','工作时长（小时）']
outpath = os.path.join(workpath,outwsum)
windraw(wsum,outpath,title)

title = ['早鸟榜','排名','名字','平均打卡时间']
outpath = os.path.join(workpath,outwon)
windraw(won,outpath,title)

title = ['夜归人','排名','名字','最晚打卡时间']
outpath = os.path.join(workpath,outwoff)
windraw(woff,outpath,title)

