import numpy as np
import pandas as pd
import random
import os
import matplotlib.pyplot as plt
import tensorboard as tb
import tensorflow as tf
from tensorflow import keras
from sklearn.preprocessing import StandardScaler

from stacking_utils import StackStencils
from shapes import num_letter_dict
from data_utils import SplitIds, IdsToOnehot, SizeOnehotToInt, ShapeOnehotToChar, ColorOnehotToChar
#====================================================================
xmin = -20
xmax = 20
ymin = -20
ymax = 20
#====================================================================
data_dir = '/Users/joshuamiller/Documents/Python Files/Stencil_IQ_Test/Stencils/Depth2'

ids = os.listdir(data_dir)
random.shuffle(ids)
#====================================================================

n_epochs = 100
batch_size = 32
#====================================================================
''' Make training, validation and testing datasets '''
train_pct = .7
val_pct   = .1
test_pct  = 1 - train_pct - val_pct
#----------------------------- inputs -------------------------------
init = pd.read_csv(os.path.join(data_dir, ids[0]))
stencils = np.ones((len(ids), init.shape[0]))

for i in range(len(ids)):
    if (ids[i].endswith('.csv')):
        #print('i=', i, ', reading:', ids[i])
        stencils[i][:] = np.squeeze(pd.read_csv(os.path.join(data_dir, ids[i])).values)

# - - - - - - - - - - - Scale and center data - - - - - - - - - - - -
orig_shape = np.shape(stencils)

scaler = StandardScaler()
scaler.fit(stencils.ravel().reshape(-1, 1))
scaled_stencils = scaler.transform(stencils.ravel().reshape(-1, 1))

scaled_stencils = scaled_stencils.reshape(orig_shape)
del(stencils)
# - - - - - - - - - - Split to train, val, test - - - - - - - - - - -
stencils_train = scaled_stencils[:int(np.shape(stencils)[0] * train_pct), ...]
stencils_val   = scaled_stencils[int(np.shape(stencils)[0] * train_pct):int(np.shape(stencils)[0] * (train_pct+val_pct)), ...]
stencils_test  = scaled_stencils[int(np.shape(stencils)[0] * (train_pct + val_pct)):, ...]

del(scaled_stencils)
print(np.shape(stencils_train), np.shape(stencils_val), np.shape(stencils_test))
#----------------------------- targets ------------------------------
split_id_arr = SplitIds(ids)

shapes_oh, sizes_oh, colors_oh = IdsToOnehot(split_id_arr)

shapes_oh_train = shapes_oh[:int(np.shape(shapes_oh)[0] * train_pct), ...]
shapes_oh_val   = shapes_oh[int(np.shape(shapes_oh)[0] * train_pct):int(np.shape(shapes_oh)[0] * (train_pct+val_pct)), ...]
shapes_oh_test  = shapes_oh[int(np.shape(shapes_oh)[0] * (train_pct + val_pct)):, ...]

sizes_oh_train = sizes_oh[:int(np.shape(sizes_oh)[0] * train_pct), ...]
sizes_oh_val   = sizes_oh[int(np.shape(sizes_oh)[0] * train_pct):int(np.shape(sizes_oh)[0] * (train_pct+val_pct)), ...]
sizes_oh_test  = sizes_oh[int(np.shape(sizes_oh)[0] * (train_pct + val_pct)):, ...]

colors_oh_train = colors_oh[:int(np.shape(colors_oh)[0] * train_pct), ...]
colors_oh_val   = colors_oh[int(np.shape(colors_oh)[0] * train_pct):int(np.shape(colors_oh)[0] * (train_pct+val_pct)), ...]
colors_oh_test  = colors_oh[int(np.shape(colors_oh)[0] * (train_pct + val_pct)):, ...]

del(shapes_oh)
del(sizes_oh)
del(colors_oh)
print(np.shape(shapes_oh_train), np.shape(shapes_oh_val), np.shape(shapes_oh_test))
print(np.shape(sizes_oh_train), np.shape(sizes_oh_val), np.shape(sizes_oh_test))
print(np.shape(colors_oh_train), np.shape(colors_oh_val), np.shape(colors_oh_test))
#====================================================================
''' '''
model = keras.Model([inputs, input_lonlattime], y, name="Fire_LSTM_Trans_TimeLastDim_SumPix_v3")
keras.utils.plot_model(model, show_shapes=True, show_layer_activations=True)
#====================================================================
''' '''



#====================================================================
''' '''



#====================================================================
''' Train model '''
import time as clock
start_time = clock.time()

history = model.fit(x=[stencils_train],
                    y=[shapes_oh_train, sizes_oh_train, colors_oh_train],
                    validation_data=([stencils_train], [shapes_oh_val, sizes_oh_val, colors_oh_val]), 
                    batch_size=batch_size,
                    epochs=n_epochs,
                    # callbacks=[early_stopping_cb, onecycle], # Maybe not needed
                    verbose=1)

end_time = clock.time()

print('-------')
print('Training time: ', end_time - start_time, 'seconds.')
print('-------')
#====================================================================



#====================================================================