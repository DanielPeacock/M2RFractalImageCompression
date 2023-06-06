import random
from matplotlib import pyplot as plt
import AffineTransformation as af

class IFS:
    def __init__(self, name, fns, probs, startPoint):
        self.name = name
        self.fns = fns
        self.probs = probs
        self.startPoint = startPoint
        
        
    def generate_image(self, n):
        #lists of x and y coords
        x, y = [], []

        x.append(self.startPoint[0])
        y.append(self.startPoint[1])

        # Randomly select functions to be applied using probabilities given
        transforms = random.choices(self.fns, self.probs, k=n)

        # Generate the transformed points
        for i in range(n):
            transforms[i].apply(x, y)

        return x, y


    def show_image(self, n):
        x, y = self.generate_image(n)
        
        plt.scatter(x, y, s=100/n)
        plt.title(f"{self.name} after {n} iterations")  


    def show_thousand_and_mil_iters(self):
        n_thousand = 1000
        n_mil = 1000000
        
        plt.subplots(1, 2, figsize=(9, 8))

        plt.subplot(2, 2, 1)
        self.show_image(n_thousand)

        plt.subplot(2, 2, 2)
        self.show_image(n_mil)

        plt.tight_layout()
        plt.show()