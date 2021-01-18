import cv2
import imutils
import urllib.request
import numpy as np
from scipy.spatial import distance as dist


# ---------------------------------------------------------------------------------------------------------------------
# [Function Name] : getImage
# [Description] : This function is responsible for get the image from the video stream and format it into a cv2 usable
#                 format.
# [Returns] : Image received in the socket
# ----------------------------------------------------------------------------------------------------------------------
def getImage(websocket):
    # Use urllib to get the image and convert into a cv2 usable format
    await websocket.send("1")
    imgResp = await websocket.recv()
    imgNp = np.array(bytearray(imgResp), dtype=np.uint8)
    img = cv2.imdecode(imgNp, -1)
    return img


# ---------------------------------------------------------------------------------------------------------------------
# [Function Name] : findEdges
# [Description] : This function is responsible for apply some filters on the image and then get edges in the image.
# [Returns] : Images which contain edges of the original image
# ----------------------------------------------------------------------------------------------------------------------
def findEdges(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (1, 1), 0)
    edged = cv2.Canny(gray, 100, 400)
    edged = cv2.dilate(edged, None, iterations=1)
    edged = cv2.erode(edged, None, iterations=1)
    return edged


# ---------------------------------------------------------------------------------------------------------------------
# [Function Name] : getImgContours
# [Description] : This function is responsible for find contours around the detected objects
# [Returns] : List of contours in the input image
# ----------------------------------------------------------------------------------------------------------------------
def getImgContours(edged):
    # find contours in the edge map
    contours = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    contours = contours[0: (len(contours) - 1)]
    return contours


# ---------------------------------------------------------------------------------------------------------------------
# [Function Name] : getBoxes
# [Description] : This function is responsible for find boxes around each contour in the input list and center of
#                 this contour.
# [Returns] : List of boxes and centers of the detected objects
# ----------------------------------------------------------------------------------------------------------------------
def getBoxes(contours, orig):
    boxes = []
    centers = []
    for contour in contours:
        box = cv2.minAreaRect(contour)
        box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
        box = np.array(box, dtype="int")
        centerX, centerY = getBoxCenter(box)
        (tl, tr, br, bl) = box
        if 200 > (dist.euclidean(tl, bl)) > 50 and 50 < (dist.euclidean(tl, tr)) < 200:
            centers.append([centerX, centerY])
            boxes.append(box)
            cv2.drawContours(orig, [box.astype("int")], -1, (0, 255, 0), 2)
            cv2.circle(orig, (int(centerX), int(centerY)), 8, (0, 255, 255), -1)
    return boxes, centers


# ---------------------------------------------------------------------------------------------------------------------
# [Function Name] : getBoxCenter
# [Description] : This function is responsible for compute the center of the bounding box
# [Returns] : return center of input box
# ----------------------------------------------------------------------------------------------------------------------
def getBoxCenter(box):
    cX = np.average(box[:, 0])
    cY = np.average(box[:, 1])
    return cX, cY


# ---------------------------------------------------------------------------------------------------------------------
# [Function Name] : takeDecision
# [Description] : This function is responsible for take a dedicated decision if the camera found object
# [Returns] : return list of orders for the car according to the input image
# ----------------------------------------------------------------------------------------------------------------------
def takeDecision(orig, centers, thresImage, leftScreenCenter, rightScreenCenter):
    if len(centers) > 0 and int(centers[0][0]) < len(thresImage):
        laneIndices = np.where(thresImage[int(centers[0][0])] > 200)
        if len(laneIndices[0]) > 0:
            leftLane = laneIndices[0][0]
            rightLane = laneIndices[0][len(laneIndices[0]) - 1]
            cv2.circle(orig, (int(leftLane), int(centers[0][1])), 8, (0, 255, 255), -1)
            cv2.circle(orig, (int(rightLane), int(centers[0][1])), 8, (0, 255, 255), -1)
            leftWidth = centers[0][0] - leftLane
            rightWidth = rightLane - centers[0][0]
            if leftScreenCenter < centers[0][0] < rightScreenCenter:
                if leftWidth > 0 and rightWidth > 0:
                    if leftWidth > rightWidth:
                        print("L, F, F")
                        return ["L", "F", "F"]
                    else:
                        print("R, F, L")
                        return ["R", "F", "F"]
                elif leftWidth < 0 and rightWidth > 0:
                    if rightWidth > 250:
                        print("R, F, F")
                        return ["R" "F", "F"]
                    else:
                        print("L, F, F")
                        return ["L", "F", "F"]
                elif leftWidth > 0 and rightWidth < 0:
                    if leftWidth > 250:
                        print("L, F, F")
                        return ["L", "F", "F"]
                    else:
                        print("R, F, F")
                        return ["R", "F", "F"]
            return None
        return None
    return None
