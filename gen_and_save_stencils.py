import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import itertools
from misc_utils import IntToColors
from shapes import Rhombus, Square, Triangle, Circle, color_key
from stacking_utils import StackStencils, StackTwoShapes, GetStencil
#====================================================================
save_path = '/Users/joshuamiller/Documents/Python Files/Stencil_IQ_Test/Stencils'
#====================================================================
''' Grid size '''
xmin = -20
xmax = 20
ymin = -20
ymax = 20
#====================================================================
''' Choose stencils to make '''
SHAPES = ['Circle', 'Square', 'Rhombus', 'Triangle']
COLORS = [1, 2, 3]
depth = 3 # Worked with 2
#-------------------------------------------------------------------
if (depth == 2):
    COLORS = [1, 2]
#-------------------------------------------------------------------
shape_combs = list(itertools.permutations(SHAPES, depth))
print("shape_combs =", shape_combs[2])
#-------------------------------------------------------------------
sizes = np.ones((len(shape_combs), depth), int)

for i in range(np.shape(sizes)[0]):
    for j in range(depth):
        sizes[i][j] = int(np.random.randint(sizes[i][j-1 % depth], 19, 1))

print("sizes =", sizes[10])
#-------------------------------------------------------------------
for i in range(len(shape_combs)):
    layered, id = StackStencils(xmin, xmax, ymin, ymax, 
                                shape_combs[i],
                                sizes[i],
                                COLORS)
#====================================================================
fig, ax = plt.subplots(1,1, figsize=(6, 6))

#a, asd, asdw, sdfsdf = GetStencil(xmin, xmax, ymin, ymax, 'Circle', 2, 'hole', return_grid=True)

x_1, y_1, x_grid, y_grid, shape_colors_1 = Rhombus(xmin, xmax, ymin, ymax, 15, 2)
#x_2, y_2, x_grid, y_grid, shape_colors_2 = Square(xmin, xmax, ymin, ymax, 11, 1)
#x_3, y_3, x_grid, y_grid, shape_colors_3 = Triangle(xmin, xmax, ymin, ymax, 25, 3)
#layered = StackTwoShapes(shape_colors_1, shape_colors_2)
#ax.scatter(x=x_grid, 
#           y=y_grid, 
#           c=shape_colors_1)



'''
layered, id = StackStencils(xmin, xmax, ymin, ymax, 
                            ['Square', 'Rhombus', 'Square'],
                            [2, 17, 12],
                            ['blue', 'green', 'red'])
'''
ax.scatter(x=x_grid,
           y=y_grid,
           c=IntToColors(layered, color_key))
ax.set_title(id)
plt.show()