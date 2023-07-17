import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import itertools
import os

from misc_utils import IntToColors
from shapes import Rhombus, Square, Triangle, Circle, num_letter_dict, letter_full_dict
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
depth  = 2 # Worked with 2

num_perm_multiples = 2  # How many times all of the permutations of
                        # shapes will be made. Ensures equal exposure
                        # to all combinations of shapes.
#-------------------------------------------------------------------
shape_combs = list(itertools.product(SHAPES, repeat=depth))
print("shapes =", np.shape(shape_combs), shape_combs[:5])
#-------------------------------------------------------------------
size_combs = np.ones((num_perm_multiples * len(shape_combs), depth), int)

for i in range(np.shape(size_combs)[0]):
    for j in range(depth):
        size_combs[i][j] = int(np.random.randint(size_combs[i][j-1 % depth], 19, 1))

print("sizes =", np.shape(size_combs), size_combs[:5])
#-------------------------------------------------------------------
color_combs = np.random.choice(COLORS, (num_perm_multiples * len(shape_combs), depth))
print("colors =", np.shape(color_combs), color_combs[:5])
#-------------------------------------------------------------------
for i in range(num_perm_multiples):
    for j in range(len(shape_combs)):
        layered, id = StackStencils(xmin, xmax, ymin, ymax, 
                                    shape_combs[j],
                                    size_combs[i * len(shape_combs) + j],
                                    color_combs[i * len(shape_combs) + j])
        layered_flat = layered.flatten()
        del(layered)    
        df = pd.DataFrame(layered_flat, columns=['color_code'])

        if (depth == 2):
            df.to_csv(os.path.join(os.path.join(save_path, 'Depth2'), id+'.csv'), index=False)
        elif (depth == 3):
            df.to_csv(os.path.join(os.path.join(save_path, 'Depth3'), id+'.csv'), index=False)
        elif (depth == 4):
            df.to_csv(os.path.join(os.path.join(save_path, 'Depth4'), id+'.csv'), index=False)

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
           c=IntToColors(layered_flat, letter_full_dict, num_letter_dict))
ax.set_title(id)
plt.show()