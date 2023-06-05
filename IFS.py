import random
import matplotlib.pyplot as plt

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

#transformations
        
#sierpinski triangle
#w1 = AffineTransformation(1/2, 0, 0, 1/2, -3/2, 0)
#w2 = AffineTransformation(1/2, 0, 0, 1/2, 3/2, 0)
#w3 = AffineTransformation(1/2, 0, 0, 1/2, 0, 3/2)

#transformations = [w1, w2, w3]
#probabilities = [1/3, 1/3, 1/3]

#barnsley fern        
w1 = AffineTransformation(0, 0, 0, 0.16, 0, 0)
w2 = AffineTransformation(0.85, 0.04, -0.04, 0.85, 0, 1.6)
w3 = AffineTransformation(0.20, -0.26, 0.23, 0.22, 0, 1.6)
w4 = AffineTransformation(-0.15, 0.28, 0.26, 0.24, 0, 0.44)

transformations = [w1, w2, w3, w4]
probabilities = [0.01, 0.85, 0.07, 0.07]


#initial point 
x, y = [0], [0]

#construct IFS via Chaos Game 
num_points = 1000000

choices = random.choices(transformations, probabilities, k=num_points)
for n in range(num_points):
    choices[n].apply(x, y)

#show IFS
plt.scatter(x, y, s=0.001)
plt.show()


