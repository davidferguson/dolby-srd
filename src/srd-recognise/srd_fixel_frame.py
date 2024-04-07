import cv2 as cv
import numpy as np
import imutils

from utils import template_match_resize, adaptive_threshold, warp_to_rect
from known_patterns import KNOWN_PATTERNS

CORNER_INNER = 'patterns/corner_7x7_100.png'
CORNER = 'patterns/corner_126x126_linear.png'

REDUCTION_AMOUNT = 0.3 # how much of a fixel (from the center) to look at in order to determine its value
CORNER_REDUCTION_PIXELS = 3 # how many pixels to trim round the side of the image once its found corners
THRESHOLD_VALUE = 127 # at what value (from 0 to 255) we should consider a pixel to be black

# The following values should be constant for SR•D on film
BLACK_FIXEL_VALUE = False # whether a black fixel is a True or False
RESOLUTION = 76 # how many pixels there are in the x and y direction
BYTE_WIDTH = 2
BYTE_HEIGHT = 4


class SRDFixelFrame():
    def __init__(self, img):
        self.original_img = img
        self.colour_img = img.copy()
        self.grey_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        self.img_height, self.img_width = self.grey_img.shape
        self.corner_scale = 1.0
        self.thresholded = None
        self.reframed = None
    
    def detect_corner_scale(self):
        template = cv.imread(CORNER, 0)
        found = template_match_resize(self.grey_img, template, cv.TM_CCOEFF, 0.7, 1.3, 20)
        if found:
            _, scale = found
            self.corner_scale = scale
    
    def find_corners(self):
        template = cv.imread(CORNER, 0)
        template = imutils.resize(template, width = round(template.shape[1] * self.corner_scale))
        mid_x = round(self.img_width / 2)
        mid_y = round(self.img_height / 2)
        top_left_img = self.grey_img[0:mid_y, 0:mid_x]
        top_right_img = self.grey_img[0:mid_y, mid_x:self.img_width]
        bottom_left_img = self.grey_img[mid_y:self.img_height, 0:mid_x]
        bottom_right_img = self.grey_img[mid_y:self.img_height, mid_x:self.img_width]
        self.top_left_corner = self.__find_corner(template, top_left_img, (0, 0))
        self.top_right_corner = self.__find_corner(template, top_right_img, (mid_x, 0))
        self.bottom_left_corner = self.__find_corner(template, bottom_left_img, (0, mid_y))
        self.bottom_right_corner = self.__find_corner(template, bottom_right_img, (mid_x, mid_y))
    
    def __find_corner(self, template, img, offset):
        template_height, template_width = template.shape
        match = cv.matchTemplate(img, template, cv.TM_CCOEFF_NORMED)
        _, _, _, max_location = cv.minMaxLoc(match)
        corner_location = [max_location[0] + offset[0], max_location[1] + offset[1]]
        corner_location = self.__precise_corner(corner_location, template_width, template_height, offset)
        return corner_location
    
    def draw_grid(self):
        assert self.reframed is not None
        fixel_size = float(self.image_size) / RESOLUTION
        for fixel_pos in range(0, RESOLUTION + 1):
            pos = round(fixel_pos * fixel_size)
            cv.line(self.colour_img, (pos, 0), (pos, self.image_size), (255, 100, 100), 1)
            cv.line(self.colour_img, (0, pos), (self.image_size, pos), (255, 100, 100), 1)
    
    def __precise_corner(self, corner_location, template_width, template_height, offset):
        inner_template = cv.imread(CORNER_INNER, 0)
        corner = self.grey_img[corner_location[1]:corner_location[1] + template_height, corner_location[0]:corner_location[0] + template_width]
        corner_height, corner_width = corner.shape

        if offset[0] != 0:
            inner_template = cv.flip(inner_template, 1)
            corner = cv.flip(corner, 1)
        if offset[1] != 0:
            inner_template = cv.flip(inner_template, 0)
            corner = cv.flip(corner, 0)

        match = template_match_resize(corner, inner_template, cv.TM_CCOEFF, 0.7, 1.3, 20)
        assert match
        max_location, _ = match

        if offset[0] != 0:
            max_location = [corner_width - max_location[0], max_location[1]]
        if offset[1] != 0:
            max_location = [max_location[0], corner_height - max_location[1]]

        corner_location = [corner_location[0] + max_location[0], corner_location[1] + max_location[1]]

        if offset[0] == 0:
            corner_location[0] += CORNER_REDUCTION_PIXELS
        else:
            corner_location[0] -= CORNER_REDUCTION_PIXELS
        if offset[1] == 0:
            corner_location[1] += CORNER_REDUCTION_PIXELS
        else:
            corner_location[1] -= CORNER_REDUCTION_PIXELS
        return corner_location
    
    def apply_thresholding(self):
        self.thresholded = adaptive_threshold(self.grey_img)
    
    def reframe(self):
        assert self.thresholded is not None
        assert self.top_left_corner is not None
        self.image_size = round(np.mean([
            self.top_right_corner[0] - self.top_left_corner[0],
            self.bottom_right_corner[0] - self.bottom_left_corner[0],
            self.bottom_left_corner[1] - self.top_left_corner[1],
            self.bottom_right_corner[1] - self.top_right_corner[1]
        ]))
        self.reframed = warp_to_rect(self.thresholded, self.top_left_corner, self.top_right_corner, self.bottom_left_corner, self.bottom_right_corner, self.image_size, self.image_size)
        self.colour_img = warp_to_rect(self.colour_img, self.top_left_corner, self.top_right_corner, self.bottom_left_corner, self.bottom_right_corner, self.image_size, self.image_size)
        self.top_left_corner = (0, 0)
        self.top_right_corner = (self.image_size, 0)
        self.bottom_left_corner = (0, self.image_size)
        self.bottom_right_corner = (self.image_size, self.image_size)
        self.fixel_size = float(self.image_size) / RESOLUTION
    
    def get_fixel_value(self, fixel_x, fixel_y):
        assert self.reframed is not None
        # fixel_size = float(self.image_size) / RESOLUTION
        offset_size = round(REDUCTION_AMOUNT * self.fixel_size)
        x = round(fixel_x * self.fixel_size)
        y = round(fixel_y * self.fixel_size)
        fixel_size_whole = round(self.fixel_size)
        fixel_crop = self.reframed[y + offset_size:y + fixel_size_whole - offset_size, x + offset_size:x + fixel_size_whole - offset_size]
        fixel_value = np.mean(fixel_crop)
        is_black_fixel = fixel_value < THRESHOLD_VALUE
        boolean_value = is_black_fixel == BLACK_FIXEL_VALUE
        if boolean_value:
            cv.circle(self.colour_img, (round(x + (self.fixel_size / 2)), round(y + (self.fixel_size / 2))), 3, (0, 0, 255))
        else:
            cv.circle(self.colour_img, (round(x + (self.fixel_size / 2)), round(y + (self.fixel_size / 2))), 3, (0, 255, 0))
        return boolean_value

    def get_byte_value(self, byte_x, byte_y):
        bits = 0
        byte_x_offset = byte_x * BYTE_WIDTH
        byte_y_offset = byte_y * BYTE_HEIGHT
        count = 0

        for x in range(0, BYTE_WIDTH):
            fixel_x = byte_x_offset + x
            for y in range(0, BYTE_HEIGHT):
                fixel_y = byte_y_offset + y
                if self.get_fixel_value(fixel_x, fixel_y):
                    bits += 2 ** count
                count += 1
        return bits
    
    def decode(self):
        all_bytes = []
        for byte_y in range(0, int(RESOLUTION / BYTE_HEIGHT)):
            for byte_x in range(0, int(RESOLUTION / BYTE_WIDTH)):
                byte = self.get_byte_value(byte_x, byte_y)
                all_bytes.append(byte)
        return all_bytes
    
    def check_known_patterns(self):
        total = 0
        correct = 0
        for known in KNOWN_PATTERNS:
            for x in range(0, len(known['value'][0])):
                for y in range(0, len(known['value'])):
                    fixel_x = x + known['left']
                    fixel_y = y + known['top']
                    found = 1 if self.get_fixel_value(fixel_x, fixel_y) else 0
                    actual = known['value'][y][x]
                    if actual == found:
                        correct += 1
                    total += 1
        print('{correct} / {total} correct'.format(correct=correct, total=total))

    def print_ascii(self):
        byte_indexes = [
            [29, 11],
            [28, 11],
            [31, 11],
            [30, 11],
            [33, 11],
            [32, 11],
            [35, 11],
            [34, 11],
            [37, 11],
            [36, 11],
        ]
        for x, y in byte_indexes:
            val = self.get_byte_value(x, y)
            print(chr(val), end='')
        print('\n', end='')