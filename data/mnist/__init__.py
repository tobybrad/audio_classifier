import os
import random

import keras
import numpy as np
from PIL import Image

classes = 10
imageSize = 28

random.seed(1971)

TRAIN_ROOT = os.path.join(os.path.dirname(__file__), "training")
TEST_ROOT = os.path.join(os.path.dirname(__file__), "testing")

def relabel(l):
  if l == "rock":
    return 1
  return 0

def getImageData(dataset, dataRoot):
  imageData = [] 
  while len(dataset):
    i = dataset.pop()
    img = Image.open(os.path.join(dataRoot, i[0], i[1]))
    imageData.append(((np.asarray(img, dtype = np.uint32) / 255), i[0]))
  return imageData

def getDataset(numSamples = 1000, test = False):
  dataset = []
  dataRoot = TEST_ROOT if test else TRAIN_ROOT
  for root, dirs, files in os.walk(dataRoot):
    for f in files:
      dataset.append((os.path.basename(root), f))

  random.shuffle(dataset)
  x, y = zip(*getImageData(dataset[:numSamples], dataRoot))
  x = np.array(x).reshape([-1, imageSize, imageSize, 1])
  y = np.array(keras.utils.to_categorical(y, classes))
  return (x, y)