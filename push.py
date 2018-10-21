#-*- coding: utf-8 -*-
from firebase import firebase
from pyfcm import FCMNotification

class push:
	def alarm(self):
		#python firebase
		self.firebase = firebase.FirebaseApplication("https://fcmpush-584cc.firebaseio.com/",None)
		self.tok = self.firebase.get("/message", None)

		#pyfcm
		self.push_service = FCMNotification(api_key="AAAAGuC81MY:APA91bFqkBCyttg2ssApIz4oN9OosVrtBO3S269UwVcNaEiGJWB-qfxKhE5IiB2L2KWrlvG_aZ1Dsocf_2IY_zxpR4ggE7Y5VaF_wR8uEs6oibA2GhWbUqx3NyrW2SYaSbqgVojcUJi8")

		self.result = self.push_service.notify_single_device(registration_id=self.tok, message_title="알림!!", message_body="무엇인가 감지되었습니다!!")
		print("푸쉬 전송!")
