import cv2
from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import numpy as np
#import argparse
import imutils
from google.colab.patches import cv2_imshow

image_raw = cv2.imread("/content/drive/MyDrive/Colab Notebooks/hoop1.jpg")

def midpoint(x, y):
	return ((x[0] + y[0]) * 0.5, (x[1] + y[1]) * 0.5)

def reconnaissance(image):

  #ap = argparse.ArgumentParser()
  #ap.add_argument("-i", "--image", required=True,
	#help="path to the input image")
  #ap.add_argument("-w", "--width", type=float, required=True,
	#help="width of the left-most object in the image (in inches)")
  #args = vars(ap.parse_args())

#the code above works when we provide the previous args in cmd line

  pixelsPerMetric = None

  gris = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
  ret, seuil = cv2.threshold(gris,175,255,cv2.THRESH_TOZERO)
  contours, h = cv2.findContours(seuil,2,1)

  countour_liste = []

  for cnt in contours:
    approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
    n = len(approx)
    if (n>9) & (cv2.contourArea(cnt)>3000):
      cv2.drawContours(image,[cnt],0,(255,0,0),5)
      countour_liste.append(cnt)
              
      if pixelsPerMetric is None:

        box = cv2.minAreaRect(cnt)
        box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
        box = np.array(box, dtype="int")
        box = perspective.order_points(box)

        (tl, tr, br, bl) = box
        (tltrX, tltrY) = midpoint(tl, tr)
        (blbrX, blbrY) = midpoint(bl, br)

        (tlblX, tlblY) = midpoint(tl, bl)
        (trbrX, trbrY) = midpoint(tr, br)

        dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
        dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))
        # if the pixels per metric has not been initialized, then
        # compute it as the ratio of pixels to supplied metric

        print(dB)
        pixelsPerMetric = dB / 2.4 #width of the reference circle, change if needed


  cnt_trier = sorted(countour_liste, key=cv2.contourArea)

  #aire du plus gros cercle
  (x1,y1),radDE = cv2.minEnclosingCircle(cnt_trier[len(cnt_trier)-1])
  DE = radDE*2
  print("Diamètre Extérieur:", DE)
  print("En métrique: ", DE/pixelsPerMetric)

  #aire du plus petit cercle
  (x2,y2),radDI = cv2.minEnclosingCircle(cnt_trier[0])
  DI = radDI*2
  print("Diamètre Intérieur:", DI)
  print("En métrique: ", DI/pixelsPerMetric)
  
  coordinées_centre = (int(x1),int(y1)) #type int est requis
  rayonDE = int(radDE) #type int est requis
  rayonDI = int(radDI) #type int est requis
  vert = (0,255,0)
  rouge = (0,0,255)
  epaisseur = 3
  image = cv2.circle(image, coordinées_centre, rayonDE, vert, epaisseur)
  image = cv2.circle(image, coordinées_centre, rayonDI, rouge, epaisseur)



  cv2_imshow(image)

  dimensions = [DE, DI]
  return dimensions

reconnaissance(image_raw)
