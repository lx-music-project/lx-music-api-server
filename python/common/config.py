# ----------------------------------------
# - mode: python -
# - author: helloplhm-qwq -
# - name: config.py -
# - project: lx-music-api-server -
# - license: MIT -
# ----------------------------------------
# This file is part of the "lx-music-api-server" project.
# Do not edit except you know what you are doing.

import ujson as json
import time
import os
import traceback
import sys
import sqlite3
from .utils import unique_list, readfile
from . import variable
from .log import log
# from dbutils.pooled_db import PooledDB
import threading

# 创建线程本地存储对象
local_data = threading.local()

def get_data_connection():
    # 检查线程本地存储对象是否存在连接对象，如果不存在则创建一个新的连接对象
    if not hasattr(local_data, 'connection'):
        local_data.connection = sqlite3.connect('data.db')
    return local_data.connection

# 创建线程本地存储对象
local_cache = threading.local()

def get_cache_connection():
    # 检查线程本地存储对象是否存在连接对象，如果不存在则创建一个新的连接对象
    if not hasattr(local_cache, 'connection'):
        local_cache.connection = sqlite3.connect('cache.db')
    return local_cache.connection

logger = log('config_manager')


class ConfigReadException(Exception):
    pass


default = {
    "common": {
        "host": "0.0.0.0",
        "_host-desc": "服务器启动时所使用的HOST地址",
        "port": "9763",
        "_port_desc": "服务器启动时所使用的端口",
    },
    "security": {
        "key": {
            "enable": False,
            "_enable-desc": "是否开启请求key，开启后只有请求头中包含key，且值一样时可以访问API",
            "ban": True,
            "value": "114514",
        },
        "whitelist_host": [
            "localhost",
            "0.0.0.0",
            "127.0.0.1",
        ],
        "_whitelist_host-desc": "强制白名单HOST，不需要加端口号（即不受其他安全设置影响的HOST）",
        "check_lxm": False,
        "_check_lxm-desc": "是否检查lxm请求头（正常的LX Music请求时都会携带这个请求头）",
        "lxm_ban": True,
        "_lxm_ban-desc": "lxm请求头不存在或不匹配时是否将用户IP加入黑名单",
        "allowed_host": {
            "desc": "HOST允许列表，启用后只允许列表内的HOST访问服务器，不需要加端口号",
            "enable": False,
            "blacklist": {
                "desc": "当用户访问的HOST并不在允许列表中时是否将请求IP加入黑名单，长度单位：秒",
                "enable": False,
                "length": 0,
            },
            "list": [
                "localhost",
                "0.0.0.0",
                "127.0.0.1",
            ],
        },
        "banlist": {
            "desc": "是否启用黑名单（全局设置，关闭后已存储的值并不受影响，但不会再检查）",
            "enable": True,
            "expire": {
                "desc": "是否启用黑名单IP过期（关闭后其他地方的配置会失效）",
                "enable": True,
                "length": 86400 * 7,  # 七天
            },
        },
    },
    "module": {
        "kg": {
            "desc": "酷狗音乐相关配置",
            "client": {
                "desc": "客户端请求配置，不懂请保持默认，修改请统一为字符串格式",
                "appid": "1005",
                "_appid-desc": "酷狗音乐的appid，官方安卓为1005，官方PC为1001",
                "signatureKey": "OIlwieks28dk2k092lksi2UIkp",
                "_signatureKey": "客户端signature采用的key值，需要与appid对应",
                "clientver": "12029",
                "_clientver-desc": "客户端versioncode，pidversionsecret可能随此值而变化",
                "pidversionsecret": "57ae12eb6890223e355ccfcb74edf70d",
                "_pidversionsecret-desc": "获取URL时所用的key值计算验证值",
            },
            "tracker": {
                "desc": "trackerapi请求配置，不懂请保持默认，修改请统一为字符串格式",
                "host": "https://gateway.kugou.com",
                "path": "/v5/url",
                "version": "v5",
                "x-router": {
                    "desc": "当host为gateway.kugou.com时需要追加此头，为tracker类地址时则不需要",
                    "enable": True,
                    "value": "tracker.kugou.com",
                },
                "extra_params": {},
                "_extra_params-desc": "自定义添加的param，优先级大于默认，填写类型为普通的JSON数据，会自动转换为请求param",
            },
            "user": {
                "desc": "此处内容请统一抓包获取，需要vip账号来获取会员歌曲，如果没有请留为空值，mid必填，可以瞎填一段数字",
                "token": "",
                "userid": "0",
                "mid": "114514",
            }
        },
        "tx": {
            "desc": "QQ音乐相关配置",
            "vkeyserver": {
                "desc": "请求官方api时使用的guid，uin等信息，不需要与cookie中信息一致",
                "guid": "114514",
                "uin": "10086",
            },
            "user": {
                "desc": "用户数据，可以通过浏览器获取，需要vip账号来获取会员歌曲，如果没有请留为空值，qqmusic_key可以从Cookie中/客户端的请求体中（comm.authst）获取",
                "qqmusic_key": "",
                "uin": "",
                "_uin-desc": "key对应的QQ号"
            }
        },
        "wy": {
            "desc": "网易云音乐相关配置",
            "user": {
                "desc": "账号cookie数据，可以通过浏览器获取，需要vip账号来获取会员歌曲，如果没有请留为空值",
                "cookie": ""
            }
        },
        "mg": {
            "desc": "咪咕音乐相关配置",
            "user": {
                "desc": "研究不深，后两项自行抓包获取，在header里",
                "aversionid": "",
                "token": "",
                "osversion": "10",
                "useragent": "Mozilla / 5.0 (Windows NT 10.0; Win64; x64) AppleWebKit / 537.36 (KHTML, like Gecko) Chrome / 89.0.4389.82 Safari / 537.36",
            },
        },
    },
}


