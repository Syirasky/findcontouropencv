import numpy as np
import cv2

im = cv2.imread('a.jpg')
newsectioncnt = im.copy()
imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)

imblur = cv2.GaussianBlur(imgray, (5, 5), 0)

#ret,thresh = cv2.threshold(imblur,60,255,cv2.THRESH_BINARY)
edged = cv2.Canny(imblur,75,200)
im2, contours, hierarchy = cv2.findContours(edged,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)



cnts = sorted(contours,key=cv2.contourArea,reverse=True)[:3]
screenCnt = None
for c in cnts:
	area = cv2.contourArea(c)
	print(area)

# draw a rectangle around the screen

orig = im.copy()
orig2 = im.copy()
cv2.drawContours(orig, cnts, 1, (0, 255, 0), 3)
#cv2.imshow("ni contour ", orig)
#cv2.waitKey(0)







mask = np.zeros(im.shape[:2], dtype = "uint8")
cv2.drawContours(mask,cnts,1,255,-1)

# Now crop

out = np.zeros_like(im)
out[mask ==255] = im[mask==255]
(x, y) = np.where(mask == 255)
(topx, topy) = (np.min(x), np.min(y))
(bottomx, bottomy) = (np.max(x), np.max(y))
out = out[topx:bottomx+1, topy:bottomy+1]

# Show the output image
#cv2.imshow('Out Rectangle Detected', out)


#detect contour on new section
newim = out.copy()

newimgray = cv2.cvtColor(newim,cv2.COLOR_BGR2GRAY)
newimblur = cv2.GaussianBlur(newimgray, (5, 5), 0)
#ret,thresh = cv2.threshold(imblur,60,255,cv2.THRESH_BINARY)
newedged = cv2.Canny(newimblur,75,700)
#detect contour dlm new segment
#-0newim2, newcontours, newhierarchy = cv2.findContours(newedged,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
#-cv2.drawContours(newim, newcontours, -1, (0, 255, 0), 3)
#-cv2.imshow("ni contour ", newim)
#-print(len(newcontours))


#nk cari circle dlm rectangle

cropped = cv2.imread('cropped.jpeg',0)


imgcr = cv2.medianBlur(cropped,1)
cimgcr = cv2.cvtColor(imgcr,cv2.COLOR_GRAY2BGR)
circles = cv2.HoughCircles(imgcr,cv2.HOUGH_GRADIENT,1.2,100,param1=50,param2=30,minRadius=0,maxRadius=0)
    
circles = np.uint16(np.around(circles))
for i in circles[0,:]:
	# draw the outer circle
	cv2.circle(cimgcr,(i[0],i[1]),i[2],(0,255,0),2)
	# draw the center of the circle
	cv2.circle(cimgcr,(i[0],i[1]),2,(0,0,255),3)
   
cv2.imshow('detected circles',cimgcr)
cv2.waitKey(0)
cv2.destroyAllWindows()
