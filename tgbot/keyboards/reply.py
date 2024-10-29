from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


request_phone_number = ReplyKeyboardMarkup(
    keyboard = [
        [
            KeyboardButton(text="📲 Kontaktni ulashish", request_contact=True)
        ],
    ],
    resize_keyboard=True
)


admin_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="➕ Bloger yaratish"),
            KeyboardButton(text="📄 Blogerlar ro'yxati")
        ],
        [
            KeyboardButton(text="📊 Statistika"),
            KeyboardButton(text="📢 E'lon berish"),
            
        ]
    ], resize_keyboard=True
)


bloger_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📊 Statistika"),
        ]
    ],  resize_keyboard=True
)