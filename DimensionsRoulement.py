#Calcul des dimensions d'un roulement
#Par : Matthias Corbeil
#GNG1503 - Groupe FD2

import cv2
import numpy as np
from Fonctions import *

#"IMG_2412.jpg"
#"Bearing5-Lab5.jpg"

print("Mesure des dimensions... ")

imgR1 = cv2.imread("IMG_2502.jpg")
imgD = cv2.imread("IMG_2502.jpg")
#imgR2 = cv2.imread("IMG_2495.jpg")
#imgH = cv2.imread("IMG_2495.jpg")

diametres = []
hauteur = 0.0

mmPPD = dimReference(imgR1)
diametres = dimDiametres(imgD)
#mmPPH = dimReference(imgR2)
#hauteur = dimHauteur(imgH)

if imgR1.shape[0]>700 or imgR1.shape[1]>2000:
        imgR1 = resize(imgR1)

if imgD.shape[0]>700 or imgD.shape[1]>2000:
        imgD = resize(imgD)

#if imgR2.shape[0]>700 or imgR2.shape[1]>2000:
        #imgR2 = resize(imgR2)

#if imgH.shape[0]>700 or imgH.shape[1]>2000:
        #imgH = resize(imgH)

mesure = [(diametres[0]*mmPPD), (diametres[1]*mmPPD), (hauteur*mmPPD)]

print("mmPP Diamètres : ", mmPPD, " mm/px")
#print("mmPP Hauteur : ", mmPPH, " mm/px")
print("Diamètre Extérieur: ", diametres[0], " px")
print("Diamètre Intérieur: ", diametres[1], " px")
#print("Largeur: ", hauteur, " px")

print("")
print("Diamètre Extérieur: ", mesure[0], " mm")
print("Diamètre Intérieur: ", mesure[1], " mm")
#print("Largeur: ", mesure[2], " mm")

cv2.imshow("Reference pour les diametres", imgR1)
cv2.imshow("Diametres", imgD)
#cv2.imshow("Reference pour la largeur", imgR2)
#cv2.imshow("Largeur", imgH)
cv2.waitKey(0)
