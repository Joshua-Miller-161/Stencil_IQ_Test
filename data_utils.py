import numpy as np

from shapes import num_letter_dict
#====================================================================
shape_int_dict = {'C': 0, 'T': 1, 'S': 2, 'R': 3}
#====================================================================
xmin = -20
xmax = 20
ymin = -20
ymax = 20
#====================================================================
def SplitIds(ids):
    depth = 1
    for letter in ids[0]:
        if (letter == '-'):
            depth += 1
    #----------------------------------------------------------------
    split_id_arr = np.empty((len(ids), 3 * depth), dtype=object)

    for i in range(len(ids)):
        split_id = ['' for n in range(3 * depth)]
        count = 0
        iter  = 0
        while (iter < 10):
            if (ids[i][iter] == '.'):
                break
            else:
                if not (ids[i][iter] == '-'):
                    if (ids[i][iter].isnumeric()):
                        #print(" - - ids[", i, "][", iter, "] =", ids[i][iter], ', count =', count)
                        if ((ids[i][iter+1]).isnumeric()):
                            #print(" - - - - ids[", i, "][", iter+1, "] =", ids[i][iter+1], ', count =', count)
                            split_id[count] += ids[i][iter] + ids[i][iter+1]
                            iter  += 1
                        else:
                            split_id[count] += ids[i][iter]
                    else:
                        #print("ids[", i, "][", iter, "] =", ids[i][iter], ', count =', count)
                        split_id[count] += ids[i][iter]
                    count += 1
                iter  += 1

        #print('i =', i, ', split =', split_id)
        split_id_arr[i][:] = split_id
    
    return split_id_arr
#====================================================================
def IdsToOnehot(split_id_arr):
    depth = int(np.shape(split_id_arr)[1] / 3)

    shapes_oh = np.zeros((np.shape(split_id_arr)[0], depth, 4), int)
    sizes_oh  = np.zeros((np.shape(split_id_arr)[0], depth, int(.5 * min([ymax-ymin, xmax-xmin]))), int)
    colors_oh = np.zeros((np.shape(split_id_arr)[0], depth, len(list(num_letter_dict.keys()))), int)

    for i in range(np.shape(split_id_arr)[0]):
        num_shapes = 0
        num_sizes = 0
        num_colors = 0

        for char in split_id_arr[i]:
            if char.isupper():
                shapes_oh[i][num_shapes][shape_int_dict[char]] = 1

                #print("Shape: got ", char, ", encoding: ", shapes_oh[i][num_shapes])
                num_shapes += 1

            elif char.isnumeric():
                sizes_oh[i][num_sizes][int(char)-1] = 1

                #print("Size: got ", char, ", encoding: ", sizes_oh[i][num_sizes])
                num_sizes += 1

            elif char.islower():
                colors_oh[i][num_colors][list(num_letter_dict.keys())[list(num_letter_dict.values()).index(char)]] = 1
                
                #print("Color: got ", char, ", encoding: ", colors_oh[i][num_colors])
                num_colors += 1
    
    return shapes_oh, sizes_oh, colors_oh
#====================================================================
def ShapeOnehotToChar(shape_oh):
    assert np.shape(shape_oh)[0] == len(list(shape_int_dict.keys())), "shape_oh must have shape (4,). Has {}".format(np.shape(shape_oh))
    
    idx = np.argmax(shape_oh)
    shape_char = list(shape_int_dict.keys())[list(shape_int_dict.values()).index(idx)]

    return shape_char
#===================================================================
def ColorOnehotToChar(color_oh):
    assert np.shape(color_oh)[0] == len(list(num_letter_dict.keys())), "color_oh must have shape (4,). Has {}".format(np.shape(color_oh))
    
    idx = np.argmax(color_oh)
    color_char = num_letter_dict[idx]

    return color_char
#====================================================================
def SizeOnehotToInt(size_oh):
    idx = np.argmax(size_oh)
    size_int = idx + 1
    return size_int