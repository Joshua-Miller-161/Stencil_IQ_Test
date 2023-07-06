import matplotlib.pyplot as plt
import numpy as np
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

fig, ax = plt.subplots(1,1, figsize=(6,6))

#a, asd, asdw, sdfsdf = GetStencil(xmin, xmax, ymin, ymax, 'Circle', 2, 'hole', return_grid=True)

x_1, y_1, x_grid, y_grid, shape_colors_1 = Rhombus(xmin, xmax, ymin, ymax, 15, 'blue')
#x_2, y_2, x_grid, y_grid, shape_colors_2 = Square(xmin, xmax, ymin, ymax, 11, 'green')
#x_3, y_3, x_grid, y_grid, shape_colors_3 = Triangle(xmin, xmax, ymin, ymax, 25, 'red')
#layered = StackTwoShapes(shape_colors_1, shape_colors_2)
#ax.scatter(x=x_grid, 
#           y=y_grid, 
#           c=shape_colors_1)




layered, id = StackStencils(xmin, xmax, ymin, ymax, 
                            ['Square', 'Rhombus', 'Square'],
                            [2, 17, 12],
                            ['blue', 'green', 'red'])

ax.scatter(x=x_grid,
           y=y_grid,
           c=layered)
ax.set_title(id)
plt.show()