try:
    from Tkinter import *
except:
    from tkinter import *

import random
import math

root = Tk()
#root.config(cursor = "none")

canvas = Canvas(root,width = root.winfo_screenwidth(),height = root.winfo_screenheight())
canvas.pack()

class _3D:
    def __init__(self,fl):
        self.fl = fl
        self.radius = 1000
        self.centerZ = 0
        self.mouseX = 0
        self.mouseY = 0
        self.camPos = [0,0,0]
        self.mousePressed = False

        self.keysPressed = []

        root.bind('<Motion>',self.mouseSet)
        root.bind('<KeyPress>',self.keyPressed)
        root.bind('<KeyRelease>',self.KeyReleased)
        root.bind('<Button-1>',self.mousePress)
        root.bind('<ButtonRelease-1>',self.mouseRelease)

    def mouseSet(self,event):
        self.mouseX = event.x
        self.mouseY = event.y
    def zsort(self,num,smallest=False):
        olen = len(num)

        ans = []

        added = False

        if smallest:
            i = 0
            while len(num) > 0:
                added = False
                if len(num) == olen:
                    ans.append(num[0])
                    num.remove(num[0])
                    added = True
                elif num[0][2] < ans[0][2]:
                    ans.insert(0,num[0])
                    num.remove(num[0])
                    added = True
                else:
                    i = 0
                    while i < len(ans):
                        if num[0][2] < ans[i][2]:
                            ans.insert(i,num[0])
                            num.remove(num[0])
                            added = True
                            break
                        i += 1

                if not added:
                    ans.append(num[0])
                    num.remove(num[0])
        else:
            i = 0
            while len(num) > 0:
                added = False
                if len(num) == olen:
                    ans.append(num[0])
                    num.remove(num[0])
                    added = True
                elif num[0][2] > ans[0][2]:
                    ans.insert(0,num[0])
                    num.remove(num[0])
                    added = True
                else:
                    i = 0
                    while i < len(ans):
                        if num[0][2] > ans[i][2]:
                            ans.insert(i,num[0])
                            num.remove(num[0])
                            added = True
                            break
                        i += 1

                if not added:
                    ans.append(num[0])
                    num.remove(num[0])
        return ans

    def perspectify(self,shape,color='black',xRad=2,yRad=2):
        perspective = self.fl/(self.fl+shape[2])
        radiusX = xRad * perspective
        radiusY = yRad * perspective
        shapeMod = [shape[0]*perspective + root.winfo_screenwidth()/2,shape[1]*perspective+root.winfo_screenheight()/2]
        return shapeMod
    def project(self,points):
        for i in range(len(points)-1):
            p = points[i+1]
            if p[2] > self.camPos[2]-self.fl:
                l = [self.fl,self.camPos[2],p[2]]
                l = list(l)
                first = float(l[0])
                second = float(l[0]-l[1]+l[2])

                scale = first/second

                p[3] = p[0] * scale + self.camPos[0] * scale
                p[4] = p[1] * scale + self.camPos[1] * scale
        return points
    def drawLines(self,points,indexes):
        for i in range(len(indexes)-1):
            p = points[indexes[i]]
            nextP = points[indexes[i+1]]
            if p[2] > -self.fl:
                x = root.winfo_screenwidth()/2
                y = root.winfo_screenheight()/2
                canvas.create_line(p[3]+x,p[4]+y,nextP[3]+x,nextP[4]+y)
    def drawFace(self,points,indexes):
        avg = 0
        for i in indexes:
            avg += points[i][2]
        avg /= len(indexes)
        if avg > -self.fl:
            face = []
            for i in indexes:
                if points[i][2] > -self.fl:
                    face.append(points[i][3] + root.winfo_screenwidth()/2)
                    face.append(points[i][4] + root.winfo_screenheight()/2)
            canvas.create_polygon(face,fill='red',outline = 'black')
    def translate(self,points,x=0,y=0,z=0):
        for i in range(len(points)):
            points[i][0] += x
            points[i][1] += y
            points[i][2] += z
        return points
    def camTranslate(self,x=0,y=0,z=0):
            self.camPos[0] += x
            self.camPos[1] += y
            self.camPos[2] += z
    def rotateX(self,points,angle):
        cos = math.cos(angle)
        sin = math.sin(angle)
        radiusX = points[0][1]
        radiusY = points[0][2]
        for i in points:
            i[1] = ((i[1]-radiusX) * cos - (i[2]-radiusX) * sin)+radiusX
            i[2] = ((i[2]-radiusY) * cos + (i[1]-radiusY) * sin)+radiusY
    def rotateY(self,points,angle):
        cos = math.cos(angle)
        sin = math.sin(angle)
        radiusX = points[0][0]
        radiusY = points[0][2]
        for i in points:
            i[2] = ((i[2]-radiusX) * cos - (i[0]-radiusX) * sin)+radiusX
            i[0] = ((i[0]-radiusY) * cos + (i[2]-radiusY) * sin)+radiusY
    def rotateZ(self,points,angle):
        cos = math.cos(angle)
        sin = math.sin(angle)
        radiusX = points[0][1]
        radiusY = points[0][0]
        for i in points:
            i[1] = ((i[1]-radiusY) * cos - (i[0]-radiusY) * sin)+radiusY
            i[0] = ((i[0]-radiusX) * cos + (i[1]-radiusX) * sin)+radiusX
    def rotateAroundX(self,points,angle):
        cos = math.cos(angle)
        sin = math.sin(angle)
        w = root.winfo_screenwidth()/2
        h = root.winfo_screenheight()/2
        for i in points:
            i[1] = ((i[1]+h) * cos - (i[2]+h) * sin)-h
            i[2] = ((i[2]+self.fl) * cos + (i[1]+self.fl) * sin)-self.fl
    def rotateAroundY(self,points,angle):
        cos = math.cos(angle)
        sin = math.sin(angle)
        w = root.winfo_screenwidth()/2
        h = root.winfo_screenheight()/2
        for i in points:
            i[0] = ((i[0]+w) * cos - (i[2]+w) * sin)-w
            i[2] = ((i[2]+self.fl) * cos + (i[0]+self.fl) * sin)-self.fl
    def rotateAroundZ(self,points,angle):
        cos = math.cos(angle)
        sin = math.sin(angle)
        w = root.winfo_screenwidth()/2
        h = root.winfo_screenheight()/2
        for i in points:
            i[1] = ((i[1]+h) * cos - (i[0]+h) * sin)-h
            i[0] = ((i[0]+w) * cos + (i[1]+w) * sin)-w
    def createCube(self,x,y,z,radius):
        points = [[x,y,z]]
        points.append([x+radius,y+radius,z+radius,0,0])#back square
        points.append([x-radius,y+radius,z+radius,0,0])
        points.append([x-radius,y-radius,z+radius,0,0])
        points.append([x+radius,y-radius,z+radius,0,0])

        points.append([x+radius,y+radius,z-radius,0,0])#front square
        points.append([x-radius,y+radius,z-radius,0,0])
        points.append([x-radius,y-radius,z-radius,0,0])
        points.append([x+radius,y-radius,z-radius,0,0])

        return points
    def keyPressed(self,event):
        self.keysPressed.append(event.keysym)
    def KeyReleased(self,event):
        i = 0
        while i < self.keysPressed.count(event.keysym):
            self.keysPressed.remove(event.keysym)
            i=0
    def mousePress(self,event):
        self.mousePressed = True
    def mouseRelease(self,event):
        self.mousePressed = False

