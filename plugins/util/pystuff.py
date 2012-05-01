import http
import re
import sys
re_lineends = re.compile(r'[\r\n]*')

def warmup(code = "2+2", nick=None):
    preres = http.get("http://eval.appspot.com/eval",statement=code, nick=None)
    res = preres.splitlines()
    ret = parse(res)
    return ret

def parse(res):
    if len(res) > 0:
        res[0] = re_lineends.split(res[0])[0]
        if not res[0] == 'Traceback (most recent call last):':
            parsed = res[0].decode('utf8', 'ignore')
        else:
            parsed = res[-1].decode('utf8', 'ignore')
    else:
        parsed = None
    return parsed


def rexec(s, bot, input, db):
    try:
        exec(s)
    except:
        print s
        raise