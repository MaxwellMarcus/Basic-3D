import render3D
import math
camera = render3D._3D(500)
camera.objects.append([[],[0,0,5,0,0]])
def render():
    camera.clearScreen()
    for i in camera.objects:
        i = camera.project(i)[0]
        camera.draw_line((camera.screenWidth/2)-36,0,camera.screenWidth/2-36,camera.screenHeight)
        camera.draw_line((camera.screenWidth/2)+36,0,camera.screenWidth/2+36,camera.screenHeight)
        camera.draw_square(i[1][3]+camera.screenWidth/2,i[1][4]+camera.screenHeight/2,7*camera.project(i)[1])
    camera.updateScreen()
while True:
    if 'w' in camera.keysPressed:
        camera.camPos[2] += 10
    if 's' in camera.keysPressed:
        camera.camPos[2] -= 10
    if 'Up' in camera.keysPressed:
        camera.camRot[0] += math.pi/180
    if 'Down' in camera.keysPressed:
        camera.camRot[0] -= math.pi/180
    render()
