#!/usr/bin/env python
from imutils.video import VideoStream
import argparse
import imutils
import time
import cv2
import sys
import serial

def drive(forward, left, led):
    if led == 0:
        print("RED AUTONOMOUS")
    elif led == 1:
        print("BLUE MANUELLY")
    elif led == 2:
        print("GREEN FLASH SUCCESSFUL")
    msg = "$" + f'{forward:.2f}' + "," + f'{left:.2f}' + "," + str(led) + ";"
    print(msg)
    #ser.write(msg.encode())
#    time.sleep(1)


#ser = serial.Serial("/dev/ttyTHS0", 38400, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE)

LINEARSPEED = 0.30
ANGULARSPEED = 0.42

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-t", "--type", type=str,
    default="DICT_4X4_1000",
    help="type of ArUCo tag to detect")
args = vars(ap.parse_args())

# define names of each possible ArUco tag OpenCV supports
ARUCO_DICT = {
    # nxn    cm
    "DICT_4X4_50": cv2.aruco.DICT_4X4_50,
    "DICT_4X4_100": cv2.aruco.DICT_4X4_100,
    "DICT_4X4_250": cv2.aruco.DICT_4X4_250,
    "DICT_4X4_1000": cv2.aruco.DICT_4X4_1000,
    "DICT_5X5_50": cv2.aruco.DICT_5X5_50,
    "DICT_5X5_100": cv2.aruco.DICT_5X5_100,
    "DICT_5X5_250": cv2.aruco.DICT_5X5_250,
    "DICT_5X5_1000": cv2.aruco.DICT_5X5_1000,
    "DICT_6X6_50": cv2.aruco.DICT_6X6_50,
    "DICT_6X6_100": cv2.aruco.DICT_6X6_100,
    "DICT_6X6_250": cv2.aruco.DICT_6X6_250,
    "DICT_6X6_1000": cv2.aruco.DICT_6X6_1000,
    "DICT_7X7_50": cv2.aruco.DICT_7X7_50,
    "DICT_7X7_100": cv2.aruco.DICT_7X7_100,
    "DICT_7X7_250": cv2.aruco.DICT_7X7_250,
    "DICT_7X7_1000": cv2.aruco.DICT_7X7_1000,
    "DICT_ARUCO_ORIGINAL": cv2.aruco.DICT_ARUCO_ORIGINAL,
#    "DICT_APRILTAG_16h5": cv2.aruco.DICT_APRILTAG_16h5,
#    "DICT_APRILTAG_25h9": cv2.aruco.DICT_APRILTAG_25h9,
#    "DICT_APRILTAG_36h10": cv2.aruco.DICT_APRILTAG_36h10,
#    "DICT_APRILTAG_36h11": cv2.aruco.DICT_APRILTAG_36h11
}

# verify that the supplied ArUCo tag exists and is supported by
# OpenCV
if ARUCO_DICT.get(args["type"], None) is None:
    print("[INFO] ArUCo tag of '{}' is not supported".format(
        args["type"]))
    sys.exit(0)

# load the ArUCo dictionary and grab the ArUCo parameters
print("[INFO] detecting '{}' tags...".format(args["type"]))
arucoDict = cv2.aruco.Dictionary_get(ARUCO_DICT[args["type"]])
arucoParams = cv2.aruco.DetectorParameters_create()

# initialize the video stream and allow the camera sensor to warm up
print("[INFO] starting video stream...")
vs = VideoStream(src=2).start()
time.sleep(2.0)
first = 1
sayac = time.time() - 20
son_hareket = 0 # 0 ise ileri , saga giderken 1, sol iken 2
# loop over the frames from the video stream
exitt = True
while exitt:
    # grab the frame from the threaded video stream and resize it
    # to have a maximum width of 600 pixels
    frame = vs.read()
    frame = imutils.resize(frame, width=1000)

    # detect ArUco markers in the input frame
    (corners, ids, rejected) = cv2.aruco.detectMarkers(frame,
        arucoDict, parameters=arucoParams)

    # verify *at least* one ArUco marker was detected
    if len(corners) > 0:
        first = 0 
        #yarismada gordugu en buyuk ArUco'yu baz almasi lazim
        dikler=[]
        #print(corners)

        #print("************************")
        for i in range(len(corners)):
            top_right = [int(corners[i][0][1][0]), int(corners[i][0][1][1])]
            bottom_right = [int(corners[i][0][2][0]), int(corners[i][0][2][1])]
            dik_dogru = bottom_right[1] - top_right[1]
            dikler.append(dik_dogru)
        biggest_index = dikler.index(max(dikler))
        #print(biggest_index)
        #print("************************")
        # flatten the ArUco IDs list
        ids = ids.flatten()

        # extract the marker corners (which are always returned
        # in top-left, top-right, bottom-right, and bottom-left
        # order)
        (topLeft, topRight, bottomRight, bottomLeft) = corners[biggest_index].reshape((4, 2))

        # convert each of the (x, y)-coordinate pairs to integers
        topRight = (int(topRight[0]), int(topRight[1]))
        bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
        bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
        topLeft = (int(topLeft[0]), int(topLeft[1]))
        print("topRight:{}, bottomRight:{},bottomLeft:{}, topLeft: {}".format(topRight, bottomRight,bottomLeft, topLeft))
        #print(bottomRight[0]-bottomLeft[0])
        # draw the bounding box of the ArUCo detection
        cv2.line(frame, topLeft, topRight, (0, 255, 0), 2)
        cv2.line(frame, topRight, bottomRight, (0, 255, 0), 2)
        cv2.line(frame, bottomRight, bottomLeft, (0, 255, 0), 2)
        cv2.line(frame, bottomLeft, topLeft, (0, 255, 0), 2)

        # compute and draw the center (x, y)-coordinates of the
        # ArUco marker
        cX = int((topLeft[0] + bottomRight[0]) / 2.0)
        cY = int((topLeft[1] + bottomRight[1]) / 2.0)

        cv2.circle(frame, (cX, cY), 4, (0, 0, 255), -1)

        # draw the ArUco marker ID on the frame
        cv2.putText(frame, str(ids[biggest_index]),
            (topLeft[0], topLeft[1] - 15),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5, (0, 255, 0), 2)
        print("Biggest ArUco -->> Center : {}     ID : {}        Side_length : {}".format((cX, cY), ids[biggest_index], int(dikler[biggest_index])))
