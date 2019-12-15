import cv2
import numpy as np

def nothing(x):
    pass

def ResizeWithAspectRatio(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    return cv2.resize(image, dim, interpolation=inter)

cv2.namedWindow("Tracking")

frame = cv2.imread('Count_Object_Of_Different_Types8.png')
frame = ResizeWithAspectRatio(frame, width=480)


cv2.destroyAllWindows()