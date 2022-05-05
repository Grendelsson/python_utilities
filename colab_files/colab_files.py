from google.colab import files
import os

def read_file(filePath="filepath"):
  if os.path.isfile(filePath) == False:
    uploaded = files.upload();
