#!/usr/bin/env python
#coding:utf-8
#tested in win

import json


def merge_json(jsonlist):
    return json.dumps(jsonlist, indent=2)




if __name__ == "__main__":
    j1 = {'o1':1,'o2':2}
    # j2 = {'o1':1,'o2':2}

    jl = [j1]
    a = json.dumps(jl, indent=2)
    print(a)
    # print(type(a))
