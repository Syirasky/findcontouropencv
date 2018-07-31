from PIL import Image
import cv2

# brightness thresholds
thpink = 180
thblack = 100

# crop & convert image to gray (rows of columns)
def to_grayscale(image):
	margin = 5
	width, height = image.size
	pixels = image.load()
	gray = []
	for y in range(margin, height-margin):
		row = []
		for x in range(margin, width-margin):
		
			pixel = pixels[x, y]
			# typical eye color response
			row.append(int(0.2126 * pixel[0] + 0.7152 * pixel[1] + 0.0722 * pixel[2]))
		gray.append(row)
	print("Width x",width)	
	print("Width x - margin =",width-margin)
	print("Height y",height)
	print("Height y - margin =",height-margin)
	
	return gray

# detect row brightness vs threshold changes
def detect_row_coordinates(gray):
	width, height = len(gray[0]), len(gray)
	prev_dark = False
	grid_y = []
	for y in range(height):
		now_dark = min(gray[y]) < thpink
		if prev_dark != now_dark:
			grid_y.append(y)
			prev_dark = now_dark
	# return center position
	out = []
	for y in range(1, len(grid_y), 2):
		out.append(int((grid_y[y] + grid_y[y - 1]) / 2))
	return out

# detect column brightness vs threshold changes
def detect_col_coordinates(gray):
	width, height = len(gray[0]), len(gray)
	prev_dark = False
	grid_x = []
	for x in range(width):
		minimum = 256
		for y in range(height):
			if gray[y][x] < minimum:
				minimum = gray[y][x]
		now_dark = minimum < thpink
		if prev_dark != now_dark:
			grid_x.append(x)
			prev_dark = now_dark
	# return center position
	out = []
	for x in range(1, len(grid_x), 2):
		out.append(int((grid_x[x] + grid_x[x - 1]) / 2))
	return out

def get_answer(question, gray, x_co, y_co):
	# each column has 2 digits and 4 answer dots
	ans = ['', '', 'A', 'B', 'C', 'D']
	x, y = 0, question-1
	for _ in range(int(question / 30)):
		x += 6
		y -= 30
	for find in range(2, len(ans)):
		if gray[y_co[y]][x_co[x+find]] < thblack:
			return ans[find]
	return ''

# load test image pixels
gray = to_grayscale(Image.open("cropped.jpeg"))
x_co = detect_col_coordinates(gray)
y_co = detect_row_coordinates(gray)
print("x_co",x_co)
print("X_co list count",len(x_co))
print("y_co",y_co)
print("Y_co list count",len(y_co))

for f in range(1, 41):
	print(f, get_answer(f, gray, x_co, y_co))
