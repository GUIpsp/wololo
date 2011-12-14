from util import hook
from collections import defaultdict, deque

class RollingDeque(deque):
    def __init__(self, *args, **keywords):
        deque.__init__(self, *args, **keywords)
        self.limit = 5
    def append(self, item):
        deque.append(self, item)
        if len(self) > self.limit:
            self.popleft()
    def countitem(self, item):
        count = 0
        for i in self:
            if i == item:
                count += 1
        return count


def check(conn, channel, user, message):
    try:
        tracker = conn.floodtracker
    except AttributeError:
        tracker = defaultdict(RollingDeque)
        conn.floodtracker = tracker
    chanuser = (channel, user)
    tracker[chanuser].append(message)
    if tracker[chanuser].countitem(message) > 2:
        return True
    return False

@hook.sieve
def sieve(bot, input, func, kind, args):
    if input.command == "PRIVMSG" and check(input.conn, input.chan.lower(), input.host, input.msg):
        return None
    return input
