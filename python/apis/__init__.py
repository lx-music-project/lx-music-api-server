# ----------------------------------------
# - mode: python - 
# - author: helloplhm-qwq - 
# - name: __init__.py - 
# - project: lx-music-api-server - 
# - license: MIT - 
# ----------------------------------------
# This file is part of the "lx-music-api-server" project.
# Do not edit except you konw what you are doing.

from common.utils import require
from common.exceptions import FailedException
from . import kw
from . import mg
from . import kg


async def SongURL(source, songId, quality):
    func = require('apis.' + source).url
    try:
        return {
            'code': 0,
            'msg': 'success',
            'data': await func(songId, quality),
        }
    except FailedException as e:
        return {
            'code': 2,
            'msg': e.args[0],
            'data': None,
        }