def handle_default_config():
    with open("./config.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(default, indent=2, ensure_ascii=False,
                escape_forward_slashes=False))
        f.close()
        logger.info('首次启动或配置文件被删除，已创建默认配置文件')
        logger.info(
            f'\n请到{variable.workdir + os.path.sep}config.json修改配置后重新启动服务器')
        sys.exit(0)


class ConfigReadException(Exception):
    pass


def load_data():
    config_data = {}
    try:
        # Connect to the database
        conn = get_data_connection()
        cursor = conn.cursor()

        # Retrieve all configuration data from the 'config' table
        cursor.execute("SELECT key, value FROM data")
        rows = cursor.fetchall()

        for row in rows:
            key, value = row
            config_data[key] = json.loads(value)

    except Exception as e:
        logger.error(f"Error loading config: {str(e)}")
        logger.error(traceback.format_exc())

    return config_data


def save_data(config_data):
    try:
        # Connect to the database
        conn = get_data_connection()
        cursor = conn.cursor()

        # Clear existing data in the 'data' table
        cursor.execute("DELETE FROM data")

        # Insert the new configuration data into the 'data' table
        for key, value in config_data.items():
            cursor.execute(
                "INSERT INTO data (key, value) VALUES (?, ?)", (key, json.dumps(value)))

        conn.commit()

    except Exception as e:
        logger.error(f"Error saving config: {str(e)}")
        logger.error(traceback.format_exc())


def getCache(module, key):
    try:
        # 连接到数据库（如果数据库不存在，则会自动创建）
        conn = get_cache_connection()

        # 创建一个游标对象
        cursor = conn.cursor()

        cursor.execute("SELECT data FROM cache WHERE module=? AND key=?",
                       (module, key))

        result = cursor.fetchone()
        if result:
            cache_data = json.loads(result[0])
            if (not cache_data['expire']):
                return cache_data
            if (int(time.time()) < cache_data['time']):
                return cache_data
    except:
        pass
        # traceback.print_exc()
    return False


def updateCache(module, key, data):
    try:
        # 连接到数据库（如果数据库不存在，则会自动创建）
        conn = get_cache_connection()

        # 创建一个游标对象
        cursor = conn.cursor()

        cursor.execute(
            "SELECT data FROM cache WHERE module=? AND key=?", (module, key))
        result = cursor.fetchone()
        if result:
            cache_data = json.loads(result[0])
            if isinstance(cache_data, dict):
                cache_data.update(data)
            else:
                logger.error(
                    f"Cache data for module '{module}' and key '{key}' is not a dictionary.")
        else:
            cursor.execute(
                "INSERT INTO cache (module, key, data) VALUES (?, ?, ?)", (module, key, json.dumps(data)))

        conn.commit()
    except:
        logger.error('缓存写入遇到错误…')
        logger.error(traceback.format_exc())


