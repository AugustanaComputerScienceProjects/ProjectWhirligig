import cv2
import numpy as np
from matplotlib import pyplot as plt

img_rgb = cv2.imread(r'H:\Project Whiriligig\opencvtesting\large1_frame0001.png')
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
template = cv2.imread(r'H:\Project Whiriligig\opencvtesting\onebug2.png',0)
w, h = template.shape[::-1]

res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
threshold = 0.5
loc = np.where( res >= threshold)
for pt in zip(*loc[::-1]):
    cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,255,255), 2)

cv2.imshow('res.png',img_rgb)
if cv2.waitKey(0) & 0xff == 27:
    cv2.destroyAllWindows()