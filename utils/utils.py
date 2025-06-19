from aiogram import Bot


async def get_chat_member(bot: Bot, chat_id: int, user_id: int):
    try:
        member = await bot.get_chat_member(chat_id, user_id)
        if member.status in ["member", 'owner', 'admin', 'creator']:
            return True
        else:
            return False
        
    except Exception as e:
        print(f"Error: {e}")
        return False
    

def get_group_id_by_name(data, name):
    for item in data:
        if item.get('name') == name:
            return item.get('group_id')
        else:
            continue