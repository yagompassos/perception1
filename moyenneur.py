import cv2 as cv
import sys

img = cv.imread(cv.samples.findFile("im.jpg"))

if img is None:
    sys.exit("Could not read the image.")

img = cv.resize(img, (600, 800))

cv.imshow("normal image", img)
 
blur = cv.blur(img,(10,10))

cv.imshow("blur avec moyenneur image", blur)
 
k = cv.waitKey(0)

if k == ord("s"):
    cv.imwrite("imagem.png", img)

    