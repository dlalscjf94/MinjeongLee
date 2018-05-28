#-*- coding: utf-8 -*-
import datetime
import os

class TimeRecord:
	def __init__(self):
		self.updateTimeHour = None
		self.updateTimeMin = None
		self.start = True
		self.record = False

	def Record(self, sense):
		if self.start == True and sense == True and os.path.exists("move.txt") == False:
			self.record = True
			firstTime = datetime.datetime.now()
			print("현재 시간을 기록합니다.")
			updateTime = firstTime + datetime.timedelta(minutes=5)
			self.updateTimeHour = updateTime.hour
			self.updateTimeMin = updateTime.minute
			self.start = False
			return True

		if self.record == True:
			current = datetime.datetime.now()
			currentHour = current.hour
			currentMin = current.minute
			if currentHour == self.updateTimeHour and currentMin == self.updateTimeMin:
				print("5분이 경과하였습니다.")
				self.record = False
				self.start = True

		return False
