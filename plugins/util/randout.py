#thank you lembas for the fancy ascii
from random import choice
enable = True

if enable:
	asuccess = ['\o/','\o','o/','8D','=D','（ ﾟーﾟ)','(〜￣▽￣)〜',':D','o7',':DDDDDDDDDDDDD']
	afail = ['（ ´_ゝ｀）','(　ﾟ,_ゝ,ﾟ)','=(',':(',':<',':\'(','D:','DDD:','ಠ_ಠ']
	def success():
		return choice(asuccess)
	def fail():
		return choice(afail)
else:
	def success():
		return False
	def fail():
		return False