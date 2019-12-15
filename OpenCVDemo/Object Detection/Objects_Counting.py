import numpy as np
import cv2 as cv
from tkinter import *
from PIL import Image
from PIL import ImageTk
import tkinter.filedialog as tkfd
from matplotlib import pyplot as plt


def sharpening(image, k, a):
    blur = cv.medianBlur(image, k)
    laplace = cv.Laplacian(blur, cv.CV_64F)
    sharp = image - a*laplace
    sharp[sharp > 255] = 255
    sharp[sharp < 0] = 0
    return sharp.astype(np.uint8)


def processing(image, k1=3, k2=3, k3=7, k4 =3, a=1, gamma=1):
    gray_image = cv.cvtColor(image, cv.COLOR_RGB2GRAY)
    # Blur
    blur_image = cv.medianBlur(gray_image, k1)
    # Sharp
    sharp_image = sharpening(blur_image, a, k2)
    # Gamma Correction
    gamma_correction = (255*(sharp_image/255)**gamma).astype(np.uint8)
    # Otsu
    ret, thresh = cv.threshold(gamma_correction, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    thresh = cv.bitwise_not(thresh)
    # Dilation and Erosion
    kernel = np.ones((k3, k3))
    dilation = cv.dilate(thresh, kernel, iterations=1)
    erosion = cv.erode(dilation, kernel, iterations=1)
    # Blur
    erosion = cv.medianBlur(erosion, k4)
    # Connected Component Labeling
    ret, labels = cv.connectedComponents(erosion)
    label_hue = np.uint8(179 * labels / np.max(labels))
    blank_ch = 255 * np.ones_like(label_hue)
    labeled_img = cv.merge([label_hue, blank_ch, blank_ch])
    labeled_img = cv.cvtColor(labeled_img, cv.COLOR_HSV2BGR)
    labeled_img[label_hue == 0] = 0
    print('objects number is:', ret - 1)
    return labeled_img


def GUI():
    global panelA, panelB
    path = tkfd.askopenfilename()
    if len(path) > 0:
        image = cv.imread(path)
        height, width, no_channels = image.shape
        image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        new_image = processing(image, k3=11, k4=7, gamma=1.3)
        image = Image.fromarray(image)
        new_image = Image.fromarray(new_image)
        if height > 703 or width > 700:
            image = image.resize((703, 700),Image.ANTIALIAS)
            new_image = new_image.resize((703, 700),Image.ANTIALIAS)
        image = ImageTk.PhotoImage(image)
        new_image = ImageTk.PhotoImage(new_image)
        if panelA is None or panelB is None:
            panelA = Label(image=image)
            panelA.image = image
            panelA.pack(side="left")
            panelB = Label(image=new_image)
            panelB.image = new_image
            panelB.pack(side="right")
        else:
            panelA.configure(image=image)
            panelB.configure(image=new_image)
            panelA.image = image
            panelB.image = new_image


root = Tk()
panelA = None
panelB = None
btn = Button(root, text="Select an image", command=GUI)
btn.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")
root.mainloop()