import math
import numpy as np
import matplotlib.pyplot as plt

def delete_duplicates(lst):
    return list(set(lst))

def step(lsp, lsf):
    joined_list = np.round(np.concatenate(lsf, axis=None), 3)
    mapped_list = [list(map(lambda x: x, lsp)) for _ in joined_list]
    return delete_duplicates(mapped_list)

def nest_step(lsp, funs, n):
    for _ in range(n):
        lsp = step(lsp, funs)
    return lsp

def gpoint(xxx):
    points = np.array(xxx)
    plt.scatter(points[:, 0], points[:, 1], color='black', s=1)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.gca().spines['left'].set_position('zero')
    plt.gca().spines['bottom'].set_position('zero')
    plt.gca().spines['right'].set_color('none')
    plt.gca().spines['top'].set_color('none')
    plt.gca().xaxis.set_ticks_position('bottom')
    plt.gca().yaxis.set_ticks_position('left')
    plt.show()

def fff(mm, tt):
    def fff_helper(xx):
        return np.dot(mm, xx) + tt
    return fff_helper

a = math.cos(math.pi / 3)
b = math.sin(math.pi / 3)
c = -math.sin(math.pi / 3)
d = math.cos(math.pi / 3)
e1 = 0.5
e2 = 0.5
f1 = -0.5
f2 = -0.5

aa = fff(np.array([[a, b], [c, d]]), np.array([0, 0]))
bb = fff(np.array([[a, b], [c, d]]), np.array([e1, e2]))
cc = fff(np.array([[a, b], [c, d]]), np.array([f1, f2]))
ee = fff(np.array([[1, 0], [0, 1]]), np.array([0, 0]))

lsf1 = [aa, bb, cc, ee]

result = nest_step([[0.4, 0.2]], lsf1, 18)
gpoint(result())