#AHMET BURDAN ASAGISINA AYAR CEKILECEK
#BU KOD TEK ARUCO ICIN OLSUN CIFT ARUCO ICIN BUNU KOPYALAYIP BIR TANE DAHA YAP BENCE
        #buraya gelindiginde elimizde bir center var cX ve cY , Side_length var
        # oncelikle centeri ortalamali
        # ortalama kismi
        istenilen_koordinat_x = 500
        istenilen_dik = 75
        hata_payi_x = 75
    #center yukseklık 75 cm        uzaklık    110 cm ıken center        kamera 50cm yukarda            logide piksel (426, 121)    kosegen 250
        ortalandi = 0
        if cX > istenilen_koordinat_x+hata_payi_x:
            print("Right")
            drive(0, -ANGULARSPEED, 0)
            son_hareket = 1
        elif cX < istenilen_koordinat_x-hata_payi_x:
            drive(0, ANGULARSPEED, 0)
            print("Left")
            son_hareket = 2
        else:
            ortalandi += 1
        if ortalandi == 1:            #uzaklik
            dik_dogru = int(max(dikler))
            if dik_dogru < istenilen_dik:
                print("Forward")
                son_hareket = 0
                drive(LINEARSPEED, 0, 0)
            else:
                print("0.75 meters forward")
                drive(LINEARSPEED, 0, 0)
                time.sleep(1.5)
                print("Reaching")
                for i in range(10):
                    drive(0, 0, 2)
                print("Mission accomplished !!")
                exitt = False
        sayac = time.time()
    elif first==1:
        print("Right")
        drive(0, -ANGULARSPEED, 0)
    else:
        if time.time() - sayac > 19:
            print("Stop")
            first = 1
        drive(0, 0, 0)
 #   elif son_hareket == 1:
  #      print("sol")
   #     drive(0, ANGULARSPEED, 0)
  #  else:
   #     print("sag")
    #    drive(0, -ANGULARSPEED, 0)


    # show the output frame
#    cv2.imshow("Frame", frame)
#    key = cv2.waitKey(1) & 0xFF

    # if the `q` key was pressed, break from the loop
#    if key == ord("q"):
#        break

# do a bit of cleanup
#cv2.destroyAllWindows()
#vs.stop()
#ser.close()
"""
# loop over the detected ArUCo corners
for (markerCorner, markerID) in zip(corners, ids):
    # extract the marker corners (which are always returned
    # in top-left, top-right, bottom-right, and bottom-left
    # order)
    corners = markerCorner.reshape((4, 2))
    (topLeft, topRight, bottomRight, bottomLeft) = corners

    # convert each of the (x, y)-coordinate pairs to integers
    topRight = (int(topRight[0]), int(topRight[1]))
    bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
    bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
    topLeft = (int(topLeft[0]), int(topLeft[1]))

    # draw the bounding box of the ArUCo detection
    cv2.line(frame, topLeft, topRight, (0, 255, 0), 2)
    cv2.line(frame, topRight, bottomRight, (0, 255, 0), 2)
    cv2.line(frame, bottomRight, bottomLeft, (0, 255, 0), 2)
    cv2.line(frame, bottomLeft, topLeft, (0, 255, 0), 2)

    # compute and draw the center (x, y)-coordinates of the
    # ArUco marker
    cX = int((topLeft[0] + bottomRight[0]) / 2.0)
    cY = int((topLeft[1] + bottomRight[1]) / 2.0)
    print(cX, cY)
    cv2.circle(frame, (cX, cY), 4, (0, 0, 255), -1)

    # draw the ArUco marker ID on the frame
    cv2.putText(frame, str(markerID),
        (topLeft[0], topLeft[1] - 15),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5, (0, 255, 0), 2)
"""
