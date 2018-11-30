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
        self.centerZ = 1000
        self.mouseX = 0
        self.mouseY = 0
        root.bind('<Motion>',self.mouseSet)
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

    def perspectify(self,shape,color):
        shapeRadius = 50
        perspective = self.fl/(self.fl+shape[2])
        radius = shapeRadius * perspective
        shapeMod = [shape[0]*perspective + root.winfo_screenwidth()/2,shape[1]*perspective+root.winfo_screenheight()/2]
        canvas.create_rectangle(shapeMod[0]-radius,shapeMod[1]-radius,shapeMod[0]+radius,shapeMod[1]+radius,fill = color)


_3d = _3D(300)

shapes = []
shapes2 = []
numShapes = 10

for i in range(numShapes):
    angle = math.pi * 2/numShapes * i
    shape = [math.cos(angle) * _3d.radius,0,_3d.centerZ + math.sin(angle) * _3d.radius]
    shapes.append(shape)
for i in range(numShapes):
    angle = math.pi * 2/numShapes * i
    shape = [0,math.cos(angle) * _3d.radius,_3d.centerZ + math.sin(angle) * _3d.radius]
    shapes2.append(shape)

rotationSpeed = 1
baseAngle = 0
rotationSpeed2 = 1
baseAngle2 = 0
colors = ['red','green','blue','yellow','orange','black']

while True:
    canvas.delete(ALL)
    rotationSpeed = (_3d.mouseX - root.winfo_screenwidth()/2) * 0.000005
    baseAngle += rotationSpeed
    i = 0
    while i < len(shapes):
        angle = math.pi * 2/numShapes * i
        shapes[i][0] = math.cos(angle + baseAngle) * _3d.radius
        shapes[i][2] = _3d.centerZ + math.sin(angle + baseAngle) * _3d.radius
        i += 1
    shapes = _3d.zsort(shapes)
    i = 0
    while i < len(shapes):
        _3d.perspectify(shapes[i],'blue')
        i += 1

    rotationSpeed2 = (_3d.mouseY - root.winfo_screenheight()/2) * 0.000005
    baseAngle2 += rotationSpeed2
    i = 0
    while i < len(shapes2):
        angle = math.pi * 2/numShapes * i
        shapes2[i][1] = math.cos(angle + baseAngle2) * _3d.radius
        shapes2[i][2] = _3d.centerZ + math.sin(angle + baseAngle2) * _3d.radius
        i += 1
    shapes2 = _3d.zsort(shapes2)
    i = 0
    while i < len(shapes2):
        _3d.perspectify(shapes2[i],'blue')
        i += 1
    root.update()
