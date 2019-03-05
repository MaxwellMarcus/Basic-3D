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
        self.usedKeys = []

        self.facing = None

        self.objects = []

        self.start = True

        self.screenWidth = root.winfo_screenwidth()
        self.screenHeight = root.winfo_screenheight()

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
            cosX = math.cos(self.camRot[0])
            sinX = math.sin(self.camRot[0])
            cosY = math.cos(self.camRot[1])
            sinY = math.sin(self.camRot[1])
            cosZ = math.cos(self.camRot[2])
            sinZ = math.sin(self.camRot[2])
            centerX = self.camPos[0]
            centerY = self.camPos[1]
            centerZ = self.camPos[2]
            newX = ((i[0][0]-centerX) * cosY - (i[0][2]-centerZ) * sinY)+centerX
            newY = i[0][1]
            newZ = ((i[0][2]-centerZ) * cosY + (i[0][0]-centerX) * sinY)+centerZ
            originDistX = abs(newX-self.camPos[0])
            originDistY = abs(newY-self.camPos[1])
            originDistZ = abs(newZ-self.camPos[2])
            valueX = abs(newX-self.camPos[0])#*originDistX
            valueY = abs(newY-self.camPos[1])#*originDistY
            valueZ = abs(newZ-self.camPos[2])#*originDistZ
            value = valueX+valueY+valueZ
            if len(sorted)==0:
                sorted.append(i)
            elif value > abs(sorted[0][0][0]-self.camPos[0])+abs(sorted[0][0][1]-self.camPos[1])+abs(sorted[0][0][2]-self.camPos[2]):
                sorted.insert(0,i)
            elif not value < abs(sorted[len(sorted)-1][0][0]-self.camPos[0])+abs(sorted[len(sorted)-1][0][1]-self.camPos[1])+abs(sorted[len(sorted)-1][0][2]-self.camPos[2]):
                for k in sorted:
                    if value >= abs(k[0][0]-self.camPos[0])+abs(k[0][1]-self.camPos[1])+abs(k[0][2]-self.camPos[2]):
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
        centerZ = -self.camPos[2]

    #    x = ((p[0]-centerX) * cosY + (p[2]-centerZ) * sinY)+centerX
    #    y = ((p[1]-centerY) * cosX - (p[2]-centerZ) * sinX)+centerY
    #    z = ((p[2]-centerZ) * cosX + (p[1]-centerY) * sinX)+centerZ
    #    newX = ((x-centerX) * cosZ + (y-centerY) * sinZ)+centerX
    #    newY = ((y-centerY) * cosZ - (x-centerX) * sinZ)+centerY
    #    newZ = ((z-centerZ) * cosY - (x-centerX) * sinY)+centerZ
        newX = ((p[0]-centerX) * cosY - (p[2]-centerZ) * sinY)+centerX
        newZ = ((p[2]-centerZ) * cosY - (p[0]-centerX) * sinY)+centerZ
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
            xrz = (p[2]*cosX)+(p[1]*sinX)
            #xry = (p[1]*cosX)+(p[2]*sinX)
            #yrx = (p[0]*cosY)+(xrz*sinY)
            #yxz = (xrz*cosY)-(p[0]*sinY)
            newX = p[0]
            newY = p[1]
            newZ = xrz
            #if p[0] < 10 and p[0] > -10 and p[1] < 10 and p[1] > -10 and p[2] < 10 and p[2] > -10:
            if p[0] == 120 and p[1] == 120 and p[2] == 120:
                print(xrz)
                print(newY)
                print('')
            if not newZ == self.camPos[2] and newZ > self.camPos[2]:
                l = [self.fl,self.camPos[2],newZ]
                l = list(l)
                first = float(l[0]-l[1])
                second = float(l[2]-l[1])
                scale = first/second
                p[3] = newX * 1 + self.camPos[0] * 1
                p[4] = newY * 1 + self.camPos[1] * 1
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

    def drawFace(self,points,indexes,color='',lines='black'):# draws a face using all indexes given
        face = []
        for p in indexes:
            if p[3]:
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
    def rotateAroundX(self,points,angle,rotationPointX,rotationPointY):#this one
        cos = math.cos(angle)
        sin = math.sin(angle)
        radiusY = rotationPointX
        radiusZ = rotationPointY
        for i in points:
            i[1] = ((i[1]-radiusY) * cos - (i[2]-radiusZ) * sin)+radiusY
            i[2] = ((i[2]-radiusZ) * cos + (i[1]-radiusY) * sin)+radiusZ
        return points
    def rotateAroundY(self,points,angle,rotationPointX,rotationPointY):#this one
        cos = math.cos(angle)
        sin = math.sin(angle)
        radiusX = rotationPointX
        radiusZ = rotationPointY
        for i in points:
            i[0] = ((i[0]-radiusX) * cos - (i[2]-radiusZ) * sin)+radiusX
            i[2] = ((i[2]-radiusZ) * cos + (i[0]-radiusX) * sin)+radiusZ
        return points
    def rotateAroundZ(self,points,angle,rotationPointX,rotationPointY):#and this one
        cos = math.cos(angle)
        sin = math.sin(angle)
        radiusX = rotationPointX
        radiusY = rotationPointY
        for i in points:
            i[0] = ((i[0]-radiusX) * cos - (i[1]-radiusY) * sin)+radiusX
            i[1] = ((i[1]-radiusY) * cos + (i[0]-radiusX) * sin)+radiusY
        return points
    def camRotateX(self,angle):#this one
        cos = math.cos(angle)
        sin = math.sin(angle)
        radiusX = points[0][1]
        radiusY = points[0][2]
        for i in points:
            i[1] = ((i[1]-radiusX) * cos - (i[2]-radiusX) * sin)+radiusX
            i[2] = ((i[2]-radiusY) * cos + (i[1]-radiusY) * sin)+radiusY
    def camRotateY(self,angle):#this one
        cos = math.cos(angle)
        sin = math.sin(angle)
        radiusX = points[0][0]
        radiusY = points[0][2]
        i = self.camPos
        i[2] = ((i[2]-radiusX) * cos - (i[0]-radiusX) * sin)+radiusX
        i[0] = ((i[0]-radiusY) * cos + (i[2]-radiusY) * sin)+radiusY
    def camRotateZ(self,angle):# and this one
        cos = math.cos(angle)
        sin = math.sin(angle)
        radiusX = points[0][1]
        radiusY = points[0][0]
        i = self.camPos
        i[1] = ((i[1]-radiusY) * cos - (i[0]-radiusY) * sin)+radiusY
        i[0] = ((i[0]-radiusX) * cos + (i[1]-radiusX) * sin)+radiusX
    # these ones are the same as the last ones, but they rotate them around the camera or the 0,0 point
    def camRotateAroundX(self,angle,rotationPointX,rotationPointY):#this one
        cos = math.cos(angle)
        sin = math.sin(angle)
        radiusY = rotationPointX
        radiusZ = rotationPointY
        i = self.camPos
        i[1] = ((i[1]-radiusY) * cos - (i[2]-radiusZ) * sin)+radiusY
        i[2] = ((i[2]-radiusZ) * cos + (i[1]-radiusY) * sin)+radiusZ
    def camRotateAroundY(self,angle,rotationPointX,rotationPointY):#this one
        cos = math.cos(angle)
        sin = math.sin(angle)
        radiusX = rotationPointX
        radiusZ = rotationPointY
        i = self.camPos
        i[0] = ((i[0]-radiusX) * cos - (i[2]-radiusZ) * sin)+radiusX
        i[2] = ((i[2]-radiusZ) * cos + (i[0]-radiusX) * sin)+radiusZ
    def camRotateAroundZ(self,angle,rotationPointX,rotationPointY):#and this one
        cos = math.cos(angle)
        sin = math.sin(angle)
        radiusX = rotationPointX
        radiusY = rotationPointY
        i = self.camPos
        i[0] = ((i[0]-radiusX) * cos - (i[1]-radiusY) * sin)+radiusX
        i[1] = ((i[1]-radiusY) * cos + (i[0]-radiusX) * sin)+radiusY
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
        r1 = (cube1[0][0]-cube1[1][0])
        r2 = (cube2[0][0]-cube2[1][0])
        x1,y1,z1 = cube1[0][0],cube1[0][1],cube1[0][2]
        x2,y2,z2 = cube2[0][0],cube2[0][1],cube2[0][2]

        if x1+r1 > x2-r2 and x1-r1 < x2+r2 and y1+r1 > y2-r2 and y1-r1 < y2+r2 and z1+r1 > z2-r2 and z1-r1 < z2+r2:
            return True
        else:
            return False
    def visible(self,cubes):
        things = []
        for p in cubes:
            newCube=[p[0]]
            for r in range(len(p)-1):
                i = p[r+1]
                newPos = self.applyCamRot(i[0],i[1],i[2])
                newPos.append(i[3])
                newPos.append(i[4])
                newCube.append(newPos)
            if newCube[0][2] > self.camPos[2]:
                things.append(newCube)
        return self.zsort(things)
    def visibleFace(self,c):
        originDistX = abs(c[0][0]-self.camPos[0])
        originDistY = abs(c[0][1]-self.camPos[1])
        originDistZ = abs(c[0][2]-self.camPos[2])
        if originDistX == 0:
            originDistX = .001
        if originDistY == 0:
            originDistY = .001
        if originDistZ == 0:
            originDistZ = .001
        face1 = [c[5],c[6],c[7],c[8]]
        face1avgZ = (face1[0][2]+face1[1][2]+face1[2][2]+face1[3][2])/4
        face1avgX = (face1[0][0]+face1[1][0]+face1[2][0]+face1[3][0])/4
        face1avgY = (face1[0][1]+face1[1][1]+face1[2][1]+face1[3][1])/4
        face1distY = abs((face1avgY)-(self.camPos[1]))*originDistY
        face1distX = abs((face1avgX)-(self.camPos[0]))*originDistX
        face1distZ = abs((face1avgZ)-(self.camPos[2]))*originDistZ
        face1.append(face1distX+face1distY+face1distZ)
        face1.append('white')
        face2 = [c[2],c[3],c[7],c[6]]
        face2avgZ = (face2[0][2]+face2[1][2]+face2[2][2]+face2[3][2])/4
        face2avgX = (face2[0][0]+face2[1][0]+face2[2][0]+face2[3][0])/4
        face2avgY = (face2[0][1]+face2[1][1]+face2[2][1]+face2[3][1])/4
        face2distX = abs((face2avgX)-(self.camPos[0]))*originDistX
        face2distZ = abs((face2avgZ)-(self.camPos[2]))*originDistZ
        face2distY = abs((face2avgY)-(self.camPos[1]))*originDistY
        face2.append(face2distX+face2distY+face2distZ)
        face2.append('orange')
        face3 = [c[1],c[4],c[8],c[5]]
        face3avgZ = (face3[0][2]+face3[1][2]+face3[2][2]+face3[3][2])/4
        face3avgX = (face3[0][0]+face3[1][0]+face3[2][0]+face3[3][0])/4
        face3avgY = (face3[0][1]+face3[1][1]+face3[2][1]+face3[3][1])/4
        face3distX = abs((face3avgX)-(self.camPos[0]))*originDistX
        face3distY = abs((face3avgY)-(self.camPos[1]))*originDistY
        face3distZ = abs((face3avgZ)-(self.camPos[2]))*originDistZ
        face3.append(face3distX+face3distY+face3distZ)
        face3.append('red')
        face4 = [c[3],c[4],c[8],c[7],]
        face4avgZ = (face4[0][2]+face4[1][2]+face4[2][2]+face4[3][2])/4
        face4avgX = (face4[0][0]+face4[1][0]+face4[2][0]+face4[3][0])/4
        face4avgY = (face4[0][1]+face4[1][1]+face4[2][1]+face4[3][1])/4
        face4distX = abs((face4avgX)-(self.camPos[0]))*originDistX
        face4distY = abs((face4avgY)-(self.camPos[1]))*originDistY
        face4distZ = abs((face4avgZ)-(self.camPos[2]))*originDistZ
        face4.append(face4distX+face4distY+face4distZ)
        face4.append('green')
        face5 = [c[2],c[1],c[5],c[6]]
        face5avgZ = (face5[0][2]+face5[1][2]+face5[2][2]+face5[3][2])/4
        face5avgX = (face5[0][0]+face5[1][0]+face5[2][0]+face5[3][0])/4
        face5avgY = (face5[0][1]+face5[1][1]+face5[2][1]+face5[3][1])/4
        face5distX = abs((face5avgX)-(self.camPos[0]))*originDistX
        face5distY = abs((face5avgY)-(self.camPos[1]))*originDistY
        face5distZ = abs((face5avgZ)-(self.camPos[2]))*originDistZ
        face5.append(face5distX+face5distY+face5distZ)
        face5.append('blue')
        face6 = [c[1],c[2],c[3],c[4]]
        face6avgZ = (face6[0][2]+face6[1][2]+face6[2][2]+face6[3][2])/4
        face6avgX = (face6[0][0]+face6[1][0]+face6[2][0]+face6[3][0])/4
        face6avgY = (face6[0][1]+face6[1][1]+face6[2][1]+face6[3][1])/4
        face6distX = abs((face6avgX)-(self.camPos[0]))*originDistX
        face6distY = abs((face6avgY)-(self.camPos[1]))*originDistY
        face6distZ = abs((face6avgZ)-(self.camPos[2]))*originDistZ
        face6.append(face6distX+face6distY+face6distZ)
        face6.append('yellow')
        list = [face1,face2,face3,face4,face5,face6]
        sorted = []
        for i in list:
            if len(sorted)==0:
                first = False
                sorted.append(i)
            elif i[4] > sorted[0][4]:
                sorted.insert(0,i)
            elif not i[4] < sorted[len(sorted)-1][4] and i[4] != sorted[len(sorted)-1][4]:
                for k in sorted:
                    if i[4] > k[4]:
                        sorted.insert(sorted.index(k),i)
                        break
            else:
                sorted.append(i)
        for i in sorted:
            i.remove(i[4])

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
    def drawRotationCircle(self,x,y,centerX,centerY):
        i=0
        while i <= math.pi*2:
            sin = math.sin(i)
            cos = math.cos(i)
            x = ((x-centerX)*cos-(y-centerY)*sin)+centerX+root.winfo_screenwidth()/2
            y = ((y-centerY)*cos+(x-centerX)*sin)+centerY+root.winfo_screenheight()/2
            self.draw_square(x,y,2)
            i += math.pi/180
    def clearScreen(self):
        canvas.delete(ALL)
    def updateScreen(self):
        root.update()
    def drawText(self,x,y,text,fontSize):
        canvas.create_text(x,y,text=text,font=('TkTextFont',fontSize))
    def draw_faces(self,points,face):
        i = points
