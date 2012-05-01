import re

from util import hook, http, pystuff
import usertracking
import sys

import time

re_lineends = re.compile(r'[\r\n]*')


@hook.command
def python(inp, prefix="direct call", conn=None, nick=None):
    ".python <prog> -- executes python code <prog>"

    pywu = pystuff.warmup()
    res = http.get("http://eval.appspot.com/eval", statement=inp, nick=prefix).splitlines()
    ret = pystuff.parse(res)
    if not ret:
        ret = "No result!"
    return ret

@hook.command
def ply(inp, bot=None, input=None, nick=None, db=None, chan=None):
    "execute local python - only admins can use this"
    if not usertracking.query(db, bot.config, nick, chan, "ply"):
        return "nope"
    try:
        _blah = dict(globals())
	_blah.update(input)
	_blah.update(locals())
        exec inp in _blah
        return _blah["_r"] if "_r" in _blah else None
    except:
        import traceback
        s = traceback.format_exc()
        sp = [x for x in s.split("\n") if x]
        if len(sp) > 2: sp = sp[-2:]
        for i in sp:
            input.notice(i)
