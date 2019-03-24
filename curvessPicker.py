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
        self.radius = 300
        self.center_x = centerX
        self.center_y = centerY
        self.point_x = centerX
        self.point_y = centerY - self.radius
        self.speed = speed
        self.lineDir = lineDir
    #    self.circle = canvas.create_oval(self.center_x-self.radius,self.center_y-self.radius,self.center_x+self.radius,self.center_y+self.radius)
    #    self.point = canvas.create_oval(self.point_x-2,self.point_y-2,self.point_x+2,self.point_y+2,fill='black')
    #    self.line = canvas.create_line(self.point_x,self.point_y,self.point_x,root.winfo_screenheight())
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
    def reset(self):
        self.x_circle.reset()
        self.y_circle.reset()
        self.first = True
    def update(self):
        self.x_circle.update()
        self.y_circle.update()
        self.last_x = self.x
        self.last_y = self.y
        self.x = self.x_circle.point_x
        self.y = self.y_circle.point_y
    def draw(self):
        if not self.first:
            canvas.create_line(self.x,self.y,self.last_x,self.last_y,width=5)
        else:
            self.first = False
circleRadius = 500
x_circles = []
y_circles = []
curves = []
num_x_circles = 1000
num_y_circles = 1000
curve_showing_x = 0
curve_showing_y = 0
x_dist = root.winfo_screenwidth()/(num_x_circles+1)
y_dist = root.winfo_screenheight()/(num_y_circles+1)
root.update()
for i in range(num_x_circles):
    x_circles.append(Circle(root.winfo_screenwidth()/2,circleRadius,(i+1),'y'))
    if i%10 == 9:
        canvas.delete(ALL)
        canvas.create_text(root.winfo_screenwidth()/2,root.winfo_screenheight()/2,text='creating new circles: '+str(i+1)+'/'+str(num_x_circles+num_y_circles),font=('TkTextFont',100))
        root.update()
        print('creating new things: '+str(i+1)+'/'+str(num_x_circles+num_y_circles))#+num_x_circles*num_y_circles))
for i in range(num_y_circles):
    y_circles.append(Circle(circleRadius,root.winfo_screenheight()/2,(i+1),'x'))
    if i%10 == 9:
        canvas.delete(ALL)
        canvas.create_text(root.winfo_screenwidth()/2,root.winfo_screenheight()/2,text='making more circles: '+str(i+1+num_x_circles)+'/'+str(num_x_circles+num_y_circles),font=('TkTextFont',100))
        root.update()
    print('some more things: '+str(i+1+num_x_circles)+'/'+str(num_x_circles+num_y_circles))#+num_x_circles*num_y_circles))
for x in x_circles:
    sublist = []
    for y in y_circles:
        #number = (x_circles.index(x))*len(x_circles)+y_circles.index(y)
        #if number%100000 == 0:
        #    print('a few more: '+str(number+1+num_x_circles+num_y_circles)+'/'+str(num_x_circles+num_y_circles+num_x_circles*num_y_circles))
        sublist.append(Curve(x,y))
    curves.append(sublist)

def next_curve_x_plus(event):
    global curve_showing_x
    global num_x_circles
    global curves
    canvas.delete(ALL)
    if curve_showing_x+1 < num_x_circles:
        curve_showing_x += 1
    else:
        curve_showing_x = 0
    curves[curve_showing_x][curve_showing_y].reset()
def next_curve_y_plus(event):
    global curve_showing_y
    global num_y_circles
    global curves
    canvas.delete(ALL)
    if curve_showing_y+1 < num_y_circles:
        curve_showing_y += 1
    else:
        curve_showing_y = 0
    curves[curve_showing_x][curve_showing_y].reset()
def next_curve_x_minus(event):
    global curve_showing_x
    global num_x_circles
    global curves
    canvas.delete(ALL)
    if curve_showing_x > 0:
        curve_showing_x -= 1
    else:
        curve_showing_x = num_x_circles-1
    curves[curve_showing_x][curve_showing_y].reset()
def next_curve_y_minus(event):
    global curve_showing_y
    global num_y_circles
    global curves
    canvas.delete(ALL)
    if curve_showing_y > 0:
        curve_showing_y -= 1
    else:
        curve_showing_y = num_y_circles-1
    curves[curve_showing_x][curve_showing_y].reset()

root.bind('d',next_curve_x_plus)
root.bind('s',next_curve_y_plus)
root.bind('a',next_curve_x_minus)
root.bind('w',next_curve_y_minus)

go = True
canvas.delete(ALL)
while go:
    try:
        for l in range(1):
            curves[curve_showing_x][curve_showing_y].update()
            curves[curve_showing_x][curve_showing_y].draw()
        canvas.create_text(root.winfo_screenwidth()/2,100,text=str(curve_showing_x)+','+str(curve_showing_y),font=('TkTextFont',50))
        root.update()
    except:
        go = False
