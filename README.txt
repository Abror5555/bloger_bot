Projectni ishga tushurish:

1. Vertual muhit yaratish
    $ python -m venv venv

2. Yaratilgan venvga kirish
    $ venv\Scripts\activate   # windows uchun

3. Venvni ichida kerakli kutubxonalarni o'rnatish
    $ pip install -r "requirements.txt"

4. Database yaratish uchun djangoni ishga tushurish
    $ python web/manage.py migrate

5. .env yaratish
    Asosiy papkada .env fayli yaratib uni .env.dist kabi kerakli malumotlarni yozing

6. Botni ishga tushurish.
    $ python bot.py


Struktura:

1. Database 
    Bot uchun db ni boshqarish uchun kichik ORM

2. tgbot
    Aiogram kutubxonasi orqali yaratilgan bot

3. web
    Databaseni boshqarish uchun django web

4. bot.py 
    botni ishga tushuruvchi fayli

5. .env &.env.dist
    Vertual muhit o'zgaruvchilari

6. requirements.txt
    Darturni ishga tushurish uchun kerakli kutubxonalar ro'yxati

7. README.txt 
    Project overview