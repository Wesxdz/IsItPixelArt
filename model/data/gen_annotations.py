import numpy as np
import numpy.random
import os
from PIL import Image, ImageDraw, ImageFont
from torchvision.io import read_image


def prepass(dir):
    for subdir, dirs, files in os.walk(dir):
        for filename in files:
            filepath = subdir + os.sep + filename
            os.rename(filepath, subdir + os.sep + (filename.replace('File:', '')).replace(' ', '').replace(',', '').replace(';', ''))
            if filename.endswith('gif'):
                img = Image.open(filepath)
                img.save(subdir + os.sep + filename.split('.')[0]+".png", 'png', optimize=True, quality=70)

def add_classification_category(dir, category):
    data = []
    for subdir, dirs, files in os.walk(dir):
        for filename in files:
            filepath = subdir + os.sep + filename

            # assume all files are image data
            if filename.endswith('png') or filename.endswith('JPEG'):
                data.append([str(filepath).strip(), str(category)])
                # print(data[-1])
    return data

prepass('yes')
prepass('no')
pixel_art = np.asarray(add_classification_category('yes', 1))
not_pixel_art = np.asarray(add_classification_category('no', 0))
data = np.concatenate((pixel_art, not_pixel_art), axis=0)
np.random.shuffle(data)
test_size = int(len(data) * 0.2)
validation_size = int(len(data) * 0.1)
print(f"Train set {int(len(data) * 0.7)}")
print(f"Test set {test_size}")
print(f"Validate set {validation_size}")
validation_data = data[:validation_size]
test_data = data[validation_size:test_size]
train_data = data[validation_size+test_size:]
np.savetxt("train_annotations.csv", train_data, fmt="%s", delimiter=",")
np.savetxt("test_annotations.csv", test_data, fmt="%s", delimiter=",")
np.savetxt("validate_annotations.csv", validation_data, fmt="%s", delimiter=",")