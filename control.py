#import RPi.GPIO as GPIO
import time
import os

class control:
	def __init__(self,p,t):
		self.pan_pwn = 18
		self.till_pwn = 4
		self.pan_default = 1.8
		self.till_default = 1.7
		self.pan_move = self.pan_default
		self.till_move = self.till_default
		self.move = 0.2
		#GPIO.setmode(GPIO.BCM)
		#GPIO.setup(self.pan_pwn, GPIO.OUT)
		#GPIO.setup(self.till_pwn, GPIO.OUT)

		#self.p = GPIO.PWM(self.pan_pwn, 30)
		#self.t = GPIO.PWM(self.till_pwn, 30)

		#self.p.start(0)
		#self.t.start(0)

		#self.default()

		self.p = p
		self.t = t

		self.p.start(0)
		self.t.start(0)

	def mv(self):
		os.system("touch move.txt")
		time.sleep(0.4)
		os.system("touch move2.txt")

	def center(self):
		os.system("touch move.txt")
		self.p.ChangeDutyCycle(self.pan_default)
		time.sleep(0.6)
		self.p.start(0)
		self.t.ChangeDutyCycle(self.till_default)
		time.sleep(0.6)
		self.t.start(0)
		#os.system("touch move.txt")
		time.sleep(0.7)
		os.system("touch move2.txt")
		self.pan_move = self.pan_default
		self.till_move = self.till_default

	def up(self):
		os.system("touch move.txt")
		self.till_move = self.till_move - self.move
		self.t.ChangeDutyCycle(self.till_move)
		time.sleep(0.5)
		self.t.start(0)
		self.mv()

	def down(self):
		os.system("touch move.txt")
		self.till_move = self.till_move + self.move
		self.t.ChangeDutyCycle(self.till_move)
		time.sleep(0.5)
		self.t.start(0)
		self.mv()

	def left(self):
		os.system("touch move.txt")
		self.pan_move = self.pan_move + self.move
		self.p.ChangeDutyCycle(self.pan_move)
		time.sleep(0.3)
		self.p.start(0)
		self.mv()

	def right(self):
		os.system("touch move.txt")
		self.pan_move = self.pan_move - self.move
		self.p.ChangeDutyCycle(self.pan_move)
		time.sleep(0.3)
		self.p.start(0)
		self.mv()
