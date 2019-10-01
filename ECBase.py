from math import sqrt
from numpy import roots, isreal

class CurveError(Exception):
    pass

'''
FUNCTION finitePoints
arguments - C (ECCurve)
returns - points (list[ECPoints]), a list of all the finite points on the curve C,
or an empty list if no finite points exist on the curve
'''
def finitePoints(C):
    if not isinstance(C, ECCurve):
        raise TypeError("finitePoints() accepts ECCurve as argument type.")
    points = set()
    y_list = [0]
    for i in range(1, round(sqrt(abs(C.disc)))):
        if not abs(C.disc) % i:
            y_list += [i, C.disc/i]

    for y in y_list:
        x_vals = roots([1, C.a, C.b, C.c-y**2])
        for x in x_vals:
            if isreal(x):
                x = round(x.real, 8) # rounding to 8 because of some small computational rounding error due to python
                if x.is_integer():
                    points.add(ECPoint(C, x, y))
                    points.add(ECPoint(C, x, -y))
    return list(points)
    
def is_on_curve(C, p):
    return True

class ECCurve:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c
        self.disc = (-4*(a**3)*c) + (a**2*b**2) + (18*a*b*c) - (4*(b**3)) - (27*c**2)
    def __eq__(self, g2):
        return (self.a == g2.a) and (self.b == g2.b) and (self.c == g2.c)
    def __repr__(self):
        return "ECCurve"

class ECPoint:
    def __init__(self, curve, x, y):

        x_good = isinstance(x, int) or isinstance(x, float)
        y_good = isinstance(y, int) or isinstance(y, float)
        if not (x_good and y_good):
            raise TypeError("x and y must be numbers.")
        if not isinstance(curve, ECCurve):
            raise TypeError("curve must be of type ECCurve")
        self.curve = curve
        self.x = x
        self.y = y
        if not is_on_curve(self, curve):
            raise CurveError("Specified points x and y are not a solution to the curve provided.")
    '''
    'Magic Method' Overloads Supported:
        eq, ne, neg, add, sub, str, hash, iadd, mul
    '''
    def __eq__(self, p2):
        assert(isinstance(p2, ECPoint)), ""
        return (self.x == p2.x) and (self.y == p2.y) and (self.curve == p2.curve)
    def __ne__(self, p2):
        return not self == p2
    def __neg__(self):
        return ECPoint(self.curve, self.x, -self.y)
    def __add__(self, p2):
        if not self.curve == p2.curve:
            raise CurveError("Cannot add points on different curves.")
        g = self.curve
        if self.x == p2.x: # CASE x1 == x2, use modified lambda and nu
            lbda = (3*(self.x)**2) + (2*g.a*self.x) + g.b
            lbda /= 2*self.y
            nu = (-self.x)**3 + (g.b*self.x) + (2*g.c)
            nu /= 2*self.y
        else: # CASE points are different
            lbda =  (p2.y - self.y)/(p2.x - self.x)
            nu = self.y - (lbda*self.x)

        x3 = lbda**2 - g.a - self.x - p2.x
        y3 = (-lbda*x3)-nu
        return ECPoint(g, round(x3, 8), round(y3, 8)) # round to 8 because of small computational error from python
    def __iadd__(self, p2):
        return self + p2
    def __sub__(self, p2):
        return self + -p2
    def __str__(self):
        return '(' + str(self.x) + ', ' + str(self.y) + ')'
    def __hash__(self):
        return (53*hash(self.x)) + (53*hash(self.y))
    def __mul__(self, n):
        assert(isinstance(n, int) or instance(n, float)), "ECPoints only support scalar multiplication"
        tmp = ECPoint(self.curve, self.x, self.y)
        for i in range(1, n):
            tmp = tmp + self
        return tmp
