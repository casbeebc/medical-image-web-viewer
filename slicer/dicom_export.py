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
    currentK = 0
    maxNum = sys.maxsize*-1
    maxNums = []
    
    for k, i, j in product(range(voxels.shape[2]), range(voxels.shape[0]), range(voxels.shape[1])):
        if currentK != k:
            maxNums.append(maxNum)
            maxNum = sys.maxsize*-1
            currentK = k
            
        if voxels[i,j,k] > maxNum:
            maxNum = voxels[i,j,k]
            
    maxNums.append(maxNum)
        
    for k, i, j in product(range(voxels.shape[2]), range(voxels.shape[0]), range(voxels.shape[1])):
        
        # initialize every time k changes
        if currentK != k:
            _save_image("{}/{}.png".format(path, currentK), img)
            img = Image.new("L", imageShape)
            pixels = img.load()
            currentK = k
            
        # Rescaling grey scale between 0-255
        pixels[i,j] = int((float(voxels[i,j,k]) / float(maxNums[k])) * 255.0)
        
    _save_image("{}/{}.png".format(path, k), img)


def _save_image(filepath, image):
    try:
        image.save(filepath, "PNG")
    except (KeyError, IOError):
        msg = 'Cannot create images for file: {}'
        logger.info(msg.format(filepath))
        