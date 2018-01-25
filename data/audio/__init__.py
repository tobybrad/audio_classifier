import os
import random
import numpy as np
from PIL import Image

classes = 10
imageSize = 128

random.seed(1971)

DATA_ROOT = os.path.join(os.path.dirname(__file__), "data")

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