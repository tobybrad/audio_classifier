import os
import sys
import eyed3
import subprocess
from shutil import copyfile
from multiprocessing import Pool, Queue

eyed3.log.setLevel("ERROR")

def toMono(audiofile):
  label = audiofile.tag.comments.get("label")
  if not label:
    print("Skipping " + audiofile.path)
    return None

  monoPath = "/tmp/mono-" + label.text + "-" + os.path.basename(audiofile.path)
  if audiofile.info.mode == 'Mono':
    copyfile(audiofile.path, monoPath) 
  else:
    cmd = ['sox', audiofile.path, monoPath, 'remix', "1,2"]
    p = subprocess.call(cmd)
  return monoPath


def toSpectrogram(monoPath):
  pixelsPerSec = "50"
  spectPath = os.path.join("./data/labelled", os.path.basename(monoPath).replace("mp3", "png"))
  cmd = [
    "sox", monoPath, "-n", "spectrogram", "-Y", "200", "-X", pixelsPerSec, 
    "-m", "-r", "-o", spectPath
  ] 
  p = subprocess.call(cmd)
  return spectPath


def process(q):
  filePath = q.get(True)
  while filePath:
    audiofile = eyed3.load(filePath)
    if audiofile:
      monoPath = toMono(audiofile)
      if monoPath:
        spectPath = toSpectrogram(monoPath)
        os.remove(monoPath)
        print("Completed " + spectPath)
    filePath = q.get(True)
  q.put(None)

def main():
  audiofiles = Queue()
  pool = Pool(8, process, (audiofiles,))
  for root, dirs, files in os.walk("/mnt/c/Users/tobybrad/Music/_genres"):
    for f in files:
      filePath = os.path.join(root, f)
      audiofiles.put(filePath)
  audiofiles.put(None)
  pool.close()
  pool.join()

if __name__ == "__main__":
  main()
