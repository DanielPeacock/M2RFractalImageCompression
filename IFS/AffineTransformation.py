#class for 2d affine transformation
class AffineTransformation:
    def __init__(self, a, b, c, d, e, f):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e
        self.f = f

        self.det = self.a*self.d - self.b*self.c
 
    def apply(self, x, y):
        new_x = self.a * x[-1] + self.b * y[-1] + self.e
        new_y = self.c * x[-1] + self.d * y[-1] + self.f
        x.append(new_x)
        y.append(new_y)

    def apply_inverse(self, x, y):
        assert(self.det != 0)

        temp_x = x[-1] - self.e 
        temp_y = y[-1] - self.f 

        new_x = self.d * temp_x - self.b * temp_y
        new_y = - self.c * temp_x + self.d * temp_y

        x.append(new_x / self.det)
        y.append(new_y / self.det)


