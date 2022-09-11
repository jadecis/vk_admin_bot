from cgitb import text
from http.client import IM_USED
from typing import Dict
from vkbottle.bot import Blueprint, Message, Bot
from vkbottle import API
from src.db import Database
from src import config as cfg
import time

db = Database("src/database.db")
bp = Blueprint("Admin settings")

bot = Bot(token=cfg.first_token)
admin= API(cfg.creator_token)

async def last_posts(bot_admin, owner_id, user_id):
    result=await bot_admin.wall.get(
        owner_id= owner_id,
        count=20,
        fliter='others'
    )
    for item in result.items:
        if item.from_id == user_id:
            await admin.wall.delete(
                owner_id=item.owner_id, 
                post_id=item.id)
            time.sleep(1)
@bp.on.private_message(text= ["/add <word>", "/get", "/del <word>"])
async def message_answer(message: Message, word=None):
    if word is not None:
        if message.text.__contains__('/add'):
            if db.words_exist(word.lower()) is False:
                db.add_badwords(word.lower())
                await message.answer(f"Добавленно слово: {word}")
            else:
                await message.answer(f"Cлово: {word}, уже было добавленно !")
        if message.text.__contains__('/del'):
            if db.words_exist(word.lower()) is False:
                await message.answer(f"Cлово: {word}, нет в списке! ")
            else:
                db.del_badwords(word.lower())
                await message.answer(f"Удаленно слово: {word}")
    elif message.text == '/get':
        msg= ""
        words= db.get_badwords()
        if words is not None:
            for wd in words:
                msg+=f"{wd[0]}\n"
            await message.answer(f"{msg}")
        else:
            await message.answer(f"Список пуст !")
        
@bp.on.chat_message(payload_map= [('Ban', str)])
async def ban_message(message: Message):
    key=message.payload.split(':')[1][1:-2]
    post= db.get_post(key)
    if post is not None:
        db.del_post(key)
        await last_posts(
                bot_admin=admin,
                owner_id=post[2],
                user_id=post[3]) 
        await message.answer("Посты удалены!")
    else:
        await message.answer("Посты уже были удалены!")

    
