#-*- coding: utf-8 -*-
import socket
import os
from control import control

class Connet:
#파이 컨트롤 함수
	def __init__(self,p,t):
		self.contl = control(p,t)
	def motor(self,input_string):
        	#라즈베리파이를 컨트롤할 명령어 설정
        	if input_string == "up":
                	print("위 입니다.")
			self.contl.up()
               		#파이 동작 명령 추가할것
        	elif input_string == "down":
                	print("아래 입니다.")
			self.contl.down()
        	elif input_string == "left":
                	print("왼쪽 입니다.")
			self.contl.left()
        	elif input_string == "right":
                	print("오른쪽 입니다.")
			self.contl.right()

	def connection(self,input_string):
		if input_string == "start":
			os.system("touch connect.txt")
			print("클라이언트 : 연결하였습니다.")

		elif input_string == "end":
			os.system("rm connect.txt")
			print("클라이언트 : 종료하였습니다.")

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
                	#접속 승인
                	conn, addr = s.accept()
                	print("Connected by ", addr)

                	#데이터 수신
                	data = conn.recv(1024)
                	data = data.decode("utf8").strip()
                	if not data: break
                	print("Received: " + data)

                	#수신한 데이터로 파이를 컨트롤 
                	self.motor(data)

			#클라이언트 연결 상태
			self.connection(data)

                	#연결 닫기
                	conn.close()
        	s.close()
