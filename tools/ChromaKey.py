import cv2
import numpy as np

def RemoveBG(frame: np.array, upperbound: np.array, lowerbound: np.array, replace: np.array):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lowerbound, upperbound)
    inv_mask = 255 - mask
    detect = cv2.bitwise_and(frame, frame, mask=inv_mask)
    partial = cv2.bitwise_and(replace, replace, mask=mask)
    return detect + partial

def ShowSeletected(frame: np.array, upperbound: np.array, lowerbound: np.array):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lowerbound, upperbound)
    cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    res = frame.copy()
    cv2.drawContours(res, cnts, -1, [200, 200, 200], 20)
    buf = res.tobytes()
    return buf

def CaptureBG(frame: np.array):
    cv2.imwrite('./src/bg.png', frame)
    
