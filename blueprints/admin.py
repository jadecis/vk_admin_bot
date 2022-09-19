from distutils.cmd import Command
from vkbottle.bot import Blueprint, Message, Bot
from vkbottle import API
from src.db import Database
from src import config as cfg
import time
from datetime import datetime, timedelta 

db = Database("src/database.db")
bp = Blueprint("Admin settings")

bot = Bot(token=cfg.first_token)
admin= API(cfg.creator_token)

async def last_posts(bot_admin, owner_id, user_id):
    result=await bot_admin.wall.get(
        owner_id= owner_id,
        count=50,
        fliter='others'
    )
    for item in result.items:
        if item.from_id == user_id:
            await admin.wall.delete(
                owner_id=item.owner_id, 
                post_id=item.id)
            time.sleep(1)

async def post_have_word(bot_admin, word, owner_id):
    result =await bot_admin.wall.get(
        owner_id= owner_id,
        count=99,
        fliter='others'
    )
    for item in result.items:
        if item.text.lower().__contains__(word):
            await admin.wall.delete(
                owner_id=item.owner_id, 
                post_id=item.id)
            time.sleep(1)
    return "Посты с новым словом, удалены"
        
@bp.on.private_message(text= ["/add <word>", "/get", "/del <word>"])
async def message_answer(message: Message, word=None):
    if word is not None:
        if message.text.__contains__('/add'):
            if db.words_exist(word.lower()) is False:
                db.add_badwords(word.lower())
                owner_id= message.group_id
                await message.answer(f"Добавленно слово: {word}")
                res= await post_have_word(
                    bot_admin=admin,
                    owner_id=-203851563,
                    word= word.lower()
                )
                res= await post_have_word(
                    bot_admin=admin,
                    owner_id=-133537998,
                    word= word.lower()
                )
                await message.answer(f"{res}")
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
    await admin.groups.ban(
        group_id=203851563,
        owner_id=post[3],
        end_date=time.mktime((datetime.now()+ timedelta(weeks=4)).timetuple()),
        comment="За нарушение правил сообщества.",
        comment_visible=1
    )
    await admin.groups.ban(
        group_id=133537998,
        owner_id=post[3],
        end_date=time.mktime((datetime.now()+ timedelta(weeks=4)).timetuple()),
        comment="За нарушение правил сообщества.",
        comment_visible=1
    )
    
    if post is not None:
        db.del_post(key)
        await last_posts(
                bot_admin=admin,
                owner_id=post[2],
                user_id=post[3]) 
        await message.answer("Посты удалены!")
    else:
        await message.answer("Посты уже были удалены!")

@bp.on.private_message(text= ["/ban <link>"])
async def ban_user(message: Message, link= None):
    if link is not None:
        user_name= str(link).replace('https://vk.com/', '')
        user_name= user_name.replace('id', '') if user_name.__contains__('id') else user_name
        user_id= await admin.users.get(
            user_ids= user_name
        )
        print(user_id[0].id)
        await admin.groups.ban(
        group_id=133537998,
        owner_id=user_id[0].id,
        end_date=time.mktime((datetime.now()+ timedelta(weeks=4)).timetuple()),
        comment="За нарушение правил сообщества.",
        comment_visible=1
        )
        await admin.groups.ban(
        group_id=203851563,
        owner_id=user_id[0].id,
        end_date=time.mktime((datetime.now()+ timedelta(weeks=4)).timetuple()),
        comment="За нарушение правил сообщества.",
        comment_visible=1
        )
        
        
        
        
    
    
