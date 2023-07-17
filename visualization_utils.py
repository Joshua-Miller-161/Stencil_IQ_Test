import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from shapes import num_letter_dict, letter_full_dict
from stacking_utils import StackStencils
from misc_utils import IntToColors

def IdToColorArr(xmin, xmax, ymin, ymax, id, return_grid=False):
    x_grid, y_grid = np.meshgrid(np.arange(xmin, xmax+1), np.arange(ymin, ymax+1))
    #----------------------------------------------------------------
    depth       = 0
    colors      = []
    shape_names = []
    sizes       = []

    for letter in id:
        if letter.islower():
            colors.append(letter)
        elif letter.isupper():
            shape_names.append(letter)
            depth += 1

    if not (depth == len(colors) and depth == len(shape_names)):
        print("AHHHHHHHHHHH depth =", depth, ', len(colors) =', len(colors), ', len(shape_names) =', len(shape_names))

    for i in range(len(colors)):
        for color_char in list(num_letter_dict.values()):
            if (colors[i] == color_char):
                colors[i] = list(num_letter_dict.keys())[list(num_letter_dict.values()).index(color_char)]
    print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    print('colors =', colors)

    SHAPES = ['Circle', 'Triangle', 'Square', 'Rhombus']
    for j in range(len(shape_names)):
        for shape_name in SHAPES:
            if (shape_names[j] == shape_name[0]):
                shape_names[j] = shape_name
    print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    print('shape_names =', shape_names)

    for i in range(len(id)-1):
        if id[i].isnumeric():
            if (id[i+1]).isnumeric():
                sizes.append(int(id[i] + id[i+1]))
                break
            sizes.append(int(id[i]))
    print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    print('sizes =', sizes)
    #----------------------------------------------------------------
    layered, id_ = StackStencils(xmin, xmax, ymin, ymax,
                                shape_names,
                                sizes,
                                colors)
    if return_grid:
        return x_grid, y_grid, layered, id_
    else:
        return layered, id_
#====================================================================

x_grid, y_grid, layered, id = IdToColorArr(-20, 20, -20, 20, 'S5c-S11a', return_grid=True)
print('- - - - - - - - - - - - - - -')
print('layered =', np.shape(layered))
print('- - - - - - - - - - - - - - -')
print('id =', id)
#====================================================================
fig, ax = plt.subplots(1,1, figsize=(6, 6))

ax.scatter(x=x_grid,
           y=y_grid,
           c=IntToColors(layered, letter_full_dict, num_letter_dict))
ax.set_title(id)
plt.show()