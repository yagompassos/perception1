import cv2 as cv
import numpy as np

def mouse_selection(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
        # prendre la couleur du pixel et faire la selection
        pixel_rgb = img[y, x]

        cor_rgb_np = np.uint8([[pixel_rgb]])    
        cor_hsv = cv.cvtColor(cor_rgb_np, cv.COLOR_BGR2HSV)[0][0]

        tolerancia_hsv = np.array([10, 200, 100])  # H, S, V     tolerance
        lower_bound = np.array(cor_hsv - tolerancia_hsv)
        upper_bound = np.array(cor_hsv + tolerancia_hsv)

        img_hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)    #on convertit l'image en HSV

        mask = cv.inRange(img_hsv, lower_bound, upper_bound)   # creation de la mask

        result_img = cv.bitwise_and(img, img, mask=mask)    # application de la mask a l'image originale

        # Hough circles

        blur = cv.medianBlur(mask, 5)   # blur pour reduire le bruit

        circles = cv.HoughCircles(blur, cv.HOUGH_GRADIENT, 1, 20,
                                    param1=100, param2=20, # ceci sont les meilleurs parametres pour detecter la balle yellow (j'ai essayé plusieurs combinaisons)
                                    minRadius=1, maxRadius=0)
        
        max_radius = 0     # on demarre ces variables pour sauvegarder le plus grand cercle aprés
        max_circle = None
        max_center = None
        
        if circles is not None:     # verification dus circles trouvés avec cv.HoughCircles
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                center = (i[0], i[1])
                radius = i[2]
                if radius > max_radius: # sauvegarder le plus grand cercle (presque toujours le bon cercle de la balle yellow)
                    max_radius = radius
                    max_center = center
                    max_circle = i
        else :
            print("No circles detected")

        if max_circle is not None: # si nous avons detecté au moins un cercle, on le dessine dans un nouvelle fenetre (ceci c'est juste pour dessiner)
            cv.circle(img, max_center, 1, (0, 100, 100), 3)
            cv.circle(img, max_center, max_radius,  (255, 0, 255), 3)
            cv.putText(img, f"centre: X: {max_center[0]}, Y: {max_center[1]}", (10, 500), cv.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2, cv.LINE_AA)
            cv.putText(img, f"radius: {max_radius} px", (10, 550), cv.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2, cv.LINE_AA)
            cv.imshow("detected circle", img)
            print("Largest circle found at:", max_circle[0:2], "with radius:", max_radius)
            

# le programe demarre ici!!!
img = cv.imread(cv.samples.findFile("../assets/balle_small.jpg"))

cv.imshow("normal image", img)
cv.setMouseCallback('normal image', mouse_selection) # appele la fonction mouse_selection()

k = cv.waitKey(0)