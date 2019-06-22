import cv2
import sys
import numpy as np
import pytesseract
from PIL import Image

if len(sys.argv)<2:
	print "image file expected"
	quit()

def readText(mat):
	gr=cv2.cvtColor(mat,cv2.COLOR_BGR2GRAY)
	gr=255-gr
	th=cv2.threshold(gr,100,255,cv2.THRESH_BINARY)[1]
	th = 255-th
	return pytesseract.image_to_string(Image.fromarray(th))

def vertical_near(point, points):
	for p in points:
		if point[0]==p[0][0] and point[1]<p[0][1]:
			return list(p[0])
	return None

def horizontal_near(point, points):
	for p in points:
		if point[1]==p[0][1] and point[0]<p[0][0]:
			return list(p[0])
	return None

def getMainTable(Mat,img1):
	nz=cv2.findNonZero(Mat)	
	if isinstance(nz,np.ndarray):
		if len(nz)<=4:
			return None
	else:
		return None
	row=list()
	table=list()
	xml = "<table>\n<tr>"
	for p in nz:
		v=vertical_near(p[0],nz)
		h=horizontal_near(p[0],nz)
		if isinstance(v,list) and isinstance(h,list):
			if Mat[int(p[0][1]),int(p[0][0])]==0:
				continue
			x1,y1=p[0]
			x2,y2=h[0],v[1]
			xmln = getMainTable(Mat[y1-1:y2,x1-1:x2],img1[y1-1:y2+1,x1-1:x2+1])
			n=False
			if isinstance(xmln,str):
				xml+="<td>"+xmln+"</td>"
				Mat[y1:y2,x1:x2]=0
				n=True
		if not isinstance(h,list):
			if len(row)>0:
				table.append(row)
				row=list()
				xml+="</tr>\n<tr>"
		elif isinstance(v,list):
			row.append(list(p[0]))
			if not n:
				xml+="<td>"+readText(img1[y1-1:y2+1,x1-1:x2+1])+"</td>"
			else:
				n=False

	xml+="\b\b\b\b</table>\n"
	return str(xml)

	
img= cv2.imread(sys.argv[1])
scale=15
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray= cv2.bitwise_not(gray)
th = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,15,-2)
hori=th.copy()
vert=th.copy()
[rows,cols]=th.shape
hsize=cols/scale
vsize=rows/scale
hstruct= cv2.getStructuringElement(cv2.MORPH_RECT,(hsize,1))
vstruct = cv2.getStructuringElement(cv2.MORPH_RECT,(1,vsize))
hori=cv2.erode(hori,hstruct)
vert=cv2.erode(vert,vstruct)
hstruct= cv2.getStructuringElement(cv2.MORPH_RECT,(hsize+1,1))
vstruct = cv2.getStructuringElement(cv2.MORPH_RECT,(1,vsize+1))
hori=cv2.dilate(hori,hstruct)
vert=cv2.dilate(vert,vstruct)
tableOut=hori+vert
joints=cv2.bitwise_and(hori,vert)	
ss= getMainTable(joints,img)
outF=open(sys.argv[1].split(".")[:-1][0]+".xml","w")
outF.write(ss)
outF.close()

