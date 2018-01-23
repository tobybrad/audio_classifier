import os
import keras
import random
import numpy as np
from PIL import Image

DATA_ROOT = "./data/slices"

def model():
  model = keras.models.Sequential()
  model.add(keras.layers.Conv2D(64, 2, activation="relu", input_shape=(128,128,1)))
  model.add(keras.layers.MaxPooling2D(pool_size=(2,2)))
  model.add(keras.layers.Conv2D(128, 2, activation="relu"))
  model.add(keras.layers.MaxPooling2D(pool_size=(2,2)))
  #model.add(keras.layers.Conv2D(256, 2, activation="relu"))
  #model.add(keras.layers.MaxPooling2D(pool_size=(2,2)))
  #model.add(keras.layers.Conv2D(512, 2, activation="relu"))
  #model.add(keras.layers.MaxPooling2D(pool_size=(2,2)))
  model.add(keras.layers.Flatten())
  model.add(keras.layers.Dense(1024, activation="relu"))
  model.add(keras.layers.Dropout(0.5))
  model.add(keras.layers.Dense(2, activation="softmax"))
  m.compile("rmsprop", "categorical_crossentropy")
  return model
 
def relabel(l):
  if l == "rock":
    return 1
  return 0

def getImageData(dataset):
  imageData = [] 
  while len(dataset):
    i = dataset.pop()
    img = Image.open(os.path.join(DATA_ROOT, i[1]))
    imageData.append(((np.asarray(img, dtype = np.uint8) / 255), i[0]))
  return imageData

def getDataset(numSamples = 1000):
  random.seed(1971)
  slices = os.listdir(DATA_ROOT)
  labels = map(lambda x: relabel(x.split("-")[2]), slices)
  dataset = zip(labels, slices)
  classes = {}
  for d in dataset:
    if d[0] not in classes:
      classes[d[0]] = []
    classes[d[0]].append(d)
  dataset = []
  for l in classes:
    dataset += random.sample(classes[l], numSamples)
  random.shuffle(dataset)
  return getImageData(dataset)

def main():
  d = getDataset()
  (train_X, train_Y) = zip(*d)
  train_X = np.array(train_X).reshape([-1, 128, 128, 1])
  train_Y = keras.utils.to_categorical(train_Y, 2)
  train_Y = np.array(train_Y)
  model().fit(train_X, train_Y, validation_split=0.2, epochs=20)

if __name__ == "__main__":
  main()