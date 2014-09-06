import sys
import itertools
import random
import math
n = int(sys.argv[1])
m = int(sys.argv[2])
o = int(sys.argv[3])
scale = int(math.sqrt(math.sqrt(n * m) + o * int(math.sqrt(o))))
print n*m + o
for i, j in itertools.product(range(0, m), range(0, n)):
    print "%f %f" % (scale * i, scale * j)
for i in range(0, o):
    print "%f %f" % (scale * random.uniform(-1, m + 1), scale * random.uniform(-1, n + 1))
