#!/usr/bin/env python

from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor
import validator
from random import randint

class FlagServer(Protocol):
	def __init__(self):
		self.invalid_flag = ["Nope! Flag is invalid :(",
							"Do you really call that a flag?",
							"^[0-9a-f]$ Hmph!",
							"Well, lemme check... Nope, not a flag!",
							]
		self.expired_flag = ["Too late! Flag's gone :('",
							"Tough luck! Flag submission first, kadalai next!",
							"I only want cool new flags, not age-old ones like yours",
							]

		self.invalid_team = "Invalid Team number"
		self.invalid_syntax = "Submit flag in format:\nTEAM# 32-DIGIT-FLAG"
						
	def dataReceived(self, data):
		self.data_parser(data)
		#self.transport.write(data)

	def data_parser(self, data):
		ret = data.split(" ")
		if not len(ret) == 2:
			self.say_invalid_syntax()
			return

		#Unpacking values from client
		team, flag = ret

		#Validate Team
		if not validator.validate_team(team):
			self.say_invalid_team()
			return
			
		#Validate flag
		if not validator.validate_flag(flag):
			self.say_invalid_flag()
			return
			
		self.send_msg('Congrats!')
						
	def say_invalid_flag(self):
		msg_index = randint(0, len(self.invalid_flag) - 1)
		self.send_msg(self.invalid_flag[msg_index])

	def say_invalid_syntax(self):
		self.send_msg(self.invalid_syntax)

	def say_invalid_team(self):
		self.send_msg(self.invalid_team)

	def send_msg(self, msg, disconnect=True):
		self.transport.write(msg + "\n")
		if disconnect:
			self.transport.loseConnection()
