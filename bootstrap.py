from CTFConfig import CTFConfig
import db

#Initial bootstrap proces for creating tables in the DB
Team.create_table()
Flag.create_table()
Pwn.create_table()
Service.create_table()
