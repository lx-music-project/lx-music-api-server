import requests
import random
import traceback
import zlib
import ujson as json
from .log import log
import re
import codecs
import binascii

def is_valid_utf8(text):
    if "\ufffe" in text:
        return False
    try:
        text.encode('utf-8').decode('utf-8')
        return True
    except UnicodeDecodeError:
        return False

def is_plain_text(text):
    pattern = re.compile(r'[^\x00-\x7F]')
    return not bool(pattern.search(text))

ua_list = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.39||Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1788.0||Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1788.0  uacq||Mozilla/5.0 (Windows NT 10.0; WOW64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5666.197 Safari/537.36||Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 uacq||Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'.split('||')
logger = log('http_utils')

def request(url, options = {}):
    try:
        method = options['method']
        options.pop('method')
    except Exception as e:
        method = 'GET'
    try:
        d_lower = {k.lower(): v for k, v in options['headers'].items()}
        useragent = d_lower['user-agent']
    except:
        # traceback.print_exc()
        try:
            options['headers']['User-Agent'] = random.choice(ua_list)
        except:
            options['headers'] = {}
            options['headers']['User-Agent'] = random.choice(ua_list)
    try:
        reqattr = getattr(requests, method.lower())
    except AttributeError:
        raise AttributeError('Unsupported method: '+method)
    if (method == 'POST') or (method == 'PUT'):
        if options['body']:
            options['data'] = options['body']
            options.pop('body')
    logger.debug(f'HTTP Request: {url}\noptions: {options}')
    try:
        req = reqattr(url, **options)
    except Exception as e:
        logger.error(f'HTTP Request runs into an Error: {traceback.format_exc()}')
        raise e
    logger.debug(f'Request to {url} succeed with code {req.status_code}')
    try:
        logger.debug(json.loads(req.content.decode("utf-8")))
    except:
        try:
            logger.debug(json.loads(zlib.decompress(req.content).decode("utf-8")))
        except zlib.error:
            if is_valid_utf8(req.text) and is_plain_text(req.text):
                logger.debug(req.text)
            else:
                logger.debug(binascii.hexlify(req.content))
        except:
            logger.debug(zlib.decompress(req.content).decode("utf-8") if is_valid_utf8(zlib.decompress(req.content).decode("utf-8")) and is_plain_text(zlib.decompress(req.content).decode("utf-8")) else binascii.hexlify(zlib.decompress(req.content)))
    return req