#        if not i[1][3] > root.winfo_screenwidth() or not i[1][3] < 0 or not i[0][4] > root.winfo_screenheight() or not i[1][4] < 0:
        self.drawFace(i,face[0][0:4],color=face[0][4],lines='black')
        self.drawFace(i,face[1][0:4],color=face[1][4],lines='black')
        self.drawFace(i,face[2][0:4],color=face[2][4],lines='black')
        self.drawFace(i,face[3][0:4],color=face[3][4],lines='black')
        self.drawFace(i,face[4][0:4],color=face[4][4],lines='black')
        self.drawFace(i,face[5][0:4],color=face[5][4],lines='black')
    def draw_square(self,x,y,radius,color='black'):#not used
        canvas.create_rectangle(x-radius,y-radius,x+radius,y+radius,fill=color)
    def keyPressed(self,event):#adds a keysym to the list of keys pressed
        self.keysPressed.append(event.keysym)
    def KeyReleased(self,event):#takes a keysym of the list of keys pressed
        i = 0
        while i < self.keysPressed.count(event.keysym):
            self.keysPressed.remove(event.keysym)
            i=0
        i = 0
        while i < self.usedKeys.count(event.keysym):
            self.usedKeys.remove(event.keysym)
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

#making the first cubes
for i in range(3):
    _3d.createCube(200,200,(i-1)*200,100)
    _3d.createCube(200,-200,(i-1)*200,100)
    _3d.createCube(-200,200,(i-1)*200,100)
    _3d.createCube(-200,-200,(i-1)*200,100)
    _3d.createCube(0,200,(i-1)*200,100)
    _3d.createCube(0,-200,(i-1)*200,100)
    _3d.createCube(200,0,(i-1)*200,100)
    _3d.createCube(-200,0,(i-1)*200,100)
    _3d.createCube(0,0,(i-1)*200,100)
