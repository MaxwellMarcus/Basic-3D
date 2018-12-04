try:
    from Tkinter import *
except:
    from tkinter import *
import random
import math

root = Tk()
canvas = Canvas(root,width = root.winfo_screenwidth(),height = root.winfo_screenheight())
canvas.pack()

class _3D:
    def __init__(self,fl):
        self.fl = fl
        self.radius = 1000
        self.centerZ = 0
        self.mouseX = 0
        self.mouseY = 0

        self.keysPressed = []

        root.bind('<Motion>',self.mouseSet)
        root.bind('<KeyPress>',self.keyPressed)
        root.bind('<KeyRelease>',self.KeyReleased)

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
        for i in range(len(points)):
            p = points[i]
            scale = self.fl/(self.fl + p[2] + self.centerZ)
            p[3] = p[0] * scale
            p[4] = p[1] * scale
        return points
    def drawLines(self,points,indexes):
        for i in range(len(indexes)-1):
            p = points[indexes[i]]
            nextP = points[indexes[i+1]]
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
                face.append(points[i][3] + root.winfo_screenwidth()/2)
                face.append(points[i][4] + root.winfo_screenheight()/2)
            canvas.create_polygon(face,fill = 'red')
    def translate(self,points,x=0,y=0,z=0):
        for i in range(len(points)):
            points[i][0] += x
            points[i][1] += y
            points[i][2] += z
        return points
    def rotateX(self,points,angle):
        cos = math.cos(angle)
        sin = math.sin(angle)
        for i in points:
            i[1] = ((i[1]+self.fl) * cos - (i[2]+self.fl) * sin)-self.fl
            i[2] = ((i[2]+self.fl) * cos + (i[1]+self.fl) * sin)-self.fl
    def rotateY(self,points,angle):
        cos = math.cos(angle)
        sin = math.sin(angle)
        for i in points:
            i[0] = ((i[0]+self.fl) * cos - (i[2]+self.fl) * sin)-self.fl
            i[2] = ((i[2]+self.fl) * cos + (i[0]+self.fl) * sin)-self.fl
    def rotateZ(self,points,angle):
        cos = math.cos(angle)
        sin = math.sin(angle)
        for i in points:
            i[1] = ((i[1]+self.fl) * cos - (i[0]+self.fl) * sin)-self.fl
            i[0] = ((i[0]+self.fl) * cos + (i[1]+self.fl) * sin)-self.fl
    def keyPressed(self,event):
        self.keysPressed.append(event.keysym)
    def KeyReleased(self,event):
        i = 0
        while i < self.keysPressed.count(event.keysym):
            self.keysPressed.remove(event.keysym)
            i=0

_3d = _3D(500)


radius = 100

points = []
points.append([radius*2,radius*2,radius*2,0,0])
points.append([0,radius*2,radius*2,0,0])
points.append([0,0,radius*2,0,0])
points.append([radius*2,0,radius*2,0,0])
points.append([radius*2,radius*2,0,0,0])
points.append([0,radius*2,0,0,0])
points.append([0,0,0,0,0])
points.append([radius*2,0,0,0,0])

rotationSpeed = 1
baseAngle = 0

points = _3d.project(points)
last = points[:]

v = 0
while v < 1:
    if 'a' in _3d.keysPressed:
        _3d.translate(points,x=-2)
    if 'd' in _3d.keysPressed:
        _3d.translate(points,x=2)
    if 'w' in _3d.keysPressed:
        if 'space' in _3d.keysPressed:_3d.translate(points,z=2)
        else:_3d.translate(points,y=-2)
    if 's' in _3d.keysPressed:
        if 'space' in _3d.keysPressed:_3d.translate(points,z=-2)
        else:_3d.translate(points,y=2)
    if 'Up' in _3d.keysPressed:
        _3d.rotateX(points,0.0005)
    if 'Down' in _3d.keysPressed:
        _3d.rotateX(points,-0.0005)
    if 'Left' in _3d.keysPressed:
        _3d.rotateY(points,-.0005)
    if 'Right' in _3d.keysPressed:
        _3d.rotateY(points,.0005)
    if 'q' in _3d.keysPressed:
        _3d.rotateZ(points,-.0005)
    if 'e' in _3d.keysPressed:
        _3d.rotateZ(points,.0005)

    canvas.delete(ALL)

    points = _3d.project(points)
    last = _3d.project(last)

    _3d.drawFace(points,[0,1,2,3])
    _3d.drawFace(points,[4,5,6,7])
    _3d.drawFace(points,[0,4,6,2])
    _3d.drawFace(points,[0,1,4,5])
    _3d.drawFace(points,[2,3,6,7])
    _3d.drawFace(points,[1,5,7,3])

    last = points[:]
    root.update()
