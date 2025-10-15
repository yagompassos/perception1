import numpy as np
import cv2 as cv
import sys

# === VARIABLES GLOBALES ===
clicked = False
first_color_hsv = None
last_center = None
roi_size = 800

# === FONCTIONS ===
def convert_pixel_to_hsv(img, x, y):
    if y >= img.shape[0] or x >= img.shape[1]:
        print("Erreur: Coordonnées hors des limites de l'image.")
        return None
        
    pixel_rgb = img[y, x]
    cor_rgb_np = np.uint8([[pixel_rgb]])
    cor_hsv = cv.cvtColor(cor_rgb_np, cv.COLOR_BGR2HSV)[0][0]
    return cor_hsv

def mouse_callback(event, x, y, flags, param):
    global clicked, first_color_hsv, last_center
    if event == cv.EVENT_LBUTTONDOWN:
        clicked = True
        first_color_hsv = convert_pixel_to_hsv(first_frame, x, y)
        last_center = (x, y)
        print(f"Mouse clicked at: ({x}, {y}), HSV color: {first_color_hsv}")

def calculate_roi(frame, center, roi_size):
    x1 = int(center[0] - roi_size / 2)
    y1 = int(center[1] - roi_size / 2)
    x2 = int(center[0] + roi_size / 2)
    y2 = int(center[1] + roi_size / 2)

    x1 = max(0, x1)
    y1 = max(0, y1)
    x2 = min(frame.shape[1], x2)
    y2 = min(frame.shape[0], y2)

    return frame[y1:y2, x1:x2], (x1, y1)

def apply_mask(img, cor_hsv):
    img_hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    H, S, V = cv.split(img_hsv)

    tolerance_H = 45
    tolerance_S = 80
    tolerance_V = 120
    
    low_h = (int(cor_hsv[0]) - tolerance_H) % 180
    high_h = (int(cor_hsv[0]) + tolerance_H) % 180

    if low_h <= high_h:
        mask_h = (H >= low_h) & (H <= high_h)
    else:
        mask_h = (H >= low_h) | (H <= high_h)

    low_s = max(0, int(cor_hsv[1]) - tolerance_S)
    high_s = min(255, int(cor_hsv[1]) + tolerance_S)
    mask_s = (S >= low_s) & (S <= high_s)

    low_v = max(0, int(cor_hsv[2]) - tolerance_V)
    high_v = min(255, int(cor_hsv[2]) + tolerance_V)
    mask_v = (V >= low_v) & (V <= high_v)
    
    mask = (mask_h & mask_s & mask_v).astype(np.uint8) * 255
    return mask

def apply_morphologie(mask):
    kernel = np.ones((5,5),np.uint8) # j'ai pris ce ligne dans la documentation d'OpenCV
    opening = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel, iterations=5) # ouverture de l'image (erosion > dilatation)
    fermeture = cv.morphologyEx(opening, cv.MORPH_CLOSE, kernel, iterations=5) # fermeture de l'image (dilatation > erosion)
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
        return [center[0], center[1], radius]
    else:
        return None

# === LE PROGRAMME DEMARRE ICI ===
vid = cv.VideoCapture('assets/balle.mp4')

ret, first_frame = vid.read()

cv.imshow('frame', first_frame)
cv.setMouseCallback('frame', mouse_callback)
print("Waiting for a mouse click on the first frame...")

while not clicked:
    if cv.waitKey(100) != -1:
        break

if clicked:
    first_mask = apply_mask(first_frame, first_color_hsv)
    first_morph = apply_morphologie(first_mask)
    first_gradient = cv.Laplacian(first_morph, cv.CV_8UC1)
    first_circle = findGoodCircle(first_gradient)

    last_center = (first_circle[0], first_circle[1])

    while True:
        ret, frame = vid.read()
        if not ret:
            print("Video stream has ended. Exiting...")
            break
        
        # TRAITER CHAQUE CADRE
        roi, roi_origin = calculate_roi(frame, last_center, roi_size)

        roi_hsv_color = convert_pixel_to_hsv(frame, last_center[0], last_center[1])
        mask = apply_mask(roi, roi_hsv_color)
        morph = apply_morphologie(mask)
        gradient = cv.Laplacian(morph, cv.CV_8UC1)
        circle_in_roi = findGoodCircle(gradient)
        
        if circle_in_roi is not None:
            # Avec un offset, obtenir les coordonnées absolues dans l'image complète
            absolute_center_x = circle_in_roi[0] + roi_origin[0]
            absolute_center_y = circle_in_roi[1] + roi_origin[1]
            last_center = (absolute_center_x, absolute_center_y)
            
            cv.circle(frame, last_center, circle_in_roi[2], (255, 0, 255), 3) #on dessine le cercle trouvé dans l'image complète

        cv.imshow('frame', frame)
        cv.imshow('ROI Mask', morph)
        
        if cv.waitKey(25) == ord('q'):
            break

vid.release()
cv.destroyAllWindows()