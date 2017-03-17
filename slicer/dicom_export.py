import logging
from itertools import product
import numpy as np
import sys
from PIL import Image

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def export_to_png(path, voxels):
    
    imageShape = (voxels.shape[0], voxels.shape[1])
    img = Image.new("I", imageShape)
    pixels = img.load()
    
    interestingKValues = []
    current_k = 0
    
    max_values = _get_maximum_values(voxels)
    
    for k, i, j in product(range(voxels.shape[2]), range(voxels.shape[0]), range(voxels.shape[1])):
        
        # initialize every time k changes
        if current_k != k:
            _save_image("{}/{}.png".format(path, current_k), img)
            img = Image.new("L", imageShape)
            pixels = img.load()
            current_k = k
            
        # Rescaling grey scale between 0-255
        pixels[i,j] = int((float(voxels[i,j,k]) / float(max_values[k])) * 255.0)
        
    _save_image("{}/{}.png".format(path, k), img)

def _get_maximum_values(voxels):
    max_values = []
    max_value = sys.maxsize*-1
    current_k = 0
    
    for k, i, j in product(range(voxels.shape[2]), range(voxels.shape[0]), range(voxels.shape[1])):
        if current_k != k:
            max_values.append(max_value)
            max_value = sys.maxsize*-1
            current_k = k
            
        if voxels[i,j,k] > max_value:
            max_value = voxels[i,j,k]
            
    max_values.append(max_value)
    
    return max_values

def _save_image(filepath, image):
    try:
        image.save(filepath, "PNG")
    except (KeyError, IOError):
        msg = 'Cannot create images for file: {}'
        logger.info(msg.format(filepath))
        