import os
from dotenv import load_dotenv

from utils import utils, request

load_dotenv()

data = request.get_telegram_ids()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = utils.get_group_id_by_name(data, "Buyuk zamon channel 3")
FIRST_CHANNEL_ID = utils.get_group_id_by_name(data, "Buyuk zamon channel") 
SECOND_CHANNEL_ID = utils.get_group_id_by_name(data, "buyuk zamon channel 2") 
