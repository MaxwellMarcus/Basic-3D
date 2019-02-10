import math
x = 100
y = 100
sin = math.sin(math.pi/180)
cos = math.cos(math.pi/180)
i = 0
while i <= math.pi*2:
    x = (x*cos)+(y*sin)
    y = (y*cos)-(x*sin)
    i += math.pi/180
print(x,y)
x = 100
y = 100
for i in range(360):
    x = (x*cos)+(y*sin)
    y = (y*cos)-(x*sin)
print(x,y)
