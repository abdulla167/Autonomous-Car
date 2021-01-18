import cv2
import numpy as np


# ---------------------------------------------------------------------------------------------------------------------
# [Function Name] : getLaneCurve
# [Description] : This function is responsible for get the curve and take decision about the order for the car
# [Returns] : Return order for the car
# ----------------------------------------------------------------------------------------------------------------------
def getLaneCurve(img, points, points1, points2, socket=0):
    # step 1
    colors = getValuesTrackbars()
    imgThreshold = threshold(img, colors)
    # step 2
    h, w, c = img.shape
    wrappedImg = wrapImg(imgThreshold, points, w, h)
    cropped1 = wrapImg(imgThreshold, points1, w, h)
    cropped2 = wrapImg(imgThreshold, points2, w, h)
    # step 3
    basePoint, imgHistOriginal = getHistogram(wrappedImg, 0.5, 1)
    point, imgHis = getHistogram(wrappedImg, 0.5, 4)
    point1, imgHis1 = getMean(cropped1, 0.5, 4)
    point2, imgHis2 = getMean(cropped2, 0.5, 4)
    curve = basePoint - point
    deflect = point1 - point2
    cv2.imshow("Wrappedimg", wrappedImg)
    cv2.resizeWindow('Wrappedimg', 480, 320)

    if deflect < -4900:
        return "J"
    elif deflect > 4900:
        return "G"
    else:
        if -35 < curve < 35:
            return "F"
        elif curve >= 35:
            return "G"
        elif curve <= -35:
            return "J"
        else:
            return None


# ---------------------------------------------------------------------------------------------------------------------
# [Function Name] : threshold
# [Description] : This function is responsible for get exact color in the image and make all pixels of the other colors
#                 equal zero
# [Returns] : Image with threshold for exact color
# ----------------------------------------------------------------------------------------------------------------------
def threshold(image, colors):
    imgHSV = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    lower_white = np.array([colors[0], colors[1], colors[2]])
    upper_white = np.array([colors[3], colors[4], colors[5]])
    maskColor = cv2.inRange(imgHSV, lower_white, upper_white)
    return maskColor


# ---------------------------------------------------------------------------------------------------------------------
# [Function Name] : wrapImg
# [Description] : Wrap the image
# [Returns] : Image after wrapping
# ----------------------------------------------------------------------------------------------------------------------
def wrapImg(img, points, width, height):
    pts1 = np.float32(points)
    pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    imgWrap = cv2.warpPerspective(img, matrix, (width, height))
    return imgWrap


# ---------------------------------------------------------------------------------------------------------------------
# [Function Name] : getHistogram
# [Description] : Get the center position of the path
# [Returns] : Return the center point of the path and image contain this center point
# ----------------------------------------------------------------------------------------------------------------------
def getHistogram(img, minPer=0.1, region=1):
    if region == 1:
        histValue = np.sum(img, axis=0)
    else:
        histValue = np.sum(img[img.shape[0] // region:, :], axis=0)
    maxValue = np.max(histValue)
    minValue = minPer * maxValue
    indexArray = np.where(histValue >= minValue)
    basePoint = int(np.average(indexArray))
    imgHist = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    cv2.circle(imgHist, (basePoint, img.shape[0]), 20, (0, 255, 255), cv2.FILLED)
    return basePoint, imgHist


def getMean(img, minPer=0.1, region=1):
    if region == 1:
        histValue = np.sum(img, axis=0)
    else:
        histValue = np.sum(img[img.shape[0] // region:, :], axis=0)
        # print(histValue)
    maxValue = np.max(histValue)
    minValue = minPer * maxValue
    indexArray = np.where(histValue >= minValue)
    basePoint = int(np.average(histValue))
    imgHist = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    cv2.circle(imgHist, (basePoint, img.shape[0]), 20, (0, 255, 255), cv2.FILLED)
    return basePoint, imgHist


def nothing(a):
    pass


# ---------------------------------------------------------------------------------------------------------------------
# [Function Name] : initializeTrackbars
# [Description] : Make track bar to adjust the desired threshold color for the image
# [Returns] : Nothing
# ----------------------------------------------------------------------------------------------------------------------
def initializeTrackbars():
    cv2.namedWindow("HSV")
    cv2.resizeWindow("HSV", 360, 240)
    cv2.createTrackbar("HUE Min", "HSV", 98, 179, nothing)
    cv2.createTrackbar("HUE Max", "HSV", 144, 179, nothing)
    cv2.createTrackbar("SAT Min", "HSV", 0, 255, nothing)
    cv2.createTrackbar("SAT Max", "HSV", 255, 255, nothing)
    cv2.createTrackbar("VALUE Min", "HSV", 180, 255, nothing)
    cv2.createTrackbar("VALUE Max", "HSV", 255, 255, nothing)


# ---------------------------------------------------------------------------------------------------------------------
# [Function Name] : getValuesTrackbars
# [Description] : Get the values of the track bar
# [Returns] : Return list with the values of the track bar
# ----------------------------------------------------------------------------------------------------------------------
def getValuesTrackbars():
    h_min = cv2.getTrackbarPos("HUE Min", "HSV")
    h_max = cv2.getTrackbarPos("HUE Max", "HSV")
    s_min = cv2.getTrackbarPos("SAT Min", "HSV")
    s_max = cv2.getTrackbarPos("SAT Max", "HSV")
    v_min = cv2.getTrackbarPos("VALUE Min", "HSV")
    v_max = cv2.getTrackbarPos("VALUE Max", "HSV")
    return [h_min, s_min, v_min, h_max, s_max, v_max]
