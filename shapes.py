import matplotlib.pyplot as plt
import matplotlib.path as mpltPath
import numpy as np
from misc_utils import Rotate, SortOutline
#====================================================================
''' Grid size '''
'''
xmin = -20
xmax = 20
ymin = -20
ymax = 20
'''
#====================================================================
''' Int '''
num_letter_dict = {0: 'b', # For the hole
                   1: 'f',
                   2: 'a',
                   3: 'c'}

letter_full_dict = {'b': 'black', # For the hole
                    'f': 'fuchsia',
                    'a': 'aquamarine',
                    'c': 'cornflowerblue'}
#====================================================================
''' Mask '''
def MakeShapeMask(xmin, xmax, ymin, ymax, outline):
    sorted_outline = SortOutline(outline)
    #print("-------------------------------------")
    #print("sorted outline =", sorted_outline)

    path = mpltPath.Path(sorted_outline)
    #print("path =", path)
    x_grid, y_grid = np.meshgrid(np.arange(xmin, xmax+1), np.arange(ymin,ymax+1))

    grid_points = [list(point) for point in zip(x_grid.ravel(), y_grid.ravel())]

    mask = np.reshape(path.contains_points(grid_points, radius=-.5), (int(xmax-xmin+1), int(xmax-xmin+1)))
    #print("-------------------------------------")
    #print("mask =", mask)
    return mask
#====================================================================
def Colorize(xmin, xmax, ymin, ymax, mask, color):
    assert color in num_letter_dict, "You put {}. Valid colors: {} corresponding to: {}".format(color, num_letter_dict.keys, letter_full_dict.values)
    # - - - - Give color to the shape. white: background, color: in shape - - - -
    colors = np.zeros((abs(xmax-xmin)+1, abs(ymax-ymin)+1), int)

    for i in range(np.shape(colors)[0]):
        for j in range(np.shape(colors)[1]):
            if mask[i][j]: # In shape
                colors[i][j] = 0 # -1 corresponds to the hole
            else: # Outside shape
                colors[i][j] = color
    
    # - - - - - - - - - Make a grid on which to plot the colors - - - - - - - - -
    x_grid, y_grid = np.meshgrid(np.arange(xmin, xmax+1), np.arange(ymin,ymax+1))
    #print('x_grid: ', np.shape(x_grid), ', y_grid: ', np.shape(y_grid), ', colors: ', np.shape(colors))
    return x_grid, y_grid, colors
#====================================================================
''' Triangle '''
def Triangle(xmin, xmax, ymin, ymax, size, color):
    #print(" - - - In Triangle - size: ", size, type(size), ', color: ', color, type(color))
    assert type(size) == np.int64 or type(size) == np.int32 or type(size) == int, "'size' must be type int"
    assert 0 < size and size <= min([.5 * (xmax-xmin), .5 * (ymax-ymin)]), "'size must be greater than 0 and less than {bound:.1f}".format(bound=min([.5 * (xmax-xmin), .5 * (ymax-ymin)]))
    
    # - - - - - - - - - Make the outline of the shape - - - - - - - - -
    vert0 = np.array([.5*(xmax+xmin), .5*(xmax+xmin)+size])
    vert1 = Rotate(vert0, 135)
    vert2 = Rotate(vert0, 225)

    #print("VERTS =", vert0, vert1, vert2)

    x0 = np.linspace(vert0[0], vert1[0], 100)
    y0 = np.linspace(vert0[1], vert1[1], 100)

    x1 = np.linspace(vert1[0], vert2[0], 100)
    y1 = np.linspace(vert1[1], vert2[1], 100)

    x2 = np.linspace(vert2[0], vert0[0], 100)
    y2 = np.linspace(vert2[1], vert0[1], 100)

    outline = np.asarray(list(zip(np.concatenate([x0,x1,x2]),
                                  np.concatenate([y0,y1,y2]))))
    
    #print("Triangle outline =", outline)

    # - - Make mask of which points lie inside the shape 1: inside, 0: outside - -
    # - - - - - - - - - - - Only works for convex polygons atm - - - - - - - - - -
    mask = MakeShapeMask(xmin, xmax, ymin, ymax, outline)

    # - - - - Give color to the shape. white: background, color: in shape - - - -
    x_grid, y_grid, colors = Colorize(xmin, xmax, ymin, ymax, mask, color)

    return outline[:, 0], outline[:, 1], x_grid, y_grid, colors
