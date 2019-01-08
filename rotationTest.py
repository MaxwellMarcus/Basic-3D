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

class _3D:# the class that handles everything
    def __init__(self,fl):#setting a few variables and binding a few keys on initiation
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

        self.facing = None

        self.objects = []

        self.start = True

        root.bind('<Motion>',self.mouseSet)
        root.bind('<KeyPress>',self.keyPressed)
        root.bind('<KeyRelease>',self.KeyReleased)
        root.bind('<Button-1>',self.mousePress)
        root.bind('<ButtonRelease-1>',self.mouseRelease)
        root.bind('<Button-2>',self.mouse2Press)
        root.bind('<ButtonRelease-2>',self.mouse2Release)
        root.bind('<Button-3>',self.mouse2Press)
        root.bind('<ButtonRelease-3>',self.mouse2Release)

    def mouseSet(self,event):#sets the class variables to the position of the mouse when the mouse is moved
        self.mouseX = event.x
        self.mouseY = event.y

    def projectSingle(self,point):# changes X and Y based on Z position used for a single point
        p = point
        cosX = math.cos(self.camRot[0])
        sinX = math.sin(self.camRot[0])
        cosY = math.cos(self.camRot[1])
        sinY = math.sin(self.camRot[1])
        cosZ = math.cos(self.camRot[2])
        sinZ = math.sin(self.camRot[2])

        centerX = self.camPos[0]
        centerY = self.camPos[1]
        centerZ = -self.fl+self.camPos[2]

        lz=[abs(centerX),abs(centerY)]
        radiusz = max(lz)
        if radiusz == abs(centerX):
            radiusz = centerX
        else:
            radiusz = centerY
        lx=[abs(centerZ),abs(centerY)]
        radiusx = max(lx)
        if radiusx == abs(centerZ):
            radiusx = centerZ
        else:
            radiusx = centerY
        ly=[abs(centerX),abs(centerZ)]
        radiusy = max(lx)
        if radiusy == abs(centerX):
            radiusy = centerX
        else:
            radiusy = centerZ

        #newX = ((p[0]-radiusy) * cosY + (p[2]-radiusy) * sinY)+radiusy
        #newY = ((p[1]-radiusx) * cosX - (p[2]-radiusx) * sinX)+radiusx
        #newZ = ((p[2]-radiusx) * cosX + (p[1]-radiusx) * sinX)+radiusx
        newZ = p[2]
        newX = ((p[0]-centerX) * cosZ + (p[1]-centerY) * sinZ)+centerX
        newY = ((p[1]-centerY) * cosZ - (p[0]-centerX) * sinZ)+centerY
        #newZ  = ((newZ-radiusy) * cosY - (newX-radiusy) * sinY)+radiusy

        if p[2] > self.camPos[2]-self.fl:
            l = [self.fl,self.camPos[2],newZ]
            l = list(l)
            first = float(l[0])
            second = float(l[0]-l[1]+l[2])

            scale = first/second

            newX = newX * scale - self.camPos[0] * scale
            newY = newY * scale - self.camPos[1] * scale

        return newX + root.winfo_screenwidth()/2, newY + root.winfo_screenheight()/2
    def project(self,points):# changes X and Y based on Z position used for a list of positions, I use it for cubes
        for i in range(len(points)-1):
            p = points[i+1]
            cosX = math.cos(self.camRot[0])
            sinX = math.sin(self.camRot[0])
            cosY = math.cos(self.camRot[1])
            sinY = math.sin(self.camRot[1])
            cosZ = math.cos(self.camRot[2])
            sinZ = math.sin(self.camRot[2])

            centerX = self.camPos[0]
            centerY = self.camPos[1]
            centerZ = -self.fl+self.camPos[2]
            x = p[0]#Y rotation isn't working properly
            y = ((p[1]-centerY) * cosX - (p[2]-centerZ) * sinX)+centerY
            z = ((p[2]-centerZ) * cosX + (p[1]-centerY) * sinX)+centerZ
            newX = ((x-centerX) * cosZ + (y-centerY) * sinZ)+centerX# I think it has to do with using x,y, and z variables instead of p[0],p[1], and p[2]
            newZ = ((y-centerY) * cosZ - (x-centerX) * sinZ)+centerY# I am pretty sure it has to do with having half of the equation using the actual values and the other half using previously found values
            newX = ((newX-centerX) * cosY + (newZ-centerZ) * sinY)+centerX
            newY = ((z-centerZ) * cosY - (x-centerX) * sinY)+centerZ

            if p[2] > self.camPos[2]-self.fl:
                l = [self.fl,self.camPos[2],newZ]
                l = list(l)
                first = float(l[0])
                second = float(l[0]-l[1]+l[2])

                scale = first/second

                p[3] = newX * scale - self.camPos[0] * scale
                p[4] = newY * scale - self.camPos[1] * scale
        f = 0
        while f < 2*math.pi:
            x = ((p[0]-centerX) * math.cos(f) + (p[2]-centerZ) * math.sin(f))+centerX
            y = ((p[1]-centerY) * cosX - (p[2]-centerZ) * sinX)+centerY
            z = ((p[2]-centerZ) * cosX + (p[1]-centerY) * sinX)+centerZ
            newX = ((x-centerX) * cosZ + (y-centerY) * sinZ)+centerX
            newZ = p[2]
            newY = ((z-centerZ) * math.cos(f) - (x-centerX) * math.sin(f))+centerZ
            if p[2] > self.camPos[2]-self.fl:
                l = [self.fl,self.camPos[2],newZ]
                l = list(l)
                first = float(l[0])
                second = float(l[0]-l[1]+l[2])

                scale = first/second

                newX = newX * scale - self.camPos[0] * scale
                newY = newY * scale - self.camPos[1] * scale

                self.draw_square(newX+root.winfo_screenwidth()/2,newY+root.winfo_screenheight()/2,2)

            f+=.1
        return points

    def drawFace(self,points,indexes,color='red',lines=''):# draws a face using all indexes given
        face = []
        for i in indexes:
            p = points[i]
            cosX = math.cos(self.camRot[0])
            sinX = math.sin(self.camRot[0])
            cosY = math.cos(self.camRot[1])
            sinY = math.sin(self.camRot[1])
            cosZ = math.cos(self.camRot[2])
            sinZ = math.sin(self.camRot[2])

            centerX = self.camPos[0]
            centerY = self.camPos[1]
            centerZ = -self.fl+self.camPos[2]
            x = ((p[0]-centerX) * cosY + (p[2]-centerZ) * sinY)+centerX
            y = ((p[1]-centerY) * cosX - (p[2]-centerZ) * sinX)+centerY
            z = ((p[2]-centerZ) * cosX + (p[1]-centerY) * sinX)+centerZ
            newX = ((x-centerX) * cosZ + (y-centerY) * sinZ)+centerX
            newZ = ((y-centerY) * cosZ - (x-centerX) * sinZ)+centerY
            newY = ((z-centerZ) * cosY - (x-centerX) * sinY)+centerZ

            if newZ > -(self.fl-self.camPos[2]):
                face.append(points[i][3] + root.winfo_screenwidth()/2)
                face.append(points[i][4] + root.winfo_screenheight()/2)
            if len(face) > 0:
                canvas.create_polygon(face,fill=color,outline = lines)
    def translate(self,points,x=0,y=0,z=0):# moves the x, and/or y, and/or z on each of the points in a list
        for i in range(len(points)):
            points[i][0] += x
            points[i][1] += y
            points[i][2] += z
        return points
    def camTranslate(self,x=0,y=0,z=0):# same as translate, but instead of points it transleates the camera. This is taken into account during the project and project single functions
        self.camPos[0] += x
        self.camPos[1] += y
        self.camPos[2] += z
    def camRotate(self,x=0,y=0,z=0):# rotates the camera. This is taken into acount during the project and projectSingle functions. it is not completly workiong correctly. I am currently trying to fix it
        self.camRot[0] += x
        self.camRot[1] += y
        self.camRot[2] += z

    #these rotates the points that are provided
    def rotateX(self,points,angle):#this one
        cos = math.cos(angle)
        sin = math.sin(angle)
        radiusX = points[0][1]
        radiusY = points[0][2]
        for i in points:
            i[1] = ((i[1]-radiusX) * cos - (i[2]-radiusX) * sin)+radiusX
            i[2] = ((i[2]-radiusY) * cos + (i[1]-radiusY) * sin)+radiusY
    def rotateY(self,points,angle):#this one
        cos = math.cos(angle)
        sin = math.sin(angle)
        radiusX = points[0][0]
        radiusY = points[0][2]
        for i in points:
            i[2] = ((i[2]-radiusX) * cos - (i[0]-radiusX) * sin)+radiusX
            i[0] = ((i[0]-radiusY) * cos + (i[2]-radiusY) * sin)+radiusY
    def rotateZ(self,points,angle):# and this one
        cos = math.cos(angle)
        sin = math.sin(angle)
        radiusX = points[0][1]
        radiusY = points[0][0]
        for i in points:
            i[1] = ((i[1]-radiusY) * cos - (i[0]-radiusY) * sin)+radiusY
            i[0] = ((i[0]-radiusX) * cos + (i[1]-radiusX) * sin)+radiusX
    # these ones are the same as the last ones, but they rotate them around the camera or the 0,0 point
    def rotateAroundX(self,points,angle):#this one
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
    def rotateAroundY(self,points,angle):#this one
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
    def rotateAroundZ(self,points,angle):#and this one
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
    def createCube(self,x,y,z,radius):#this function adds the a list of the points of a cube to a list
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
    def returnCube(self,x,y,z,radius):# same as createCube, but instead of adding it to a list it returns the points
        points = [[x,y,z]]
        points.append([x+radius,y+radius,z+radius,0,0])#back square
        points.append([x-radius,y+radius,z+radius,0,0])
        points.append([x-radius,y-radius,z+radius,0,0])
        points.append([x+radius,y-radius,z+radius,0,0])

        points.append([x+radius,y+radius,z-radius,0,0])#front square
        points.append([x-radius,y+radius,z-radius,0,0])
        points.append([x-radius,y-radius,z-radius,0,0])
        points.append([x+radius,y-radius,z-radius,0,0])

        points = self.project(points)
        return points
    def draw_square(self,x,y,radius,color='black'):#not used
        canvas.create_rectangle(x-radius,y-radius,x+radius,y+radius,fill=color)
    def keyPressed(self,event):#adds a keysym to the list of keys pressed
        self.keysPressed.append(event.keysym)
    def KeyReleased(self,event):#takes a keysym of the list of keys pressed
        i = 0
        while i < self.keysPressed.count(event.keysym):
            self.keysPressed.remove(event.keysym)
            i=0
    def mousePress(self,event):#changes the variable mousePressed to true if left mouse button is pressed
        self.mousePressed = True
    def mouseRelease(self,event):#changes the variable mousePressed to false if left mouse button is released
        self.mousePressed = False
    def mouse2Press(self,event):#changes the variable mouse2Pressed to true if right mouse button is pressed or the scroll wheel is pressed, I might give them two seperate variable in the future
        self.mouse2Pressed = True
    def mouse2Release(self,event):#changes the variable mouse2Pressed to false if right mouse button isn't released or the scroll wheel is relesed
        self.mouse2Pressed = False

