# ----------------------------------------
# - mode: python - 
# - author: helloplhm-qwq - 
# - name: __init__.py - 
# - project: lx-music-api-server - 
# - license: MIT - 
# ----------------------------------------
# This file is part of the "lx-music-api-server" project.

from common import Httpx
from common import config
from .encrypt import eapiEncrypt
import ujson as json

tools = {
    'qualityMap': {
        '128k': 'standard',
        '320k': 'exhigh',
        'flac': 'loseless',
        'flac24bit': 'hires',
    },
    'cookie': config.read_config('module.wy.user.cookie'),
}

def url(songId, quality):
    path = '/eapi/song/enhance/player/url/v1'
    host = 'https://interface.music.163.com'
    req = Httpx.request(host + path, {
        'method': 'POST',
        'headers': {
            'Cookie': tools['cookie'],
        },
        'form': eapiEncrypt(path, json.loads({}))
    })
