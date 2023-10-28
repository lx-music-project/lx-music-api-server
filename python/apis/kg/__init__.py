# ----------------------------------------
# - mode: python - 
# - author: helloplhm-qwq - 
# - name: __init__.py - 
# - project: lx-music-api-server - 
# - license: MIT - 
# ----------------------------------------
# This file is part of the "lx-music-api-server" project.

from common import utils
from common import config
from common import Httpx

def buildsignparams(dictionary, body = ""):
    joined_str = ''.join([f'{k}={v}' for k, v in dictionary.items()])
    return joined_str + body

def buildrequestparams(dictionary):
    joined_str = '&'.join([f'{k}={v}' for k, v in dictionary.items()])
    return joined_str

tools = {
    "signkey": config.read_config("module.kg.client.signatureKey"),
    "pidversec": config.read_config("module.kg.client.pidversionsecret"),
    "clientver": config.read_config("module.kg.client.clientver"),
    "x-router": config.read_config("module.kg.tracker.x-router"),
    "url": config.read_config("module.kg.tracker.host") + config.read_config("module.kg.tracker.path"),
    "version": config.read_config("module.kg.tracker.version"),
    "uid": config.read_config("module.kg.user.userid"),
    "token": config.read_config("module.kg.user.token"),
    "mid": config.read_config("module.kg.user.mid"),
    "extra_params": config.read_config("module.kg.tracker.extra_params"),
}

def sign(params, body = ""):
    params = utils.sort_dict(params)
    params = buildsignparams(params, body)
    return utils.md5(tools["signkey"] + params + tools["signkey"])

def signRequest(url, params, options):
    params = utils.merge_dict(tools["extra_params"], params)
    url = url + "?" + buildrequestparams(params) + "&signature=" + sign(params, options.get("body") if options.get("body") else (options.get("data") if options.get("data") else "")
    return Httpx.request(url, options)

def url(songId, quality):
    inforeq = Httpx.request("https://m.kugou.com/app/i/getSongInfo.php?cmd=playInfo&hash=" + songId)
    body_ = inforeq.json()
    album_id = body_["albumid"]
    
