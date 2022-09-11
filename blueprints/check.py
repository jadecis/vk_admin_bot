from re import I
from vkbottle.bot import Blueprint, Message, Bot
from vkbottle import Callback, GroupEventType, GroupTypes
from src import config as cfg
from vkbottle import Keyboard, KeyboardButtonColor, Text
import uuid

from src.db import Database
db = Database("src/database.db")

bot = Bot(token=cfg.first_token)
bp = Blueprint("Check new wall in group")

@bp.on.raw_event(GroupEventType.WALL_POST_NEW, dataclass=GroupTypes.WallPostNew)
async def new_wall(event: GroupTypes.WallPostNew):
    text= event.object.text
    words= db.get_badwords()
    if words is not None:
        for wd in words:
            if text.lower().__contains__(wd[0].lower()):
                key= str(uuid.uuid4())
                decide_menu= Keyboard(inline=True)
                decide_menu.add(Text("Бан", {"Ban" : f"{key}"}),
                                color=KeyboardButtonColor.NEGATIVE)
                owner_id= event.object.owner_id
                id= event.object.id
                user_id= event.object.from_id
                db.add_post(
                    key=key,
                    owner_id=owner_id,
                    post_id=id,
                    user_id=user_id
                )
                await bot.api.messages.send(
                peer_id=2000000002,
                attachment=f"wall{owner_id}_{id}",
                random_id=0,
                keyboard=decide_menu.get_json())
                return
