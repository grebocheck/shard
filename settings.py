import os

my_path = os.path.abspath(os.getcwd())

DEBUG = True  # Режим відладки

if DEBUG:
    #  Режив відладки увімкнено
    TOKEN = "1040706632:AAFHkdd0nR8YrcrWlQBK75e2QO0FtdrEO18"  # Телеграм токен для авторизації бота
    LANGUAGE = "UA"  # Мова бота, на даний момент доступна лише UA
    DELIVERY_PRICE = 60  # Ціна доставки в грн.
    ONLY_ADMIN_GROUP = True  # Дозвіл на роботу лише в групі адміністраторів
    ID_ADMIN_GROUP = -1001673592113  # ID групи адміністраторів
    FEEDBACK_MODERATORS = ["heridium"]  # Модератори до кого можуть звернутись користувачі для зворотнього зв'язку
    COMMENT_GROUP = -1001673592113  # ID групи для відгуків
    ADMINS = ["heridium"]  # username адміністраторів
    IMG_FOLDER = my_path+"\\images\\"  # Папка фото
else:
    #  Робочий режим
    TOKEN = "1040706632:AAFHkdd0nR8YrcrWlQBK75e2QO0FtdrEO18"  # Телеграм токен для авторизації бота
    LANGUAGE = "UA"  # Мова бота, на даний момент доступна лише UA
    DELIVERY_PRICE = 60  # Ціна доставки в грн.
    ONLY_ADMIN_GROUP = True  # Дозвіл на роботу лише в групі адміністраторів
    ID_ADMIN_GROUP = -1001673592113  # ID групи адміністраторів
    FEEDBACK_MODERATORS = ["heridium"]  # Модератори до кого можуть звернутись користувачі для зворотнього зв'язку
    COMMENT_GROUP = -1001673592113  # ID групи для відгуків
    ADMINS = ["heridium"]  # username адміністраторів
    IMG_FOLDER = my_path+"\\images\\"  # Папка фото
