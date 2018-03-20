#!/usr/bin/env python
#
# Project: Video Streaming with Flask
# Author: Log0 <im [dot] ckieric [at] gmail [dot] com>
# Date: 2014/12/21
# Website: http://www.chioka.in/
# Description:
# Modified to support streaming out with webcams, and not just raw JPEGs.
# Most of the code credits to Miguel Grinberg, except that I made a small tweak. Thanks!
# Credits: http://blog.miguelgrinberg.com/post/video-streaming-with-flask
#
# Usage:
# 1. Install Python dependencies: cv2, flask. (wish that pip install works like a charm)
# 2. Run "python main.py".
# 3. Navigate the browser to the local webpage.
from flask import Flask, render_template, Response, send_file
from camera import VideoCamera
import time #add
import threading
import cv2
import StringIO, numpy
from PIL import Image
from connet import Connet

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def gen():
    while True:
        time.sleep(0.1)
	try:
		with open('output.jpg', 'rb') as img_bin:
			buff = StringIO.StringIO()
			buff.write(img_bin.read())
			buff.seek(0)
			temp_img = numpy.array(Image.open(buff), dtype=numpy.uint8)
			frame = cv2.cvtColor(temp_img, cv2.COLOR_RGB2BGR)
		#frame = cv2.imread('output.jpg',1)

		ret,jpeg = cv2.imencode('.jpg', frame)
		jpeg = jpeg.tobytes()
		yield (b'--frame\r\n'
       			b'Content-Type: image/jpeg\r\n\r\n' + jpeg + b'\r\n\r\n')


	except:
		pass

@app.route('/video_feed')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

#add image
@app.route('/get_image')
def get_image():
    return send_file('capture.jpg', mimetype='image/gif')

def thread():
    vc = VideoCamera()
    cn = Connet()
    t1 = threading.Thread(target=vc.Camera, args=())
    t2 = threading.Thread(target=cn.sock, args=())
    t1.daemon = True
    t2.daemon = True
    t1.start()
    t2.start()

def run():
    app.run(host = '0.0.0.0', debug = True)

if __name__ == '__main__':
    #vc = VideoCamera()
    #cn = Connet()
    #t1 = threading.Thread(target=vc.Camera, args=())
    #t2 = threading.Thread(target=cn.sock, args=())
    #t1.daemon = True
    #t2.daemon = True
    #t1.start()
    #t2.start()
    thread()
    run()
