import os
import keras
import random
import numpy as np
from PIL import Image

import data.mnist as dataset

def model():
  model = keras.models.Sequential()
  model.add(keras.layers.Conv2D(32, 2, activation="relu", input_shape=(dataset.imageSize,dataset.imageSize,1)))
  model.add(keras.layers.MaxPooling2D(pool_size=(2,2)))
  model.add(keras.layers.Conv2D(64, 2, activation="relu"))
  model.add(keras.layers.MaxPooling2D(pool_size=(2,2)))
  model.add(keras.layers.Conv2D(128, 2, activation="relu"))
  model.add(keras.layers.MaxPooling2D(pool_size=(2,2)))
  #model.add(keras.layers.Conv2D(256, 2, activation="elu"))
  #model.add(keras.layers.MaxPooling2D(pool_size=(2,2)))
  model.add(keras.layers.Flatten())
  model.add(keras.layers.Dense(512, activation="relu"))
  model.add(keras.layers.Dropout(0.5))
  model.add(keras.layers.Dense(dataset.classes, activation="softmax"))
  model.compile("rmsprop", "categorical_crossentropy", metrics=[keras.metrics.categorical_accuracy])
  # keras.utils.plot_model(model, to_file='model.png')
  
  return model
 
def main():
  m = model()

  train_X, train_Y = dataset.getDataset(5000)
  m.fit(train_X, train_Y, validation_split = 0.2, epochs = 50)

  test_X, test_Y = dataset.getDataset(test = True)
  results = m.evaluate(test_X, test_Y, verbose = 1)
  print("Loss: " + repr(results[0]) + " Acc: " + repr(results[1]))

  """
  layer_dict = dict([(layer.name, layer) for layer in m.layers])

  layer_name = 'conv2d_2'
  filter_index = 0  # can be any integer from 0 to 511, as there are 512 filters in that layer

  # build a loss function that maximizes the activation
  # of the nth filter of the layer considered
  layer_output = layer_dict[layer_name].output
  loss = keras.backend.mean(layer_output[:, :, :, filter_index])

  # compute the gradient of the input picture wrt this loss
  grads = keras.backend.gradients(loss, input_img)[0]

  # normalization trick: we normalize the gradient
  grads /= (keras.backend.sqrt(keras.backend.mean(keras.backend.square(grads))) + 1e-5)

  # this function returns the loss and grads given the input picture
  iterate = keras.backend.function([input_img], [loss, grads])
  """

if __name__ == "__main__":
  main()
