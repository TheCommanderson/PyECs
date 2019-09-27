from .ECCurve import ECCurve
class ECPoint:
    def __init__(self, graph, x, y):
        assert(isinstance(x, int) or isinstance(x, float)), "x must be a real number"
        assert(isinstance(y, int) or isinstance(y, float)), "y must be a real number"
        assert(isinstance(graph, ECCurve)), "graph must be of type ECCurve"
        self.graph = graph
        self.x = x
        self.y = y
    def __eq__(self, p2):
        return (self.x == p2.x) and (self.y == p2.y) and (self.graph == p2.graph)
    def __ne__(self, p2):
        return not self == p2
    def dup(self):

    def __add__(self, p2):
        if self == p2:
            return self.dup()
        elif self.x == p2.x:
            lbda = (3*(self.x)**2) + (2*graph.a*self.x) + graph.b
            lbda /= 2*self.y
            nu = (-self.x)**3 + (graph.b*self.x) + (2*graph.c)
            nu /= 2*self.y
        else:
            lbda =  (p2.y - self.y)/(p2.y - self.y)
            nu =
        x3 = lbda**2 - graph.a - self.x - p2.x
        y3 = (-lbda*x3)-nu
        return ECPoint(x3, y3)
