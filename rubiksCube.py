import render3D
from math import *

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
                    self.cubes.append(camera.returnCube((x-1)*100,(y-1)*100,(z-1)*100,200))
        for i in self.cubes:
            i = camera.project(i)

    def rotateCubeX(self,angle):
        sin = sin(angle)
        cos = cos(angle)
        for i in self.cubes:
            for l in i:
                l[1] = (l[1]*cos)-(l[2]*sin)
                l[2] = (l[2]*cos)+(l[1]*sin)
    def rotateCubeY(self,angle):
        sin = sin(angle)
        cos = cos(angle)
        for i in self.cubes:
            for l in i:
                l[0] = (l[0]*cos)-(l[2]*sin)
                l[2] = (l[2]*cos)+(l[0]*sin)
    def rotateCubeZ(self,angle):
        sin = sin(angle)
        cos = cos(angle)
        for i in self.cubes:
            for l in i:
                l[1] = (l[1]*cos)-(l[0]*sin)
                l[0] = (l[0]*cos)+(l[1]*sin)
    def render(self):
        for i in camera.visible(self.cubes):
            i = camera.project(i)
            face = camera.visibleFace(i)
            camera.draw_faces(face)


cube = rubiksCube(0,0,0)
while camera.start:
    if 'Escape' in camera.keysPressed:
        camera.start = False
    cube.render()
