from tgbot.config import SOCIAL_MEDIA
from tgbot.misc.encode_decode import make_referral_link
from database.database import db

async def make_bloger_detail(bloger, bot_info):
    total_user_count = 0
    text =  f"<b>Nomi:</b> {bloger[1]}\n"
    text += f'<b>Ma\'sul:</b> <a href="tg://user?id={bloger[3]}"> {bloger[3]} </a>\n'
    text += "<b>Referal:</b>  {}\n"
    
    for i in SOCIAL_MEDIA:
        user_count = db.count_users_with_filter(bloger_id=bloger[0], social_media=i)[0]
        total_user_count += user_count
        
        text += f"   🔹<b>{i.title()}:</b>  {user_count}\n"
        
        
    text += f"\n<b>Yaratilgan:</b> {bloger[2]}\n"
    text += f"<b>ID:</b> {bloger[0]}\n"
    text += f"<b>Link:</b>\n"
    for i in SOCIAL_MEDIA:
        text += f"    🔹<b>{i.title()}:</b> <code> {make_referral_link(bot_info.username, bloger[0], i)} </code>\n"
        
    return text.format(total_user_count)