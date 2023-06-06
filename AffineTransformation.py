#class for 2d affine transformation
class AffineTransformation:
    a: float
    b: float
    c: float
    d: float 
    e: float
    f: float
    
    def __init__(self, a, b, c, d, e, f):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e
        self.f = f
    
    def apply(self, x, y):
        new_x = self.a * x[-1] + self.b * y[-1] + self.e
        new_y = self.c * x[-1] + self.d * y[-1] + self.f
        x.append(new_x)
        y.append(new_y)
