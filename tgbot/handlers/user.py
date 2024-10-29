import asyncio
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram import F

from tgbot.keyboards.reply import request_phone_number
from tgbot.misc.states import UserState
from database.database import  db
from aiogram.types import ReplyKeyboardRemove
from tgbot.config import load_config
from tgbot.services import broadcaster

from tgbot.misc.encode_decode import decode_string


config = load_config(".env")
user_router = Router()


#Start Command For Ordinary Users
@user_router.message(CommandStart())
async def user_start(message: Message, state=FSMContext):
    
    
    
    try:
        code = message.text[6:].strip()
        deep_link = decode_string(code)
        data = list(deep_link.split(","))
        bloger_id = int(data[0])
        social_media = data[1] 
        
    except: 
        
        bloger_id = None
        social_media = None
        
    
    try:
        #trying to create user
        db.add_user(id=message.from_user.id, name=message.from_user.full_name, bloger_id=bloger_id, social_media=social_media)
        
        text = "Assalomu Aleykum, botimizga xush kelibsiz!! \nRo'yxatdan o'tishni yakunlash uchun iltimos pastdagi tugma orqali telefon raqamingizni yuboring.🔽"
        
        await  message.reply(text, reply_markup=request_phone_number)
        
        await state.set_state(UserState.phone_number)
        
        await state.update_data({
                    "id":message.from_user.id,
                    "name":message.from_user.full_name,
                    "bloger":bloger_id,
                    "social_media": social_media,
            })
        
        
        
    except:
        #if user is exists
        user = db.select_user(id=message.from_user.id)
        
        if not user[2]:
            text="Iltimos ro'yxatdan o'tishni yakunlash uchun telefon raqamingizni jo'nating."
            await message.answer(text, reply_markup=request_phone_number)
            
            await state.set_state(UserState.phone_number)
            
        
        else:
            await message.answer("Botga yana bir bor xush kelibsiz. \nSavollar bo'lsa shu yerda  qoldirishingiz mumkin.")

    
    
   

#getting user phone_number
@user_router.message(UserState.phone_number, F.contact)
async def update_phone_number(message: Message, state: FSMContext):

    
    await state.update_data(
        {"phone_number":message.contact.phone_number.strip("+")}
    )
    
    db.update_user_phone_number(id=message.from_user.id, phone_number=message.contact.phone_number.strip("+"))

    data = await state.get_data()
    await message.answer("Rahmat, tez orada adminlarimiz siz bilan bog'lanadi. \nSizni qiziqtirgan mahsulot haqida va savollar bo'lsa shu yerda yozib qoldirishingiz mumkin.", reply_markup=ReplyKeyboardRemove())
    
    try:
        bloger = db.select_blog(id=data['bloger'])[1]
    except:
        bloger = None
    
    text  = "Botga yangi odam qo'shildi:\n"
    text += f'Ismi: <a href="tg://user?id={data["id"]}">{data["name"]}</a> \n'
    text += f"Telefon raqami: {data['phone_number']}\n"
    text += f"Kimdan: {bloger}\n"
    text += f"Ijtimoiy tarmoq: {data['social_media']}\n"
    
    
    await broadcaster.broadcast(bot=message.bot, users=config.tg_bot.admin_ids, text=text)
    
    await state.clear()


#if user sends other info instead of contact
@user_router.message(UserState.phone_number, F)
async def update_phone_number_form_error(message: Message, state: FSMContext):
    await message.answer("Iltimos pastdagi tugma orqali telefon raqamingini yuboring.", reply_markup=request_phone_number)

    

#send question
@user_router.message()
async def send_question(message: Message, state:FSMContext):
    user = db.select_user(id=message.from_user.id)
    
    if user and user[2]:
        for admin in config.tg_bot.admin_ids:
            await message.forward(admin, disable_notification=False)
            await asyncio.sleep(0.05)
        
    else:
        await user_start(message, state)

