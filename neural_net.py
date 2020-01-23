# get snake grid as input

# get direction as output

import tensorflow as tf
from tensorflow.keras import layers, models
import matplotlib.pyplot as plt

model = models.Sequential()
model.add(layers.Conv2D(16, (3, 3), activation='elu', input_shape=(20, 20, 1)))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(8, (3, 3), activation='elu'))
model.add(layers.Flatten())
model.add(layers.Dense(8, activation='elu'))
model.add(layers.Dense(4, activation='softmax'))


