from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import AffineTransformation as af
import IFS as ifs

class PIFS:
    def __init__(self, name, domain_blocks, ifs_list):
        assert len(domain_blocks) == len(ifs_list)
        
        self.name = name
        self.domain_blocks = domain_blocks
        self.ifs_list = ifs_list

        
    def generate_image(self, n):
        #generates 2d arrays containing x coordinates (resp. y coordinates) for each of the blocks
        x, y = [], []
        
        num_blocks = len(self.domain_blocks)
        block_n = round(n/num_blocks)

        for i in range(num_blocks):
            block_x, block_y = self.ifs_list[i].generate_image(block_n) #total number of points is n * num_blocks

            x.append(block_x)
            y.append(block_y)
        
        return x, y

    def show_image(self, n):
        x, y = self.generate_image(n)
        
        plt.scatter(x, y, s=100/n)
        plt.title(f"{self.name} with {n} points")
        
    
        