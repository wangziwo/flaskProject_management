# encoding: utf-8
d = {'a':'1','b':'2'}
t = ('a','b','b')
l3 = []

for l in d:
    l1 = []
    l1.append(l)
    l1.append(d[l])
    l3.append(l1)
# print(l3)
for i in t:
    print(i,t.index(i))