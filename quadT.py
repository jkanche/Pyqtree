from pyqtree import Index
import pickle
import sys
import math
from hilbertcurve.hilbertcurve import HilbertCurve
class Point(object):

    def __init__(self, start, end, offset, length, fileName):
        x = start//16000
        y = start%16000
        self.bbox = (x, y, x+1, y+1)
        self.start = start
        self.end = end
        self.offset = offset
        self.length = length
        self.fileName = fileName

    def __repr__(self):
        return str((self.start, self.end, self.offset, self.fileName))


def hcoords(x, chromLength, dims = 2):
    hlevel = math.ceil(math.log2(chromLength)/dims)
    print("hlevel, ", hlevel)
    hilbert_curve = HilbertCurve(hlevel, dims)
    [x,y] = hilbert_curve.coordinates_from_distance(x)
    return x, y, hlevel


# assuming chr11 length = 10000000000
chromLength = 10000000000
dims=2
# i = chromLength - 1
# print(i, ", ", hcoords(i, chromLength))
hlevel = math.ceil(math.log2(chromLength)/dims)
print("hlevel", hlevel)
x_y_dim = math.ceil(math.pow(2, hlevel))
print("max x|y =", x_y_dim)

tree = Index(bbox=(0, 0, x_y_dim, x_y_dim))

data = pickle.load(open( "result1.p", "rb"))
print(len(data))
for entry in data:
    print(entry)
    (start, end, offset, length, fileName) = (entry[0], entry[1], entry[2], entry[3], 1)
    x, y, _ = hcoords(start, chromLength)
    print("x,y", x, y)
    tree.insert((start, end, offset, length, fileName), (x, y, x + 1, y + 1))

data = pickle.load(open( "result2.p", "rb"))
print(len(data))
for entry in data:
    print(entry)
    (start, end, offset, length, fileName) = (entry[1], entry[3], entry[4], entry[5], 2)
    x, y, _ = hcoords(start, chromLength)
    print("x,y", x, y)
    tree.insert((start, end, offset, length, fileName), (x, y, x + 1, y + 1))

# repeating to see overhead
data = pickle.load(open( "result1.p", "rb"))
print(len(data))
for entry in data:
    print(entry)
    (start, end, offset, length, fileName) = (entry[0], entry[1], entry[2], entry[3], 3)
    x, y, _ = hcoords(start, chromLength)
    print("x,y", x, y)
    tree.insert((start, end, offset, length, fileName), (x, y, x + 1, y + 1))


# need to store the mapping of file names to node ids
map = {
    39033: 1,
    39031: 2,
    39033: 3 # same as 1
}

overlapbbox = (0, 0, 2860, 2860)
matches = tree.intersect(overlapbbox)
print("intersect comes back")

print(len(matches))

# print(matches[0])
print("all matched nodes")
print("format is (start, end, offset, length, fileName)")
for item in matches:    
    print(item)
    print(sys.getsizeof(item))
# print(sys.getsizeof(data))