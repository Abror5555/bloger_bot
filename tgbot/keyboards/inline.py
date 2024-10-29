from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram_widgets.pagination import KeyboardPaginator
from database.database import db


class OrderCallbackData(CallbackData, prefix="bloger",):
    bloger_id: int


class UpdateBlogerCallbackData(CallbackData, prefix="update"):
    bloger_id: int
    
    
class AddBlogerUserCallbackData(CallbackData, prefix="bloger_user"):
    bloger_id: int
    


class ConfirmAdCallBackData(CallbackData, prefix="confirm"):
    confirm: bool



def blogers_keyboard(blogers: list):

    keyboard = InlineKeyboardBuilder()
    keyboard.adjust(1, repeat=True)
    keyboard.max_width = 1
    
    for bloger in blogers:
        button = InlineKeyboardButton(
            text=bloger[1],
            callback_data=OrderCallbackData(bloger_id=bloger[0]).pack(),
        )
        keyboard.add(button)
        
    return keyboard.as_markup()



def blogers_p_keyboards(blogers: list, router):
    buttons = []
    
    for bloger in blogers:
        # user_count = db.count_users_for_bloger(bloger[0])[0]
        buttons.append(
            InlineKeyboardButton(text=f"{bloger[1]}", callback_data=OrderCallbackData(bloger_id=bloger[0]).pack())
        )

    paginator = KeyboardPaginator(
        router=router,
        data=buttons,
        per_page=5,
        per_row=1
    )


    return paginator.as_markup()



def bloger_detail_keyboard(bloger_id):
    keyboard = InlineKeyboardBuilder()
    keyboard.adjust(2, repeat=True)
    keyboard.max_width = 2
    
    keyboard.button(text="✏️ Tahrirlash", callback_data=UpdateBlogerCallbackData(bloger_id=bloger_id).pack())
    keyboard.button(text="💻 Bloger Admin", callback_data=AddBlogerUserCallbackData(bloger_id=bloger_id,).pack())
    keyboard.button(text="◀️ Orqaga", callback_data="back")
    
    return  keyboard.as_markup()


def confirm_ad_keyboard():
    keyboard = InlineKeyboardBuilder()
    
    keyboard.button(text="✅ Ha", callback_data=ConfirmAdCallBackData(confirm=True).pack())
    keyboard.button(text="❌ Yo'q", callback_data=ConfirmAdCallBackData(confirm=False).pack())
    
    return  keyboard.as_markup()


def ad_keyboard(name, username):
    keyboard = InlineKeyboardBuilder()
    
    keyboard.button(text=name, url=f"https://t.me/{username}")

    return keyboard.as_markup()