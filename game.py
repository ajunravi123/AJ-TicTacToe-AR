import cv2
import random
import winsound
import math
import mediapipe as mp
import numpy as np

cap = cv2.VideoCapture(0)
# cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 9)
# cap.set(cv2.CAP_PROP_EXPOSURE, -7.0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
dotX = 50
dotY = 153
rect1_X1 = 400
rect1_Y1 = 13
rect_wid = 20
rect_len = 170
clr1 = (255, 165, 199)

bartipX = rect1_X1 + 48
bartipY = rect1_Y1
vbar = 20

org = (rect1_X1 + rect_len + 10, rect1_Y1 + rect_wid - 2)
fontScale = 0.8
color = (255, 0, 0)
thickness = 2
radiFix = 100
radi = int((vbar / 100) * radiFix)
bx = radi
selected_cir = 0
font = cv2.FONT_HERSHEY_SIMPLEX
Aclr = (255,115,5)
Bclr = (5,115,225)
cdif = 3
circles = [{"radi":radi, "dotX": dotX, "dotY": dotY, "ciclr": Aclr, "user": "A"}, {"radi":radi, "dotX": dotX, "dotY": dotY + 100, "ciclr": Aclr, "user": "A"}, {"radi":radi, "dotX": dotX, "dotY": dotY + 200, "ciclr": Aclr, "user": "A"},
          {"radi":radi - cdif, "dotX": dotX + 500, "dotY": dotY, "ciclr": Bclr, "user": "B"}, {"radi":radi - cdif, "dotX": dotX + 500, "dotY" : dotY + 100, "ciclr": Bclr, "user": "B"}, {"radi":radi - cdif, "dotX": dotX + 500, "dotY": dotY + 200, "ciclr": Bclr, "user": "B"}]

addcir_x = 10
addcir_y = 10
addcir_len = 20
precirX = dotX
minfix = 10
AC = []
BC = []
            
stop = False   
stopX1 = None
stopY1 = None
stopClr = None

cfingX = 0
cfingY = 0
tfingX = 0
tfingY = 0

asking = False
btnX = 190
btnLen = 70

cancelClr = (196,0, 0)
okClr = (196,0, 0)
btClr = (196,0, 0)

glen = 360
gx = 130
gy = 70
gp = int(glen / 3)
tik = 3


def handInCheck(fx, fy, gx, gy, gp, radi):
    if fx != None or fy != None or gx != None or gy != None or gp != None or radi != None:
        return True
    elif ( fx > gx and fx < (gx + gp + gp + gp) and fy > gy and fy < gy + gp + gp + gp ):
        return True
    else:
        return False
    
def collinear(p0, p1, p2):
    x1, y1 = p1[0] - p0[0], p1[1] - p0[1]
    x2, y2 = p2[0] - p0[0], p2[1] - p0[1]
    return abs(x1 * y2 - x2 * y1) < 1e-12

def sucessCheck(cpoints,iniX, minX, maxX, minY, maxY):
    flag = False
    for po in cpoints:
        if po[0] == iniX or po[0] < minX or po[0] > maxX or po[1] < minY or po[1] > maxY:
            flag = True
            break
            
    if flag == True:
        return False
    elif len(cpoints) != 3:
        return False
    else:
        return collinear(cpoints[0], cpoints[1], cpoints[2])
    
