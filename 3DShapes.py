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
        self.camRot = [0,0,0]

        self.mousePressed = False
        self.mouse2Pressed = False
        self.keysPressed = []

        self.objects = []

        root.bind('<Motion>',self.mouseSet)
        root.bind('<KeyPress>',self.keyPressed)
        root.bind('<KeyRelease>',self.KeyReleased)
        root.bind('<Button-1>',self.mousePress)
        root.bind('<ButtonRelease-1>',self.mouseRelease)
        root.bind('<Button-2>',self.mouse2Press)
        root.bind('<ButtonRelease-2>',self.mouse2Release)

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
            cosX = math.cos(self.camRot[0])
            sinX = math.sin(self.camRot[0])
            cosY = math.cos(self.camRot[1])
            sinY = math.sin(self.camRot[1])
            cosZ = math.cos(self.camRot[2])
            sinZ = math.sin(self.camRot[2])

            radiusX = self.camPos[0]
            radiusY = self.camPos[1]
            radiusZ = -self.fl+self.camPos[2]

            lz=[abs(radiusX),abs(radiusY)]
            radiusz = max(lz)
            if radiusz == abs(radiusX):
                radiusz = radiusX
            else:
                radiusz = radiusY
            lx=[abs(radiusZ),abs(radiusY)]
            radiusx = max(lx)
            if radiusx == abs(radiusZ):
                radiusx = radiusZ
            else:
                radiusx = radiusY
            ly=[abs(radiusX),abs(radiusZ)]
            radiusy = max(lx)
            if radiusy == abs(radiusX):
                radiusy = radiusX
            else:
                radiusy = radiusZ

            newX = ((p[0]-radiusy) * cosY + (p[2]-radiusy) * sinY)+radiusy
            newY = ((p[1]-radiusx) * cosX - (p[2]-radiusx) * sinX)+radiusx
            newZ = ((p[2]-radiusx) * cosX + (p[1]-radiusx) * sinX)+radiusx

            newX = ((newX-radiusz) * cosZ + (newY-radiusz) * sinZ)+radiusz
            newY = ((newY-radiusz) * cosZ - (newX-radiusz) * sinZ)+radiusz
            newZ = ((newZ-radiusy) * cosY - (newX-radiusy) * sinY)+radiusy

            if p[2] > self.camPos[2]-self.fl:
                l = [self.fl,self.camPos[2],newZ]
                l = list(l)
                first = float(l[0])
                second = float(l[0]-l[1]+l[2])

                scale = first/second

                p[3] = newX * scale - self.camPos[0] * scale
                p[4] = newY * scale - self.camPos[1] * scale

        return points
    def drawLines(self,points,indexes):
        for i in range(len(indexes)-1):
            p = points[indexes[i]]
            nextP = points[indexes[i+1]]
            if p[2] > -self.fl and p[0] > 0 and p[1] > 0 and p[0] < root.winfo_screenwidth() and p[1] < root.winfo_screenheight():
                x = root.winfo_screenwidth()/2
                y = root.winfo_screenheight()/2
                canvas.create_line(p[3]+x,p[4]+y,nextP[3]+x,nextP[4]+y)
    def drawFace(self,points,indexes,color='red'):
        avg = 0
        for i in indexes:
            avg += points[i][2]
        avg /= len(indexes)

        if avg > -self.fl:
            face = []
            for i in indexes:
                p = points[i]
                cosX = math.cos(self.camRot[0])
                sinX = math.sin(self.camRot[0])
                cosY = math.cos(self.camRot[1])
                sinY = math.sin(self.camRot[1])
                cosZ = math.cos(self.camRot[2])
                sinZ = math.sin(self.camRot[2])

                radiusX = self.camPos[0]
                radiusY = self.camPos[1]
                radiusZ = -self.fl+self.camPos[2]

                lz=[abs(radiusX),abs(radiusY)]
                radiusz = max(lz)
                if radiusz == abs(radiusX):
                    radiusz = radiusX
                else:
                    radiusz = radiusY
                lx=[abs(radiusZ),abs(radiusY)]
                radiusx = max(lx)
                if radiusx == abs(radiusZ):
                    radiusx = radiusZ
                else:
                    radiusx = radiusY
                ly=[abs(radiusX),abs(radiusZ)]
                radiusy = max(lx)
                if radiusy == abs(radiusX):
                    radiusy = radiusX
                else:
                    radiusy = radiusZ

                newX = ((p[0]-radiusy) * cosY + (p[2]-radiusy) * sinY)+radiusy
                newY = ((p[1]-radiusx) * cosX - (p[2]-radiusx) * sinX)+radiusx
                newZ = ((p[2]-radiusx) * cosX + (p[1]-radiusx) * sinX)+radiusx

                newX = ((newX-radiusz) * cosZ + (newY-radiusz) * sinZ)+radiusz
                newY = ((newY-radiusz) * cosZ - (newX-radiusz) * sinZ)+radiusz
                newZ = ((newZ-radiusy) * cosY - (newX-radiusy) * sinY)+radiusy
                if newZ > -(self.fl-self.camPos[2]):
                    face.append(points[i][3] + root.winfo_screenwidth()/2)
                    face.append(points[i][4] + root.winfo_screenheight()/2)
            if len(face) > 0:
                canvas.create_polygon(face,fill=color,outline = 'black')
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
    def camRotate(self,x=0,y=0,z=0):
        self.camRot[0] += x
        self.camRot[1] += y
        self.camRot[2] += z
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
        radiusY = self.camPos[1]
        radiusZ = -self.fl+self.camPos[2]

        lx=[abs(radiusZ),abs(radiusY)]
        radiusx = max(lx)
        if radiusx == abs(radiusZ):
            radiusx = radiusZ
        else:
            radiusx = radiusY

        for i in points:
            i[1] = ((i[1]-radiusx) * cos - (i[2]-radiusx) * sin)+radiusx
            i[2] = ((i[2]-radiusx) * cos + (i[1]-radiusx) * sin)+radiusx
        return points
    def rotateAroundY(self,points,angle):
        cos = math.cos(angle)
        sin = math.sin(angle)
        radiusY = self.camPos[0]
        radiusZ = -self.fl+self.camPos[2]

        ly=[abs(radiusZ),abs(radiusY)]
        radiusx = max(ly)
        if radiusx == abs(radiusZ):
            radiusx = radiusZ
        else:
            radiusx = radiusY
        for i in points:
            i[0] = ((i[0]-radiusx) * cos - (i[2]-radiusx) * sin)+radiusx
            i[2] = ((i[2]-radiusx) * cos + (i[0]-radiusx) * sin)+radiusx
        return points
    def rotateAroundZ(self,points,angle):
        cos = math.cos(angle)
        sin = math.sin(angle)
        radiusX = self.camPos[0]
        radiusZ = self.camPos[1]

        ly=[abs(radiusZ),abs(radiusX)]
        radiusy = max(ly)
        if radiusy == abs(radiusZ):
            radiusy = radiusZ
        else:
            radiusy = radiusX
        for i in points:
            i[0] = ((i[0]-radiusy) * cos - (i[1]-radiusy) * sin)+radiusy
            i[1] = ((i[1]-radiusy) * cos + (i[0]-radiusy) * sin)+radiusy
        return points
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

        self.objects.append(points)
    def returnCube(self,x,y,z,radius):
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
    def mouse2Press(self,event):
        self.mouse2Pressed = True
    def mouse2Release(self,event):
        self.mouse2Pressed = False

