from zlapi import ZaloAPI
from zlapi.models import ThreadType, Message

from import_helper import *
from utils import ReadJSONFile, WriteJSONFile

JSON_DATA = ReadJSONFile("config.json")
# Thông tin đăng nhập
phone = JSON_DATA["phone_zalo"]
password = JSON_DATA["password_zalo"]
imei = JSON_DATA["imei_zalo"]
cookies = JSON_DATA["cookies_zalo"]

# Khởi tạo và chạy bot
ZALO = ZaloAPI(phone, password, imei=imei, cookies=cookies) if JSON_DATA["use_zalo"] else None

def SendMessage(msg: str | Message, thread_id: str | int):
    if not JSON_DATA["use_zalo"]:
        print("Set 'use_zalo' to true (config.json) to use Zalo features.")
        return False

    try:
        if type(msg) == str:
            ZALO.sendMessage(Message(msg), thread_id, ThreadType.GROUP) # type: ignore
        else:
            ZALO.sendMessage(msg, thread_id, ThreadType.GROUP) # type: ignore

        return True
    except:
        return False

def GetAllGroups():
    if not JSON_DATA["use_zalo"]:
        print("Set 'use_zalo' to true (config.json) to use Zalo features.")
        return False

    GROUP_ID = ZALO.fetchAllGroups().gridVerMap.keys() # type: ignore

    json = {}
    for id in GROUP_ID:
        json[id] = ZALO.fetchGroupInfo(id).gridInfoMap[id]["name"] # type: ignore

    return WriteJSONFile("zalo_groups.json", json)
