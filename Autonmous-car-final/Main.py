from LaneDetection import *
import cv2
import numpy as np
import asyncio
import websockets
import ObjectDetection


url = 'http://10.42.0.237:8080/shot.jpg'
urlCamera = "ws://10.42.0.134:38301"
points = np.float32([(-5, 150), (485, 150), (-5, 300), (485, 300)])
objectPoints = np.float32([(-5, 100), (485, 100), (-5, 280), (485, 280)])
points1 = np.float32([(-5, 190), (240, 190), (-5, 280), (240, 280)])
points2 = np.float32([(240, 190), (485, 190), (240, 280), (485, 280)])
leftCenterScreen = 150
rightCenterScreen = 350
initializeTrackbars()


async def main():
    async with websockets.connect(urlCamera, ping_timeout=None, ping_interval=None) as websocket:
        await websocket.send("desktop")
        while True:
            # USE SOCKET TO GET THE IMAGE AND CONVERT IT INTO A CV2 USABLE FORMAT
            await websocket.send("1")
            imgResp = await websocket.recv()
            imgNp = np.array(bytearray(imgResp), dtype=np.uint8)
            img = cv2.imdecode(imgNp, -1)

            # CHECK IF THERE IS ANY OBJECT
            orig = img.copy()
            h, w, c = img.shape
            colors = getValuesTrackbars()
            wrappedOrig = wrapImg(orig, objectPoints, w, h)
            thresholdImage = threshold(wrappedOrig, colors)
            edgedImage = ObjectDetection.findEdges(wrappedOrig)
            edgedContours = ObjectDetection.getImgContours(edgedImage)
            edgedBoxes, centers = ObjectDetection.getBoxes(edgedContours, wrappedOrig)
            orderList = ObjectDetection.takeDecision(wrappedOrig, centers, thresholdImage, leftCenterScreen
                                                     , rightCenterScreen)
            cv2.circle(wrappedOrig, (int(leftCenterScreen), int(100)), 8, (0, 0, 255), -1)
            cv2.circle(wrappedOrig, (int(rightCenterScreen), int(100)), 8, (0, 0, 255), -1)
            cv2.imshow("final img", wrappedOrig)
            cv2.resizeWindow('final img', 480, 320)
            if orderList is not None:
                print("it is in")
                for order in orderList:
                    await websocket.send(order)
                    await asyncio.sleep(0.4)

            # USE SOCKET TO GET ANOTHER THE IMAGE AND CONVERT IT INTO A CV2 USABLE FORMAT
            await websocket.send("1")
            imgResp = await websocket.recv()
            imgNp = np.array(bytearray(imgResp), dtype=np.uint8)
            img = cv2.imdecode(imgNp, -1)

            # GET THE LANE CURVE AND SEND IT TO THE CAR
            result = str(getLaneCurve(img, points, points1, points2))
            await websocket.send(result)
            await asyncio.sleep(0.6)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
asyncio.get_event_loop().run_until_complete(main())
