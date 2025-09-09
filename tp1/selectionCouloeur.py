#converstion de RGB pour HSV

import cv2 as cv
import sys

def mouse_selection(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
        print(f"Mouse clicked at: ({x}, {y})")
        pixel = img[y, x]
        print(f"Pixel value (BGR): {pixel}")

img = cv.imread(cv.samples.findFile("balle_small.jpg"))

if img is None:
    sys.exit("Could not read the image.")

# img = cv.resize(img, (600, 800))

cv.imshow("normal image", img)
cv.setMouseCallback('normal image', mouse_selection)

# hsv img
img_hsv = cv.cvtColor(img, cv.COLOR_RGB2HSV)
cv.imshow("HSV image", img_hsv)

k = cv.waitKey(0)

if k == ord("s"):
    cv.imwrite("imagem.png", img)

    