import os
from PIL import Image

sliceWidth = 128

def _slice(filePath):
  img = Image.open(filePath)
  w, h = img.size
  slices = int(w / sliceWidth)
  for i in range(slices):
    n = i * sliceWidth	
    crop = img.crop((n, 1, n + sliceWidth, sliceWidth + 1))
    crop.save("./data/slices/" + str(i) + "-" + os.path.basename(filePath))
  print(filePath + " (" + str(i) + " slices)")

def main():
  for root, dirs, files in os.walk("./data/labelled"):
    for f in files:
      filePath = os.path.join(root, f)
      _slice(filePath)

if __name__ == "__main__":
  main()
 
