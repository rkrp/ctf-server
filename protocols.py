#!/usr/bin/env python

from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor
import validator
from random import randint
from db import *
import datetime

class FlagServer(Protocol):
	def __init__(self):
		self.invalid_flag = ["Nope! Flag is invalid :(",
							"Do you really call that a flag?",
							"^[0-9a-f{32}]$ Hmph!",
							"Well, lemme check... Nope, not a flag!",
							]
		self.expired_flag = ["Too late! Flag's gone :('",
							"Tough luck! Flag submission first, kadalai next!",
							"I only want cool new flags, not age-old ones like yours",
							]

		self.invalid_team = "Invalid Team number"
		self.invalid_syntax = "Submit flag in format:\nTEAM# 32-DIGIT-FLAG"
		self.congrats = "Congrats! You've earned yourself some points"
		self.own_flag = "You must be really really high."
						
	def dataReceived(self, data):
		data = data.strip()
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
			
		id_flag = self.is_flag_valid(team, flag)
		if id_flag:
			pwned(team, id_flag)
			self.send_msg("Got it! Valid Flag!")
			return

		if self.is_flag_expired(team, flag):
			self.say_expired_flag()
			return

		if self.is_own_flag(team, flag):
			self.send_msg(self.own_flag)
			return

		#If nothing is done :(
		self.send_msg("We know no flag by that name")
		return
			
	def	pwned(byteam, flagid):
		if Pwn.insert(id_team=byteam, id_flag=flagid).execute():
			return True
		else:
			return False

	def is_flag_valid(self, team, flag):
		try:
			expr = ((Flag.doc_time >= datetime.datetime.now() - \
				datetime.timedelta(minutes=15)) and Flag.id_team != team \
				and Flag.flag == flag)
			db_flag = Flag.get(expr)
			return db_flag.id_flag
		except Flag.DoesNotExist:
			return False

	def is_flag_expired(self, team, flag):
		try:
			expr = (Flag.doc_time < datetime.datetime.now() - \
				datetime.timedelta(minutes=15)) and Flag.id_team != team \
				and Flag.flag == flag
			Flag.get(expr)
			return True
		except Flag.DoesNotExist:
			return False

	def is_own_flag(self, team, flag):
		try:
			Flag.get(Flag.flag == flag and Flag.id_team == team)
			return True
		except:
			return False

	def say_invalid_flag(self):
		msg_index = randint(0, len(self.invalid_flag) - 1)
		self.send_msg(self.invalid_flag[msg_index])

	def say_expired_flag(self):
		msg_index = randint(0, len(self.expired_flag) - 1)
		self.send_msg(self.expired_flag[msg_index])

	def say_invalid_syntax(self):
		self.send_msg(self.invalid_syntax)

	def say_invalid_team(self):
		self.send_msg(self.invalid_team)

	def send_msg(self, msg, disconnect=True):
		self.transport.write(msg + "\n")
		if disconnect:
			self.transport.loseConnection()
