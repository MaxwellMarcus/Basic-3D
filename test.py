from Tkinter import *
import math

root = Tk()
canvas = Canvas(root,width = 500,height = 500)
canvas.pack()


class Vector:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def create(self,x,y):
        return Vector(x,y)
    def getLength(self):
        return math.sqrt(self.x * self.x + self.y * self.y)
    def setX(self,value):
        self.x = value
    def getX(self):
        return self.x
    def setY(self,value):
        self.y = value
    def getY(self):
        return self.y
    def setAngle(self,angle):
        length = self.getLength()
        self.x = math.cos(angle) * length
        self.y = math.sin(angle) * length
    def getAngle(self):
        return math.atan2(self.y,self.x)
    def setLength(self,length):
        angle = self.getAngle()
        self.x = math.cos(angle) * length
        self.y = math.sin(angle) * length
    def add(self,v2):
        return self.create(self.x + v2.getX(),self.y + v2.getY())
    def subtract(self,v2):
        return self.create(self.x - v2.getX(),self.y - v2.getY())
    def multiply(self,value):
        return self.create(self.x*value,self.y*value)
    def divide(self,value):
        return self.create(self.x/value,self.y/value)
    def addTo(self,v2):
        self.x += v2.getX()
        self.y += v2.getY()
    def subtractFrom(self,v2):
        self.x -= v2.getX()
        self.y -= v2.getY()
    def multiplyBy(self,value):
        self.x *= value
        self.y *= value
    def divideBy(self,value):
        self.x /= value
        self.y /= value
