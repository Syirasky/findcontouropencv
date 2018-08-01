import numpy as np
import cv2

image = cv2.imread("cropped.jpeg")
kernel = np.ones((3, 3), np.uint8)
image = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
TotalQstn = 7.0
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
ret, thresh1 = cv2.threshold(gray, 210, 255, cv2.THRESH_BINARY)

thresh = cv2.threshold(thresh1, 200, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
# cv2.imwrite(ROI+"_.jpg",thresh)
print("--------------roi written---")
# thresh = cv2.dilate(thresh,kernel,iterations = 1)

# finding for all contours in image

_,cnts, _ = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
sum = 0
circles = []  # array for storing all bubbles

if len(cnts) > 0:
	print ("------Total contours---------" + str(len(cnts)))
else:
	print ("---------blank------")
for cn in cnts:
	area = cv2.contourArea(cn)
	if area > 100:
		(x, y, w, h) = cv2.boundingRect(cn)
		# print "bounding rect"
		# print cv2.boundingRect(cn)
		if w >= 22 and h >= 16 and w < 35 and w > h:  # suitable condition for detecting circle
			circles.append(cn)  # storing bubble contour

