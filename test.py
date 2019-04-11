import random
l = []
for i in range(1000):
    l.append([None,random.randint(1,100)])
def sort(l):
    sorted = []
    print(len(l))
    for i in l:
        if len(sorted)==0:
            sorted.append(i)
        else:
            for k in sorted:
                #print(len(sorted))
                #print(i[1],k[1])
                #print(len(l))
                #print(sorted.index(k))
                #print('')
                if i[1] <= k[1]:
                    sorted.insert(sorted.index(k),i)
                #    print('this')
                    break
                elif sorted.index(k) == len(sorted)-1:
                #    print('that')
                    sorted.append(i)
                    break
    return sorted
for i in range(2):
    l = sort(l)
    print(len(l))
    print('')
