
a = {'ge':'s'}
# print(hash(a))

from dis import dis

dis(a['ge'])

print(id(a))