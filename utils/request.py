import datetime
import requests

from tasks import verification_failed
from .import bot_text


def get_user(phone, full_name, contract_number):
    filter_phone = phone.strip("+")
    res = requests.get(f"https://buyuk.zamon.repid.uz/api/v1/bot/bot/verify_user?phone={filter_phone}&full_name={full_name}&contract_number={contract_number}")
    if res.status_code == 200:
        return res.json()
    else:
        verification_failed.delay(bot_text.register_failed, full_name, phone, contract_number)
        return {"success": False}


def create_invite_link(token, chat_id, user_id):
    url = f"https://api.telegram.org/bot{token}/createChatInviteLink"
    expire_date = datetime.datetime.now() + datetime.timedelta(minutes=1) 
    data = {
        'chat_id': chat_id,
        'member_limit': 1,
        'expire_date': int(expire_date.timestamp()),
        'name': f"user_{user_id}",
        "creates_join_request": False
    }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        result = response.json()['result']
        return result['invite_link']
    else:
        print(f"Error creating invite link: {response.status_code}, {response.text}")
        return None


def get_telegram_ids():
    url = f"https://buyuk.zamon.repid.uz/api/v1/bot/bot/telegram_group/list/"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return response

def get_user_by_tg_id(tg_id: int):
    url = f"https://buyuk.zamon.repid.uz/api/v1/bot/bot/student/get_by_tg_id/{tg_id}/"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return response
