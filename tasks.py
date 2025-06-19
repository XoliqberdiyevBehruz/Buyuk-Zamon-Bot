from celery import Celery
import requests

app = Celery("taks")

app.conf.broker_url = 'redis://localhost:6379/0'


@app.task
def update_user(id, tg_id, tg_username, tg_name):
    data = {
        "telegram_id": tg_id,
        "telegram_username": tg_username,
        "telegram_full_name": tg_name
    }
    res = requests.put(f"https://buyuk.zamon.repid.uz/api/v1/bot/bot/student/{id}/update/", data=data)
    if res.status_code == 200:
        return {"success": True, "message": "updated"}
    elif res.status_code == 404:
        return {"success": False, "message": "Not found"}
    else:
        return {"success": False, "message": res.json()}
    

@app.task
def verification_failed(text, full_name, phone, contract_number):
    data = {
            "description": text,
            "full_name": full_name,
            "phone_number": phone,
            "contract_number": contract_number
        }
    requests.post(f"https://buyuk.zamon.repid.uz/api/v1/bot/bot/verification_failed/", data=data)
    return True


@app.task
def change_user_group_joined(user_id):
    requests.get(f'https://buyuk.zamon.repid.uz/api/v1/bot/bot/user/{user_id}/join_group/')
    return True


@app.task
def create_telegram_group(group_name, group_id):
    response = requests.post(
        f"https://buyuk.zamon.repid.uz/api/v1/bot/bot/telegram_group/create/", 
        data={"name": group_name, "group_id": group_id}
    )
    if response.status_code != 200:
        return False
    else:
        return True


@app.task
def set_student_to_tg_group(group_id, user_id):
    response = requests.put(
        f"https://buyuk.zamon.repid.uz/api/v1/bot/bot/set_telegram_group/{group_id}/",
        data={"student_id": user_id}
    )
    if response.status_code == 200:
        return True
    else:
        return False