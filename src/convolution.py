import numpy as np
from PIL import Image

class convolution:
    def __init__(self, image_data, size, overlap):
        ''' Initialise values '''
        y_size = len(list(range(0, len(image_data)-size+1, overlap)))
        x_size = len(list(range(0, len(image_data[0])-size+1, overlap)))
        total_squares =y_size*x_size
        self.filter = np.zeros((total_squares, size, size))
        if np.amax(image_data) > 1:
            image_data = image_data/255
        self.image_data = image_data
        self.size = size
        self.overlap = overlap

    def expand(self):
        image_number = 0
        for y in range(0, len(self.image_data)-self.size+1, self.overlap):
            for x in range(0, len(self.image_data[y])-self.size+1, self.overlap):
                snippit = np.array([i[x:x+self.size] for i in self.image_data[y:y+self.size]])
                self.filter[image_number] = snippit
                image_number +=1
        return self.filter

    def show_image(self):
        for image in self.filter:
            img = Image.fromarray(np.uint8(image*255), 'L')
            img.show()

