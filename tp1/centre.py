import cv2 as cv
import numpy as np

def mouse_selection(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
        pixel_rgb = img[y, x]

        cor_rgb_np = np.uint8([[pixel_rgb]])
        cor_hsv = cv.cvtColor(cor_rgb_np, cv.COLOR_BGR2HSV)[0][0]

        tolerancia_hsv = np.array([10, 200, 100])  # H, S, V
        lower_bound = np.array(cor_hsv - tolerancia_hsv)
        upper_bound = np.array(cor_hsv + tolerancia_hsv)

        img_hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

        mask = cv.inRange(img_hsv, lower_bound, upper_bound)

        result_img = cv.bitwise_and(img, img, mask=mask)

        #hough circles

        blur = cv.medianBlur(mask, 5)

        circles = cv.HoughCircles(blur, cv.HOUGH_GRADIENT, 1, 20,
                                    param1=100, param2=20,
                                    minRadius=1, maxRadius=0)
        
        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                center = (i[0], i[1])
                # circle center
                cv.circle(img, center, 1, (0, 100, 100), 3)
                # circle outline
                radius = i[2]
                cv.circle(img, center, radius, (255, 0, 255), 3)
                cv.imshow("detected circles", img)
        else :
            print("No circles detected")



img = cv.imread(cv.samples.findFile("../assets/balle_small.jpg"))


cv.imshow("normal image", img)
cv.setMouseCallback('normal image', mouse_selection)

k = cv.waitKey(0)