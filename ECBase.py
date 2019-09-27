class ECCurve:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def __eq__(self, g2):
        return (self.a == g2.a) and (self.b == g2.b) and (self.c == g2.c)
        
class ECPoint:
    def __init__(self, graph, x, y):
        assert(isinstance(x, int) or isinstance(x, float)), "x must be a real number"
        assert(isinstance(y, int) or isinstance(y, float)), "y must be a real number"
        assert(isinstance(graph, ECCurve)), "graph must be of type ECCurve"
        self.graph = graph
        self.x = x
        self.y = y
    '''
    'Magic Method' Overloads Supported:
    eq
    ne
    neg
    add
    str
    '''
    def __eq__(self, p2):
        return (self.x == p2.x) and (self.y == p2.y) and (self.graph == p2.graph)
    def __ne__(self, p2):
        return not self == p2
    def __neg__(self):
        return ECPoint(self.graph, self.x, -self.y)
    def __add__(self, p2):
        assert(self.graph == p2.graph), "Cannot add points on different graphs"
        g = self.graph
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
        return ECPoint(g, round(x3, 7), round(y3, 7))
    def __str__(self):
        return '(' + str(self.x) + ', ' + str(self.y) + ')'
