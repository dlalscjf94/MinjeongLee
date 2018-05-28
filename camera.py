#-*- coding: utf-8 -*-
# import the necessary packages
import argparse
import datetime
import imutils
import time
import cv2
import threading
import os
from timer import TimeRecord
from push import push
import coolsms
from example_utf8_sendsms  import sendsms

class VideoCamera(object):
    def __init__(self):
	# construct the argument parser and parse the arguments
	self.ap = argparse.ArgumentParser()
	self.ap.add_argument("-v", "--video", help="path to the video file")
	self.ap.add_argument("-a", "--min-area", type=int, default=8000, help="minimum area size")
	self.args = vars(self.ap.parse_args())
	os.system("sudo modprobe bcm2835-v4l2")
	self.frame = None
	self.grebbed = None
	self.gray = None
	self.text = None
	self.frameDelta = None
	self.thresh = None
	self.timer = TimeRecord()
	self.pushAL = push()

	# if the video argument is None, then we are reading from webcam
	if self.args.get("video", None) is None:
		self.camera = cv2.VideoCapture(0)
		time.sleep(0.25)

	# otherwise, we are reading from a video file
	else:
		self.camera = cv2.VideoCapture(self.args["video"])

	# initialize the first frame in the video stream
	self.firstFrame = None

    def __del__(self):
        self.cemera.release()
	cv2.destroyAllWindows()

    def getFrame(self):
	# grab the current frame and initialize the occupied/unoccupied
        # text
        (self.grabbed, self.frame) = self.camera.read()
        self.frame = cv2.flip(self.frame,0)
	self.frame = cv2.flip(self.frame,1)
        self.text = ""

    def resizeFrame(self):
        # resize the frame, convert it to grayscale, and blur it
        self.frame = imutils.resize(self.frame, width=350)
        self.gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        self.gray = cv2.GaussianBlur(self.gray, (21, 21), 0)

    def showFrame(self,frame,thresh,frameDelta):
        # show the frame and record if the user presses a key
        cv2.imshow("Security Feed", frame)
        cv2.imshow("Thresh", thresh)
        cv2.imshow("Frame Delta", frameDelta)

    def motion(self):
	# compute the absolute difference between the current frame and
        # first frame
        self.frameDelta = cv2.absdiff(self.firstFrame, self.gray)
        self.thresh = cv2.threshold(self.frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

        # dilate the thresholded image to fill in holes, then find contours
        # on thresholded image
        self.thresh = cv2.dilate(self.thresh, None, iterations=2)
        (_, cnts, _) = cv2.findContours(self.thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	sense = None

        # loop over the contours
        for c in cnts:
		# if the contour is too small, ignore it
		if cv2.contourArea(c) < self.args["min_area"]:
			continue

		# compute the bounding box for the contour, draw it on the frame,
		# and update the text
		(x, y, w, h) = cv2.boundingRect(c)
		cv2.rectangle(self.frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
		self.text = "Something sensering now"

		sense = True

	if self.timer.Record(sense) == True:
		print("이미지를 캡처합니다.")
		cv2.imwrite("capture.jpg", self.frame)
		self.pushAL.alarm()
		sendsms()

    def putText(self):
	# draw the text and timestamp on the frame
        cv2.putText(self.frame, "{}".format(self.text), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.putText(self.frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"), (10, self.frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)


    def Camera(self):
	while True:
		if os.path.exists("move2.txt"):
			self.firstFrame = None
			os.system("rm move.txt")
			os.system("rm move2.txt")
			continue

		self.getFrame()

		# if the frame could not be grabbed, then we have reached the end
		# of the video
		if not self.grabbed:
			break

		self.resizeFrame()

		# if the first frame is None, initialize it
		if self.firstFrame is None:
			self.firstFrame = self.gray
			continue

		if os.path.exists("move.txt")==False:
			self.motion()

		cv2.imwrite("output.jpg",self.frame)

		self.putText()

		self.showFrame(self.frame,self.thresh,self.frameDelta)

		# if the `q` key is pressed, break from the lop
		key = cv2.waitKey(1) & 0xFF
		if key == ord("q"):
			break
