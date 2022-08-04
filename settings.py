import os

my_path = os.path.abspath(os.getcwd())

DEBUG = True  # Режим відладки

if DEBUG:
    #  Режив відладки увімкнено
    TOKEN = ""  # Телеграм токен для авторизації бота
    LANGUAGE = "UA"  # Мова бота, на даний момент доступна лише UA
    DELIVERY_PRICE = 60  # Ціна доставки в грн.
    ONLY_ADMIN_GROUP = True  # Дозвіл на роботу лише в групі адміністраторів
    ID_ADMIN_GROUP =   # ID групи адміністраторів
    FEEDBACK_MODERATORS = ["heridium"]  # Модератори до кого можуть звернутись користувачі для зворотнього зв'язку
    COMMENT_GROUP =   # ID групи для відгуків
    ADMINS = ["heridium"]  # username адміністраторів
    IMG_FOLDER = my_path+"\\images\\"  # Папка фото
else:
    #  Робочий режим
    TOKEN = ""  # Телеграм токен для авторизації бота
    LANGUAGE = "UA"  # Мова бота, на даний момент доступна лише UA
    DELIVERY_PRICE = 60  # Ціна доставки в грн.
    ONLY_ADMIN_GROUP = True  # Дозвіл на роботу лише в групі адміністраторів
    ID_ADMIN_GROUP =  # ID групи адміністраторів
    FEEDBACK_MODERATORS = ["heridium"]  # Модератори до кого можуть звернутись користувачі для зворотнього зв'язку
    COMMENT_GROUP =   # ID групи для відгуків
    ADMINS = ["heridium"]  # username адміністраторів
    IMG_FOLDER = my_path+"\\images\\"  # Папка фото
