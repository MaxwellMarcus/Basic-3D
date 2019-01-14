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

    def zsort(self,list):#sorts something based on the Z values not currently used
        sorted = []
        for i in list:
            if len(sorted)==0:
                first = False
                sorted.append(i)
            elif i[0][2] > sorted[0][0][2]:
                sorted.insert(0,i)
            elif not i[0][2] < sorted[len(sorted)-1][0][2]:
                for k in sorted:
                    if i[0][2] > k[0][2]:
                        sorted.insert(sorted.index(k),i)
                        break
            else:
                sorted.append(i)
        return sorted
    def sort(self,list):
        sorted = []
        for i in list:
            if len(sorted)==0:
                first = False
                sorted.append(i)
            elif i > sorted[0]:
                sorted.insert(0,i)
            elif not i < sorted[len(sorted)-1]:
                for k in sorted:
                    if i > k:
                        sorted.insert(sorted.index(k),i)
                        break
            else:
                sorted.append(i)
        return sorted
    def perspectify(self,shape,color='black',xRad=2,yRad=2):#changes X and Y based on Z position used for postcards in space not currently used
        perspective = self.fl/(self.fl+shape[2])
        radiusX = xRad * perspective
        radiusY = yRad * perspective
        shapeMod = [shape[0]*perspective + root.winfo_screenwidth()/2,shape[1]*perspective+root.winfo_screenheight()/2]
        return shapeMod

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
        centerZ = self.camPos[2]

        x = ((p[0]-centerX) * cosY + (p[2]-centerZ) * sinY)+centerX
        y = ((p[1]-centerY) * cosX - (p[2]-centerZ) * sinX)+centerY
        z = ((p[2]-centerZ) * cosX + (p[1]-centerY) * sinX)+centerZ
        newX = ((x-centerX) * cosZ + (y-centerY) * sinZ)+centerX
        newY = ((y-centerY) * cosZ - (x-centerX) * sinZ)+centerY
        newZ = ((z-centerZ) * cosY - (x-centerX) * sinY)+centerZ

        if -p[2] == self.camPos[2]:
            l = [self.fl,self.camPos[2],newZ]
            l = list(l)
            first = float(l[0])
            second = float(l[1]+l[2])

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
            centerZ = -self.camPos[2]

            x = p[0]
            y = ((p[1]-centerY) * cosX - (p[2]-centerZ) * sinX)+centerY
            z = ((p[2]-centerZ) * cosX + (p[1]-centerY) * sinX)+centerZ
            newX = ((x-centerX) * cosZ + (y-centerY) * sinZ)+centerX
            newY = ((y-centerY) * cosZ - (x-centerX) * sinZ)+centerY
            newZ = ((z-centerZ) * cosY - (x-centerX) * sinY)+centerZ
            newX = ((newX-centerX) * cosY + (newZ-centerZ) * sinY)+centerX

            if not -p[2] == self.camPos[2]:
                l = [self.fl,self.camPos[2],newZ]
                l = list(l)
                first = float(l[0])
                second = float(l[1]+l[2])

                scale = first/second
                p[3] = newX * scale + self.camPos[0] * scale
                p[4] = newY * scale + self.camPos[1] * scale
            else:
                p[3] = False
                p[4] = False

        return points
    def drawLines(self,points,indexes):# draws a line from given indexes of a list of points not currently in use
        for i in range(len(indexes)-1):
            p = points[indexes[i]]
            nextP = points[indexes[i+1]]
            if p[2] > -self.fl and p[0] > 0 and p[1] > 0 and p[0] < root.winfo_screenwidth() and p[1] < root.winfo_screenheight():
                x = root.winfo_screenwidth()/2
                y = root.winfo_screenheight()/2
                canvas.create_line(p[3]+x,p[4]+y,nextP[3]+x,nextP[4]+y)

    def drawFace(self,points,indexes,color='red',lines='black'):# draws a face using all indexes given
        face = []
        for p in indexes:
            if p[3]:
                cosX = math.cos(self.camRot[0])
                sinX = math.sin(self.camRot[0])
                cosY = math.cos(self.camRot[1])
                sinY = math.sin(self.camRot[1])
                cosZ = math.cos(self.camRot[2])
                sinZ = math.sin(self.camRot[2])

                centerX = self.camPos[0]
                centerY = self.camPos[1]
                centerZ = self.camPos[2]

                x = p[0]
                y = ((p[1]-centerY) * cosX - (p[2]-centerZ) * sinX)+centerY
                z = ((p[2]-centerZ) * cosX + (p[1]-centerY) * sinX)+centerZ
                newX = ((x-centerX) * cosZ + (y-centerY) * sinZ)+centerX
                newY = ((y-centerY) * cosZ - (x-centerX) * sinZ)+centerY
                newZ = ((z-centerZ) * cosY - (x-centerX) * sinY)+centerZ
                newX = ((newX-centerX) * cosY + (newZ-centerZ) * sinY)+centerX
                if newZ > self.camPos[2]:
                    face.append(p[3] + root.winfo_screenwidth()/2)
                    face.append(p[4] + root.winfo_screenheight()/2)
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
        radiusZ = self.camPos[2]
        for i in points:
            i[1] = ((i[1]-radiusY) * cos - (i[2]-radiusZ) * sin)+radiusY
            i[2] = ((i[2]-radiusZ) * cos + (i[1]-radiusY) * sin)+radiusZ
        return points
    def rotateAroundY(self,points,angle):#this one
        cos = math.cos(angle)
        sin = math.sin(angle)
        radiusX = self.camPos[0]
        radiusZ = self.camPos[2]
        for i in points:
            i[0] = ((i[0]-radiusX) * cos - (i[2]-radiusZ) * sin)+radiusX
            i[2] = ((i[2]-radiusZ) * cos + (i[0]-radiusX) * sin)+radiusZ
        return points
    def rotateAroundZ(self,points,angle):#and this one
        cos = math.cos(angle)
        sin = math.sin(angle)
        radiusX = self.camPos[0]
        radiusY = self.camPos[1]
        for i in points:
            i[0] = ((i[0]-radiusX) * cos - (i[1]-radiusY) * sin)+radiusZ
            i[1] = ((i[1]-radiusY) * cos + (i[0]-radiusX) * sin)+radiusY
        return points
    def createCube(self,x,y,z,radius):#this function adds the a list of the points of a cube to a list
        points = [[x,y,z,0,0]]
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
    def ray(self,x1,y1,z1,x2=0,y2=0,z2=0,radius=1,range=100):# this function returns the first cube it hits. You provide the starting point and the increments it adds to the XYZ values.
        a = False
        b = None
        c = 0
        x = x1
        y = y1
        z = z1
        while not a and c < range:
            cube = self.returnCube(x,y,z,radius)
            for i in self.objects:
                if self.collision(cube,i) == True:
                    b = self.objects.index(i)
                    a = True
            x += x2*200
            y += y2*200
            z += z2*200
            c += 1
        return b
    def drawRay(self,x1,y1,z1,x2=0,y2=0,z2=0,radius=1,range=100,color='black'):#this function does the same as the ray function, but instead of returning the first cube it hits it draws a line there
        a = False
        c = 0
        x = x1
        y = y1
        z = z1
        while not a and c < range:
            cube = self.returnCube(x,y,z,radius)
            for i in self.objects:
                if self.collision(cube,i) == True:
                    a = True
            x += x2*200
            y += y2*200
            z += z2*200
            c += 1
        if a:
            l = [self.fl,self.camPos[2],z1]
            l = list(l)
            first = float(l[0])
            second = float(l[1]+l[2])

            scale = first/second

            p1x = x1 * scale - self.camPos[0] * scale
            p1y = y1 * scale - self.camPos[1] * scale

            l = [self.fl,self.camPos[2],z]
            l = list(l)
            first = float(l[0])
            second = float(l[1]+l[2])

            scale = first/second

            p2x = x * scale - self.camPos[1] * scale
            p2y = y * scale - self.camPos[1] * scale

            canvas.create_line(p1x,p1y,p2x,p2y,fill = color)
    def sameCubePos(self, cube1, cube2):# this detects if two cubes have the same position
        if cube1[0][0] == cube2[0][0] and cube1[0][1] == cube2[0][1] and cube1[0][2] == cube2[0][2]:
            return True
        else:
            return False
    def collision(self,cube1,cube2):#this detects if two cubes are touching each other
        r1 = abs(cube1[0][0]-cube1[1][0])
        r2 = abs(cube2[0][0]-cube2[1][0])
        x1,y1,z1 = cube1[0][0],cube1[0][1],cube1[0][2]
        x2,y2,z2 = cube2[0][0],cube2[0][1],cube2[0][2]

        if x1+r1 > x2-r2 and x1-r1 < x2+r2 and y1+r1 > y2-r2 and y1-r1 < y2+r2 and z1+r1 > z2-r2 and z1-r1 < z2+r2:
            return True
        else:
            return False
    def visible(self):
        things = []
        for p in self.objects:
            newCube=[]
            for i in p:
                newPos = self.applyCamRot(i[0],i[1],i[2])
                newPos.append(i[3])
                newPos.append(i[4])
                newCube.append(newPos)
            if newCube[0][2] > self.camPos[2]:
                things.append(newCube)
        return self.zsort(things)
    def visibleFace(self,c):
        face1 = [c[5],c[6],c[7],c[8]]
        face1avgZ = (face1[0][2]+face1[1][2]+face1[2][2]+face1[3][2])/4
        face1avgX = (face1[0][0]+face1[1][0]+face1[2][0]+face1[3][0])/4
        face1avgY = (face1[0][1]+face1[1][1]+face1[2][1]+face1[3][1])/4
        
        face1.append(face1avg)
        face2 = [c[2],c[3],c[7],c[6]]
        face2avg = (face2[0][2]+face2[1][2]+face2[2][2]+face2[3][2])/4
        face2.append(face2avg)
        face3 = [c[1],c[3],c[8],c[5]]
        face3avg = (face3[0][2]+face3[1][2]+face3[2][2]+face3[3][2])/4
        face3.append(face3avg)
        face4 = [c[3],c[4],c[8],c[7]]
        face4avg = (face4[0][2]+face4[1][2]+face4[2][2]+face4[3][2])/4
        face4.append(face4avg)
        face5 = [c[2],c[1],c[5],c[6]]
        face5avg = (face5[0][2]+face5[1][2]+face5[2][2]+face5[3][2])/4
        face5.append(face5avg)
        face6 = [c[1],c[2],c[3],c[4]]
        face6avg = (face6[0][2]+face6[1][2]+face6[2][2]+face6[3][2])/4
        face6.append(face6avg)

        list = [face1,face2,face3,face4,face5,face6]
        sorted = []
        for i in list:
            if len(sorted)==0:
                first = False
                sorted.append(i)
            elif i[4] > sorted[0][4]:
                sorted.insert(0,i)
            elif not i[4] < sorted[len(sorted)-1][4]:
                for k in sorted:
                    if i[4] > k[4]:
                        sorted.insert(sorted.index(k),i)
                        break
            else:
                sorted.append(i)
        for i in range(len(sorted)):
            sorted[i].remove(sorted[i][4])

        return sorted
    def applyCamRot(self,x,y,z):
        cosX = math.cos(self.camRot[0])
        sinX = math.sin(self.camRot[0])
        cosY = math.cos(self.camRot[1])
        sinY = math.sin(self.camRot[1])
        cosZ = math.cos(self.camRot[2])
        sinZ = math.sin(self.camRot[2])

        centerX = self.camPos[0]
        centerY = self.camPos[1]
        centerZ = -self.camPos[2]

        y = ((y-centerY) * cosX - (z-centerZ) * sinX)+centerY
        z = ((z-centerZ) * cosX + (y-centerY) * sinX)+centerZ
        newX = ((x-centerX) * cosZ + (y-centerY) * sinZ)+centerX
        newY = ((y-centerY) * cosZ - (x-centerX) * sinZ)+centerY
        newZ = ((z-centerZ) * cosY - (x-centerX) * sinY)+centerZ
        newX = ((newX-centerX) * cosY + (newZ-centerZ) * sinY)+centerX

        return [x,y,z]
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
_3d = _3D(350)

