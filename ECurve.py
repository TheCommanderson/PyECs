class ECCurve:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def __eq__(self, g2):
        return (self.a == g2.a) and (self.b == g2.b) and (self.c == g2.c)
