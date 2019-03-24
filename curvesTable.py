try:
    from tkinter import *
except:
    from Tkinter import *
import math

root = Tk()
canvas = Canvas(root,width = root.winfo_screenwidth(),height = root.winfo_screenheight())
canvas.pack()

class Circle:
    def __init__(self,centerX,centerY,speed,lineDir):
        self.radius = 20
        self.center_x = centerX
        self.center_y = centerY
        self.point_x = centerX
        self.point_y = centerY - self.radius
        self.speed = speed
        self.lineDir = lineDir
        self.circle = canvas.create_oval(self.center_x-self.radius,self.center_y-self.radius,self.center_x+self.radius,self.center_y+self.radius)
        self.point = canvas.create_oval(self.point_x-2,self.point_y-2,self.point_x+2,self.point_y+2,fill='black')
        self.line = canvas.create_line(self.point_x,self.point_y,self.point_x,root.winfo_screenheight())
    def reset(self):
        self.point_x = self.center_x
        self.point_y = self.center_y - self.radius
    def update(self):
        x = self.point_x - self.center_x
        y = self.point_y - self.center_y
        cos = math.cos((math.pi/180)*self.speed)
        sin = math.sin((math.pi/180)*self.speed)
        self.point_x = (x*cos)-(y*sin)+self.center_x
        self.point_y = (y*cos)+(x*sin)+self.center_y
    def draw(self):
        canvas.delete(self.circle)
        canvas.delete(self.point)
        canvas.delete(self.line)
        self.circle = canvas.create_oval(self.center_x-self.radius,self.center_y-self.radius,self.center_x+self.radius,self.center_y+self.radius)
        self.point = canvas.create_oval(self.point_x-2,self.point_y-2,self.point_x+2,self.point_y+2,fill='black')
        if self.lineDir == 'y':
            self.line = canvas.create_line(self.point_x,self.point_y,self.point_x,root.winfo_screenheight())
        elif self.lineDir == 'x':
            self.line = canvas.create_line(self.point_x,self.point_y,root.winfo_screenwidth(),self.point_y)

class Curve:
    def __init__(self,xcircle,ycircle):
        self.x_circle = xcircle
        self.y_circle = ycircle
        self.x = self.x_circle.point_x
        self.y = self.y_circle.point_y
        self.last_x = self.x
        self.last_y = self.y
        self.first = True
        self.loops = 0
    def reset(self):
        self.x_circle.reset()
        self.y_circle.reset()
        self.first = True
        self.loops = 0
    def update(self):
        #if self.loops <= 360+min([self.x_circle.speed,self.y_circle.speed]):
        self.last_x = self.x
        self.last_y = self.y
        self.x = self.x_circle.point_x
        self.y = self.y_circle.point_y
        self.loops += min([self.x_circle.speed,self.y_circle.speed])

    def draw(self):
        if not self.first:# and self.loops <= 360+min([self.x_circle.speed,self.y_circle.speed]):
            canvas.create_line(self.x,self.y,self.last_x,self.last_y,width=1)
        elif self.first:
            self.first = False
circleRadius = 20
x_circles = []
y_circles = []
curves = []
num_x_circles = 10
num_y_circles = 8
x_dist = root.winfo_screenwidth()/(num_x_circles+1)
y_dist = root.winfo_screenheight()/(num_y_circles+1)
for i in range(num_x_circles):
    x_circles.append(Circle((i+1)*x_dist,circleRadius,(i+1),'y'))
#    if i%10 == 9:
#        canvas.delete(ALL)
#        canvas.create_text(root.winfo_screenwidth()/2,root.winfo_screenheight()/2,text='creating new circles: '+str(i+1)+'/'+str(num_x_circles+num_y_circles),font=('TkTextFont',100))
#        root.update()
for i in range(num_y_circles):
    y_circles.append(Circle(circleRadius,(i+1)*y_dist,(i+1),'x'))
#    if i%10 == 9:
#        canvas.delete(ALL)
#        canvas.create_text(root.winfo_screenwidth()/2,root.winfo_screenheight()/2,text='making more circles: '+str(i+1+num_x_circles)+'/'+str(num_x_circles+num_y_circles),font=('TkTextFont',100))
#        root.update()
for x in x_circles:
    sublist = []
    for y in y_circles:
        #number = (x_circles.index(x))*len(x_circles)+y_circles.index(y)
        #if number%100000 == 0:
        #    print('a few more: '+str(number+1+num_x_circles+num_y_circles)+'/'+str(num_x_circles+num_y_circles+num_x_circles*num_y_circles))
        sublist.append(Curve(x,y))
    curves.append(sublist)

go = True
loops = 0
while go:
    try:
        for l in range(2):
            for i in x_circles:
                i.update()
                i.draw()
            for i in y_circles:
                i.update()
                i.draw()
            for i in curves:
                for q in i:
                    q.update()
                    q.draw()
            loops += 1
        root.update()
        if loops == 450:
            loops = 0
            for i in curves:
                for l in i:
                    canvas.delete(ALL)
                    l.reset()
    except:
        go = False
