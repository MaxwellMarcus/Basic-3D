try:
    from tkinter import *
except:
    from Tkinter import *
import random

root = Tk()
canvas = Canvas(root,width = root.winfo_screenwidth(),height = root.winfo_screenheight())
canvas.pack()
height = float(root.winfo_screenheight())
width = float(root.winfo_screenwidth())
class Creature:
    def __init__(self,speed):
        self.x = 0
        self.speed = speed
    def run(self):
        x = self.speed
        #for i in range(1000):
            #self.x += self.speed
    def mutate(self):
        change = random.randint(-1,1)
        while self.speed + change < minSpeed or self.speed + change > maxSpeed or change == 0:
            change = random.randint(-1,1)
        self.speed += change
def sort(l):
    for i in range(len(l)):
        l[i] = [(l[i])]
        l[i].append(l[i][0].speed)
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

maxSpeed = 100
minSpeed = 0
num_creatures = 15
creatures = []
lines = []
lines2 = []
lines3 = []
for i in range(num_creatures):
    creatures.append(Creature(random.randint(1,100)))
last = None
for i in range(15):
    for l in creatures:
        l.run()
    creatures = sort(creatures)
    half = len(creatures)/2
    lines.append(creatures[len(creatures)-1].speed)
    print(half)
    for i in range(len(creatures)):
        print(i)
        if i+1 == int(half):
            median = creatures[i]
        if i+1 > half:
        #    creatures[i] = Creature(creatures[int(i-half)].speed)
            creatures[i].mutate()
    lines2.append(creatures[0].speed)
    lines3.append(median.speed)
    canvas.delete(ALL)
    lastX = 0
    lastY = height/2
    for i in range(11):
        canvas.create_line(0,lastY-(i*10)*3,width,lastY-(i*10)*3)
        canvas.create_text(20,lastY-(i*10)*3,text=str(i*10),font=('TkTextFont',20))
    for i in range(len(lines)):
        canvas.create_line(i*width/len(lines),0,i*width/len(lines),height)
        canvas.create_text()
    for i in lines:
        x = lastX + width/len(lines)
        y = height/2-i*3
        canvas.create_line(lastX,lastY,x,y,fill = 'red')
        lastX = x
        lastY = y
    lastX = 0
    lastY = height/2
    for l in lines2:
        x = lastX + width/len(lines)
        y = height/2-l*3
        canvas.create_line(lastX,lastY,x,y,fill = 'green')
        lastX = x
        lastY = y
    lastX = 0
    lastY = height/2
    for l in lines3:
        x = lastX + width/len(lines)
        y = height/2-l*3
        canvas.create_line(lastX,lastY,x,y,fill = 'black')
        lastX = x
        lastY = y

    root.update()
root.mainloop()