#====================================================================
''' Square '''
def Square(xmin, xmax, ymin, ymax, size, color):
    #print(" - - - In Square - size: ", size, type(size), ', color: ', color, type(color))
    assert type(size) == np.int64 or type(size) == np.int32 or type(size) == int, "'size' must be type int"
    assert 0 < size and size <= min([.5 * (xmax-xmin), .5 * (ymax-ymin)]), "'size must be greater than 0 and less than {bound:.1f}".format(bound=min([.5 * (xmax-xmin), .5 * (ymax-ymin)]))
    
    # - - - - - - - - - Make the outline of the shape - - - - - - - - -
    vert0 = np.array([size, size])
    vert1 = Rotate(vert0, 90)
    vert2 = Rotate(vert0, 180)
    vert3 = Rotate(vert0, 270)

    #print("VERTS =", vert0, vert1, vert2, vert3)

    x0 = np.linspace(vert0[0], vert1[0], 100)
    y0 = np.linspace(vert0[1], vert1[1], 100)

    x1 = np.linspace(vert1[0], vert2[0], 100)
    y1 = np.linspace(vert1[1], vert2[1], 100)

    x2 = np.linspace(vert2[0], vert3[0], 100)
    y2 = np.linspace(vert2[1], vert3[1], 100)

    x3 = np.linspace(vert3[0], vert0[0], 100)
    y3 = np.linspace(vert3[1], vert0[1], 100)


    outline = np.asarray(list(zip(np.concatenate([x0,x1,x2,x3]),
                                  np.concatenate([y0,y1,y2,y3]))))
    
    #print("Square outline =", outline)

    # - - Make mask of which points lie inside the shape 1: inside, 0: outside - -
    # - - - - - - - - - - - Only works for convex polygons atm - - - - - - - - - -
    mask = MakeShapeMask(xmin, xmax, ymin, ymax, outline)

    # - - - - Give color to the shape. white: background, color: in shape - - - -
    x_grid, y_grid, colors = Colorize(xmin, xmax, ymin, ymax, mask, color)

    return outline[:, 0], outline[:, 1], x_grid, y_grid, colors
#====================================================================
''' Rhombus '''
def Rhombus(xmin, xmax, ymin, ymax, size, color):
    #print(" - - - In Rhombus - size: ", size, type(size), ', color: ', color, type(color))

    assert type(size) == np.int64 or type(size) == np.int32 or type(size) == int, "'size' must be type int"
    assert 0 < size and size <= min([.5 * (xmax-xmin), .5 * (ymax-ymin)]), "'size must be greater than 0 and less than {bound:.1f}".format(bound=min([.5 * (xmax-xmin), .5 * (ymax-ymin)]))
    
    # - - - - - - - - - Make the outline of the shape - - - - - - - - -
    vert0 = np.array([size, 0])
    vert1 = Rotate(vert0, 90)
    vert2 = Rotate(vert0, 180)
    vert3 = Rotate(vert0, 270)

    #print("VERTS =", vert0, vert1, vert2, vert3)

    x0 = np.linspace(vert0[0], vert1[0], 100)
    y0 = np.linspace(vert0[1], vert1[1], 100)

    x1 = np.linspace(vert1[0], vert2[0], 100)
    y1 = np.linspace(vert1[1], vert2[1], 100)

    x2 = np.linspace(vert2[0], vert3[0], 100)
    y2 = np.linspace(vert2[1], vert3[1], 100)

    x3 = np.linspace(vert3[0], vert0[0], 100)
    y3 = np.linspace(vert3[1], vert0[1], 100)


    outline = np.asarray(list(zip(np.concatenate([x0,x1,x2,x3]),
                                  np.concatenate([y0,y1,y2,y3]))))
    
    #print("Rhombus outline =", outline)

    # - - Make mask of which points lie inside the shape 1: inside, 0: outside - -
    # - - - - - - - - - - - Only works for convex polygons atm - - - - - - - - - -
    mask = MakeShapeMask(xmin, xmax, ymin, ymax, outline)

    # - - - - Give color to the shape. white: background, color: in shape - - - -
    x_grid, y_grid, colors = Colorize(xmin, xmax, ymin, ymax, mask, color)

    return outline[:, 0], outline[:, 1], x_grid, y_grid, colors
#====================================================================
''' Circle '''
def Circle(xmin, xmax, ymin, ymax, radius, color):
    #print(" - - - In Circle - radius: ", radius, type(radius), ', color: ', color, type(color))
    assert type(radius) == np.int64 or type(radius) == np.int32 or type(radius) == int, "'radius' must be type int"
    assert 0 < radius and radius <= min([.5 * (xmax-xmin), .5 * (ymax-ymin)]), "'radius must be greater than 0 and less than {bound:.1f}".format(bound=min([.5 * (xmax-xmin), .5 * (ymax-ymin)]))
    
    # - - - - - - - - - Make the outline of the shape - - - - - - - - -
    center = [.5 * (xmax+xmin), .5 * (ymax+ymin)]

    x = np.linspace(int(center[0] - radius), int(center[0] + radius)+1, 100)

    y = np.sqrt(radius**2 - x**2)

    outline = []
    for i in range(len(x)):
        for j in range(2):
            if j == 0:
                if not (y[i] == -0):
                    outline.append([x[i], y[i]])
            else:
                outline.append([x[i], -y[i]])

    # - - Make mask of which points lie inside the shape 1: inside, 0: outside - -
    # - - - - - - - - - - - Only works for convex polygons atm - - - - - - - - - -
    mask = MakeShapeMask(xmin, xmax, ymin, ymax, outline)

    # - - - - Give color to the shape. white: background, color: in shape - - - -
    x_grid, y_grid, colors = Colorize(xmin, xmax, ymin, ymax, mask, color)

    return x, y, x_grid, y_grid, colors
#====================================================================