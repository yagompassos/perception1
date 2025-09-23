import cv2 as cv
import numpy as np

def aplly_mask(cor_hsv):
    # Distance circulaire sur H (0..180) -> gérer le wrap
    img_hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)    # on convertit l'image en HSV
    H, S, V = cv.split(img_hsv)

    tolerance_H = 30 # tolérance sur la teinte (0..180)
    tolerance_S = 120  # tolérance sur la saturation (0..255)
    low_h = (int(cor_hsv[0]) - tolerance_H) % 180
    high_h = (int(cor_hsv[0]) + tolerance_H) % 180

    if low_h <= high_h:
        mask_h = (H >= low_h) & (H <= high_h)
    else:
        # l'intervalle traverse 0 -> union de deux morceaux
        mask_h = (H >= low_h) | (H <= high_h)

    # Bande de saturation
    low_s = max(0, int(cor_hsv[1]) - tolerance_S)
    high_s = min(255, int(cor_hsv[1]) + tolerance_S)
    mask_s = (S >= low_s) & (S <= high_s)

    # Masque binaire final (balle=255, fond=0)
    mask = (mask_h & mask_s).astype(np.uint8) * 255
    return mask

def apply_morphologie(mask):
    # Morfologie pour nettoyer le masque
    kernel = np.ones((5,5),np.uint8) # j'ai pris ce ligne dans la documentation d'OpenCV
    opening = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel) # ouverture de l'image (erosion > dilatation)
    fermeture = cv.morphologyEx(opening, cv.MORPH_CLOSE, kernel) # fermeture de l'image (dilatation > erosion)
    return fermeture

def findGoodCircle(gradient):
    circles = cv.HoughCircles(
        gradient,
        cv.HOUGH_GRADIENT,
        1,
        50,
        param1=100,
        param2=15,
        minRadius=10,
        maxRadius=200
    )

    if circles is not None:
        first_circle = circles[0][0]
        center = (int(first_circle[0]), int(first_circle[1]))
        radius = int(first_circle[2])
        print("First circle center:", center, "with radius:", radius)
        cv.circle(img, center, radius, (255, 0, 255), 3)
        cv.imshow("detected circle", img)
        return first_circle
    else:
        print("No circles found")
        return None

def mouse_selection(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:

        # prendre la couleur du pixel et faire la selection
        print(f"Mouse clicked at: ({x}, {y})")
        pixel_rgb = img[y, x]
        cor_rgb_np = np.uint8([[pixel_rgb]])    
        cor_hsv = cv.cvtColor(cor_rgb_np, cv.COLOR_BGR2HSV)[0][0]
 
        mask = aplly_mask(cor_hsv)
        cv.imshow("mask", mask)
        
        morphologie = apply_morphologie(mask)
        # cv.imshow("morphologie", morphologie)

        gradient = cv.Laplacian(morphologie, cv.CV_8UC1)
        # cv.imshow("mask after morphologie, blur et gradient", gradient)

        # bon_cercle = findGoodCircle(gradient) #find the first circle with HOUGH CIRCLES


# le programe demarre ici!!!
img = cv.imread(cv.samples.findFile("assets/balle_small.jpg"))

cv.imshow("normal image", img)
cv.setMouseCallback('normal image', mouse_selection) # appele la fonction mouse_selection()

k = cv.waitKey(0)