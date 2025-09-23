import cv2 as cv
import numpy as np



def mouse_selection(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
        print(f"Mouse clicked at: ({x}, {y})")
        pixel_rgb = img[y, x]
        print(f"Pixel value (BGR): {pixel_rgb}")

        cor_rgb_np = np.uint8([[pixel_rgb]])

        tolerancia_rgb = np.array([100, 100, 100]) 
        lower_bound = np.array(cor_rgb_np - tolerancia_rgb)
        upper_bound = np.array(cor_rgb_np + tolerancia_rgb)

        mask = cv.inRange(img, lower_bound, upper_bound)

        result_img = cv.bitwise_and(img, img, mask=mask )

        cv.imshow("selecao", result_img)
        # cv.imshow("Mascara", mask)


img = cv.imread("../assets/balle_small.jpg")

cv.imshow("bola", img)
cv.setMouseCallback('bola', mouse_selection)

k = cv.waitKey(0)
