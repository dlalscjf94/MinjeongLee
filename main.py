from flask import Flask, render_template, Response, send_file
from camera import VideoCamera
import time
import threading
import cv2
import StringIO, numpy
from PIL import Image
from connect import Connect
import RPi.GPIO as GPIO

pan_pwn = 18
till_pwn = 4

GPIO.setmode(GPIO.BCM)
GPIO.setup(pan_pwn, GPIO.OUT)
GPIO.setup(till_pwn, GPIO.OUT)

p = GPIO.PWM(pan_pwn, 15)
t = GPIO.PWM(till_pwn, 15)

p.start(0)
t.start(0)

p.ChangeDutyCycle(1.8)
time.sleep(1)
p.start(0)

t.ChangeDutyCycle(1.7)
time.sleep(1)
t.start(0)

app = Flask(__name__)

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

def thread():
	cn = Connect(p,t)
	vc = VideoCamera()
	t1 = threading.Thread(target=vc.Camera, args=())
	t2 = threading.Thread(target=cn.sock, args=())
	t3 = threading.Thread(target=cn.auto, args=())
	t1.daemon = True
	t2.daemon = True
	t3.daemon = True
	t1.start()
	t2.start()
	t3.start()

def run():
	app.run(host = '0.0.0.0', debug = False)

if __name__ == '__main__':
	thread()
	run()