def resetRequestTime(ip):
    config_data = load_data()
    try:
        try:
            config_data['requestTime'][ip] = 0
        except KeyError:
            config_data['requestTime'] = {}
            config_data['requestTime'][ip] = 0
        save_data(config_data)
    except:
        logger.error('配置写入遇到错误…')
        logger.error(traceback.format_exc())


def updateRequestTime(ip):
    try:
        config_data = load_data()
        try:
            config_data['requestTime'][ip] = time.time()
        except KeyError:
            config_data['requestTime'] = {}
            config_data['requestTime'][ip] = time.time()
        save_data(config_data)
    except:
        logger.error('配置写入遇到错误...')
        logger.error(traceback.format_exc())


def getRequestTime(ip):
    config_data = load_data()
    try:
        value = config_data['requestTime'][ip]
    except:
        value = 0
    return value


def read_data(key):
    config = load_data()
    keys = key.split('.')
    value = config
    for k in keys:
        if k not in value and keys.index(k) != len(keys) - 1:
            value[k] = {}
        elif k not in value and keys.index(k) == len(keys) - 1:
            value = None
        value = value[k]

    return value


def write_data(key, value):
    config = load_data()

    keys = key.split('.')
    current = config
    for k in keys[:-1]:
        if k not in current:
            current[k] = {}
        current = current[k]

    current[keys[-1]] = value

    save_data(config)


def push_to_list(key, obj):
    config = load_data()

    keys = key.split('.')
    current = config
    for k in keys[:-1]:
        if k not in current:
            current[k] = {}
        current = current[k]

    if keys[-1] not in current:
        current[keys[-1]] = []

    current[keys[-1]].append(obj)

    save_data(config)


def read_config(key):
    config = variable.config
    keys = key.split('.')
    value = config
    for k in keys:
        if isinstance(value, dict):
            if k not in value and keys.index(k) != len(keys) - 1:
                value[k] = {}
            elif k not in value and keys.index(k) == len(keys) - 1:
                value = None
            value = value[k]
        else:
            value = None
            break

    return value


def initConfig():
    try:
        with open("./config.json", "r", encoding="utf-8") as f:
            try:
                variable.config = json.loads(f.read())
            except:
                if os.path.getsize("./config.json") != 0:
                    logger.error("配置文件加载失败，请检查是否遵循JSON语法规范")
                    sys.exit(1)
                else:
                    variable.config = handle_default_config()
    except FileNotFoundError:
        variable.config = handle_default_config()
    # print(variable.config)
    logger.debug("配置文件加载成功")
    conn = sqlite3.connect('cache.db')

    # 创建一个游标对象
    cursor = conn.cursor()

    # 创建一个表来存储缓存数据
    cursor.execute(readfile(os.path.join(variable.workdir, 'common/sql/create_cache_db.sql')))

    conn.close()

    conn2 = sqlite3.connect('data.db')

    # 创建一个游标对象
    cursor2 = conn2.cursor()

    cursor2.execute(readfile(variable.workdir +
                    '/common/sql/create_data_db.sql'))

    conn2.close()

    logger.debug('数据库初始化成功')

    # print
    if (load_data() == {}):
        write_data('banList', [])
        write_data('requestTime', {})
        logger.debug('数据库内容为空，已写入默认值')


def ban_ip(ip_addr, ban_time=-1):
    if read_config('security.banlist.enable'):
        banList = read_data('banList')
        banList.append({
            'ip': ip_addr,
            'expire': read_config('security.banlist.expire.enable'),
            'expire_time': read_config('security.banlist.expire.length') if (ban_time == -1) else ban_time,
        })
        write_data('banList', banList)
    else:
        if (variable.banList_suggest < 10):
            variable.banList_suggest += 1
            logger.warning('黑名单功能已被关闭，我们墙裂建议你开启这个功能以防止恶意请求')


def check_ip_banned(ip_addr):
    if read_config('security.banlist.enable'):
        banList = read_data('banList')
        for ban in banList:
            if (ban['ip'] == ip_addr):
                if (ban['expire']):
                    if (ban['expire_time'] > int(time.time())):
                        return True
                    else:
                        banList.remove(ban)
                        write_data('banList', banList)
                        return False
                else:
                    return True
            else:
                return False
        return False
    else:
        variable.banList_suggest += 1
        logger.warning('黑名单功能已被关闭，我们墙裂建议你开启这个功能以防止恶意请求')


initConfig()