#making the first cubes
i = 0
while i < 10:
    l = random.randint(1,10)
    _3d.createCube(0,0,l*200,100)
    i += 1

#setting a few variables
rotationSpeed = 1
baseAngle = 0

lastMouseY = _3d.mouseY
lastMouseX = _3d.mouseX

clickable = True
clickable2 = True

#the game loop
while _3d.start:
    #handling all things with input
    #   handling exiting with no errors
    if 'Escape' in _3d.keysPressed:
        _3d.start = False
    #   handling rotation
    #       currently Z rotation
    if 'Up' in _3d.keysPressed:
        _3d.camRotate(z=-.01)
    if 'Down' in _3d.keysPressed:
        _3d.camRotate(z=.01)
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
    #   handling creating cubes currently not used
    if _3d.mousePressed and type(_3d.ray(_3d.camPos[0],_3d.camPos[1],_3d.camPos[2],z2=1,range=10)) == int and False:
        closest = _3d.ray(_3d.camPos[0],_3d.camPos[1],_3d.camPos[2],z2=1,range=10)
        x,y,z = _3d.objects[closest][0][0], _3d.objects[closest][0][1], _3d.objects[closest][0][2]-200
        cube = _3d.returnCube(x,y,z,100)
        cube = _3d.rotateAroundX(cube,-_3d.camRot[0])
        cube = _3d.rotateAroundY(cube,-_3d.camRot[1])
        cube = _3d.rotateAroundX(cube,-_3d.camRot[2])
        a = False
        for i in _3d.objects:
            if _3d.sameCubePos(cube,i):
                a = True
        if clickable and not a:
            _3d.objects.append(cube)
        clickable = False
    #   handling deleting cubes currently not used
    if clickable2 and _3d.mouse2Pressed and type(_3d.ray(_3d.camPos[0],_3d.camPos[1],_3d.camPos[2],z2=1,range=10)) == int:
        cube = _3d.returnCube(_3d.camPos[0],_3d.camPos[1],_3d.camPos[2]+100,100)
        closest = _3d.ray(_3d.camPos[0],_3d.camPos[1],_3d.camPos[2],z2=1,range=1000)
        x,y,z = _3d.objects[closest][0][0], _3d.objects[closest][0][1], _3d.objects[closest][0][2]
        x = (x//200)*200
        y = (y//200)*200
        z = (z//200)*200
        cube = _3d.returnCube(x,y,z,100)
        if cube in _3d.objects:
            _3d.objects.remove(cube)
        clickable2 = False
    #   handling if the mouse has been pressed or is already pressed
    if not _3d.mousePressed:
        clickable = True
    if not _3d.mouse2Pressed:
        clickable2 = True
    #drawing the cubes
    canvas.delete(ALL)

    for i in _3d.visible():
        i = _3d.project(i)
        if not i[1][3] > root.winfo_screenwidth() or not i[1][3] < 0 or not i[0][4] > root.winfo_screenheight() or not i[1][4] < 0:
            face = _3d.visibleFace(i)
            _3d.drawFace(i,face[0],lines='black')
            _3d.drawFace(i,face[1],lines='black')
            _3d.drawFace(i,face[2],lines='black')
            _3d.drawFace(i,face[3],lines='black')
            _3d.drawFace(i,face[4],lines='black')
            _3d.drawFace(i,face[5],lines='black')

    lastMouseX = _3d.mouseX
    lastMouseY = _3d.mouseY

    canvas.create_oval(root.winfo_screenwidth()/2-5,root.winfo_screenheight()/2-5,root.winfo_screenwidth()/2+5,root.winfo_screenheight()/2+5,fill='black')
    root.update()