'''for i in range(3):
    for k in range(3):
        for l in range(3):
            _3d.createCube(i*100,k*100,l*100,200'''
#setting a few variables
rotationSpeed = 1
baseAngle = 0

lastMouseY = _3d.mouseY
lastMouseX = _3d.mouseX

clickable = True
clickable2 = True

#the game loop
while _3d.start and __name__ == '__main__':
    #handling all things with input
    #   handling exiting with no errors
    if 'Escape' in _3d.keysPressed:
        _3d.start = False
    #   handling rotation
    #       currently Z rotation
    if 'Up' in _3d.keysPressed:
        for i in _3d.objects:
            _3d.camRotate(0,math.pi/180,0)
    if 'Down' in _3d.keysPressed:
        for i in _3d.objects:
            _3d.camRotate(0,-math.pi/180,0)
    #       currently Y rotation, but it is not used
    if 'Left' in _3d.keysPressed:
        _3d.camRotateAroundY(math.pi/180,0,0)
    if 'Right' in _3d.keysPressed:
        _3d.camRotateAroundY(-math.pi/180,0,0)#rotateAroundY(i,-math.pi/180,0,0)
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
        _3d.objects = []
        for i in range(3):
            _3d.createCube(200,200,(i-1)*200,100)
            _3d.createCube(200,-200,(i-1)*200,100)
            _3d.createCube(-200,200,(i-1)*200,100)
            _3d.createCube(-200,-200,(i-1)*200,100)
            _3d.createCube(0,200,(i-1)*200,100)
            _3d.createCube(0,-200,(i-1)*200,100)
            _3d.createCube(200,0,(i-1)*200,100)
            _3d.createCube(-200,0,(i-1)*200,100)
            _3d.createCube(0,0,(i-1)*200,100)
    if 'j' in _3d.keysPressed:
        for i in range(9):
            s = _3d.objects[i]
            _3d.rotateAroundZ(s,math.pi/180,0,0)
    if 'p' in _3d.keysPressed:
        _3d.camPos = [0,0,-800]
        _3d.camRot = [0,0,0]
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
            _3d.drawFace(i,face[0][0:4],color=face[0][4],lines='black')
            _3d.drawFace(i,face[1][0:4],color=face[1][4],lines='black')
            _3d.drawFace(i,face[2][0:4],color=face[2][4],lines='black')
            _3d.drawFace(i,face[3][0:4],color=face[3][4],lines='black')
            _3d.drawFace(i,face[4][0:4],color=face[4][4],lines='black')
            _3d.drawFace(i,face[5][0:4],color=face[5][4],lines='black')
    lastMouseX = _3d.mouseX
    lastMouseY = _3d.mouseY

    canvas.create_oval(root.winfo_screenwidth()/2-5,root.winfo_screenheight()/2-5,root.winfo_screenwidth()/2+5,root.winfo_screenheight()/2+5,fill='black')
    root.update()
