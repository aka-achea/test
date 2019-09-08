


import numpy as np
import os


base = np.array([
    [1,4,4],
    [0,2,2],
    [1,3,3],  ])


a = base[1][1]
b = base[1][2]

print(f'{a} at (1,1)')

start = (1,1)
startrow,startcol = start[0],start[1]


for g in ['up','down','left','right']:
    print(f'go {g}')
    if g == 'up':
        row = startrow - 1
        col = startcol
        next = base[row][col]
        print(f'{next} at ({row},{col})')
        if next == a:
            print('match')
            break
    elif g == 'right':
        row = startrow
        col = startcol + 1
        next = base[row][col]
        print(f'{next} at ({row},{col})')
        if next == a:
            print('match')
            break
    elif g == 'down':
        row = startrow + 1
        col = startcol
        next = base[row][col]
        print(f'{next} at ({row},{col})')
        if next == a:
            print('match')
            break
    elif g == 'left':
        row = startrow 
        col = startcol -1 
        next = base[row][col]
        print(f'{next} at ({row},{col})')
        if next == a:
            print('match')
            break