def pointInRect(point,rect):
    x1, y1, w, h = rect
    x2, y2 = x1+w, y1+h
    x, y = point
    if (x1 < x and x < x2):
        if (y1 < y and y < y2):
            return True
    return False
    
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    if asking == False:
        cv2.line(img, (gx, gy), (gx, gy + glen), (0, 255, 0), thickness=tik)
        cv2.line(img, (gx, gy), (gx + glen, gy), (0, 255, 0), thickness=tik)
        cv2.line(img, (gx, gy + glen), (gx + glen, gy + glen), (0, 255, 0), thickness=tik)
        cv2.line(img, (gx + glen, gy), (gx + glen, gy + glen), (0, 255, 0), thickness=tik)

        cv2.line(img, (gx + gp, gy), (gx + gp, gy + glen), (0, 255, 0), thickness=tik)
        cv2.line(img, (gx + gp + gp, gy), (gx + gp + gp, gy + glen), (0, 255, 0), thickness=tik)

        cv2.line(img, (gx, gy + gp), (gx + glen, gy + gp), (0, 255, 0), thickness=tik)
        cv2.line(img, (gx, gy + gp + gp), (gx + glen, gy + gp + gp), (0, 255, 0), thickness=tik)

        if stop == True and stopX1 != None and stopY1 != None:
            cv2.line(img, (stopX1, stopY1), (stopX2, stopY2), stopClr, thickness=tik)
            cv2.line(img, (stopX1, stopY1), (stopmx1, stopmy1), stopClr, thickness=tik)
    
    if asking == True:
        font = cv2.FONT_HERSHEY_SIMPLEX
        blk = np.zeros(img.shape, np.uint8)
        cv2.rectangle(blk, (145, 115), (470, 325), (184,0,0), cv2.FILLED)
        out = cv2.addWeighted(img, 1.0, blk, 11, 20)
        img = out
        cv2.putText(img, 'Do you want to Restart the game?', (btnX - 20, btnX - btnLen  + 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)

        cv2.rectangle(img, (btnX, btnX + 50), (btnX + btnLen, btnX + 80), cancelClr, cv2.FILLED)
        cv2.putText(img, 'Cancel', (btnX + 10, btnX + btnLen), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,212), 1)

        cv2.rectangle(img, (btnX + 150, btnX + 50), (btnX + 150 + btnLen, btnX + 80), okClr, cv2.FILLED)
        cv2.putText(img, 'Restart', (btnX + 150 + 10, btnX + btnLen), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,212), 1)
    else:
        cv2.rectangle(img, (530, 10), (530 + 80, 30), btClr, cv2.FILLED)
        cv2.putText(img, 'Restart', (530 + 10, 10 + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,212), 1)
            
    if results.multi_hand_landmarks: 
        for handLms in results.multi_hand_landmarks:
            flg = 0
            cfingX = None
            cfingY = None
            tfingX = None
            tfingY = None
            std = False
            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                cnt = 0
                #************Ball Drag Check***********
                rect3 = [530, 10, 80, 20]
                if asking == True and id == 8:
                    rect1 = [btnX, btnX + 50, btnLen, 30]
                    rect2 = [btnX + 150, btnX + 50, btnLen, 30]
                    if pointInRect([cx, cy],rect1):
                        cancelClr = (0,0,0)
                        asking = False
                        stop = False
                        winsound.Beep(2000, 100)
                    elif pointInRect([cx, cy],rect2):
                        okClr = (0,0,0)
                        circles = [{"radi":radi, "dotX": dotX, "dotY": dotY, "ciclr": Aclr, "user": "A"}, {"radi":radi, "dotX": dotX, "dotY": dotY + 100, "ciclr": Aclr, "user": "A"}, {"radi":radi, "dotX": dotX, "dotY": dotY + 200, "ciclr": Aclr, "user": "A"},
          {"radi":radi - cdif, "dotX": dotX + 500, "dotY": dotY, "ciclr": Bclr, "user": "B"}, {"radi":radi - cdif, "dotX": dotX + 500, "dotY" : dotY + 100, "ciclr": Bclr, "user": "B"}, {"radi":radi - cdif, "dotX": dotX + 500, "dotY": dotY + 200, "ciclr": Bclr, "user": "B"}]
                        asking = False
                        stop = False
                        winsound.Beep(2000, 100)
                    else:
                        cancelClr = btClr
                        okClr = btClr
                elif pointInRect([cx, cy],rect3):
                    asking = True
                    stop = True
                    winsound.Beep(2000, 100)
                elif (id == 8 or id == 4) and len(circles) > 0: # and cfingX != None and tfingX != None:
                    if id == 8:
                        cfingX = cx
                        cfingY = cy
                    if id == 4:
                        tfingX = cx
                        tfingY = cy
                    if cfingX != None and tfingX != None:
                        dist = int(math.dist([cfingX, cfingY], [tfingX, tfingY]))
                        for cir in circles:
                            if (dist < 30 and id == 8 or id == 4) and (cx < (cir["dotX"] + cir["radi"]) and cx > (cir["dotX"] - cir["radi"])) and (cy < (cir["dotY"] + cir["radi"]) and cy > (cir["dotY"] - cir["radi"]) ):
                                circles[cnt]["dotX"] = cx
                                circles[cnt]["dotY"] = cy
                                if selected_cir != cnt:
                                    winsound.Beep(2000, 100)
                                selected_cir = cnt
                                bartipX   = int((circles[cnt]["radi"] / radiFix) * (rect_len - 10) + rect1_X1)
                                stop = False
                                std = True
                                break
                            cnt = cnt + 1
  
                mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
                if std == True:
                    break
    
    
    if asking == False:
        #*********Centralizing the balls*************
        minfix = 10
        AC = []
        BC = []
        for cir in circles:
            if cir["user"] == "A":
                AC.append([cir["dotX"], cir["dotY"]])
            elif cir["user"] == "B":
                BC.append([cir["dotX"], cir["dotY"]])
            if cfingX != None and tfingX != None:
                dist = int(math.dist([cfingX, cfingY], [tfingX, tfingY]))
            else:
                dist = 0
            if handInCheck(cfingX, cfingY, gx, gy, gp, radi) == False or dist > 30 or dist == 0:
                cmidX = cir["dotX"]
                cmidY = cir["dotY"]
                parts = [0,1,2]
                for pt in parts:
                    if cmidX > gx + int(pt * gp) + minfix and cmidX < (gx + int(pt * gp) + gp - minfix) and cmidY > gy + minfix and cmidY < gy + gp - minfix:
                        cir["dotX"] = gx + int(gp / 2) + (pt * gp)
                        cir["dotY"] = gy + int(gp / 2)
                    if cmidX > gx + int(pt * gp) + minfix and cmidX < (gx + int(pt * gp) + gp - minfix) and cmidY > gy + gp + minfix and cmidY < gy + gp + gp - minfix:
                        cir["dotX"] = gx + int(gp / 2) + (pt * gp)
                        cir["dotY"] = gy + int(gp / 2) +  gp
                    if cmidX > gx + int(pt * gp) + minfix and cmidX < (gx + int(pt * gp) + gp - minfix) and cmidY > gy + gp + gp + minfix and cmidY < gy + gp + gp + gp - minfix:
                        cir["dotX"] = gx + int(gp / 2) + (pt * gp)
                        cir["dotY"] = gy + int(gp / 2) +  gp + gp

            cv2.circle(img, (cir["dotX"], cir["dotY"]), cir["radi"], cir["ciclr"], cv2.FILLED)
    
    #*********Success Check Added Here***********
    minX = gx
    maxX = gx + glen
    minY = gy
    maxY = gy + glen
    if stop == False and len(AC) > 0 and len(BC) > 0:
        if sucessCheck(AC,dotX, minX, maxX, minY, maxY):
            print("Winner: A")
            stopX1 = AC[0][0]
            stopY1 = AC[0][1]
            stopX2 = AC[1][0]
            stopY2 = AC[1][1]
            
            stopmx1 = AC[2][0]
            stopmy1 = AC[2][1]
            stopClr = Aclr
            winsound.Beep(2000, 200)
            stop = True
        elif sucessCheck(BC,dotX + 500, minX, maxX, minY, maxY):
            print("Winner: B")
            stopX1 = BC[0][0]
            stopY1 = BC[0][1]
            stopX2 = BC[1][0]
            stopY2 = BC[1][1]
            
            stopmx1 = BC[2][0]
            stopmy1 = BC[2][1]
            stopClr = Bclr
            winsound.Beep(2000, 200)
            stop = True
            
    cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
    cv2.setWindowProperty('frame', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    
    cv2.imshow("frame", img)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

    
cv2.destroyAllWindows()
cap.release()