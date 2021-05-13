import time
import cv2 as cv
import numpy as np

List = [ [ ] ]
cList = [[]]
isDrawing = False

def nothing(x):
	pass
	pass

def render_lines(x, y):
	global List, cList
	b,g,r = (0, 0, 0)
	List[-1].append([x, y])
	cList[-1].append([int(b),int(g),int(r)])

def clear(event, x, y, flags, params):
	global List, cList
	if event == cv.EVENT_FLAG_LBUTTON:
		List = [[]]
		cList = [[]]


def calibration():
	global cap

	cv.namedWindow("calibration")
	cv.createTrackbar('hue lower', 'calibration', 50, 179, nothing)
	cv.createTrackbar('hue upper', 'calibration', 130, 179, nothing)
	cv.createTrackbar('sat lower', 'calibration', 90,255,nothing)
	cv.createTrackbar('sat upper', 'calibration', 255,255,nothing)
	cv.createTrackbar('vib lower', 'calibration', 60, 255, nothing)
	cv.createTrackbar('vib upper', 'calibration', 189, 255, nothing)
	cv.createTrackbar('start app', 'calibration', 0, 1, nothing)

	while(cap.isOpened()):
		if cv.waitKey(20) & 0xff == 27:
			break

		_, frameO = cap.read()
		frame = cv.flip(frameO, 1)
		hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

		hl = cv.getTrackbarPos('hue lower', 'calibration')
		hu = cv.getTrackbarPos('hue upper', 'calibration')
		sl = cv.getTrackbarPos('sat lower', 'calibration')
		su = cv.getTrackbarPos('sat upper', 'calibration')
		vl = cv.getTrackbarPos('vib lower', 'calibration')
		vu = cv.getTrackbarPos('vib upper', 'calibration')

		lower = np.array([hl,sl,vl])
		range = np.array([hu,su,vu])

		rows,cols,chan = frame.shape
		temp = frame[20:rows-20, 20:cols-20]
		mask = cv.inRange(hsv, lower, range)
		
		tempmask = mask[20:rows-20, 20:cols-20]
		tempres = cv.bitwise_and(temp, temp, mask=tempmask)
		res = cv.copyMakeBorder(tempres, 20,20,20, 20, cv.BORDER_CONSTANT, value=[0,0,0])
		
		cv.imshow("calibration", res)

		if cv.getTrackbarPos('start app', 'calibration') == 1:
			cv.destroyWindow('calibration')
			return (hl, hu, sl, su, vl, vu)
	return None

def canvas(frameO):

	global cap, List, cList , isDrawing

	hl, hu, sl, su, vl, vu = [50, 130, 90, 255, 60, 189] 

	frame = cv.flip(frameO, 1)
	hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

	lower = np.array([hl,sl,vl])
	range = np.array([hu,su,vu])

	rows,cols,chan = frame.shape
	temp = frame[20:rows-20, 20:cols-20]
	mask = cv.inRange(hsv, lower, range)
	
	tempmask =  mask[20:rows-20, 20:cols-20]
	tempres = cv.bitwise_and(temp, temp, mask=tempmask)
	res = cv.copyMakeBorder(tempres, 20,20,20, 20, cv.BORDER_CONSTANT, value=[0,0,0])
	
	res2gray = cv.cvtColor(res, cv.COLOR_BGR2GRAY)
	median = cv.medianBlur(res2gray, 23)

	contours, hierarchy = cv.findContours(median, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
	if (len(contours) > 0) and (contours is not None) :
		cnt = contours[0]
		(a, b), r = cv.minEnclosingCircle(cnt)
		center = (int(a), int(b))
		radius = int(r)
		cv.circle(frame, center, radius, (0, 128 ,128), 4)

		render_lines(center[0], center[1])
		isDrawing = True
	else:
		if isDrawing:
			List.append([])
			cList.append([])
		isDrawing = False
	
	for i,j in zip(List,cList):
		if j !=[]:
			r,g,b = j[0]
			cv.polylines(frame,[np.array(i, dtype=np.int32)], False, (r,g,b), 2, cv.LINE_AA)
			
	return frame