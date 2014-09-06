import sys
import itertools
import random
import math
n = int(sys.argv[1])
o = int(sys.argv[2])
scale = float(n + o) / 4

def gen_points(n):
    if n == 0:
        return [[0, 0]]
    else:
        p = [[0, 2 * n]]
        for i in range(0, n):
            i = n - i
            j = 2*n - i
            p.append([i, j])
            p.append([-i, j])
        return p + gen_points(n - 1)

print (n+1)**2 + o
for i, j in gen_points(n):
    print "%f %f" % (scale * i, scale * j)
for i in range(0, o):
    print "%f %f" % (scale * random.uniform(-float(n)/2 - n, float(n)/2 + n), scale * random.uniform(-float(n)/2, 2 * n + float(n)/2))
