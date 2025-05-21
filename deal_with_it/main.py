import numpy as np
import cv2

def censor(image, size = (10, 10)):
    result = np.zeros_like(image)
    stepy = result.shape[0] // size[0]
    stepx = result.shape[1] // size[1]
    for y in range(0, image.shape[0], stepy):
        for x in range(0, image.shape[1], stepx):
            result[y:y+stepy, x:x+stepx] = np.mean(image[y:y+stepy, x:x+stepx])
    return result

def glassed(image,eyes):
    glass_f = cv2.imread("deal-with-it.png", cv2.IMREAD_UNCHANGED)
    for (x, y, w, h) in eyes:
        if x + w > image.shape[1]:
            w = image.shape[1] - x
        if y + h > image.shape[0]:
            h = image.shape[0] - y
        resize_glass = cv2.resize(glass_f, (w, h))
        if resize_glass.shape[2] == 4:
            alpha_chanal = resize_glass[:, :, 3] / 255
            put_glass = resize_glass[:, :, :3]
            
            roi = image[y:y+h, x:x+w]

            for c in range(3):
                image[y:y+h, x:x+w, c] = put_glass[:, :, c] * alpha_chanal + image[y:y+h, x:x+w, c] * (1 - alpha_chanal)
            image[y:y+h, x:x+w] = roi
        else:
            image[y:y+h, x:x+w] = resize_glass
    return image

cv2.namedWindow("Camera", cv2.WINDOW_NORMAL)

capture = cv2.VideoCapture(0 + cv2.CAP_DSHOW)
capture.set(cv2.CAP_PROP_AUTO_EXPOSURE,3)
capture.set(cv2.CAP_PROP_AUTO_EXPOSURE,1)
capture.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)

face_cascade = cv2.CascadeClassifier("haarcascade-frontalface-default.xml")
eye_cascade = cv2.CascadeClassifier("haarcascade-eye.xml")

while capture.isOpened():
    ret, frame = capture.read()
    blurred = cv2.GaussianBlur(frame, (7, 7), 0)
    gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
    eyes = eye_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
    
    if len(eyes) == 2:
       
        (x1, y1, w1, h1), (x2, y2, w2, h2) = eyes[0], eyes[1]
        x = min(x1, x2) 
        y = min(y1, y2)
        w = max(x1 + w1, x2 + w2) - x 
        h = max(y1 + h1, y2 + h2) - y
        
        new_w = int(w * 1.8)
        new_h = int(h * 1.5)
        x -= (new_w - w) // 2 
        y -= (new_h - h) // 2 
        frame = glassed(frame, [(x, y, new_w, new_h)])        

    key =  chr(cv2.waitKey(1) & 0xFF)
    if key == "q":
        break
    cv2.imshow("Camera", frame)

capture.release()
cv2.destroyAllWindows()