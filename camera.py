#-*- coding: utf-8 -*-
import argparse
import datetime
import imutils
import time
import cv2
import threading
import os
from timer import TimeRecord
from push import push
from example_utf8_sendsms  import sendsms

class VideoCamera(object):
	def __init__(self):
		self.ap = argparse.ArgumentParser()
		self.ap.add_argument("-v", "--video", help="path to the video file")
		self.ap.add_argument("-a", "--min-area", type=int, default=1500, help="minimum area size")
		self.args = vars(self.ap.parse_args())
		os.system("sudo modprobe bcm2835-v4l2")
		self.frame = None
		self.grebbed = None
		self.gray = None
		self.text = None
		self.autotext = None
		self.frameDelta = None
		self.thresh = None
		self.timer = TimeRecord()
		self.pushAL = push()

		self.x = None
		self.y = None
		self.ii = 1

		if self.args.get("video", None) is None:
			self.camera = cv2.VideoCapture(0)
			time.sleep(0.25)

		else:
			self.camera = cv2.VideoCapture(self.args["video"])

		self.firstFrame = None

		if os.path.exists("auto.txt")==False:
			os.system("touch auto.txt")

	def __del__(self):
		self.cemera.release()
		cv2.destroyAllWindows()

	def getFrame(self):
		(self.grabbed, self.frame) = self.camera.read()
		self.frame = cv2.flip(self.frame,0)
		self.frame = cv2.flip(self.frame,1)
		self.text = ""

	def resizeFrame(self):
		self.frame = imutils.resize(self.frame, width=350)
		self.gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
		self.gray = cv2.GaussianBlur(self.gray, (21, 21), 0)

	def showFrame(self,frame,thresh,frameDelta):
		cv2.imshow("Security Feed", frame)
		cv2.imshow("Thresh", thresh)
		cv2.imshow("Frame Delta", frameDelta)

	def di(self):
		if self.ii == 1:
			time.sleep(5)
			self.ii = 0

		if self.x >= 0 and self.x <= 146 and self.y >=0 and self.y <= 111:
			self.x = None
			self.y = None
			os.system("touch leftup.txt")

		elif self.x >= 0 and self.x <= 146 and self.y >111 and self.y <= 148:
			self.x = None
			self.y = None
			os.system("touch left.txt")

		elif self.x >= 0 and self.x <= 146 and self.y >148:
			self.x = None
			self.y = None
			os.system("touch leftdown.txt")

		elif self.x > 146 and self.x <=195 and self.y >=0 and self.y <=111:
			self.x = None
			self.y = None
			os.system("touch up.txt")

		elif self.x >146 and self.x <= 195 and self.y >148:
			self.x = None
			self.y = None
			os.system("touch down.txt")

		elif self.x > 195 and self.y >=0 and self.y <=111:
			self.x = None
			self.y = None
			os.system("touch rightup.txt")

		elif self.x > 195 and self.y > 111 and self.y <= 148:
			self.x = None
			self.y = None
			os.system("touch right.txt")

		elif self.x > 195 and self.y >148:
			self.x = None
			self.y = None
			os.system("touch rightdown.txt")


	def motion(self):
		self.frameDelta = cv2.absdiff(self.firstFrame, self.gray)
		self.thresh = cv2.threshold(self.frameDelta ,67 , 255, cv2.THRESH_BINARY)[1]

		self.thresh = cv2.dilate(self.thresh, None, iterations=2)
		(_, cnts, _) = cv2.findContours(self.thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

		sense = None

		for c in cnts:
			if cv2.contourArea(c) < self.args["min_area"]:
				continue

			(x, y, w, h) = cv2.boundingRect(c)
			cv2.rectangle(self.frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
			self.text = "Something sensering now"

			sense = True

			self.x = x + w / 2
			self.y = y + h / 2

			break

		if self.timer.Record(sense) == True:
			print("이미지를 캡처합니다.")
			cv2.imwrite("capture.jpg", self.frame)
			self.pushAL.alarm()
			sendsms()

	def putText(self):
		cv2.putText(self.frame, "{}".format(self.text), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
		cv2.putText(self.frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"), (10, self.frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
		cv2.putText(self.frame, "{}".format(self.autotext), (self.frame.shape[1]-35, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 2)

	def Camera(self):
		while True:
			self.autotext = ""
			if os.path.exists("auto.txt"):
				self.autotext = "Auto"
				self.di()

			if os.path.exists("move2.txt"):
				self.firstFrame = None
				os.system("rm move.txt")
				os.system("rm move2.txt")
				continue

			self.getFrame()

			if not self.grabbed:
				break

			self.resizeFrame()

			if self.firstFrame is None:
				self.firstFrame = self.gray
				continue

			if os.path.exists("move.txt")==False:
				self.motion()

			cv2.imwrite("output.jpg",self.frame)

			self.putText()

			self.showFrame(self.frame,self.thresh,self.frameDelta)

			key = cv2.waitKey(1) & 0xFF
			if key == ord("q"):
				break
