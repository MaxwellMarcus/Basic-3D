import math
sin = math.sin(math.pi/180)
cos = math.cos(math.pi/180)
x = 100
y = 0
for i in range(360):
    ox = x
    oy = y
    x = (ox*cos)+(oy*sin)
    y = (oy*cos)-(ox*sin)
print(x,y)
