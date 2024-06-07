import cv2 as cv

img = cv.VideoCapture(0)

params = cv.SimpleBlobDetector_Params()

params.filterByColor = 0

params.minThreshold = 10
params.maxThreshold = 200

params.filterByArea = True
params.minArea = 200
params.maxArea = 2000

params.filterByCircularity = True
params.minCircularity = 0.7

params.filterByConvexity = True
params.minConvexity = 0.87

params.filterByInertia = True
params.minInertiaRatio = 0.05
while True:
    ret, frame = img.read()

    detector = cv.SimpleBlobDetector_create(params)
    keypoints = detector.detect(frame)
    try:
        xKey = []
        yKey = []
        distanceX = []
        distanceY = []
        radius = 0

        for i in range(len(keypoints)):
            radius = keypoints[i].size/2
            xKey.append(keypoints[i].pt[0])
            yKey.append(keypoints[i].pt[1])
        
        xKey.sort()
        yKey.sort()

        # print(xKey)

        xLength = len(xKey)
        xQ1 = int(xLength * 0.25)
        xQ3 = int(xLength * 0.75)
        xIQR = (xQ3 - xQ1) * 1.5

        yLength = len(yKey)
        yQ1 = int(yLength * 0.25)
        yQ3 = int(yLength * 0.75)
        yIQR = (yQ3 - yQ1) * 1.5

        xReal = []
        yReal = []

        for i in range(len(xKey)):
            if i > xQ1 and i < xQ3:
                xReal.append(xKey[i])

        for i in range(len(yKey)):
            if i > yQ1 and i < yQ3:
                yReal.append(yKey[i])

        xKey.clear()
        yKey.clear()

        for i in range(len(xReal)):
            xKey.append(xReal[i])

        for i in range(len(yReal)):
            yKey.append(yReal[i])

        print(f'xReal: {yReal}')

        if len(xReal) > 4:
            cv.rectangle(frame, (int(min(xReal) - radius), int(min(yReal) - radius)), (int(max(xReal) + radius), int(max(yReal) + radius)), (0, 255, 0), 3)

            cx = int((min(xKey) + max(xKey))/2)
            cy = int((min(yKey) + max(yKey))/2)
        
            cv.circle(frame, (cx, cy), 20, (0, 255, 0))
        else:
            xKey.clear()
            yKey.clear()
            xReal.clear()
            yReal.clear()

    except:
        ret, frame = img.read()


    cv.imshow("FTC", frame)
    key = cv.waitKey(5) 
    if key == 27:
        break
img.release()
cv.destroyAllWindows()