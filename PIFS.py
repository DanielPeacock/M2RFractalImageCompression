from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import numpy as np

class Window:
  def __init__(self, x_min, x_max, y_min, y_max, resolution):
    self.x_min = x_min
    self.x_max = x_max
    self.y_min = y_min
    self.y_max = y_max
    self.resolution = resolution


class PIFS:
  def __init__(self, domain_blocks, range_blocks, transformations):
    self.domain_blocks = domain_blocks
    self.range_blocks = range_blocks
    self.transformations = transformations

  #checks if a point is in the approximate attractor (for a given number of iterations)
  def is_in_attractor(self, n, init_point):
    x, y = [init_point[0]], [init_point[1]] 

    #generate f(x,y), f^2(x,y), ..., f^n(x,y)
    for _ in range(n):
      point = (x[-1], y[-1])
      length = len(x)

      #check if point in any range block, and apply f(x,y) if so
      for i in range(len(self.range_blocks)):
        if self.range_blocks[i].contains(point):
          self.transformations[i].apply_inverse(x, y)
          break
      
      if length == len(x): 
        #no new points added, i.e. does not appear in a range block
        return False 

    #all points generated are in the range blocks
    return True

  #generates the points in the approximate attractor
  #for a given number of iterations, in a given viewing window
  def eta_generate_image(self, n, window):
    #lists of x and y coordinates
    x, y = [], []

    #for each point in the viewing window (at given resolution)
    #add if in the approximate attractor
    for i in np.linspace(window.x_min, window.x_max, window.resolution):
      for j in np.linspace(window.y_min, window.y_max, window.resolution):
        if self.is_in_attractor(n, (i,j)):
          x.append(i)
          y.append(j)

    return x, y

  #sets plot to only show viewing window
  def set_figure(self, window):
    plt.xlim([window.x_min - 0.1, window.x_max + 0.1])
    plt.ylim([window.y_min - 0.1, window.y_max + 0.1])

  #generates and plots the approximate attractor
  #given a number of iterations and a viewing window
  def show_image(self, n, window):
    x, y = self.eta_generate_image(n, window)

    self.set_figure(window)
    plt.scatter(x, y, s=100/window.resolution)

  #shows the domain and range block of the PIFS in a given viewing window
  def show_blocks(self, window):
        w_width = window.x_max - window.x_min
        w_height = window.y_max - window.y_min

        fig, ax = plt.subplots(figsize=(w_width, w_height))
        self.set_figure(window)

        num_blocks = len(self.domain_blocks)

        #colors the different rectangles
        cmap = cm.get_cmap('rainbow')
        norm = mcolors.Normalize(0, num_blocks - 1)

        #add blocks
        for i in range(num_blocks):
            color = cmap(norm(i))

            domain_block = self.domain_blocks[i]  
            ax.add_patch(Rectangle(domain_block.bot_left, domain_block.width, domain_block.height,
                                   edgecolor = color, facecolor = 'none'))
          
            range_block = self.range_blocks[i]
            ax.add_patch(Rectangle(range_block.bot_left, range_block.width, range_block.height,
                                   edgecolor = color, facecolor = color, alpha = 0.5, label=f"$w_{i+1}$"))
            
        plt.legend()
        plt.show()