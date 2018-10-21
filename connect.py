#-*- coding: utf-8 -*-
import socket
import os
from control import control
import time

class Connect:
	def __init__(self,p,t):
		self.contl = control(p,t)

	def motor(self,input_string):

		if input_string == "center":
			print("중앙(center)")
			self.contl.center()

		elif input_string == "up":
			print("위(up)")
			self.contl.up()

		elif input_string == "down":
			print("아래(down)")
			self.contl.down()

		elif input_string == "left":
			print("왼쪽(left)")
			self.contl.left()

		elif input_string == "right":
			print("오른쪽(right)")
			self.contl.right()

	def connection(self,input_string):
		if input_string == "start":
			os.system("touch connect.txt")
			print("클라이언트 : 연결하였습니다.")

		elif input_string == "end":
			os.system("rm connect.txt")
			print("클라이언트 : 종료하였습니다.")

	def autoSwitch(self,input_string):
		if input_string == "on":
			if os.path.exists("auto.txt")==False:
				os.system("touch auto.txt")
				print("Auto on")

		elif input_string == "off":
			if os.path.exists("auto.txt"):
				os.system("rm auto.txt")
				print("Auto off")

	def sock(self):
		HOST = ""
		PORT = 8888
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		print ('Socket created')
		s.bind((HOST, PORT))
		print ('Socket bind complete')
		s.listen(1)
		print ('Socket now listening')

		while True:
			conn, addr = s.accept()

			data = conn.recv(1024)
			data = data.decode("utf8").strip()
			if not data: break

			self.motor(data)

			self.connection(data)

			self.autoSwitch(data)

			conn.close()
		s.close()

	def auto(self):
		while True:
			time.sleep(0.5)
			if os.path.exists("leftup.txt"):
				self.motor("left")
				self.motor("up")
				os.system("rm leftup.txt")

			elif os.path.exists("left.txt"):
				self.motor("left")
				os.system("rm left.txt")

			elif os.path.exists("leftdown.txt"):
				self.motor("left")
				self.motor("down")
				os.system("rm leftdown.txt")

			elif os.path.exists("up.txt"):
				self.motor("up")
				os.system("rm up.txt")

			elif os.path.exists("down.txt"):
				self.motor("down")
				os.system("rm down.txt")

			elif os.path.exists("rightup.txt"):
				self.motor("right")
				self.motor("up")
				os.system("rm rightup.txt")

			elif os.path.exists("right.txt"):
				self.motor("right")
				os.system("rm right.txt")

			elif os.path.exists("rightdown.txt"):
				self.motor("right")
				self.motor("down")
				os.system("rm rightdown.txt")
