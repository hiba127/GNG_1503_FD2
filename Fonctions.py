#Calcul des dimensions d'un roulement
#Par : Matthias Corbeil
#GNG1503 - Groupe FD2

import cv2
import numpy as np


def dimDiametres(img):

    grey = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    t, threshold = cv2.threshold(grey,135,255,cv2.THRESH_TOZERO)
    
    contours, hierarchy = cv2.findContours(threshold,cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)

    contour_liste = []

    
    
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
        n = len(approx)

        if (n>9) & (cv2.contourArea(cnt)>3000):
            (mx1,my1), rayE = cv2.minEnclosingCircle(cnt)
            mx1 = int(mx1)
            my1 = int(my1)
            if (mx1 > int(img.shape[1]/3)) & (mx1 < int(2*img.shape[1]/3)) & (my1 > int(img.shape[0]/3)) & (my1 < int(2*img.shape[0]/3)):
                cv2.drawContours(img,[cnt],0,(255,0,0),5)
                contour_liste.append(cnt)

    cnt_trier = sorted(contour_liste, key=cv2.contourArea)

    if len(cnt_trier)-1 < 1:
        threshold = resize(threshold)
        cv2.imshow("None Found", threshold)
        return 0

    #aire du plus gros cercle
    (x1,y1), rayE = cv2.minEnclosingCircle(cnt_trier[len(cnt_trier)-1])
    diaE = rayE*2
    M = cv2.moments(cnt_trier[len(cnt_trier)-1])
    cx1 = int(M['m10']/M['m00'])
    cy1 = int(M['m01']/M['m00'])

    #aire du plus petit cercle
    (x2,y2), rayI = cv2.minEnclosingCircle(cnt_trier[0])
    diaI = rayI*2
    M = cv2.moments(cnt_trier[0])
    cx2 = int(M['m10']/M['m00'])
    cy2 = int(M['m01']/M['m00'])

    #Constantes
    p = 1.1
    diaE = diaE*p
    

    coordCentreExt = (cx1, cy1) #type int est requis
    coordCentreInt = (cx2, cy2)
    rayE = int(rayE) #type int est requis
    rayI = int(rayI) #type int est requis
    vert = (22, 155, 98)
    rouge = (0,0,255)
    epaisseur = int(5*img.shape[0]/900)
    img = cv2.circle(img, coordCentreExt, rayE, vert, epaisseur)
    img = cv2.circle(img, coordCentreExt, rayI, vert, epaisseur)

    strExt = f'Exterieur = {"%.2f" % diaE}px'
    strInt = f'Interieur = {"%.2f" % diaI}px'

    cv2.putText(img, text= strExt, org=(100,150),
            fontFace= cv2.FONT_HERSHEY_PLAIN, fontScale=(2*img.shape[0]/900), color= rouge,
            thickness=2, lineType=cv2.LINE_AA)
    cv2.putText(img, text= strInt, org=(100,300),
            fontFace= cv2.FONT_HERSHEY_PLAIN, fontScale=(2*img.shape[0]/900), color= rouge,
            thickness=2, lineType=cv2.LINE_AA)


    threshold = resize(threshold)
    cv2.imshow("Greyscalling", threshold)
    dimensions = [diaE, diaI]
    return dimensions





def resize(img):
    if img.shape[0]>img.shape[1]:
        scale_percent = 600/img.shape[0] # percent of original size
    else:
        scale_percent = 900/img.shape[1]

    width = int(img.shape[1] * scale_percent)
    height = int(img.shape[0] * scale_percent)
    ImgDim = (width, height)

    # resize image
    img = cv2.resize(img, ImgDim, interpolation = cv2.INTER_AREA)
    return img






