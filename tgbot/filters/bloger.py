from aiogram.filters import BaseFilter
from aiogram.types import Message

from tgbot.config import Config

from database.database import db



class BlogerFilter(BaseFilter):
    is_admin: bool = True

    async def __call__(self, obj: Message, config: Config) -> bool:
        
        for bloger in db.select_all_bloger():
            if bloger[3] == obj.from_user.id:
                return True
        else:
            return False
