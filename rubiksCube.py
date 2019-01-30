import render3D
import math
camera = render3D._3D(500)

class rubiksCube:
    def __init__(self,x,y,z):
        self.cubes = []
        self.x = x
        self.y = y
        self.z = z
        for x in range(3):
            for y in range(3):
                for z in range(3):
                    self.cubes.append(camera.returnCube((x-1)*100,(y-1)*100,(z-1)*100,20))
        for i in self.cubes:
            i = camera.project(i)

    def rotateAroundCubeX(self,angle):
        sin = math.sin(angle)
        cos = math.cos(angle)
        y = camera.camPos[1]
        z = camera.camPos[2]
        camera.camPos[1] = (y*cos)-(z*sin)
        camera.camPos[2] = (z*cos)+(y*sin)

    def rotateAroundCubeY(self,angle):
        sin = math.sin(angle)
        cos = math.cos(angle)
        x = camera.camPos[0]
        z = camera.camPos[2]
        camera.camPos[0] = (x*cos)+(z*sin)
        camera.camPos[2] = (z*cos)-(x*sin)
        camera.camRot[1] -= angle*2
    def rotateAroundCubeZ(self,angle):
        sin = math.sin(angle)
        cos = math.cos(angle)
        x = camera.camPos[0]
        y = camera.camPos[1]
        camera.camPos[0] = (x*cos)-(y*sin)
        camera.camPos[1] = (y*cos)+(x*sin)
    def render(self):
        camera.clearScreen()
        for i in camera.visible(self.cubes):
            i = camera.project(i)
            face = camera.visibleFace(i)
            camera.draw_faces(i,face)
        camera.updateScreen()


cube = rubiksCube(0,0,0)
while camera.start:
    if 'Escape' in camera.keysPressed:
        camera.start = False
    if 'w' in camera.keysPressed:
        camera.camPos[2] -= 10
    if 's' in camera.keysPressed:
        camera.camPos[2] += 10
    if 'j' in camera.keysPressed:
        cube.rotateAroundCubeY(math.pi/180)
    if 'k' in camera.keysPressed:
        cube.rotateAroundCubeY(-math.pi/180)

    cube.render()
