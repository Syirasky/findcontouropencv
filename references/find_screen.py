# USAGE
# python find_screen.py --query queries/query_marowak.jpg

# import the necessary packages
import imutils
from skimage import exposure
import numpy as np
import argparse
import cv2

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-q", "--query", required = True,
	help = "Path to the query image")
args = vars(ap.parse_args())

# load the query image, compute the ratio of the old height
# to the new height, clone it, and resize it
image = cv2.imread(args["query"])
image2 = image.copy()
ratio = image.shape[0] / 400.0
orig = image.copy()
image = imutils.resize(image, height = 400)

# convert the image to grayscale, blur it, and find edges
# in the image
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.bilateralFilter(gray, 11, 17, 17)
edged = cv2.Canny(gray, 30, 200)

# find contours in the edged image, keep only the largest
# ones, and initialize our screen contour
#(cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)



_a,cnts,_g = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cnts = sorted(cnts,key=cv2.contourArea,reverse=True)[:10]

print(type(cnts))
for c in cnts:
	cnt_len = cv2.arcLength(c,True)
	c = cv2.approxPolyDP(c,0.02*cnt_len,True)
	area = cv2.contourArea(c) 
	print(area)
	#cv2.drawContours(image, c, -1, (0,255,0), 3)
	#cv2.imshow("Game Boy Screen", image)
	#cv2.waitKey(0)
screenCnt = None

cv2.drawContours(image, cnts, -1, (0,255,0), 3)
cv2.imshow("Game Boy Screen", image)
cv2.waitKey(0)

# loop over our contours
for cn in cnts:
	# approximate the contour
	peri = cv2.arcLength(cn, True)
	approx = cv2.approxPolyDP(cn, 0.02 * peri, True)

	# if our approximated contour has four points, then
	# we can assume that we have found our screen
	if len(approx) == 4:
		print('Screencnt found')
		screenCnt = approx
		cv2.drawContours(image2, [screenCnt], -1, (0, 255, 0), 3)
		cv2.imshow("ni hk line 69", image2)
		
	else :
		print('Screencnt not found')

# draw a rectangle around the screen
orig = image.copy()
cv2.drawContours(orig, [screenCnt], -1, (0, 255, 0), 3)
cv2.imshow("ni hk line 69", orig)

# create a mask for the screen
mask = np.zeros(image.shape[:2], dtype = "uint8")
cv2.drawContours(mask, [screenCnt], -1, 255, -1)
cv2.imshow("Masked", cv2.bitwise_and(orig, orig, mask = mask))
cv2.waitKey(0)