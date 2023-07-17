import tensorflow as tf
from tensorflow import keras

from keras.layers import Dense, Flatten, Reshape, Concatenate, Lambda, Input

def BuildDense(input_shape, depth):
    input_layer = Input(input_shape, name='Input')

    x = 

    model = keras.Model(input_layer, y, name="DENSE")
    keras.utils.plot_model(model, show_shapes=True, show_layer_activations=True)

    keras.Model(input_layer, [outputs] * depth * 3)
    return 0