from vkbottle.bot import Bot, Message, run_multibot
from vkbottle import load_blueprints_from_package
from vkbottle.api import API

import asyncio
import logging
from src import config as cfg
from src.db import Database



bot = Bot()
logging.getLogger("vkbottle").setLevel(logging.INFO)

for bp in load_blueprints_from_package("blueprints"):
    bp.load(bot)




run_multibot(bot, apis=(API(cfg.first_token), API(cfg.second_token)))