_3d = _3D(500)

points = _3d.createCube(0,0,0,100)

rotationSpeed = 1
baseAngle = 0

points = _3d.project(points)
last = points[:]

lastMouseY = _3d.mouseY
lastMouseX = _3d.mouseX


v = 0
while v < 1:

    mouseChangeY = root.winfo_screenwidth()/2 - _3d.mouseY
    mouseChangeX = root.winfo_screenwidth()/2 - _3d.mouseX
    #_3d.rotateAroundX(points,mouseChangeY/1000000)
    #_3d.rotateAroundY(points,mouseChangeX/1000000)

    if 'w' in _3d.keysPressed:
        _3d.camTranslate(z=10)
    if 's' in _3d.keysPressed:
        _3d.camTranslate(z=-10)
    if 'a' in _3d.keysPressed:
        _3d.camTranslate(x=-10)
    if 'd' in _3d.keysPressed:
        _3d.camTranslate(x=10)
    if '??' in _3d.keysPressed:
        _3d.camTranslate(y=-10)
    if 'space' in _3d.keysPressed:
        _3d.camTranslate(y=10)
    if _3d.mousePressed:
        _3d.createCube(_3d.camPos[0],_3d.camPos[1],_3d.camPos[2]+100,100)


    canvas.delete(ALL)

    for i in _3d.Objects:
        points = _3d.project(points)

        _3d.drawFace(points,[5,6,7,8])
        _3d.drawFace(points,[2,3,7,6])
        _3d.drawFace(points,[1,4,8,5])
        _3d.drawFace(points,[3,4,8,7])
        _3d.drawFace(points,[2,1,5,6])

    lastMouseX = _3d.mouseX
    lastMouseY = _3d.mouseY

    root.update()
