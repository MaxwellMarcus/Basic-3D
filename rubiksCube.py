import render3D
import math
camera = render3D._3D(500)

class rubiksCube:
    def __init__(self,x,y,z):
        self.cubes = []
        self.originalCubes = []
        self.x = x
        self.y = y
        self.z = z
        for x in range(3):
            for y in range(3):
                for z in range(3):
                    self.cubes.append(camera.returnCube((x-1)*100,(y-1)*100,(z-1)*100,20))
                    self.originalCubes.append(camera.returnCube((x-1)*100,(y-1)*100,(z-1)*100,20))

        for i in self.cubes:
            i = camera.project(i)
    def rotate(self,x=0,y=0,z=0):
        camera.camRotate(x=x,y=y,z=z)
    def rotateX(self,angle):
        sin = math.sin(angle)
        cos = math.cos(angle)
        for i in self.cubes:
            for l in i:
                xo = l[2]
                yo = l[1]
                l[1] = (yo*cos)+(xo*sin)
                l[2] = (xo*cos)-(yo*sin)
    def rotateY(self,angle):
        sin = math.sin(angle)
        cos = math.cos(angle)
        for i in self.cubes:
            for l in i:
                xo = l[0]
                yo = l[2]
                l[2] = (yo*cos)+(xo*sin)
                l[0] = (xo*cos)-(yo*sin)
    def rotateZ(self,angle):
        sin = math.sin(angle)
        cos = math.cos(angle)
        for i in self.cubes:
            for l in i:
                xo = l[0]
                yo = l[1]
                l[1] = (yo*cos)+(xo*sin)
                l[0] = (xo*cos)-(yo*sin)
    def rotateSide(self,side,angle):
        if side == 1:
            list = []
            for z in self.cubes:
                if z[0][2] < -90:
                    list.append(z)
            if len(list) == 9:
                for z in list:
                    for i in z:
                        sin = math.sin(angle)
                        cos = math.cos(angle)
                        ox = i[0]
                        oy = i[1]
                        i[0]=(ox*cos)-(oy*sin)
                        i[1]=(oy*cos)+(ox*sin)
                        dist=z[0][2]-i[2]
                       # i[2]=-100-dist
        elif side == 2:
            list = []
            for z in self.cubes:
                if z[0][2] > 90:
                    list.append(z)
            if len(list) == 9:
                for z in list:
                    if z[0][2] > 0:
                        for i in z:
                            sin = math.sin(angle)
                            cos = math.cos(angle)
                            ox = i[0]
                            oy = i[1]
                            i[0]=(ox*cos)-(oy*sin)
                            i[1]=(oy*cos)+(ox*sin)
                            dist=z[0][2]-i[2]
                          #  i[2]=100-dist
        elif side == 3:
            list = []
            for z in self.cubes:
                if z[0][1] > 90:
                    list.append(z)
            if len(list) == 9:
                for z in list:
                    if z[0][1] > 0:
                        for i in z:
                            sin = math.sin(angle)
                            cos = math.cos(angle)
                            ox = i[0]
                            oy = i[2]
                            i[0]=(ox*cos)-(oy*sin)
                            i[2]=(oy*cos)+(ox*sin)
                            dist=z[0][1]-i[1]
                         #   i[1]=100-dist
        elif side == 4:
            list = []
            for z in self.cubes:
                if z[0][1] < -90:
                    list.append(z)
            if len(list) == 9:
                for z in list:
                    if z[0][1] < 0:
                        for i in z:
                            sin = math.sin(angle)
                            cos = math.cos(angle)
                            ox = i[0]
                            oy = i[2]
                            i[0]=(ox*cos)-(oy*sin)
                            i[2]=(oy*cos)+(ox*sin)
                            dist=z[0][1]-i[1]
                           # i[1]=100-dist
        elif side == 5:
            list = []
            for z in self.cubes:
                if z[0][0] > 90:
                    list.append(z)
            if len(list) == 9:
                for z in list:
                    if z[0][0] > 0:
                        for i in z:
                            sin = math.sin(angle)
                            cos = math.cos(angle)
                            ox = i[1]
                            oy = i[2]
                            i[1]=(ox*cos)-(oy*sin)
                            i[2]=(oy*cos)+(ox*sin)
                            dist=z[0][0]-i[0]
                            #i[0]=100-dist
        elif side == 6:
            list = []
            for z in self.cubes:
                if z[0][0] < -90:
                    list.append(z)
            if len(list) == 9:
                for z in list:
                    if z[0][0] < 0:
                        for i in z:
                            sin = math.sin(angle)
                            cos = math.cos(angle)
                            ox = i[1]
                            oy = i[2]
                            i[1]=(ox*cos)-(oy*sin)
                            i[2]=(oy*cos)+(ox*sin)
                            dist=z[0][0]-i[0]
                           # i[0]=100-dist
    def recenterCube(self,index):
        l = []
        c = self.cubes[index][0]
        for i in range(3):
            if c[i] > 50:
                l.append(100)
            elif c[i] < 50:
                l.append(-100)
            else:
                l.append(0)
        self.cubes[index] = camera.returnCube(l[0],l[1],l[2],20)
        #for i in self.cubes[index]:
        #    print(i)
    def render(self):
        try:
            camera.clearScreen()
            for i in self.originalCubes:
                i = camera.project(i)
            for i in camera.visible(self.cubes):
                i = camera.project(i)
                face = camera.visibleFace(i)
                camera.draw_faces(i,face)
            camera.updateScreen()
        except:
            camera.start = False


cube = rubiksCube(0,0,0)
cube.render()

while camera.start:
    if 'Escape' in camera.keysPressed:
        camera.start = False
    if 'w' in camera.keysPressed:
        camera.camPos[2] += 10
    if 's' in camera.keysPressed:
        camera.camPos[2] -= 10
    if 'l' in camera.keysPressed and 'l' not in camera.usedKeys:
        cube.rotateSide(1,math.pi/4)
        camera.usedKeys.append('l')
    if 'k' in camera.keysPressed and 'k' not in camera.usedKeys:
        cube.rotateSide(2,math.pi/4)
        camera.usedKeys.append('k')
    if 'j' in camera.keysPressed and 'j' not in camera.usedKeys:
        cube.rotateSide(3,math.pi/4)
        camera.usedKeys.append('j')
    if 'h' in camera.keysPressed and 'h' not in camera.usedKeys:
        cube.rotateSide(4,math.pi/4)
        camera.usedKeys.append('h')
    if 'g' in camera.keysPressed and 'g' not in camera.usedKeys:
        cube.rotateSide(5,math.pi/4)
        camera.usedKeys.append('g')
    if 'f' in camera.keysPressed and 'f' not in camera.usedKeys:
        cube.rotateSide(6,math.pi/4)
        camera.usedKeys.append('f')

    if 'Up' in camera.keysPressed:

        camera.camRotate(x=math.pi/180)
    if 'Down' in camera.keysPressed:
        pass
    if 'Left' in camera.keysPressed:
        pass
    if 'Right' in camera.keysPressed:
        pass
    cube.render()
