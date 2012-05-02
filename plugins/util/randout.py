#thank you lembas for the fancy ascii
from random import choice
enable = True

if enable:
	success = ['\o/','\o','o/','8D','=D','（ ﾟーﾟ)','(〜￣▽￣)〜',':D','o7',':DDDDDDDDDDDDD']
	fail = ['（ ´_ゝ｀）','(　ﾟ,_ゝ,ﾟ)','=(',':(',':<',':\'(','D:','DDD:','ಠ_ಠ']
	def success:
		return choice(success)
	def fail():
		return choice(fail)
else:
	def success():
		return False
	def fail():
		return False