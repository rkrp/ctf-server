from CTFConfig import CTFConfig
from db import *
#Initial bootstrap proces for creating tables in the DB

Team.create_table()
Flag.create_table()
Pwn.create_table()
Service.create_table()
