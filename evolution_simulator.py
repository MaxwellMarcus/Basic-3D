try:
    from tkinter import *
except:
    from Tkinter import *
import random
import math
import time

root = Tk()
canvas = Canvas(root,width = root.winfo_screenwidth(),height = root.winfo_screenheight())
canvas.pack()
height = float(root.winfo_screenheight())
width = float(root.winfo_screenwidth())
class Creature:
    def __init__(self,speed_x,speed_y):
        self.x = 0
        self.speed_x = speed_x
        self.speed_y = speed_y
    def run(self):
        self.fittness = math.sqrt(self.speed_y**2+self.speed_x**2)
        #for i in range(1000):
            #self.x += self.speed
    def mutate(self):
        change = random.randint(-maxSpeed/10,maxSpeed/10)
        while self.speed_x + change < minSpeed or self.speed_x + change > maxSpeed or change == 0:
            change = random.randint(-maxSpeed/10,maxSpeed/10)
        self.speed_x += change
        change = random.randint(-maxSpeed/10,maxSpeed/10)
        while self.speed_y + change < minSpeed or self.speed_y + change > maxSpeed:
            change = random.randint(-maxSpeed/10,maxSpeed/10)
        self.speed_y += change
def sort(l):
    for i in range(len(l)):
        l[i] = [(l[i])]
        l[i].append(l[i][0].fittness)
    sorted = []
    for i in l:
        if len(sorted)==0:
            sorted.append(i)
        else:
            for k in sorted:
                if i[1] > k[1]:
                    sorted.insert(sorted.index(k),i)
                    break
                elif sorted.index(k) == len(sorted)-1:
                    sorted.append(i)

    for i in range(len(sorted)):
        sorted[i] = sorted[i][0]
    return sorted

maxSpeed = 100
minSpeed = 0
maxFittness = math.sqrt(100**2+100**2)
def new_creatures(event):
    num_creatures = 15
    num_gens = 15
    creatures = []
    lines = []
    lines2 = []
    lines3 = []
    for i in range(num_creatures):
        creatures.append(Creature(random.randint(minSpeed,maxSpeed),random.randint(minSpeed,maxSpeed)))#random.randint(minSpeed,maxSpeed),random.randint(minSpeed,maxSpeed)))
    for i in range(num_gens):
        for l in creatures:
            l.run()
        creatures = sort(creatures)
        half = len(creatures)/2
        lines2.append(creatures[0].fittness)
        lines.append(creatures[len(creatures)-1].fittness)
        for i in range(len(creatures)):
            if i+1 == int(half):
                median = creatures[i]
            if i+1 > half:
                creatures[i] = Creature(creatures[int(i-half)].speed_x,creatures[int(i-half)].speed_y)
            creatures[i].mutate()
        lines3.append(median.fittness)
        canvas.delete(ALL)
        lastX = 0
        lastY = height/2
        for i in range(int(maxFittness)):
            if i%(int(maxFittness)/10) < 1:
                canvas.create_line(0,lastY-i*2,width,lastY-i*2)
                canvas.create_text(50,lastY-i*2,text=str(int(i)),font=('TkTextFont',20))
        for i in range(len(lines)+1):
            canvas.create_line(i*width/len(lines),0,i*width/len(lines),height-height/2+15)
            canvas.create_text(i*width/len(lines),height-height/2+10,text=str(i),font=('TkTextFont',20))
        for i in lines:
            x = lastX + width/len(lines)
            y = height/2-i*2
            canvas.create_line(lastX,lastY,x,y,fill = 'red',width=3)
            lastX = x
            lastY = y
        lastX = 0
        lastY = height/2
        for l in lines2:
            x = lastX + width/len(lines)
            y = height/2-l*2
            canvas.create_line(lastX,lastY,x,y,fill = 'green',width=3)
            lastX = x
            lastY = y
        lastX = 0
        lastY = height/2
        for l in lines3:
            x = lastX + width/len(lines)
            y = height/2-l*2
            canvas.create_line(lastX,lastY,x,y,fill = 'black',width=3)
            lastX = x
            lastY = y

        root.update()
        time.sleep(.5)

root.bind('<Key>',new_creatures)
root.mainloop()
