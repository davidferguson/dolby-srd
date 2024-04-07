import cv2 as cv
import imutils
import numpy as np

def warp_to_rect(img, tl, tr, bl, br, width, height):
    source = np.array([tl, tr, br, bl])
    target = np.array([(0, 0), (width, 0), (width, height), (0, height)])
    homography, _ = cv.findHomography(source, target)
    warped = cv.warpPerspective(img, homography, (width, height))
    return warped


def template_match_resize(img, template, method, min, max, step):
    found = None
    for scale in np.linspace(min, max, step)[::-1]:
        template_resized = imutils.resize(template, width = round(template.shape[1] * scale))
        ratio = template.shape[1] / float(template_resized.shape[1])
        result = cv.matchTemplate(img, template_resized, method)
        _, max_val, _, max_loc = cv.minMaxLoc(result)
        if found is None or max_val > found[0]:
            found = (max_val, max_loc, ratio, scale)
    if found != None:
        (_, max_loc, ratio, scale) = found
        return (max_loc, scale)
    return None

def adaptive_threshold(img):
    return cv.adaptiveThreshold(
        img,
        255, # what values the white should be
        cv.ADAPTIVE_THRESH_MEAN_C,
        cv.THRESH_BINARY,
        61, # the size of the window - needs to be high to not have "holes"
        10 # constant C
    )