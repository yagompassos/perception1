import cv2 as cv
import sys
import numpy as np

img = cv.imread(cv.samples.findFile("im.jpg"), cv.IMREAD_GRAYSCALE)

if img is None:
    sys.exit("Could not read the image.")

img = cv.resize(img, (600, 800))

kernel = np.ones((5,5),np.float32)/25
dst = cv.filter2D(img,-1,kernel)

cv.imshow("normal image", img)
cv.imshow("result", dst)
 
k = cv.waitKey(0)

if k == ord("s"):
    cv.imwrite("imagem.png", img)

    