import random
class Creature:
    def __init__(self,speed):
        self.x = 0
        self.speed = speed
    def run(self):
        for i in range(1000):
            self.x += self.speed
    def mutate(self):
        self.speed += random.randint(-10,10)/10

def sort(l):
    for i in range(len(l)):
        l[i] = [(l[i])]
        l[i].append(l[i][0].x)
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
    return sorted

creatures = []
for i in range(1000):
    creatures.append(Creature(random.randint(1,1000000)))
    creatures[i].run()
for i in range(100):
    creatures = sort(creatures)
    half = len(creatures)/2
    for i in range(len(creatures)):
         if i+1 > half:
             creatures[i] = creatures[int(i-half)]
         creatures[i].mutate()
    print(creatures[0].x)
