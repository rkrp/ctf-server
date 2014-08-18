#!/usr/bin/env python
import re

def validate_flag(flag):
	return bool(re.match(r'^[0-9a-f]{32}$', flag))

def validate_team(team):
	return team.isdigit()
