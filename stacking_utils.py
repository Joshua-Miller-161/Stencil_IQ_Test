import matplotlib.pyplot as plt
import numpy as np
from shapes import Rhombus, Square, Triangle, Circle, color_key
#====================================================================
def StackTwoShapes(shape_colors_1, shape_colors_2):
    # shape_colors_1 goes down first, shape_colors_2 is place over top
    assert np.shape(shape_colors_1) == np.shape(shape_colors_2), "'shape_colors_1' and 'shape_colors_2' must have same dimensions."
    
    layered = shape_colors_2

    for i in range(np.shape(layered)[0]):
        for j in range(np.shape(layered)[1]):
            #print(" - - - In StackTwoShapes, shape_colors_2[i][j] =", shape_colors_2[i][j])
            if (shape_colors_2[i][j] == -1): # -1 corresponds to hole
                layered[i][j] = shape_colors_1[i][j]

    return layered
#====================================================================
def GetStencil(xmin, xmax, ymin, ymax, shape_name, size, color):
    assert shape_name=='Circle' or shape_name=='Triangle' or shape_name=='Square' or shape_name=='Rhombus', "Shapes are: 'Circle', 'Triangle', 'Square', 'Rhombus'."
    #----------------------------------------------------------------
    x_out, y_out, x_grid, y_grid, identifier, shape_colors = 0, 0, 0, 0, '', 0 # Init da variables idk
    if shape_name=='Circle':
        x_out, y_out, x_grid, y_grid, shape_colors = Circle(xmin, xmax, ymin, ymax, size, color)
        identifier = 'C'+str(size)+color_key[color][0]+'-'
    
    elif shape_name=='Triangle':
        x_out, y_out, x_grid, y_grid, shape_colors = Triangle(xmin, xmax, ymin, ymax, size, color)
        identifier = 'T'+str(size)+color_key[color][0]+'-'
    
    elif shape_name=='Square':
        x_out, y_out, x_grid, y_grid, shape_colors = Square(xmin, xmax, ymin, ymax, size, color)
        identifier = 'S'+str(size)+color_key[color][0]+'-'
    
    elif shape_name=='Rhombus':
        x_out, y_out, x_grid, y_grid, shape_colors = Rhombus(xmin, xmax, ymin, ymax, size, color)
        identifier = 'R'+str(size)+color_key[color][0]+'-'
    
    return x_out, y_out, x_grid, y_grid, shape_colors, identifier
#====================================================================
def StackStencils(xmin, xmax, ymin, ymax, shape_names, sizes, colors, return_grid=False, return_outline=False):
    assert len(shape_names)==len(sizes) and len(sizes)==len(colors), "len(shape_names), len(sizes), len(colors) must be equal."
    #print(' - - - in StackStencils - shape =', shape_names)
    #print(' - - - in StackStencils - sizes =', sizes)
    #print(' - - - in StackStencils - color =', colors)
    
    #----------------------------------------------------------------
    layered_colors, stencil_id = np.ones((abs(xmax-xmin)+1, abs(ymax-ymin)+1, 3), float)*9999, '' # Init da variables idk
    
    for i in range(len(shape_names)-1):
        x_out_1, y_out_1, x_grid_1, y_grid_1, shape_colors_1, identifier_1 = GetStencil(xmin, xmax, ymin, ymax, shape_names[i], sizes[i], colors[i])
        print(shape_names[i+1])
        x_out_2, y_out_2, x_grid_2, y_grid_2, shape_colors_2, identifier_2 = GetStencil(xmin, xmax, ymin, ymax, shape_names[i+1], sizes[i+1], colors[i+1])

        if (i == 0):
            layered_colors = StackTwoShapes(shape_colors_1, shape_colors_2)
            if (len(shape_names)<=2):
                stencil_id = identifier_1 + identifier_2
                break
        else:
            layered_colors = StackTwoShapes(layered_colors, shape_colors_2)

    if return_grid:
        if return_outline:
            return x_out_1, y_out_1, x_grid_1, y_grid_1, layered_colors, stencil_id[:-1]
        return x_grid_1, y_grid_1, layered_colors, stencil_id[:-1]
    else:
        return layered_colors, stencil_id[:-1]
#====================================================================