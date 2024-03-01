import cv2
import numpy as np

def RemoveBG(frame: np.array, upperbound: np.array, lowerbound: np.array, replace: np.array, board: int, is_fullRes: int):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lowerbound, upperbound)
    mask = boarder_adjustment(cv2.cvtColor(cv2.merge([mask, mask, mask]), cv2.COLOR_BGR2GRAY), board)
    if not is_fullRes:
        cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        if len(cnts):
            x, y, w, h = cv2.boundingRect(cnts[0])
            transform = np.array([[w/frame.shape[1], 0, x],
                                  [0, h/frame.shape[0], y]], dtype=np.float32)
            replace = cv2.warpAffine(replace, transform, (frame.shape[1], frame.shape[0]), borderValue=(0, 0, 0))
            cv2.imwrite('test.png', replace)
    partial = cv2.bitwise_and(replace, replace, mask=mask)
    inv_mask = 255 - mask
    detect = cv2.bitwise_and(frame, frame, mask=inv_mask)
    return detect + partial

def ShowSeletected(frame: np.array, upperbound: np.array, lowerbound: np.array):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lowerbound, upperbound)
    cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    res = frame.copy()
    cv2.drawContours(res, cnts, -1, [200, 200, 200], 20)
    buf = res.tobytes()
    return buf

def boarder_adjustment(mask: np.array, value: int):
    if value == 0:
        n_mask = mask
    elif value < 0:
        n_mask = cv2.erode(mask, np.ones((3, 3), dtype=np.uint8), iterations=abs(value))
    else:
        n_mask = cv2.dilate(mask, np.ones((3, 3), dtype=np.uint8), iterations=abs(value))
    
    n_mask = cv2.GaussianBlur(n_mask, (3, 3), 0)
    _, res = cv2.threshold(n_mask, 5, 255, cv2.THRESH_BINARY)
    
    return res

def CaptureBG(frame: np.array):
    cv2.imwrite('./src/bg.png', frame)
    
