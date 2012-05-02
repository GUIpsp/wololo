import re

from util import hook, http, randout

@hook.command('wa')
@hook.command
def wolframalpha(inp, bot=None):
    ".wa <query> -- Computes <query> using Wolfram Alpha."
    api_key = bot.config.get("api", {}).get("wolframalpha")
    if api_key is None:
        return "I have a lazy owner, they won't even bother adding an API key! " + randout.fail() 

    url = 'http://api.wolframalpha.com/v2/query?format=plaintext'

    result = http.get_xml(url, input=inp, appid=api_key)
    fail = 'No results. ' + randout.fail()

    pod_texts = []
    for pod in result.xpath("//pod"):
        title = pod.attrib['title']
        if pod.attrib['id'] == 'Input':
            continue

        results = []
        for subpod in pod.xpath('subpod/plaintext/text()'):
            subpod = subpod.strip().replace('\\n', '; ')
            subpod = re.sub(r'\s+', ' ', subpod)
            if subpod:
                results.append(subpod)
        if results:
            pod_texts.append(title + ': ' + '|'.join(results))

    ret = '. '.join(pod_texts)

    if not pod_texts:
        return fail

    ret = re.sub(r'\\(.)', r'\1', ret)

    def unicode_sub(match):
        return unichr(int(match.group(1), 16))

    ret = re.sub(r'\\:([0-9a-z]{4})', unicode_sub, ret)

    if len(ret) > 430:
        ret = ret[:ret.rfind(' ', 0, 430)]
        ret = re.sub(r'\W+$', '', ret) + '...'

    if not ret:
        return fail

    return ret

