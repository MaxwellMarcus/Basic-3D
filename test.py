import random
l = []
for i in range(5):
    l.append([None,random.randint(1,100)])
sorted = []
def sort(l):
    sorted = []
    for i in l:
        if len(sorted)==0:
            sorted.append(i)
        else:
            for k in sorted:
                if i[1] < k[1]:
                    print(i[1],k[1])
                    sorted.insert(sorted.index(k),i)
                    break
                elif sorted.index(k) == len(sorted)-1:
                    sorted.append(i)
    return sorted

for i in sort(l):
    print(i[1])
