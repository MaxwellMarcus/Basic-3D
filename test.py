import random
l = []
for i in range(100):
    l.append([None,random.randint(1,100)])
sorted = []
for i in l:
    if len(sorted)==0:
        first = False
        sorted.append(i)
    elif i[1] > sorted[0][1]:
        sorted.insert(0,i)
    elif not i[1] < sorted[len(sorted)-1][1]:
        for k in sorted:
            if i[1] > k[1]:
                sorted.insert(sorted.index(k),i)
                break
    else:
        sorted.append(i)
for i in range(len(sorted)):
    sorted[i] = sorted[i][0]
print(len(sorted))
