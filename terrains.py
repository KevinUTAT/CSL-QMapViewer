import math
import numpy as np
from PIL import Image as im

MAX_16UINT = 65535

class Terrains(object):

    def __init__(self, ter_str, sea_level):
        self.sea_level = sea_level
        ter_points_strs = ter_str.split(',')
        ter_size = int(math.sqrt(len(ter_points_strs)))
        print("Loading terrain data:", ter_size, "x", ter_size, "points")
        self.ter_points = []
        self.max_height = 0
        self.max_depth = 0
        for ter_points_str in ter_points_strs:
            ptr_str_pair = ter_points_str.split(':')
            cur_height = int(ptr_str_pair[0])
            cur_depth = int(ptr_str_pair[1])
            self.ter_points.append([cur_height, cur_depth])
            # find max 
            if (cur_height > self.max_height):
                self.max_height = cur_height
            if (cur_depth > self.max_depth):
                self.max_depth = cur_depth

        # self.generate_test_images() 
        self.get_terrain_img()

    # generate two PNG images
    def generate_test_images(self):
        img_size = int(math.sqrt(len(self.ter_points)))
        # height image
        img_array = np.arange(0, img_size * img_size, 1, np.uint8).reshape(img_size, img_size)
        for r in range(img_size):
            for c in range(img_size):
                h = self.ter_points[r * img_size + c][0]
                colour = np.uint8(256 * (h / self.max_height))
                img_array[img_size - r - 1][c] = colour     # flip the image "up-side-down"
        print(img_array.shape)
        img_data = im.fromarray(img_array)
        img_data.save('testmap_h.png')
        # depth image
        img_array = np.arange(0, img_size * img_size, 1, np.uint8).reshape(img_size, img_size)
        for r in range(img_size):
            for c in range(img_size):
                d = self.ter_points[r * img_size + c][1]
                colour = np.uint8(256 * (d / self.max_depth))
                img_array[img_size - r - 1][c] = colour
        print(img_array.shape)
        img_data = im.fromarray(img_array)
        img_data.save('testmap_d.png')

    # get a PIL Image in RGB
    def get_terrain_img(self):
        img_size = int(math.sqrt(len(self.ter_points)))
        # prepare a 3d array of 8bit (w * h * rgb)
        img_array = np.arange(0, img_size * img_size * 3, 1, np.uint8).reshape(img_size, img_size, 3)

        for row in range(img_size):
            for col in range(img_size):
                h = self.ter_points[row * img_size + col][0]
                d = self.ter_points[row * img_size + col][1]
                r, g, b = self.height_depth_2_RGB(h, d)
                img_array[img_size - row - 1][col][0] = r
                img_array[img_size - row - 1][col][1] = g
                img_array[img_size - row - 1][col][2] = b

        img_data = im.fromarray(img_array, mode="RGB")
        img_data.save('test.png')
        return img_data
 
    # convert the height/depth of a point to colour
    def height_depth_2_RGB(self, h_origin, d_origin):
        # deep water
        if (h_origin < self.sea_level):
            r = 170
            g = 221
            b = 255
        # shallow water
        elif (d_origin > self.sea_level):
            r = 170
            g = 221
            b = 223
        # land
        else:
            b = 0
            h = 382 - int(382 * (h_origin / MAX_16UINT))
            if (h > 64):
                increase = int(math.floor((382 - h) / 64))
                odd = (382 - h) % 64
                r = 159 - increase * 32
                g = 223 - increase * 32 - odd
            else:
                r = 0
                g = h
        
        return np.uint8(r), np.uint8(g), np.uint8(b)