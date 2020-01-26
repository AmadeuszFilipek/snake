import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' # disable tensorflow debug info

import tensorflow as tf
from tensorflow.keras import layers, models
import matplotlib.pyplot as plt
import numpy as np

# input to Conv2D:
# 4D tensor with shape: (batch, rows, cols, channels) if data_format is "channels_last".
model = models.Sequential()
model.add(layers.Conv2D(
   8, (3, 3),
   activation='elu',
   input_shape=(20, 20, 1),
   data_format='channels_last'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(4, (3, 3), activation='elu'))
model.add(layers.Flatten())
model.add(layers.Dense(4, activation='elu'))
model.add(layers.Dense(3, activation='softmax'))

model.summary()
print("MODEL WEIGHTS")
weights = model.get_weights()
model.set_weights(weights)

def predict_next_move(grid):
   prepared_grid = prepare_grid(grid)
   result = model.predict(prepared_grid)
   return result[0].tolist()

def prepare_grid(grid):
   wrap_batches = np.array([grid]) # single batch
   return wrap_batches
