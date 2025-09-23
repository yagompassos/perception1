import cv2 as cv
import numpy as np

def mouse_selection(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
        print(f"Mouse clicked at: ({x}, {y})")
        pixel_rgb = img[y, x]
        print(f"Pixel value (BGR): {pixel_rgb}")

        cor_rgb_np = np.uint8([[pixel_rgb]])
        cor_hsv = cv.cvtColor(cor_rgb_np, cv.COLOR_BGR2HSV)[0][0]
        
        tolerancia_hsv = np.array([10, 200, 100])  # H, S, V
        lower_bound = np.array(cor_hsv - tolerancia_hsv)
        upper_bound = np.array(cor_hsv + tolerancia_hsv)

        img_hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

        mask = cv.inRange(img_hsv, lower_bound, upper_bound)

        result_img = cv.bitwise_and(img, img, mask=mask)

        cv.imshow("selecao", mask)


img = cv.imread(cv.samples.findFile("../assets/balle_small.jpg"))

# img = cv.resize(img, (600, 800))

cv.imshow("normal image", img)
cv.setMouseCallback('normal image', mouse_selection)

k = cv.waitKey(0)

#haufh