try:
    from Tkinter import *
except:
    from tkinter import *1
import math

root = Tk()
canvas = Canvas(root,width = root.winfo_screenwidth(),height = root.winfo_screenheight())
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

class Particle:
    def __init__(self,x,y,speed = 0,angle = 0,accelAngle = 0,acceleration = 0,accelerationX=0,accelerationY=0,friction = 1,mass = 10,maxVel = 10000000,radius = 10):
        self.position = Vector(x,y)
        self.velocity = Vector(0,0)
        self.acceleration = Vector(accelerationX,accelerationY)
        self.acceleration.setAngle(accelAngle)
        self.acceleration.setLength(acceleration)
        self.acceleration.setAngle(accelAngle)
        self.velocity.setAngle(angle)
        self.velocity.setLength(speed)
        self.velocity.setAngle(angle)

        self.radius = radius
        self.maxVel = maxVel
        self.mass = mass
        self.friction = Vector(friction,friction)
        self.color = 'black'

        root.bind('<KeyPress>',self.keypress)
        root.bind('<KeyRelease>',self.keyrelease)
        #root.bind('<Motion>',self.moveToMouse)
    def keypress(self,event):
        if event.keysym == 'w':self.acceleration.setY(-0.1)
        if event.keysym == 's':self.acceleration.setY(0.1)
        if event.keysym == 'a':self.acceleration.setX(-0.1)
        if event.keysym == 'd':self.acceleration.setX(0.1)
    def keyrelease(self,event):
        if event.keysym == 'w':self.acceleration.setY(0)#self.velocity.setY(0);self.acceleration.setY(0)
        if event.keysym == 's':self.acceleration.setY(0)#self.velocity.setY(0);self.acceleration.setY(0)
        if event.keysym == 'a':self.acceleration.setX(0)#self.velocity.setX(0);self.acceleration.setX(0)
        if event.keysym == 'd':self.acceleration.setX(0)#self.velocity.setX(0);self.acceleration.setX(0)
    def angleTo (self,p2):
        return math.atan2(p2.position.getY()-self.position.getY(),p2.position.getX() - self.position.getX())
    def distanceTo(self,p2):
        dx = p2.position.getX() - (self.position.getX())
        dy = p2.position.getY() - (self.position.getY())
        return math.sqrt(dx*dx+dy*dy)
    def gravitateTo(self,p2):
        grav = Vector(0,0)
        dist = self.distanceTo(p2)
        grav.setLength(p2.mass/(dist*dist))
        grav.setAngle(self.angleTo(p2))
        self.velocity.addTo(grav)
    def moveToMouse(self,event):
        self.position.setX(event.x)
        self.position.setY(event.y)
    def update(self):
        if self.velocity.getLength() < self.maxVel:
            self.position.addTo(self.velocity.divide(100))
        self.velocity.addTo(self.acceleration)

        if self.position.getX() + self.radius > root.winfo_screenwidth():self.velocity.setX(-self.velocity.getX()*-1);self.position.setX(root.winfo_screenwidth() - self.radius)#self.position.setX(- self.radius)
        if self.position.getY() + self.radius > root.winfo_screenheight():self.velocity.setY(-self.velocity.getY()*-1);self.position.setY(root.winfo_screenheight() - self.radius)#self.position.setY(- self.radius)
        if self.position.getX() - self.radius < 0:self.velocity.setX(self.velocity.getX()*-1);self.position.setX(self.radius)#self.position.setX(2000 + self.radius )
        if self.position.getY() - self.radius < 0:self.velocity.setY(self.velocity.getY()*-1);self.position.setY(self.radius)#self.position.setY(2000 + self.radius )

particles = []
planet = Particle(400,300,-2,maxVel = 1000,radius = 50)
planet.color = 'blue'
particles.append(planet)
def update():
    canvas.delete(ALL)
    for i in particles:
        i.update()
        canvas.create_oval(i.position.getX()-i.radius,i.position.getY()-i.radius,i.position.getX()+i.radius,i.position.getY()+i.radius,fill = i.color)
    root.update()

while True:
    update()
