from PIL import Image
import numpy
import sys
sys.path.append("..")
from src.convolution import convolution
img = Image.open('/Users/connor.isaiaswhite/Documents/colour.jpeg')
img = img.convert('L')
beep = numpy.array(img)
cool = convolution(beep, 50,25)
cool.expand()
print(cool.filter.shape)
