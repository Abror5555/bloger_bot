from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from database.database import db
from tgbot.filters.admin import AdminFilter
from tgbot.keyboards.reply import admin_menu
from tgbot.misc.states import  BlogerState, BlogerUpdateState, SendAdState
from tgbot.config import SOCIAL_MEDIA
from tgbot.misc.bloger_detail import make_bloger_detail
from tgbot.services.broadcaster import send_copy_broadcast
from tgbot.config import load_config
from tgbot.keyboards.inline import (blogers_p_keyboards, OrderCallbackData, 
                                    bloger_detail_keyboard, UpdateBlogerCallbackData, AddBlogerUserCallbackData,
                                    confirm_ad_keyboard, ConfirmAdCallBackData, ad_keyboard)

config = load_config(".env")


admin_router = Router()
admin_router.message.filter(AdminFilter())


#Start Command For Admins
@admin_router.message(CommandStart())
async def admin_start(message: Message):
    try:
        db.add_user(id=message.from_user.id, name=message.from_user.full_name)
    except:
       pass
   
    await message.reply(f"Assalomu alaykum, {message.from_user.full_name}", reply_markup=admin_menu)



# =====================================CREATE BLOGER================================================

#Create Bloger Command
@admin_router.message(F.text.contains("➕ Bloger yaratish"))
async def create_bloger(message: Message, state=FSMContext):
    await  message.answer("Ok, bloger nomini kiriting:")
    await  state.set_state(BlogerState.id)


#Create Bloger
@admin_router.message(BlogerState.id)
async def actually_create_bloger(message: Message, state=FSMContext):
    db.add_bloger(message.text)
    await message.reply("Bloger muvaffaqiyatli yaratildi!")
    await  state.clear()


# =================================BLOGER DATA========================================================
# Bloger List
@admin_router.message(F.text.contains("📄 Blogerlar ro'yxati"))
async def blogers_list(message: Message):
    blogers = db.select_all_bloger()
    markup = blogers_p_keyboards(blogers,admin_router)

    await  message.delete()
    await  message.answer("Blogerlar ro'yxati:", reply_markup=markup)


#Bloger detail
@admin_router.callback_query(OrderCallbackData.filter())
async  def bloger_detail(call: CallbackQuery, callback_data:OrderCallbackData):
    await call.answer()
    bloger_id = callback_data.bloger_id
    bloger = db.select_blog(id=str(bloger_id))
    bot_info = await call.bot.get_me()
    
    markup = bloger_detail_keyboard(bloger_id=bloger_id)
    text = await make_bloger_detail(bloger, bot_info)
    
    await call.message.edit_text(text, reply_markup=markup)


#Back to bloger list
@admin_router.callback_query(F.data == "back")
async def back_to_bloger_list(call:CallbackQuery):
    blogers = db.select_all_bloger()
    markup = blogers_p_keyboards(blogers,admin_router)

    await  call.message.edit_text("Blogerlar ro'yxati:", reply_markup=markup)
    
  
    
#   =======================================BLOGER UPDATE-==============================================

#update bloger name
@admin_router.callback_query(UpdateBlogerCallbackData.filter())
async def update_bloger(call:CallbackQuery, callback_data:UpdateBlogerCallbackData, state=FSMContext):
    bloger_id = callback_data.bloger_id
    message_id = call.message.message_id
    chat_id = call.message.chat.id
    
    await state.update_data(
        {"bloger_id":bloger_id, "message": message_id, "chat":chat_id}
    )
    
    text = call.message.text
    await call.message.edit_text(text=text+"\n\nBloger nomini kiriting:", reply_markup=None)
    
    await state.set_state(BlogerUpdateState.id)
    

#Update Bloger
@admin_router.message(BlogerUpdateState.id)
async def actually_update_bloger(message: Message, state=FSMContext):
    data = await state.get_data()
    message_text =  message.text
    
    db.update_bloger_name(name=message_text, id=data['bloger_id'])
    await message.delete()
    
    bloger_id = data['bloger_id']
    bloger = db.select_blog(id=str(bloger_id))
    
    bot_info = await message.bot.get_me()
    
    
    text = await make_bloger_detail(bloger, bot_info)
    
    markup = bloger_detail_keyboard(bloger_id=bloger_id)
    await message.bot.edit_message_text(text, chat_id=data["chat"], message_id=data['message'], reply_markup=markup)
    await  state.clear()




