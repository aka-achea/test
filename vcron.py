#!/usr/bin/python3
#coding:utf-8
# tested in win


'''
Tool to centrally managed scheduled task
'''

import json,re
import datetime
from pprint import pprint


wday = datetime.datetime.now().isoweekday()
print(wday)


with open(r'M:\GH\test\job.json','r',encoding='utf8') as f:
    j=json.load(f)
    # pprint(j)
    tasklist = j['1'][0]
    # pprint(tasklist)

    # pprint(tasklist['0'])
    for x in range(len(tasklist)):
        command = tasklist[str(x)][0]['command']
        command = command.replace('|','\\')
        print(command)
        # param =  tasklist[str(x)][0]['param']



# if __name__ == "__main__":
#     pass