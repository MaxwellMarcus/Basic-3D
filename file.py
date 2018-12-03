try:
    from Tkinter import *
except:
    from tkinter import *
import random
import math

root = Tk()
canvas = Canvas(root,width = root.winfo_screenwidth(),height = root.winfo_screenheight())
canvas.pack()

screenX = root.winfo_screenwidth()
screenY = root.winfo_screenheight()

centerY = screenY * .5
centerX = screenX * .5
offset = 100
speed = 0.001
angle = 0

while True:
    canvas.delete(ALL)

    y = math.tan(angle) * offset

    canvas.create_oval(centerX + y,centerY + y,centerX - y,centerY - y,fill = 'black')

    angle += speed

    root.update()
