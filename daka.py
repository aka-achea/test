
import openpyxl

s = r'D:\Profile\Desktop\wt.txt'
xl = r'e:\上海钒兆钛智能科技有限公司_考勤报表_20190101-20190125.xlsx'
kq = r'e:\kq.xlsx'

wb = openpyxl.load_workbook(kq)

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
    # sheet2 = wb['统计']
    for i in range(2,sheet1.max_row+1):
    # for i in range(2,60):        
        name = sheet1.cell(row=i,column=1).value
        if name not in tjdic:
            tjdic[name] = {}

        dk = sheet1.cell(row=i,column=2).value # 打卡日期时间
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
            # print(tjdic)
        else:   # 上班
            tjdic[name][day]['on'] = hm
            # print(tjdic)
    # print(tjdic)
    return tjdic
    #     sheet2.cell(row=r,column=c).value = ti
    # wb.save(kq)

def fillempty(tjdic):
    for i in tjdic:
        name = i
        for d in tjdic[i]:
            day = d
            if 'on' not in tjdic[i][d]:
                tjdic[name][day]['on'] = 9
            if 'off' not in tjdic[i][d]:
                tjdic[name][day]['off'] = 18
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
        for d in tjdic[i]:
            day = d
            off = tjdic[name][day]['off']
            on = tjdic[name][day]['on']
            sumt = sumt + off - on
            avgt = avgt + on
            if off > maxt: maxt = off
        avgt = avgt / len(tjdic[i])
        # print(name,maxt,avgt,sumt)
        result[name]['max'] = maxt
        result[name]['avg'] = avgt
        result[name]['sum'] = sumt
    # print(result)
    return result

def winner(result):
    print('='*15)
    print('最晚下班排行榜')
    print('='*15)
    maxwinner = {}
    for i in result:
        maxwinner[result[i]['max']] = i
    for i in sorted(maxwinner,reverse=True):
        print('%s : %.2f' % (maxwinner[i],i) )

    print('='*15)
    print('平均早鸟排行榜')
    print('='*15)
    avgwinner = {}
    for i in result:
        avgwinner[result[i]['avg']] = i
    for i in sorted(avgwinner):
        print('%s : %.2f' % (avgwinner[i],i) )

    print('='*15)
    print('最拼命榜')
    print('='*15)
    sumwinner = {}
    for i in result:
        sumwinner[result[i]['sum']] = i
    for i in sorted(sumwinner,reverse=True):
        print('%s : %.2f' % (sumwinner[i],i) )

            

try:
    # tjrow = buildtongji(wb)
    tjdic = tj(wb)
    tjdic = fillempty(tjdic)
    result = cal(tjdic)
    winner(result)
except PermissionError as e:
    print(e)
    print('Is file being opened?')






