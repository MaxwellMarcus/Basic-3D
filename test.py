import random
l = []
for i in range(1000):
    l.append([None,random.randint(1,100)])
def sort(l):
    sorted = []
    print(len(l))
    for i in l:
        now = len(sorted)
        if len(sorted)==0:
            sorted.append(i)
        elif i[1] > sorted[len(sorted)-1][1]:
            sorted.append(i)
        else:
            for k in sorted:
                if i[1] < k[1]:
                    sorted.insert(sorted.index(k),i)
                    break
                elif sorted.index(k) == len(sorted)-1:
                    sorted.append(i)
                    break
        #if now == len(sorted):
            #print(i[1])
    return sorted
l.sort()
for i in l:
    print(i)
