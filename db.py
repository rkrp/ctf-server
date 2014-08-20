#!/usr/bin/env python

import CTFConfig
from peewee import *

db = MySQLDatabase(CTFConfig.DB.db_name,
				user=CTFConfig.DB.username,
				passwd=CTFConfig.DB.password
	)

class Team(Model):
	id_team = IntegerField(primary_key=True, index=True)
	team_name = CharField()
	
	class Meta:
		database = db

class Service(Model):
	id_service = IntegerField(primary_key=True, index=True)
	service_name = CharField()
	port = IntegerField()

	class Meta:
		database = db

class Flag(Model):
	id_flag = IntegerField(primary_key=True)
	flag = CharField(max_length=32, index=True, unique=True)
	id_team = IntegerField()
	doc_time = DateTimeField()

	class Meta:
		database = db

class Pwn(Model):
	id_pwn = IntegerField(primary_key=True, index=True)
	id_team = IntegerField()
	id_flag = IntegerField()
	pwn_time = DateTimeField()

	class Meta:
		database = db