def dimHauteur(img):

    vert = (22, 155, 98)
    rouge = (0,0,255)
    bleu = (255,0,0)

    grey = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    t, threshold = cv2.threshold(grey,105,255,cv2.THRESH_TOZERO)

    contours, hierarchy = cv2.findContours(threshold,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

    contour_liste = []
    
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt,0.05*cv2.arcLength(cnt,False),True)
        n = len(approx)
        
        if (n>3) & (cv2.contourArea(cnt)>3000):
            (mx1,my1), rayE = cv2.minEnclosingCircle(cnt)
            mx1 = int(mx1)
            my1 = int(my1)
            if (mx1 > int(img.shape[1]/3)) & (mx1 < int(2*img.shape[1]/3)) & (my1 > int(img.shape[0]/3)) & (my1 < int(2*img.shape[0]/3)):
                cv2.drawContours(img,[cnt],0,(255,0,0),5)
                contour_liste.append(cnt)

    cnt_trier = sorted(contour_liste, key=cv2.contourArea)

    if len(cnt_trier) < 1:
        threshold = resize(threshold)
        cv2.imshow("None Found", threshold)
        return 0

    #aire du plus gros rectangle
    rect = cv2.minAreaRect(cnt_trier[len(cnt_trier)-1])
    (x1,y1), (w, b), angle = rect
    M = cv2.moments(cnt_trier[len(cnt_trier)-1])
    cx1 = int(M['m10']/M['m00'])
    cy1 = int(M['m01']/M['m00'])

    coordCentreExt = (cx1, cy1) #type int est requis

    if w < b:
        h = w
    elif b < w:
        h = b
    else:
        h = w

    c = 1.053
    w = int(w) #type int est requis
    b = int(b)
    h = h
        
    boite = cv2.boxPoints(rect)
    boite = np.int0(boite)
        
    epaisseur = int(5*img.shape[0]/900)
    img = cv2.polylines(img, [boite], True, vert, epaisseur)

    strH = f'Hauteur = {"%.2f" % h}px'
        

    cv2.putText(img, text= strH, org=(100, 150),
            fontFace= cv2.FONT_HERSHEY_PLAIN, fontScale=(2*img.shape[0]/900), color= rouge,
            thickness=2, lineType=cv2.LINE_AA)

    threshold = resize(threshold)
    cv2.imshow("Greyscalling", threshold)
        
    return h



def dimReference(img):
        
    vert = (22, 155, 98)
    rouge = (0,0,255)
    bleu = (255,0,0)
    mmPP = 0.0
    c = 1.1
    basVert = np.array([36,0,0])
    hautVert = np.array([86,255,255])

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, basVert, hautVert)
    

    contours, hierarchy = cv2.findContours(mask,2,1)
    contour_liste = []

    for cnt in contours:
        approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
        n = len(approx)

        if (n>9) & (cv2.contourArea(cnt)>3000):
            (mx1,my1), rayE = cv2.minEnclosingCircle(cnt)
            mx1 = int(mx1)
            my1 = int(my1)
            if (mx1 > int(img.shape[1]/3)) & (mx1 < int(2*img.shape[1]/3)) & (my1 < 2*int(img.shape[0]/5)):
                cv2.drawContours(img,[cnt],0,(255,0,0),5)
                contour_liste.append(cnt)

    cnt_trier = sorted(contour_liste, key=cv2.contourArea)

    if len(cnt_trier) < 1:
        mask = resize(mask)
        cv2.imshow("Aucunes Reference", mask)
        return 0

    (x1,y1), r = cv2.minEnclosingCircle(cnt_trier[len(cnt_trier)-1])
    dr = r*2
    M = cv2.moments(cnt_trier[len(cnt_trier)-1])
    cx1 = int(M['m10']/M['m00'])
    cy1 = int(M['m01']/M['m00'])

    mmPP = 20/dr*c
    coordCentre = (cx1,cy1)
    r = int(r)

    epaisseur = int(5*img.shape[0]/900)
    img = cv2.circle(img, coordCentre, r, vert, epaisseur)

    mask = resize(mask)
    cv2.imshow("Mask", mask)


    return mmPP


