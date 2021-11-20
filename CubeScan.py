import cv2
import numpy as np
import math

def empty(a):
    pass

def getContours(img, color, imgContour):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    for cnt in contours:
        area = cv2.contourArea(cnt)

        if area > 6000:
            #cv2.drawContours(imgContour, cnt, -1, (255,0,255), 3)

            # draw filled contour on black background
            cnt_mask = np.zeros_like(imgContour)
            cv2.drawContours(cnt_mask, [cnt], 0, (255,255,255), -1)

            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02*peri, True)
            x, y, w, h = cv2.boundingRect(approx)

            cv2.rectangle(imgContour, (x,y), (x+w,y+h), (0,255,0), 5)            

            cv2.putText(imgContour, color, (x, y+h//2), cv2.FONT_HERSHEY_COMPLEX, 
                        .4,(0,0,0), 1)

def StickerContor(sticker, color, imgContour):
    sticker = cv2.GaussianBlur(sticker,(9,9),1)
    # == find contors == 
    threshold1 = cv2.getTrackbarPos("Thres1", "param")
    threshold2 = cv2.getTrackbarPos("Thres2", "param")
    print(threshold1, threshold2)
    imgcanny = cv2.Canny(sticker, threshold1, threshold2) 
    kernel = np.ones((3,3))
    imgDil = cv2.dilate(imgcanny, kernel, iterations=1)

    getContours(imgDil, color, imgContour)

cap = cv2.VideoCapture(0)

cv2.namedWindow('param')
cv2.createTrackbar('Thres1', 'param', 80, 255, empty)
cv2.createTrackbar('Thres2', 'param', 110, 255, empty)

while True:
    ret, img = cap.read()
    #img = cv2.imread('test.png')
    imgContour = img.copy()

    # == sharpen Image ==
    kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    sharp = cv2.filter2D(img, -1, kernel)

    # Convert to HSV format and color threshold
    hsv = cv2.cvtColor(sharp, cv2.COLOR_BGR2HSV)

    # == Seperate Colors == 
    # Set minimum and maximum HSV values for each Color 
    # == Green ==
    GLower, GUpper = np.array([57, 81, 63]), np.array([93, 255, 255])
    GMask = cv2.inRange(hsv, GLower, GUpper)
    GSticker = cv2.bitwise_and(img, img, mask=GMask)
    GSticker = cv2.cvtColor(GSticker, cv2.COLOR_BGR2GRAY)
    StickerContor(GSticker, 'Green', imgContour)

    # == white == 
    WLower,WUpper = np.array([41, 0, 129]),np.array([178, 92, 236])
    WMask = cv2.inRange(hsv, WLower, WUpper)
    WSticker = cv2.bitwise_and(img, img, mask=WMask)
    WSticker = cv2.cvtColor(WSticker, cv2.COLOR_BGR2GRAY)
    StickerContor(WSticker, 'White', imgContour)

    # == blue == 
    BLower,BUpper = np.array([86, 132, 61]), np.array([166, 255, 255])
    BMask = cv2.inRange(hsv, BLower, BUpper)
    BSticker = cv2.bitwise_and(img, img, mask=BMask)
    BSticker = cv2.cvtColor(BSticker, cv2.COLOR_BGR2GRAY)
    StickerContor(BSticker, 'Blue', imgContour)

    # == yellow == 
    YLower,YUpper = np.array([13, 65, 140]),np.array([47, 255, 255])
    YMask = cv2.inRange(hsv, YLower, YUpper)
    YSticker = cv2.bitwise_and(img, img, mask=YMask)
    YSticker = cv2.cvtColor(YSticker, cv2.COLOR_BGR2GRAY)
    StickerContor(YSticker, 'Yellow', imgContour)

    # == Orange == 
    OLower,OUpper = np.array([4, 67, 152]),np.array([31, 255, 255])
    OMask = cv2.inRange(hsv, OLower, OUpper)
    OSticker = cv2.bitwise_and(img, img, mask=OMask)
    OSticker = cv2.cvtColor(OSticker, cv2.COLOR_BGR2GRAY)
    StickerContor(OSticker, 'Orange', imgContour)

    # == red == 
    RLower,RUpper = np.array([0, 151, 0]),np.array([40, 230, 232])
    RMask = cv2.inRange(hsv, RLower, RUpper)
    RSticker = cv2.bitwise_and(img, img, mask=RMask)

    StickerContor(RSticker, 'Red', imgContour)

    cv2.imshow("contour", imgContour)
    cv2.imshow("Green", GSticker)
    cv2.imshow("White", WSticker)
    cv2.imshow("Blue", BSticker)
    cv2.imshow("Yellow", YSticker)
    cv2.imshow("Orange", OSticker)
    cv2.imshow("Red", RSticker)

    if cv2.waitKey(1) == 27:
        break # esc to quit

cv2.destroyAllWindows()

