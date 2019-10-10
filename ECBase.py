from math import sqrt
from numpy import roots, isreal, inf
from fractions import Fraction

# Error to throw for illegal use of elliptic curves
class CurveError(Exception):
    pass

# Returns type list[ECPoint], a list of finite points on the curve C
def finitePoints(C): # C - an ECCurve
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

# returns boolean, true if ECPoint p is on ECCurve C, else returns false
def is_on_curve(p, C): # p - an ECPoint, C - an ECCurve
    left = p.y**2
    right = p.x**3 + (C.a * p.x**2) + (C.b * p.x) + C.c
    return left == right

# returns type int, the ord of rational number n with regards to prime number p
def Qord(p, n): # p - a prime number, n - a rational number
    f = Fraction(n)
    if n == 0: # return inf by convention if n == 0
        return inf

    numerator = f.numerator
    denominator = f.denominator
    n_ord = 0
    d_ord = 0
    while not numerator % p:
        numerator /= p
        n_ord += 1
    while not denominator % p:
        denominator /= p
        d_ord -= 1
    return n_ord - d_ord

# returns a number, the p-adic absolute value of rational number n with regards
# to prime number p
def padicAbs(p, n): # p - a prime number, n - a rational number
    if n == 0: # return 1 by convention if n == 0
        return 1

    nu = Qord(p, n)
    return 1/(p**nu)

class ECCurve:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c
        self.disc = (-4*(a**3)*c) + (a**2*b**2) + (18*a*b*c) - (4*(b**3)) - (27*c**2)

    def __eq__(self, c2):
        if not isinstance(c2, ECCurve):
            raise TypeError("Cannot compare type ECCurve to type {}".format(type(c2)))
        return (self.a == c2.a) and (self.b == c2.b) and (self.c == c2.c)

    def __repr__(self):
        return "ECCurve"

class ECPoint:
    def __init__(self, curve, x, y):
        # Points must be on the curve and have number x and y values
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

    def __eq__(self, p2):
        if not isinstance(p2, ECPoint):
            raise TypeError("Cannot compare type ECPoint to type {}".format(type(p2)))
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
        return ECPoint(g, x3, y3)

    def __iadd__(self, p2):
        return self + p2

    def __sub__(self, p2):
        return self + -p2

    def __str__(self):
        return '(' + str(self.x) + ', ' + str(self.y) + ')'

    def __hash__(self):
        return (53*hash(self.x)) + (53*hash(self.y))

    def __mul__(self, n):
        if not (isinstance(n, int) or instance(n, float)):
            raise TypeError("Cannot multiply ECPoint and {} (is your scalar multiple the second argument?)".format(type(n)))
        tmp = ECPoint(self.curve, self.x, self.y)
        for i in range(1, n):
            tmp = tmp + self
        return tmp
