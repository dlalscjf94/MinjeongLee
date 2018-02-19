#-*- coding: utf-8 -*-
# 위에줄 추가
import cv2
import os  #추가
import time #추가

class VideoCamera(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        os.system('sudo modprobe bcm2835-v4l2')  #추가(파이 카메라 모듈 인식)
        self.video = cv2.VideoCapture(0)
	    self.cascade = cv2.CascadeClassifier('/home/pi/opencv/opencv-3.4.0/data/haarcascades/haarcascade_frontalface_alt.xml') #추가(얼굴인식)
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')
    
    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        success, image = self.video.read()
	    image = cv2.flip(image,0)  #추가(카메라 뒤집기)
	    #gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
	    #gray = cv2.equalizeHist(gray)
	    #time.sleep(0.1)
	    rects = self.cascade.detectMultiScale(image, scaleFactor=1.1, minNeighbors=5, minSize=(30,30), flags=cv2.CASCADE_SCALE_IMAGE)

	for x, y, w, h in rects:
		cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()