_3d = _3D(300)

#_3d.createCube(0,0,0,100)

rotationSpeed = 1
baseAngle = 0

lastMouseY = _3d.mouseY
lastMouseX = _3d.mouseX


v = 0
while v < 1:

    if 'Up' in _3d.keysPressed:
        _3d.camRotate(x=-.01)
    if 'Down' in _3d.keysPressed:
        _3d.camRotate(x=.01)
    if 'Left' in _3d.keysPressed:
        _3d.camRotate(y=.01)
    if 'Right' in _3d.keysPressed:
        _3d.camRotate(y=-.01)
    if 'w' in _3d.keysPressed:
        _3d.camTranslate(z=10)
    if 's' in _3d.keysPressed:
        _3d.camTranslate(z=-10)
    if 'a' in _3d.keysPressed:
        _3d.camTranslate(x=-10)
    if 'd' in _3d.keysPressed:
        _3d.camTranslate(x=10)
    if 'r' in _3d.keysPressed:
        _3d.camRot = [0,0,0]
        _3d.camPos = [0,0,0]
    if '??' in _3d.keysPressed:
        _3d.camTranslate(y=10)
    if 'space' in _3d.keysPressed:
        _3d.camTranslate(y=-10)
    if _3d.mousePressed:
        a = False
        cube = _3d.returnCube(_3d.camPos[0],_3d.camPos[1],_3d.camPos[2]+100,100)
        x,y,z = _3d.camPos[0],_3d.camPos[1],_3d.camPos[2]+100
        x = (x//200)*200
        y = (y//200)*200
        z = (z//200)*200
        for i in _3d.objects:
            for k in range(len(i)-1):
                f = i[k]
                if (f[0] - 100 < cube[k][0] + 100 and f[0] + 100 > cube[k][0] - 100 and f[1] - 100 < cube[k][1] + 100 and f[1] + 100 > cube[k][1] - 100 and f[2] - 100 < cube[k][2] + 100 and f[2] + 100 > cube[k][2] - 100):
                    a = True
        if a:
            z -= 200
        if clickable:
            cube = _3d.returnCube(x,y,z,100)
            #cube = _3d.rotateAroundX(cube,-_3d.camRot[0])
            #cube = _3d.rotateAroundY(cube,-_3d.camRot[1])
            #cube = _3d.rotateAroundZ(cube,-_3d.camRot[2])
            _3d.objects.append(cube)
        clickable = False

    if _3d.mouse2Pressed:
        cube = _3d.returnCube(_3d.camPos[0],_3d.camPos[1],_3d.camPos[2]+100,100)
        x,y,z = _3d.camPos[0],_3d.camPos[1],_3d.camPos[2]+100
        x = (x//200)*200
        y = (y//200)*200
        z = (z//200)*200
        cube = _3d.returnCube(x,y,z,100)
        _3d.project(cube)
        if cube in _3d.objects:
            _3d.objects.remove(cube)

    if not _3d.mousePressed:
        clickable = True


    canvas.delete(ALL)
    for i in _3d.objects:
        i = _3d.project(i)

        _3d.drawFace(i,[5,6,7,8])
        _3d.drawFace(i,[2,3,7,6])
        _3d.drawFace(i,[1,4,8,5])
        _3d.drawFace(i,[3,4,8,7])
        _3d.drawFace(i,[2,1,5,6])

    cube = _3d.returnCube((_3d.camPos[0]/200)*200,(_3d.camPos[1]/200)*200,(_3d.camPos[2]+100/200)*200,100)
    cube = _3d.project(cube)
    _3d.drawFace(cube,[5,6,7,8],color = '')
    _3d.drawFace(cube,[2,3,7,6],color = '')
    _3d.drawFace(cube,[1,4,8,5],color = '')
    _3d.drawFace(cube,[3,4,8,7],color = '')
    _3d.drawFace(cube,[2,1,5,6],color = '')

    lastMouseX = _3d.mouseX
    lastMouseY = _3d.mouseY

    root.update()