# initiating the class that handles everything
_3d = _3D(500)
_3d.camRot = [0,math.pi*.5,0]
#making the first cube
_3d.createCube(0,0,0,50)

#setting a few variables
rotationSpeed = 1
baseAngle = 0

lastMouseY = _3d.mouseY
lastMouseX = _3d.mouseX

#the game loop
while _3d.start:
    #handling all things with input
    #   handling exiting with no errors
    if 'Escape' in _3d.keysPressed:
        _3d.start = False
    #   handling rotation
    #       currently Z rotation
    if 'Up' in _3d.keysPressed:
        _3d.camRotate(x=-.01)
    if 'Down' in _3d.keysPressed:
        _3d.camRotate(x=.01)
    #       currently Y rotation, but it is not used
    if 'Left' in _3d.keysPressed:
        _3d.camRotate(y=.01)
    if 'Right' in _3d.keysPressed:
        _3d.camRotate(y=-.01)
    #   handling movement
    #       Z movement
    if 'w' in _3d.keysPressed:
        _3d.camTranslate(z=10)
    if 's' in _3d.keysPressed:
        _3d.camTranslate(z=-10)
    #       X movement
    if 'a' in _3d.keysPressed:
        _3d.camTranslate(x=-10)
    if 'd' in _3d.keysPressed:
        _3d.camTranslate(x=10)
    #       Y movement
    if '??' in _3d.keysPressed or 'Shift_L' in _3d.keysPressed:
        _3d.camTranslate(y=10)
    if 'space' in _3d.keysPressed:
        _3d.camTranslate(y=-10)
    #   resets the position and rotation
    if 'r' in _3d.keysPressed:
        _3d.camRot = [0,0,0]
        _3d.camPos = [0,0,0]

    #drawing the cubes
    canvas.delete(ALL)
    for i in _3d.objects:
        i = _3d.project(i)
        if not i[1][3] > root.winfo_screenwidth() or not i[1][3] < 0 or not i[0][4] > root.winfo_screenheight() or not i[1][4] < 0:
            _3d.drawFace(i,[5,6,7,8],color='green')
            _3d.drawFace(i,[2,3,7,6],color='blue')
            _3d.drawFace(i,[1,4,8,5],color='red')
            _3d.drawFace(i,[3,4,8,7],color='orange')
            _3d.drawFace(i,[2,1,5,6],color='white',lines='black')

    lastMouseX = _3d.mouseX
    lastMouseY = _3d.mouseY

    canvas.create_oval(root.winfo_screenwidth()/2-5,root.winfo_screenheight()/2-5,root.winfo_screenwidth()/2+5,root.winfo_screenheight()/2+5,fill='black')
    root.update()
