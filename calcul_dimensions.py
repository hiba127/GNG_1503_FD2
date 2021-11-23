import cv2
import numpy as np
from google.colab.patches import cv2_imshow

image_raw = cv2.imread("/content/drive/MyDrive/Colab Notebooks/tape.jpg") //change address of image

def reconnaissance(image):

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

  cnt_trier = sorted(countour_liste, key=cv2.contourArea)

  #aire du plus gros cercle
  (x1,y1),radDE = cv2.minEnclosingCircle(cnt_trier[len(cnt_trier)-1])
  DE = radDE*2
  print("Diamètre Extérieur:", DE)
  print("En métrique (mm): ", DE/pixelsPerMetric)

  #aire du plus petit cercle
  (x2,y2),radDI = cv2.minEnclosingCircle(cnt_trier[0])
  DI = radDI*2
  print("Diamètre Intérieur:", DI)
  print("En métrique (mm): ", DI/pixelsPerMetric)
  
  coordinées_centre = (int(x1),int(y1)) #type int est requis
  rayonDE = int(radDE) #type int est requis
  rayonDI = int(radDI) #type int est requis
  vert = (0,255,0)
  rouge = (0,0,255)
  epaisseur = 3
  image = cv2.circle(image, coordinées_centre, rayonDE, vert, epaisseur)
  image = cv2.circle(image, coordinées_centre, rayonDI, rouge, epaisseur)

  cv2_imshow(image)

reconnaissance(image_raw)
