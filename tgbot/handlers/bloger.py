from aiogram import F, Router
from aiogram.filters import CommandStart
from tgbot.filters.bloger import BlogerFilter
from tgbot.config import SOCIAL_MEDIA
from aiogram.types import Message
from tgbot.keyboards.reply import bloger_menu
from database.database import db
from tgbot.misc.bloger_detail import make_bloger_detail

bloger_router = Router()
bloger_router.message.filter(BlogerFilter())


#Start Command For Admins
@bloger_router.message(CommandStart())
async def bloger_start(message: Message):
    await message.reply(f"Assalomu aleykum, {message.from_user.full_name}\nXush kelibsiz!", reply_markup=bloger_menu)
    
    
# Show stats
@bloger_router.message(F.text.contains("📊 Statistika"))
async  def bloger_detail(message:Message):
    
    bloger = db.select_blog(user_id=str(message.from_user.id))
    bot_info = await message.bot.get_me()
    text = await make_bloger_detail(bloger, bot_info)

    await message.delete()
    await message.answer(text)


#===================================================QUESTIONS===========================================================  
#answer questions

# @bloger_router.message()
# async def answer_question(message: Message):
#     try:
#         await message.send_copy(message.reply_to_message.forward_from.id)
#     except:
#         pass
        
   
    