#add user to bloger
@admin_router.callback_query(AddBlogerUserCallbackData.filter())
async def add_user_to_bloger(call:CallbackQuery, callback_data:UpdateBlogerCallbackData, state:FSMContext):
    bloger_id = callback_data.bloger_id
    message_id = call.message.message_id
    chat_id = call.message.chat.id
    
    await state.update_data(
        {"bloger_id":bloger_id, "message": message_id, "chat":chat_id}
    )
    
    text = call.message.text
    await call.message.edit_text(text=text+"\n\nQo'shish uchun foydalanuvchini telefon raqamini kiriting(E.x: 998901234567):", reply_markup=None)
    
    await state.set_state(BlogerUpdateState.phone_number)
    
    

        

#Actually add user to bloger
@admin_router.message(BlogerUpdateState.phone_number)
async def actually_add_user_to_bloger(message: Message, state=FSMContext):
    await message.delete()
    
    data = await state.get_data()
    phone_number =  message.text
    
    bloger_id = data['bloger_id']
    bloger = db.select_blog(id=str(bloger_id))
    bot_info = await message.bot.get_me()
    text = await make_bloger_detail(bloger, bot_info)
    
    user = db.select_user(phone_number=phone_number)
    
    try:
        db.update_bloger_user(user[0], bloger_id)
        markup = bloger_detail_keyboard(bloger_id=bloger_id)
        await message.bot.edit_message_text(text+"\n\n✅ O'zgaririldi", chat_id=data["chat"], message_id=data['message'], reply_markup=markup)
    except:
        markup = bloger_detail_keyboard(bloger_id=bloger_id)
        await message.bot.edit_message_text(text+"\n\n❌ O'zgartirishda xatolik", chat_id=data["chat"], message_id=data['message'], reply_markup=markup)
    
    
    await  state.clear()
        
    

# ==========================================STATS=======================================================

# Show stats
@admin_router.message(F.text.contains("📊 Statistika"))
async def stats(message:Message):
    users = 0
    await message.delete()
    text = "\t\tStatistika"
    text += f"\n\n<b>Blogerlar soni :</b>  {db.count_blogers()[0]}"
    text += "\n<b>Barcha foydalanuvchilar :</b>  {} "
    for i in SOCIAL_MEDIA:
        user_count = db.count_users_with_filter(social_media=i)[0]
        users += user_count
        text += f"\n    🔹<b>{i.title()}:</b>  {user_count} "
        
    await message.answer(text.format(users))
    

#======================================ADS=========================================================

#Send AD
@admin_router.message(F.text.contains("📢 E'lon berish"))
async def send_ad(message:Message, state:FSMContext):
    await message.answer("Ok, Barchaga yuborish uchun xabarni kiriting:")
    await state.set_state(SendAdState.message)
    
    
#Confirm The Ad
@admin_router.message(SendAdState.message)
async def confirm_ad(message:Message, state:FSMContext):
    await state.update_data(
        {"message_id":message.message_id,
         "chat_id":message.chat.id
         }
    )
    markup = confirm_ad_keyboard()
    await message.reply("Ushbu xabar barcha foydalanuvchilarga jo'natilsinmi?", reply_markup=markup)
    
    
#Send the AD
@admin_router.callback_query(ConfirmAdCallBackData.filter())
async def send_the_ad(call: CallbackQuery, state: FSMContext, callback_data: ConfirmAdCallBackData):
    await call.answer()
    
    if callback_data.confirm:
        data = await state.get_data()
        message_id = data['message_id']
        chat_id = data['chat_id']
        users = db.select_all_users()
        
        markup = ad_keyboard(name="🖇 Bog'lanish", username=config.tg_bot.ad_username)
        await send_copy_broadcast(call.bot, users, message_id, chat_id, reply_markup=markup)
        await call.message.edit_text("✅ Jarayon boshlandi tugagandan so'ng sizni ogohlantiramiz.", reply_markup=None)
        
    else:
        await call.message.edit_text("❌ Xabarni yuborish bekor qilindi.", reply_markup=None)
        
    await state.clear()
    
  
#===================================================QUESTIONS===========================================================  
#answer questions
@admin_router.message()
async def answer_question(message: Message):
    try:
        await message.send_copy(message.reply_to_message.forward_from.id)
    except:
        pass
        
   
    
    
    
    
    