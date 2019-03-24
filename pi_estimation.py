import math
from decimal import Decimal
circle_dots = 0
dots = 0
length = 10
for x in range(length):
    for y in range(length):
        dots += 1
        _x = abs(x-length/2)*abs(x-length/2)
        _y = abs(y-length/2)*abs(y-length/2)
        dist = math.sqrt(_x+_y)
        if dist <= length/2:
            circle_dots += 1
        print(float(circle_dots)/float(dots))
print(circle_dots,dots)
