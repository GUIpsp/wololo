from util import hook
import socket

@hook.command
def resolve(inp, say=None):
	try:
		ips=set()
		for family, socktype, proto, canonname, sockaddr in socket.getaddrinfo(inp, None):
			ips.add(sockaddr[0])
		
		say(" ".join(ips))
	except socket.gaierror as e:
		say(e.args[1])

