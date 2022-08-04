import telebot
from telebot import types
import re

import bot_texts
from box import *
from datetime import datetime

log("Старт")

# Ініціалізація бота
bot = telebot.TeleBot(settings.TOKEN)
log("Бот ініціалізований")

# Клавіатура відміни
cance_button = types.KeyboardButton(bot_texts.cance)
cance_markup = types.ReplyKeyboardMarkup()
cance_markup = cance_markup.row(cance_button)

back_button = types.KeyboardButton(bot_texts.back)
bc_markup = types.ReplyKeyboardMarkup()
bc_markup = bc_markup.row(back_button).row(cance_button)

# Прибрати клавіатуру
remove_markup = types.ReplyKeyboardRemove()

# Меню користувача
my_orders_button = types.KeyboardButton(bot_texts.my_orders)
shop_button = types.KeyboardButton(bot_texts.shop)
feedback_button = types.KeyboardButton(bot_texts.feedback)
about_button = types.KeyboardButton(bot_texts.about)
menu_markup = types.ReplyKeyboardMarkup()
menu_markup = menu_markup.row(my_orders_button, shop_button).row(feedback_button, about_button)


# Ініціалізація клавіатури групи товарів
def get_group_markup():
    log("Ініціалізація клавіатури")
    group_markup = types.ReplyKeyboardMarkup()
    mass_groups = select_all_group()
    for a in mass_groups:
        group_markup.row(types.KeyboardButton(a.name))
    group_markup.row(cance_button)
    return group_markup


global group_markup
group_markup = get_group_markup()

# Клавіатура після додавання товару
shop_markup = types.ReplyKeyboardMarkup()
shop_markup = shop_markup.row(types.KeyboardButton(bot_texts.start_order))
shop_markup = shop_markup.row(types.KeyboardButton(bot_texts.continue_buy))
shop_markup = shop_markup.row(cance_button)

# Клавіатура пропуску
pass_markup = types.ReplyKeyboardMarkup().row(types.KeyboardButton(bot_texts.pass_text))

# Клавіатура yes/no
yes_button = types.KeyboardButton(bot_texts.yes)
no_button = types.KeyboardButton(bot_texts.no)
yn_markup = types.ReplyKeyboardMarkup()
yn_markup = yn_markup.row(yes_button).row(no_button)

# Клавіатура початку реєстрації
button = types.KeyboardButton(bot_texts.reg_start_button)
reg_markup = types.ReplyKeyboardMarkup()
reg_markup = reg_markup.row(button).row(cance_button)

# Клавіатура зворотнього зв`язку
feed_markup = types.ReplyKeyboardMarkup()
feed_markup = feed_markup.row(types.KeyboardButton(bot_texts.create_comment)).row(cance_button)

# Клавіатура зміни данних товару
change_product_markup = types.ReplyKeyboardMarkup()
cp_name_b = types.KeyboardButton(bot_texts.change_product_name)
cp_price_b = types.KeyboardButton(bot_texts.change_product_price)
cp_desc_b = types.KeyboardButton(bot_texts.change_product_description)
cp_img_b = types.KeyboardButton(bot_texts.change_product_img)
cp_group_b = types.KeyboardButton(bot_texts.change_product_group)
change_product_markup = change_product_markup.row(cp_name_b, cp_price_b).row(cp_desc_b, cp_img_b).row(cp_group_b,
                                                                                                      cance_button)

# Клавіатура зміни данних групи
change_group_markup = types.ReplyKeyboardMarkup()
cg_name_b = types.KeyboardButton(bot_texts.change_group_name)
cg_img_b = types.KeyboardButton(bot_texts.change_group_img)
change_group_markup = change_group_markup.row(cg_name_b, cg_img_b).row(cance_button)

# Адмін клавіатура
button_all_open_orders = types.KeyboardButton(bot_texts.all_open_orders)
button_add_product = types.KeyboardButton(bot_texts.add_product)
button_add_group = types.KeyboardButton(bot_texts.add_group)
button_change_product = types.KeyboardButton(bot_texts.change_product)
button_change_group = types.KeyboardButton(bot_texts.change_group)
button_delete_product = types.KeyboardButton(bot_texts.del_product)
button_delete_group = types.KeyboardButton(bot_texts.del_group)
admin_markup = types.ReplyKeyboardMarkup()
admin_markup = admin_markup.row(button_all_open_orders).row(button_add_group, button_add_product)
admin_markup = admin_markup.row(button_change_group, button_change_product)
admin_markup = admin_markup.row(button_delete_group, button_delete_product)


# Отримати ID групи/чату
@bot.message_handler(commands=['id'])
def how_id(message):
    log(f"{message.from_user.id} викликав функцію /id")
    if message.chat.id == settings.ID_ADMIN_GROUP or not settings.ONLY_ADMIN_GROUP:
        if message.from_user.username in settings.ADMINS:
            bot.send_message(chat_id=message.chat.id,
                             text=message.chat.id,
                             parse_mode="Markdown")
            log(f"/id виконана")


# Бан в боті, видалення всіх замовлень
@bot.message_handler(commands=['ban'])
def ban(message):
    log(f"{message.from_user.id} викликав функцію /ban")
    if message.chat.id == settings.ID_ADMIN_GROUP or not settings.ONLY_ADMIN_GROUP:
        if message.from_user.username in settings.ADMINS:
            it_user_id = int(message.text.split(' ')[1])
            result = db_ban(it_user_id)
            log(f"{message.from_user.id} забанив {it_user_id}, {result}")
            bot.send_message(chat_id=message.chat.id,
                             text=result,
                             parse_mode="Markdown")


# Розбан в боті, видалення всіх замовлень
@bot.message_handler(commands=['unban'])
def unban(message):
    log(f"{message.from_user.id} викликав функцію /unban")
    if message.chat.id == settings.ID_ADMIN_GROUP or not settings.ONLY_ADMIN_GROUP:
        if message.from_user.username in settings.ADMINS:
            it_user_id = int(message.text.split(' ')[1])
            result = db_unban(it_user_id)
            log(f"{message.from_user.id} розбанив {it_user_id}, {result}")
            bot.send_message(chat_id=message.chat.id,
                             text=result,
                             parse_mode="Markdown")


# Стартова команда
@bot.message_handler(commands=['start'])
def starter(message):
    log(f"{message.from_user.id} викликав функцію /start")
    if extend_banlist(message.from_user.id):

        # IF ADMIN
        if message.chat.id == settings.ID_ADMIN_GROUP or not settings.ONLY_ADMIN_GROUP:
            if message.from_user.username in settings.ADMINS:
                # Перехід до меню адміна
                log(f"{message.from_user.id} перейшов в меню адміна")
                bot.send_message(chat_id=message.chat.id,
                                 text=bot_texts.welcome,
                                 reply_markup=admin_markup,
                                 parse_mode="Markdown")

        # IF USER
        else:
            # Початок дерева реєстрації, перехід до register_two
            if extend_user(message.from_user.id):
                log(f"{message.from_user.id} почав реєстрацію")
                bot.send_message(chat_id=message.chat.id,
                                 text=bot_texts.first_start,
                                 reply_markup=reg_markup,
                                 parse_mode="Markdown")
                bot.register_next_step_handler(message, register_two)
            # Перехід до меню користувача
            else:
                log(f"{message.from_user.id} перейшов в меню користувача")
                bot.send_message(chat_id=message.chat.id,
                                 text=bot_texts.welcome,
                                 reply_markup=menu_markup,
                                 parse_mode="Markdown")
    else:
        # Користувач забанений
        log(f"{message.from_user.id} не зміг скористатись ботом так як він забанений")
        bot.send_message(chat_id=message.chat.id,
                         text=bot_texts.you_have_ban,
                         reply_markup=remove_markup)


# Отримування username
def register_two(message):
    if message.text != bot_texts.cance:
        # Перехід до register_three
        user_username = message.from_user.username
        bot.send_message(chat_id=message.chat.id,
                         text=bot_texts.h_your_name,
                         reply_markup=cance_markup,
                         parse_mode="Markdown")
        bot.register_next_step_handler(message, register_three, user_username)
    else:
        # Реєстрація відмінена
        log(f"{message.from_user.id} відмінив реєстрацію")
        bot.send_message(chat_id=message.chat.id,
                         text=bot_texts.cance_reg,
                         reply_markup=remove_markup,
                         parse_mode="Markdown")


# Отримування як звертатись до користувача
def register_three(message, user_username):
    if message.text != bot_texts.cance:
        if message.text is not None:
            # Перехід до register_four
            user_name = message.text
            bot.send_message(chat_id=message.chat.id,
                             text=bot_texts.h_your_phone,
                             reply_markup=cance_markup,
                             parse_mode="Markdown")
            bot.register_next_step_handler(message, register_four, user_username, user_name)
        else:
            # Потреба у користувача ввести коректно
            bot.send_message(chat_id=message.chat.id,
                             text=bot_texts.write_correct,
                             reply_markup=cance_markup,
                             parse_mode="Markdown")
            bot.register_next_step_handler(message, register_three, user_username)
    else:
        # Реєстрація відмінена
        log(f"{message.from_user.id} відмінив реєстрацію")
        bot.send_message(chat_id=message.chat.id,
                         text=bot_texts.cance_reg,
                         reply_markup=remove_markup,
                         parse_mode="Markdown")


# Отримування номеру телефону
def register_four(message, user_username, user_name):
    if message.text != bot_texts.cance:
        if message.text is not None:
            user_phone = message.text
            rule = re.compile(r'^\+?(38)?(0)\d{9,13}$')
            if rule.search(user_phone):
                # Перехід до register_five
                button_a = types.KeyboardButton(bot_texts.reg_pass_addres)
                markup = types.ReplyKeyboardMarkup()
                markup = markup.row(button_a).row(cance_button)

                bot.send_message(chat_id=message.chat.id,
                                 text=bot_texts.h_your_addres,
                                 reply_markup=markup,
                                 parse_mode="Markdown")
                bot.register_next_step_handler(message, register_five, user_username, user_name, user_phone)
            else:
                # Потреба у користувача ввести коректно
                bot.send_message(chat_id=message.chat.id,
                                 text=bot_texts.write_correct,
                                 reply_markup=cance_markup,
                                 parse_mode="Markdown")
                bot.register_next_step_handler(message, register_four, user_username, user_name)
        else:
            # Потреба у користувача ввести коректно
            bot.send_message(chat_id=message.chat.id,
                             text=bot_texts.write_correct,
                             reply_markup=cance_markup,
                             parse_mode="Markdown")
            bot.register_next_step_handler(message, register_four, user_username, user_name)
    else:
        # Реєстрація відмінена
        log(f"{message.from_user.id} відмінив реєстрацію")
        bot.send_message(chat_id=message.chat.id,
                         text=bot_texts.cance_reg,
                         reply_markup=remove_markup,
                         parse_mode="Markdown")


# Отримування адреси для замовлення
def register_five(message, user_username, user_name, user_phone):
    if message.text != bot_texts.cance:
        if message.text is not None:
            # Перехід до register_six
            if message.text == bot_texts.reg_pass_addres:
                user_addres = bot_texts.none_addres
            else:
                user_addres = message.text

            button_yes = types.KeyboardButton(bot_texts.yes)
            button_no = types.KeyboardButton(bot_texts.no)
            markup = types.ReplyKeyboardMarkup()
            markup = markup.row(button_yes, button_no).row(cance_button)

            text = bot_texts.user_correct_info(name=user_name,
                                               username=user_username,
                                               phone=user_phone,
                                               addres=user_addres)
            bot.send_message(chat_id=message.chat.id,
                             text=text,
                             reply_markup=markup,
                             parse_mode="Markdown")
            bot.register_next_step_handler(message, register_six, user_username, user_name, user_phone, user_addres)
        else:
            # Потреба у користувача ввести коректно
            button_a = types.KeyboardButton(bot_texts.reg_pass_addres)
            markup = types.ReplyKeyboardMarkup()
            markup = markup.row(button_a).row(cance_button)

            bot.send_message(chat_id=message.chat.id,
                             text=bot_texts.write_correct,
                             reply_markup=markup,
                             parse_mode="Markdown")
            bot.register_next_step_handler(message, register_five, user_username, user_name, user_phone)
    else:
        # Реєстрація відмінена
        log(f"{message.from_user.id} відмінив реєстрацію")
        bot.send_message(chat_id=message.chat.id,
                         text=bot_texts.cance_reg,
                         reply_markup=remove_markup,
                         parse_mode="Markdown")


# Перевірка на правильність введених данних
def register_six(message, user_username, user_name, user_phone, user_addres):
    if message.text != bot_texts.cance:
        if message.text == bot_texts.no:
            #  Повернення на register_three
            bot.send_message(chat_id=message.chat.id,
                             text=bot_texts.reg_restart,
                             reply_markup=cance_markup,
                             parse_mode="Markdown")
            user_username = message.from_user.username
            bot.register_next_step_handler(message, register_three, user_username)
        elif message.text == bot_texts.yes:
            #  Завершення реєстрації
            log(f"{message.from_user.id} зареєструвався")
            User(user_id=message.from_user.id,
                 name=user_name,
                 username=user_username,
                 phone_number=user_phone,
                 addres=user_addres).insert()
            bot.send_message(chat_id=message.chat.id,
                             text=bot_texts.reg_succes,
                             reply_markup=menu_markup,
                             parse_mode="Markdown")
        else:
            # Обрано те чого немає в меню, повернення сюди ж
            button_yes = types.KeyboardButton(bot_texts.yes)
            button_no = types.KeyboardButton(bot_texts.no)
            markup = types.ReplyKeyboardMarkup()
            markup = markup.row(button_yes, button_no).row(cance_button)
            bot.send_message(chat_id=message.chat.id,
                             text=bot_texts.none_in_menu,
                             reply_markup=markup,
                             parse_mode="Markdown")
            bot.register_next_step_handler(message, register_six, user_username, user_name, user_phone, user_addres)
    else:
        # Реєстрація відмінена
        log(f"{message.from_user.id} відмінив реєстрацію")
        bot.send_message(chat_id=message.chat.id,
                         text=bot_texts.cance_reg,
                         reply_markup=remove_markup,
                         parse_mode="Markdown")


# обробка текстових команд
@bot.message_handler(content_types=['text'])
def texter(message):
    log(f"{message.from_user.id} попав в текстовий обробник")
    # Перевірка на бан
    if extend_banlist(message.from_user.id):
        # USER

        if not extend_user(message.from_user.id):

            # Мої замовлення
            if message.text == bot_texts.my_orders:
                log(f"{message.from_user.id} запросив свої замовлення")
                orders = get_my_open_orders(message.from_user.id)
                if len(orders) != 0:
                    # Виведення активних замовлень
                    bot.send_message(chat_id=message.chat.id,
                                     text=bot_texts.active_orders,
                                     reply_markup=menu_markup,
                                     parse_mode="Markdown")
                    for i in orders:
                        bot.send_message(chat_id=message.chat.id,
                                         text=bot_texts.order_text(i),
                                         parse_mode="Markdown")
                else:
                    # Замовлення відсутні
                    bot.send_message(chat_id=message.chat.id,
                                     text=bot_texts.none_active_orders,
                                     reply_markup=menu_markup,
                                     parse_mode="Markdown")

            # Створити нове замовлення
            elif message.text == bot_texts.shop:
                log(f"{message.from_user.id} почав створювати нове замовлення")
                #  Перехід до shop_category
                list_products = []
                list_amounts = []
                bot.send_message(chat_id=message.chat.id,
                                 text=bot_texts.choice_group,
                                 reply_markup=group_markup,
                                 parse_mode="Markdown")
                bot.register_next_step_handler(message, shop_kategory, list_products, list_amounts)

            # Відправити фідбек
            elif message.text == bot_texts.feedback:
                log(f"{message.from_user.id} Обрав відправлення фідбеку")
                #  Перехід до create_feedback
                bot.send_message(chat_id=message.chat.id,
                                 text=bot_texts.feed_text,
                                 reply_markup=feed_markup,
                                 parse_mode="Markdown")
                bot.register_next_step_handler(message, create_feedback)

            # Вивід тексту про нас
            elif message.text == bot_texts.about:
                log(f"{message.from_user.id} запросив текст про нас")
                bot.send_message(chat_id=message.chat.id,
                                 text=bot_texts.about_text,
                                 reply_markup=menu_markup,
                                 parse_mode="Markdown")

            # ADMIN
            elif message.chat.id == settings.ID_ADMIN_GROUP or not settings.ONLY_ADMIN_GROUP:
                if message.from_user.username in settings.ADMINS:

                    # Вивести всі активні замовлення
                    if message.text == bot_texts.all_open_orders:
                        log(f"{message.from_user.id} запросив всі активні замовлення")
                        mass_orders = get_all_open_orders()
                        if len(mass_orders) != 0:
                            for b in mass_orders:
                                keyboard = types.InlineKeyboardMarkup()
                                data_mass = [bot_texts.command, bot_texts.change_status, str(b.order_id)]
                                data_str = "|".join(data_mass)
                                keyboard.add(types.InlineKeyboardButton(text=bot_texts.change_status,
                                                                        callback_data=data_str))
                                bot.send_message(chat_id=message.chat.id,
                                                 text=bot_texts.order_text_admin(b),
                                                 reply_markup=keyboard,
                                                 parse_mode="Markdown")
                        else:
                            # Немає активних замовлень
                            bot.send_message(chat_id=message.chat.id,
                                             text=bot_texts.none_active_orders_admin,
                                             reply_markup=admin_markup,
                                             parse_mode="Markdown")

                    # Додати новий товар
                    elif message.text == bot_texts.add_product:
                        log(f"{message.from_user.id} почав додавати новий товар")
                        #  Перехід до add_product
                        bot.send_message(chat_id=message.chat.id,
                                         text=bot_texts.add_product_group,
                                         reply_markup=group_markup,
                                         parse_mode="Markdown")
                        bot.register_next_step_handler(message, add_product)

                    # Додати нову групу товарів
                    elif message.text == bot_texts.add_group:
                        log(f"{message.from_user.id} почав створювати нову групу")
                        #  Перехід до add_group
                        bot.send_message(chat_id=message.chat.id,
                                         text=bot_texts.add_group_name,
                                         reply_markup=cance_markup,
                                         parse_mode="Markdown")
                        bot.register_next_step_handler(message, add_group)

                    # Змінити дані продукту
                    elif message.text == bot_texts.change_product:
                        log(f"{message.from_user.id} почав змінювати дані продукту")
                        #  Перехід до cp_get_group
                        bot.send_message(chat_id=message.chat.id,
                                         text=bot_texts.cp_get_group,
                                         reply_markup=group_markup,
                                         parse_mode="Markdown")
                        bot.register_next_step_handler(message, cp_get_group)

                    # Змінити дані групи
                    elif message.text == bot_texts.change_group:
                        log(f"{message.from_user.id} почав змінювати дані групи")
                        #  Перехід до cg_get_group
                        bot.send_message(chat_id=message.chat.id,
                                         text=bot_texts.cg_get_group,
                                         reply_markup=group_markup,
                                         parse_mode="Markdown")
                        bot.register_next_step_handler(message, cg_get_group)

                    # Видалити продукт
                    elif message.text == bot_texts.del_product:
                        #  Перехід до dp_get_group
                        log(f"{message.from_user.id} почав видалення продукту")
                        bot.send_message(chat_id=message.chat.id,
                                         text=bot_texts.dp_get_group,
                                         reply_markup=group_markup,
                                         parse_mode="Markdown")
                        bot.register_next_step_handler(message, dp_get_group)

                    # Видалити групу продуктів та її продукти
                    elif message.text == bot_texts.del_group:
                        #  Перехід до dg_get_group
                        log(f"{message.from_user.id} почав видалення групи")
                        bot.send_message(chat_id=message.chat.id,
                                         text=bot_texts.dg_get_group,
                                         reply_markup=group_markup,
                                         parse_mode="Markdown")
                        bot.register_next_step_handler(message, dg_get_group)
            else:
                # Не найдено в меню
                bot.send_message(message.chat.id, bot_texts.none_in_menu, reply_markup=menu_markup)
        else:
            bot.send_message(message.chat.id, bot_texts.go_start, reply_markup=remove_markup)
    else:
        # Користувач забанений
        bot.send_message(message.chat.id, bot_texts.you_have_ban, reply_markup=remove_markup)


# Шлях створення замовлення, отримання групи продукту
def shop_kategory(message, list_products, list_amounts):
    if bot_texts.cance != message.text:
        product_markup = types.ReplyKeyboardMarkup()
        if extend_group(message.text):
            #  Перехід до shop_product
            it_group = get_group(get_group_id(message.text))
            products = get_products_by_group(it_group.group_id)
            for b in products:
                product_markup.row(types.KeyboardButton(b.name))
            product_markup.row(cance_button).row(back_button)
            photo = open(f"{settings.IMG_FOLDER + it_group.prev_img}", 'rb')
            bot.send_photo(message.chat.id,
                           photo=photo,
                           caption=bot_texts.choice_product,
                           reply_markup=product_markup,
                           parse_mode="Markdown")
            bot.register_next_step_handler(message, shop_product, list_products, list_amounts, it_group)
        else:
            # Потреба у користувача ввести коректно
            bot.send_message(chat_id=message.chat.id,
                             text=bot_texts.none_in_menu,
                             reply_markup=group_markup,
                             parse_mode="Markdown")
            bot.register_next_step_handler(message, shop_kategory, list_products, list_amounts)
    else:
        # Дія відмінена
        bot.send_message(chat_id=message.chat.id,
                         text=bot_texts.return_to_menu,
                         reply_markup=menu_markup,
                         parse_mode="Markdown")


# Отримання продукту
def shop_product(message, list_products, list_amounts, it_group):
    product_name = message.text
    if bot_texts.cance == message.text:
        # Дія відмінена
        bot.send_message(chat_id=message.chat.id,
                         text=bot_texts.return_to_menu,
                         reply_markup=menu_markup,
                         parse_mode="Markdown")
    elif bot_texts.back == message.text:
        bot.send_message(chat_id=message.chat.id,
                         text=bot_texts.choice_group,
                         reply_markup=group_markup,
                         parse_mode="Markdown")
        bot.register_next_step_handler(message, shop_kategory, list_products, list_amounts)
    elif extend_product(message.text):
        #  Перехід до shop_amount
        s_product = get_product_by_name(product_name)
        photo = open(f"{settings.IMG_FOLDER + s_product.prev_img}", 'rb')
        bot.send_photo(chat_id=message.chat.id,
                       photo=photo,
                       caption=bot_texts.product_send(s_product) + "\n" + bot_texts.choice_amount,
                       reply_markup=bc_markup,
                       parse_mode="Markdown")
        bot.register_next_step_handler(message, shop_amount, list_products, list_amounts, it_group, s_product)
    else:
        # Потреба у користувача ввести коректно
        bot.send_message(chat_id=message.chat.id,
                         text=bot_texts.none_in_menu,
                         parse_mode="Markdown")
        bot.register_next_step_handler(message, shop_product, list_products, list_amounts, it_group)


# Отримання кількості продукту
def shop_amount(message, list_products, list_amounts, it_group, s_product):
    if message.text == bot_texts.cance:
        # Дія відмінена
        bot.send_message(chat_id=message.chat.id,
                         text=bot_texts.return_to_menu,
                         reply_markup=menu_markup,
                         parse_mode="Markdown")
    elif bot_texts.back == message.text:
        #  Перехід до shop_product
        product_markup = types.ReplyKeyboardMarkup()
        products = get_products_by_group(it_group.group_id)
        for b in products:
            product_markup.row(types.KeyboardButton(b.name))
        product_markup.row(cance_button).row(back_button)
        photo = open(f"{settings.IMG_FOLDER + it_group.prev_img}", 'rb')
        bot.send_photo(message.chat.id,
                       photo=photo,
                       caption=bot_texts.choice_product,
                       reply_markup=product_markup,
                       parse_mode="Markdown")
        bot.register_next_step_handler(message, shop_product, list_products, list_amounts, it_group)
    elif extend_int(message.text):
        #  Перехід до shop_per
        amount = int(message.text)
        list_products.append(s_product)
        list_amounts.append(amount)
        cart_text = bot_texts.cart_text(list_products, list_amounts)
        bot.send_message(chat_id=message.chat.id,
                         text=bot_texts.con_text(cart_text),
                         reply_markup=shop_markup,
                         parse_mode="Markdown")
        bot.register_next_step_handler(message, shop_per, list_products, list_amounts)
    else:
        # Потреба у користувача ввести коректно
        bot.send_message(chat_id=message.chat.id,
                         text=bot_texts.write_correct,
                         reply_markup=bc_markup,
                         parse_mode="Markdown")
        bot.register_next_step_handler(message, shop_amount, list_products, list_amounts, it_group, s_product)


# Вибір чи продовжити покупки/створення замовлення
def shop_per(message, list_products, list_amounts):
    if message.text == bot_texts.cance:
        # Дія відмінена
        bot.send_message(chat_id=message.chat.id,
                         text=bot_texts.return_to_menu,
                         reply_markup=menu_markup,
                         parse_mode="Markdown")

    # Початок оформлення замовлення
    elif message.text == bot_texts.start_order:
        #  Перехід до shop_comment
        bot.send_message(chat_id=message.chat.id,
                         text=bot_texts.shop_comment,
                         reply_markup=pass_markup,
                         parse_mode="Markdown")
        bot.register_next_step_handler(message, shop_comment, list_products, list_amounts)

    # Продовження покупок
    elif message.text == bot_texts.continue_buy:
        bot.send_message(chat_id=message.chat.id,
                         text=bot_texts.choice_group,
                         reply_markup=group_markup,
                         parse_mode="Markdown")
        bot.register_next_step_handler(message, shop_kategory, list_products, list_amounts)

    # Відсутнє в меню
    else:
        # Потреба у користувача ввести коректно
        bot.send_message(chat_id=message.chat.id,
                         text=bot_texts.none_in_menu,
                         reply_markup=shop_markup,
                         parse_mode="Markdown")
        bot.register_next_step_handler(message, shop_per, list_products, list_amounts)


# Отримання коментаря
def shop_comment(message, list_products, list_amounts):
    if message.text != bot_texts.cance:
        # Перехід до shop_delivery

        # Перевірка коментаря
        if message.text != bot_texts.pass_text and message.text is not None:
            comment = message.text
        else:
            comment = bot_texts.non_comment

        # Перевірка на те чи є користувач в базі
        if not extend_user(message.from_user.id):
            its_user = get_user(message.from_user.id)
            bot.send_message(chat_id=message.chat.id,
                             text=bot_texts.pid_addres(its_user.addres),
                             reply_markup=yn_markup,
                             parse_mode="Markdown")
            bot.register_next_step_handler(message, shop_delivery, list_products, list_amounts, comment)
        else:
            # Користувача немає в базі
            bot.send_message(chat_id=message.chat.id,
                             text=bot_texts.unknown_err,
                             reply_markup=menu_markup,
                             parse_mode="Markdown")
    else:
        # Дія відмінена
        bot.send_message(chat_id=message.chat.id,
                         text=bot_texts.return_to_menu,
                         reply_markup=menu_markup,
                         parse_mode="Markdown")


# Вибір чи доставляти й куди
def shop_delivery(message, list_products, list_amounts, comment):
    # Перехід до shop_delivery_two

    # Доставляти на дефолтну адресу
    if message.text == bot_texts.yes:
        its_user = get_user(message.from_user.id)
        text = bot_texts.pid_order(list_products=list_products,
                                   list_amounts=list_amounts,
                                   comment=comment,
                                   delivery=its_user.addres)
        bot.send_message(chat_id=message.chat.id,
                         text=text,
                         reply_markup=yn_markup,
                         parse_mode="Markdown")
        bot.register_next_step_handler(message, shop_delivery_two, list_products, list_amounts, comment)

    # Не доставляти
    elif message.text == bot_texts.no:
        text = bot_texts.pid_order(list_products=list_products,
                                   list_amounts=list_amounts,
                                   comment=comment,
                                   delivery=bot_texts.none_addres)
        bot.send_message(chat_id=message.chat.id,
                         text=text,
                         reply_markup=yn_markup,
                         parse_mode="Markdown")
        bot.register_next_step_handler(message, shop_delivery_two, list_products, list_amounts, comment)

    # Доставляти але на змінивши адресу
    else:
        if message.text is not None:
            text = bot_texts.pid_order(list_products=list_products,
                                       list_amounts=list_amounts,
                                       comment=comment,
                                       delivery=message.text)
            it_user = get_user(message.from_user.id)
            it_user.addres = message.text
            it_user.update()

            bot.send_message(chat_id=message.chat.id,
                             text=text,
                             reply_markup=yn_markup,
                             parse_mode="Markdown")
            bot.register_next_step_handler(message, shop_delivery_two, list_products, list_amounts, comment)
        else:
            # Потреба у користувача ввести коректно
            bot.send_message(chat_id=message.chat.id,
                             text=bot_texts.write_correct,
                             reply_markup=yn_markup,
                             parse_mode="Markdown")
            bot.register_next_step_handler(message, shop_per, list_products, list_amounts)


# Перевірка чи все правильно та оформлення замовлення
def shop_delivery_two(message, list_products, list_amounts, comment):
    if message.text == bot_texts.yes:
        its_user = get_user(message.from_user.id)
        it_order_content = bot_texts.order_content(list_products=list_products,
                                                   list_amounts=list_amounts,
                                                   delivery=its_user.addres,
                                                   comment=comment)
        new_order = Order(user=its_user,
                          content=it_order_content,
                          status=get_status(1),
                          create_date=datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                          close_date=bot_texts.none_close_date, )
        new_order.insert()

        log(f"{message.from_user.id} створив замовлення")

        bot.send_message(chat_id=message.chat.id,
                         text=bot_texts.succes_create_order,
                         parse_mode="Markdown")

        keyboard = types.InlineKeyboardMarkup()
        data_mass = [bot_texts.command, bot_texts.change_status, str(new_order.order_id)]
        data_str = "|".join(data_mass)
        keyboard.add(types.InlineKeyboardButton(text=bot_texts.change_status,
                                                callback_data=data_str))
        # в адмін групу
        bot.send_message(chat_id=settings.ID_ADMIN_GROUP,
                         text=bot_texts.order_text_admin(new_order),
                         parse_mode="Markdown",
                         reply_markup=keyboard)

        # користувачу
        bot.send_message(chat_id=message.chat.id,
                         text=bot_texts.order_text(new_order),
                         parse_mode="Markdown",
                         reply_markup=menu_markup)
    else:
        # Дія відмінена
        bot.send_message(chat_id=message.chat.id,
                         text=bot_texts.unsucces_order,
                         parse_mode="Markdown",
                         reply_markup=menu_markup)


# Шлях feedback
def create_feedback(message):
    # Перейти до send_feedback
    if message.text == bot_texts.create_comment:
        bot.send_message(chat_id=message.chat.id,
                         text=bot_texts.p_send_feedback,
                         parse_mode="Markdown",
                         reply_markup=remove_markup)
        bot.register_next_step_handler(message, send_feedback)

    # Повернутися в меню
    elif message.text == bot_texts.cance:
        bot.send_message(chat_id=message.chat.id,
                         text=bot_texts.return_to_menu,
                         parse_mode="Markdown",
                         reply_markup=menu_markup)

    # Потреба у користувача ввести коректно
    else:
        bot.send_message(chat_id=message.chat.id,
                         text=bot_texts.write_correct,
                         reply_markup=feed_markup,
                         parse_mode="Markdown")
        bot.register_next_step_handler(message, create_feedback)


# Відправка повідомлення в групу фідбеку
def send_feedback(message):
    if message.text != bot_texts.cance:
        # В групу коментарів
        bot.send_message(chat_id=settings.COMMENT_GROUP,
                         text=f"Від: ID `{message.from_user.id}`",
                         parse_mode="Markdown")
        try:
            bot.forward_message(chat_id=settings.COMMENT_GROUP,
                                from_chat_id=message.chat.id,
                                message_id=message.id)
            log(f"{message.from_user.id} відправив коментарій в фідбек")

            # Користувачу, що повідомлення доставлено
            bot.send_message(chat_id=message.chat.id,
                             text=bot_texts.s_send_feedback,
                             parse_mode="Markdown",
                             reply_markup=menu_markup)
        except Exception as ex:
            # Користувачу, що повідомлення НЕ доставлено
            print(ex)
            log(f"{message.from_user.id} не зміг відправити коментарій")
            bot.send_message(chat_id=message.chat.id,
                             text=bot_texts.forward_err,
                             parse_mode="Markdown",
                             reply_markup=menu_markup)
    else:
        # Дія відмінена
        bot.send_message(chat_id=message.chat.id,
                         text=bot_texts.return_to_menu,
                         parse_mode="Markdown",
                         reply_markup=menu_markup)


# Шлях додовання товару, отримання групи
def add_product(message):
    if message.text != bot_texts.cance:
        if extend_group(message.text):
            # Перейти до add_product_two
            it_group = get_group_id(message.text)
            bot.send_message(chat_id=message.chat.id,
                             text=bot_texts.add_product_name,
                             parse_mode="Markdown",
                             reply_markup=cance_markup)
            bot.register_next_step_handler(message, add_product_two, it_group)
        else:
            # Потреба у користувача ввести коректно
            bot.send_message(chat_id=message.chat.id,
                             text=bot_texts.none_in_menu,
                             reply_markup=group_markup,
                             parse_mode="Markdown")
            bot.register_next_step_handler(message, add_product)
    else:
        # Дія відмінена
        bot.send_message(chat_id=message.chat.id,
                         text=bot_texts.return_to_menu,
                         parse_mode="Markdown",
                         reply_markup=admin_markup)


# Отримання name
def add_product_two(message, it_group):
    if message.text != bot_texts.cance:
        name = message.text
        if name is not None:
            # Перейти до add_product_three
            bot.send_message(chat_id=message.chat.id,
                             text=bot_texts.add_product_img,
                             parse_mode="Markdown",
                             reply_markup=cance_markup)
            bot.register_next_step_handler(message, add_product_three, it_group, name)
        else:
            # Потреба у користувача ввести коректно
            bot.send_message(chat_id=message.chat.id,
                             text=bot_texts.write_correct,
                             reply_markup=cance_markup,
                             parse_mode="Markdown")
            bot.register_next_step_handler(message, add_product_two, it_group)
    else:
        # Дія відмінена
        bot.send_message(chat_id=message.chat.id,
                         text=bot_texts.return_to_menu,
                         parse_mode="Markdown",
                         reply_markup=admin_markup)


# Отримання фото
def add_product_three(message, it_group, name):
    if message.text != bot_texts.cance:
        try:
            # Перейти до add_product_four
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            src = settings.IMG_FOLDER + file_info.file_path[10:]
            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)
            img_prev = file_info.file_path[10:]
            bot.send_message(chat_id=message.chat.id,
                             text=bot_texts.add_product_description,
                             parse_mode="Markdown",
                             reply_markup=cance_markup)
            bot.register_next_step_handler(message, add_product_four, it_group, name, img_prev)
        except Exception as ex:
            # Бот не зміг прийняти фото
            print(ex)
            log(f"{message.from_user.id} не зміг відправити боту картинку")
            bot.send_message(chat_id=message.chat.id,
                             text=bot_texts.image_err,
                             reply_markup=cance_markup,
                             parse_mode="Markdown")
            bot.register_next_step_handler(message, add_product_three, it_group, name)
    else:
        # Дія відмінена
        bot.send_message(chat_id=message.chat.id,
                         text=bot_texts.return_to_menu,
                         parse_mode="Markdown",
                         reply_markup=admin_markup)


# Отримання опису
def add_product_four(message, it_group, name, img_prev):
    if message.text != bot_texts.cance:
        # Перейти до add_product_five
        description = message.text
        if description is not None:
            bot.send_message(chat_id=message.chat.id,
                             text=bot_texts.add_product_price,
                             parse_mode="Markdown",
                             reply_markup=cance_markup)
            bot.register_next_step_handler(message, add_product_five, it_group, name, img_prev, description)
        else:
            # Потреба у користувача ввести коректно
            bot.send_message(chat_id=message.chat.id,
                             text=bot_texts.write_correct,
                             reply_markup=cance_markup,
                             parse_mode="Markdown")
            bot.register_next_step_handler(message, add_product_four, it_group, name, img_prev)
    else:
        # Дія відмінена
        bot.send_message(chat_id=message.chat.id,
                         text=bot_texts.return_to_menu,
                         parse_mode="Markdown",
                         reply_markup=admin_markup)


# Отримання ціни
def add_product_five(message, it_group, name, img_prev, description):
    if message.text != bot_texts.cance:
        # Перейти до add_product_six
        if extend_int(message.text):
            price = int(message.text)
            bot.send_message(chat_id=message.chat.id,
                             text=bot_texts.correct,
                             parse_mode="Markdown",
                             reply_markup=yn_markup)
            s_product = Product(group=get_group(it_group),
                                name=name,
                                prev_img=img_prev,
                                description=description,
                                price=price)
            photo = open(f"{settings.IMG_FOLDER + s_product.prev_img}", 'rb')
            print(bot_texts.product_send(s_product))
            bot.send_photo(chat_id=message.chat.id,
                           photo=photo,
                           caption=bot_texts.product_send(s_product),
                           parse_mode="Markdown")
            bot.register_next_step_handler(message, add_product_six, it_group, name, img_prev, description, price)
        else:
            # Потреба у користувача ввести коректно
            bot.send_message(chat_id=message.chat.id,
                             text=bot_texts.write_correct,
                             reply_markup=cance_markup,
                             parse_mode="Markdown")
            bot.register_next_step_handler(message, add_product_five, it_group, name, img_prev, description)
    else:
        # Дія відмінена
        bot.send_message(chat_id=message.chat.id,
                         text=bot_texts.return_to_menu,
                         parse_mode="Markdown",
                         reply_markup=admin_markup)


# Підтвердження
def add_product_six(message, it_group, name, img_prev, description, price):
    if message.text == bot_texts.yes:
        # Завершення створення товару
        s_product = Product(group=get_group(it_group),
                            name=name,
                            prev_img=img_prev,
                            description=description,
                            price=price)
        s_product.insert()
        log(f"{message.from_user.id} додав новий продукт {s_product.name}")
        bot.send_message(chat_id=message.chat.id,
                         text=bot_texts.add_product_succes,
                         parse_mode="Markdown",
                         reply_markup=admin_markup)
    else:
        # Дія відмінена
        bot.send_message(chat_id=message.chat.id,
                         text=bot_texts.return_to_menu,
                         parse_mode="Markdown",
                         reply_markup=admin_markup)


#  Шлях по додаванню групи
def add_group(message):
    if message.text != bot_texts.cance:
        name = message.text
        if name is not None:
            # Перейти до add_product_two
            bot.send_message(chat_id=message.chat.id,
                             text=bot_texts.add_group_img,
                             parse_mode="Markdown",
                             reply_markup=cance_markup)
            bot.register_next_step_handler(message, add_group_two, name)
        else:
            # Потреба у користувача ввести коректно
            bot.send_message(chat_id=message.chat.id,
                             text=bot_texts.write_correct,
                             reply_markup=cance_markup,
                             parse_mode="Markdown")
            bot.register_next_step_handler(message, add_group)
    else:
        # Дія відмінена
        bot.send_message(chat_id=message.chat.id,
                         text=bot_texts.return_to_menu,
                         parse_mode="Markdown",
                         reply_markup=admin_markup)


# Отримування фото
def add_group_two(message, name):
    if message.text != bot_texts.cance:
        try:
            # Перейти до add_product_three
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            src = settings.IMG_FOLDER + file_info.file_path[10:]
            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)
            img_prev = file_info.file_path[10:]
            bot.send_message(chat_id=message.chat.id,
                             text=bot_texts.correct,
                             parse_mode="Markdown",
                             reply_markup=yn_markup)
            s_group = Group(name=name,
                            prev_img=img_prev)
            photo = open(f"{settings.IMG_FOLDER + s_group.prev_img}", 'rb')
            print(bot_texts.group_send(s_group))
            bot.send_photo(chat_id=message.chat.id,
                           photo=photo,
                           caption=s_group.name,
                           parse_mode="Markdown")
            bot.register_next_step_handler(message, add_group_three, name, img_prev)
        except Exception as ex:
            # Бот не зміг прийняти фото
            print(ex)
            log(f"{message.from_user.id} не зміг відправити боту картинку")
            bot.send_message(chat_id=message.chat.id,
                             text=bot_texts.image_err,
                             reply_markup=cance_markup,
                             parse_mode="Markdown")
    else:
        # Дія відмінена
        bot.send_message(chat_id=message.chat.id,
                         text=bot_texts.return_to_menu,
                         parse_mode="Markdown",
                         reply_markup=admin_markup)


# Підтвердження
def add_group_three(message, name, img_prev):
    if message.text == bot_texts.yes:
        # Завершення створення групи
        s_group = Group(name=name,
                        prev_img=img_prev)
        s_group.insert()

        log(f"{message.from_user.id} додав нову групу {s_group.name}")

        # Оновленя глобальної клавіатури груп
        global group_markup
        group_markup = get_group_markup()

        bot.send_message(chat_id=message.chat.id,
                         text=bot_texts.add_group_succes,
                         parse_mode="Markdown",
                         reply_markup=admin_markup)
    else:
        # Дія відмінена
        bot.send_message(chat_id=message.chat.id,
                         text=bot_texts.return_to_menu,
                         parse_mode="Markdown",
                         reply_markup=admin_markup)


# Вибір групи продукту що змінюється
def cp_get_group(message):
    if message.text != bot_texts.cance:
        if extend_group(message.text):
            # Перейти до cp_get_product
            it_group = get_group(get_group_id(message.text))
            products = get_products_by_group(it_group.group_id)
            product_markup = types.ReplyKeyboardMarkup()
            for b in products:
                product_markup.row(types.KeyboardButton(b.name))
            bot.send_message(chat_id=message.chat.id,
                             text=bot_texts.cp_get_product,
                             parse_mode="Markdown",
                             reply_markup=product_markup)
            bot.register_next_step_handler(message, cp_get_product)
        else:
            # Потреба у користувача ввести коректно
            bot.send_message(chat_id=message.chat.id,
                             text=bot_texts.none_in_menu,
                             reply_markup=group_markup,
                             parse_mode="Markdown")
            bot.register_next_step_handler(message, cp_get_group)
    else:
        # Дія відмінена
        bot.send_message(chat_id=message.chat.id,
                         text=bot_texts.return_to_menu,
                         parse_mode="Markdown",
                         reply_markup=admin_markup)


# Вибір продукту що змінюється
def cp_get_product(message):
    if message.text != bot_texts.cance:
        if extend_product(message.text):
            # Перейти до change_product
            s_product = get_product_by_name(message.text)
            photo = open(f"{settings.IMG_FOLDER + s_product.prev_img}", 'rb')
            bot.send_photo(chat_id=message.chat.id,
                           photo=photo,
                           caption=bot_texts.product_send(s_product),
                           parse_mode="Markdown", )
            bot.send_message(chat_id=message.chat.id,
                             text=bot_texts.change_text,
                             parse_mode="Markdown",
                             reply_markup=change_product_markup)
            bot.register_next_step_handler(message, change_product, s_product.product_id)
        else:
            # Потреба у користувача ввести коректно
            bot.send_message(chat_id=message.chat.id,
                             text=bot_texts.none_in_menu,
                             parse_mode="Markdown")
            bot.register_next_step_handler(message, cp_get_product)
    else:
        # Дія відмінена
        bot.send_message(chat_id=message.chat.id,
                         text=bot_texts.return_to_menu,
                         parse_mode="Markdown",
                         reply_markup=admin_markup)


# Меню вибору що змінити в продукті
def change_product(message, product_id):
    # Зміна назви
    if message.text == bot_texts.change_product_name:
        # Перейти до change_product_name
        bot.send_message(chat_id=message.chat.id,
                         text=bot_texts.change_product_name_text,
                         parse_mode="Markdown",
                         reply_markup=cance_markup)
        bot.register_next_step_handler(message, change_product_name, product_id)

    # Зміна ціни
    elif message.text == bot_texts.change_product_price:
        # Перейти до change_product_price
        bot.send_message(chat_id=message.chat.id,
                         text=bot_texts.change_product_price_text,
                         parse_mode="Markdown",
                         reply_markup=cance_markup)
        bot.register_next_step_handler(message, change_product_price, product_id)

    # Зміна картинки
    elif message.text == bot_texts.change_product_img:
        # Перейти до change_product_img
        bot.send_message(chat_id=message.chat.id,
                         text=bot_texts.change_product_img_text,
                         parse_mode="Markdown",
                         reply_markup=cance_markup)
        bot.register_next_step_handler(message, change_product_img, product_id)

    # Зміна опису
    elif message.text == bot_texts.change_product_description:
        # Перейти до change_product_description
        bot.send_message(chat_id=message.chat.id,
                         text=bot_texts.change_product_desc_text,
                         parse_mode="Markdown",
                         reply_markup=cance_markup)
        bot.register_next_step_handler(message, change_product_description, product_id)

    # Зміна групи
    elif message.text == bot_texts.change_product_group:
        # Перейти до change_product_group
        bot.send_message(chat_id=message.chat.id,
                         text=bot_texts.change_product_group_text,
                         parse_mode="Markdown",
                         reply_markup=group_markup)
        bot.register_next_step_handler(message, change_product_group, product_id)

    # Повернення в меню
    else:
        bot.send_message(chat_id=message.chat.id,
                         text=bot_texts.return_to_menu,
                         parse_mode="Markdown",
                         reply_markup=admin_markup)


# Зміна імені продукту
def change_product_name(message, product_id):
    if message.text != bot_texts.cance:
        if message.text is not None:
            # Зміна імені в продукті
            s_product = get_product(product_id)
            old_name = s_product.name
            s_product.name = message.text
            s_product.update()
            log(f"{message.from_user.id} змінив назву продукту з {old_name} на {s_product.name}")
            photo = open(f"{settings.IMG_FOLDER + s_product.prev_img}", 'rb')
            bot.send_photo(chat_id=message.chat.id,
                           photo=photo,
                           caption=bot_texts.product_send(s_product),
                           parse_mode="Markdown", )
            bot.send_message(chat_id=message.chat.id,
                             text=bot_texts.change_text,
                             parse_mode="Markdown",
                             reply_markup=change_product_markup)
            bot.register_next_step_handler(message, change_product, product_id)
        else:
            # Потреба у користувача ввести коректно
            bot.send_message(chat_id=message.chat.id,
                             text=bot_texts.write_correct,
                             reply_markup=cance_markup,
                             parse_mode="Markdown")
            bot.register_next_step_handler(message, change_product_name, product_id)

    # Повернення до меню зміни продукту
    else:
        s_product = get_product_by_name(product_id)
        photo = open(f"{settings.IMG_FOLDER + s_product.prev_img}", 'rb')
        bot.send_photo(chat_id=message.chat.id,
                       photo=photo,
                       caption=bot_texts.product_send(s_product),
                       parse_mode="Markdown", )
        bot.send_message(chat_id=message.chat.id,
                         text=bot_texts.change_text,
                         parse_mode="Markdown",
                         reply_markup=change_product_markup)
        bot.register_next_step_handler(message, change_product, product_id)


# Зміна ціни продукту
def change_product_price(message, product_id):
    if message.text != bot_texts.cance:
        if extend_int(message.text):
            # Зміна ціни в продукті
            s_product = get_product(product_id)
            old_price = s_product.price
            s_product.price = int(message.text)
            s_product.update()
            log(f"{message.from_user.id} змінив ціну продукту {s_product.name} з {old_price} на {s_product.price}")
            photo = open(f"{settings.IMG_FOLDER + s_product.prev_img}", 'rb')
            bot.send_photo(chat_id=message.chat.id,
                           photo=photo,
                           caption=bot_texts.product_send(s_product),
                           parse_mode="Markdown", )
            bot.send_message(chat_id=message.chat.id,
                             text=bot_texts.change_text,
                             parse_mode="Markdown",
                             reply_markup=change_product_markup)
            bot.register_next_step_handler(message, change_product, product_id)
        else:
            # Потреба у користувача ввести коректно
            bot.send_message(chat_id=message.chat.id,
                             text=bot_texts.write_correct,
                             reply_markup=cance_markup,
                             parse_mode="Markdown")
            bot.register_next_step_handler(message, change_product_price, product_id)

    # Повернення до меню зміни продукту
    else:
        s_product = get_product_by_name(product_id)
        photo = open(f"{settings.IMG_FOLDER + s_product.prev_img}", 'rb')
        bot.send_photo(chat_id=message.chat.id,
                       photo=photo,
                       caption=bot_texts.product_send(s_product),
                       parse_mode="Markdown", )
        bot.send_message(chat_id=message.chat.id,
                         text=bot_texts.change_text,
                         parse_mode="Markdown",
                         reply_markup=change_product_markup)
        bot.register_next_step_handler(message, change_product, product_id)


# Зміна опису продукту
def change_product_description(message, product_id):
    if message.text != bot_texts.cance:
        if message.text is not None:
            # Зміна опису продукту
            s_product = get_product(product_id)
            s_product.description = message.text
            s_product.update()
            log(f"{message.from_user.id} змінив опис продукту {s_product.name}")
            photo = open(f"{settings.IMG_FOLDER + s_product.prev_img}", 'rb')
            bot.send_photo(chat_id=message.chat.id,
                           photo=photo,
                           caption=bot_texts.product_send(s_product),
                           parse_mode="Markdown", )
            bot.send_message(chat_id=message.chat.id,
                             text=bot_texts.change_text,
                             parse_mode="Markdown",
                             reply_markup=change_product_markup)
            bot.register_next_step_handler(message, change_product, product_id)
        else:
            # Потреба у користувача ввести коректно
            bot.send_message(chat_id=message.chat.id,
                             text=bot_texts.write_correct,
                             reply_markup=cance_markup,
                             parse_mode="Markdown")
            bot.register_next_step_handler(message, change_product_description, product_id)

    # Повернення до меню зміни продукту
    else:
        s_product = get_product_by_name(product_id)
        photo = open(f"{settings.IMG_FOLDER + s_product.prev_img}", 'rb')
        bot.send_photo(chat_id=message.chat.id,
                       photo=photo,
                       caption=bot_texts.product_send(s_product),
                       parse_mode="Markdown", )
        bot.send_message(chat_id=message.chat.id,
                         text=bot_texts.change_text,
                         parse_mode="Markdown",
                         reply_markup=change_product_markup)
        bot.register_next_step_handler(message, change_product, product_id)


# Зміна зображення продукту
def change_product_img(message, product_id):
    if message.text != bot_texts.cance:
        try:
            # Зміна зображення продукту
            s_product = get_product(product_id)
            old_img = s_product.prev_img
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            src = settings.IMG_FOLDER + file_info.file_path[10:]
            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)
            img_prev = file_info.file_path[10:]
            s_product.prev_img = img_prev
            s_product.update()
            log(f"{message.from_user.id} змінив картинку продукту {s_product.name} з {old_img} на {s_product.prev_img}")
            photo = open(f"{settings.IMG_FOLDER + s_product.prev_img}", 'rb')
            bot.send_photo(chat_id=message.chat.id,
                           photo=photo,
                           caption=bot_texts.product_send(s_product),
                           parse_mode="Markdown", )
            bot.send_message(chat_id=message.chat.id,
                             text=bot_texts.change_text,
                             parse_mode="Markdown",
                             reply_markup=change_product_markup)
            bot.register_next_step_handler(message, change_product, product_id)
        except Exception as ex:
            # Бот не зміг прийняти фото
            print(ex)
            log(f"{message.from_user.id} не зміг відправити боту картинку")
            bot.send_message(chat_id=message.chat.id,
                             text=bot_texts.image_err,
                             reply_markup=cance_markup,
                             parse_mode="Markdown")
            bot.register_next_step_handler(message, change_product_img, product_id)

    # Повернення до меню зміни продукту
    else:
        s_product = get_product_by_name(product_id)
        photo = open(f"{settings.IMG_FOLDER + s_product.prev_img}", 'rb')
        bot.send_photo(chat_id=message.chat.id,
                       photo=photo,
                       caption=bot_texts.product_send(s_product),
                       parse_mode="Markdown", )
        bot.send_message(chat_id=message.chat.id,
                         text=bot_texts.change_text,
                         parse_mode="Markdown",
                         reply_markup=change_product_markup)
        bot.register_next_step_handler(message, change_product, product_id)


# Зміна групи продукту
def change_product_group(message, product_id):
    if message.text != bot_texts.cance:
        if extend_group(message.text):
            # Зміна групи продукту
            s_product = get_product(product_id)
            old_group = s_product.group.name
            s_product.group = get_group(get_group_id(message.text))
            s_product.update()
            log(f"{message.from_user.id} змінив групу продукту {s_product.name} з"
                f" {old_group} на {s_product.group.name}")
            photo = open(f"{settings.IMG_FOLDER + s_product.prev_img}", 'rb')
            bot.send_photo(chat_id=message.chat.id,
                           photo=photo,
                           caption=bot_texts.product_send(s_product),
                           parse_mode="Markdown", )
            bot.send_message(chat_id=message.chat.id,
                             text=bot_texts.change_text,
                             parse_mode="Markdown",
                             reply_markup=change_product_markup)
            bot.register_next_step_handler(message, change_product, product_id)
        else:
            # Потреба у користувача ввести коректно
            bot.send_message(chat_id=message.chat.id,
                             text=bot_texts.none_in_menu,
                             reply_markup=cance_markup,
                             parse_mode="Markdown")
            bot.register_next_step_handler(message, change_product_group, product_id)

    # Повернення до меню зміни продукту
    else:
        s_product = get_product_by_name(product_id)
        photo = open(f"{settings.IMG_FOLDER + s_product.prev_img}", 'rb')
        bot.send_photo(chat_id=message.chat.id,
                       photo=photo,
                       caption=bot_texts.product_send(s_product),
                       parse_mode="Markdown", )
        bot.send_message(chat_id=message.chat.id,
                         text=bot_texts.change_text,
                         parse_mode="Markdown",
                         reply_markup=change_product_markup)
        bot.register_next_step_handler(message, change_product, product_id)


# Вибір групи для зміни
def cg_get_group(message):
    if message.text != bot_texts.cance:
        if extend_group(message.text):
            # Перехід до change_group
            group_id = get_group_id(message.text)
            s_group = get_group(group_id)
            photo = open(f"{settings.IMG_FOLDER + s_group.prev_img}", 'rb')
            bot.send_photo(chat_id=message.chat.id,
                           photo=photo,
                           caption=bot_texts.group_send(s_group),
                           parse_mode="Markdown", )
            bot.send_message(chat_id=message.chat.id,
                             text=bot_texts.change_text,
                             parse_mode="Markdown",
                             reply_markup=change_group_markup)
            bot.register_next_step_handler(message, change_group, group_id)
        else:
            # Потреба у користувача ввести коректно
            bot.send_message(chat_id=message.chat.id,
                             text=bot_texts.none_in_menu,
                             reply_markup=cance_markup,
                             parse_mode="Markdown")
            bot.register_next_step_handler(message, cg_get_group)
    else:
        # Дія відмінена
        bot.send_message(chat_id=message.chat.id,
                         text=bot_texts.return_to_menu,
                         parse_mode="Markdown",
                         reply_markup=admin_markup)


# Меню зміни групи
def change_group(message, group_id):
    # Зміна назви
    if message.text == bot_texts.change_group_name:
        bot.send_message(chat_id=message.chat.id,
                         text=bot_texts.change_group_name_text,
                         parse_mode="Markdown",
                         reply_markup=cance_markup)
        bot.register_next_step_handler(message, change_group_name, group_id)

    # Зміна картинки
    elif message.text == bot_texts.change_group_img:
        bot.send_message(chat_id=message.chat.id,
                         text=bot_texts.change_group_img_text,
                         parse_mode="Markdown",
                         reply_markup=cance_markup)
        bot.register_next_step_handler(message, change_group_img, group_id)

    # Повернення в меню
    else:
        bot.send_message(chat_id=message.chat.id,
                         text=bot_texts.return_to_menu,
                         parse_mode="Markdown",
                         reply_markup=admin_markup)


# Зміна імені групи
def change_group_name(message, group_id):
    if message.text != bot_texts.cance:
        if message.text is not None:
            # Зміна імені групи
            s_group = get_group(group_id)
            old_name = s_group.name
            s_group.name = message.text
            s_group.update()
            log(f"{message.from_user.id} змінив назву групи з {old_name} на {s_group.name}")

            # Оновлення глобальної клавіатури груп
            global group_markup
            group_markup = get_group_markup()

            photo = open(f"{settings.IMG_FOLDER + s_group.prev_img}", 'rb')
            bot.send_photo(chat_id=message.chat.id,
                           photo=photo,
                           caption=bot_texts.group_send(s_group),
                           parse_mode="Markdown", )
            bot.send_message(chat_id=message.chat.id,
                             text=bot_texts.change_text,
                             parse_mode="Markdown",
                             reply_markup=change_group_markup)
            bot.register_next_step_handler(message, change_group, group_id)
        else:
            # Потреба у користувача ввести коректно
            bot.send_message(chat_id=message.chat.id,
                             text=bot_texts.write_correct,
                             reply_markup=cance_markup,
                             parse_mode="Markdown")
            bot.register_next_step_handler(message, change_group_name, group_id)

    # Повернення до меню зміни групи
    else:
        s_group = get_group(group_id)
        photo = open(f"{settings.IMG_FOLDER + s_group.prev_img}", 'rb')
        bot.send_photo(chat_id=message.chat.id,
                       photo=photo,
                       caption=bot_texts.group_send(s_group),
                       parse_mode="Markdown", )
        bot.send_message(chat_id=message.chat.id,
                         text=bot_texts.change_text,
                         parse_mode="Markdown",
                         reply_markup=change_product_markup)
        bot.register_next_step_handler(message, change_group, group_id)


# Зміна зображення групи
def change_group_img(message, group_id):
    if message.text != bot_texts.cance:
        try:
            # Зміна зображення групи
            s_group = get_group(group_id)
            old_img = s_group.prev_img
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            src = settings.IMG_FOLDER + file_info.file_path[10:]
            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)
            img_prev = file_info.file_path[10:]
            s_group.prev_img = img_prev
            s_group.update()
            log(f"{message.from_user.id} змінив картинку групи {s_group.name} з {old_img} на {s_group.prev_img}")

            # Оновлення глобальної клавіатури груп
            global group_markup
            group_markup = get_group_markup()

            photo = open(f"{settings.IMG_FOLDER + s_group.prev_img}", 'rb')
            bot.send_photo(chat_id=message.chat.id,
                           photo=photo,
                           caption=bot_texts.group_send(s_group),
                           parse_mode="Markdown", )
            bot.send_message(chat_id=message.chat.id,
                             text=bot_texts.change_text,
                             parse_mode="Markdown",
                             reply_markup=change_group_markup)
            bot.register_next_step_handler(message, change_group, group_id)
        except Exception as ex:
            # Бот не зміг прийняти фото
            print(ex)
            log(f"{message.from_user.id} не зміг відправити боту картинку")
            bot.send_message(chat_id=message.chat.id,
                             text=bot_texts.image_err,
                             reply_markup=cance_markup,
                             parse_mode="Markdown")
            bot.register_next_step_handler(message, change_group_img, group_id)

    # Повернення до меню зміни групи
    else:
        s_group = get_group(group_id)
        photo = open(f"{settings.IMG_FOLDER + s_group.prev_img}", 'rb')
        bot.send_photo(chat_id=message.chat.id,
                       photo=photo,
                       caption=bot_texts.group_send(s_group),
                       parse_mode="Markdown", )
        bot.send_message(chat_id=message.chat.id,
                         text=bot_texts.change_text,
                         parse_mode="Markdown",
                         reply_markup=change_group_markup)
        bot.register_next_step_handler(message, change_group, group_id)


# Вибір групи продукту що видаляється
def dp_get_group(message):
    if message.text != bot_texts.cance:
        if extend_group(message.text):
            # Перехід до dp_get_product
            it_group = get_group(get_group_id(message.text))
            products = get_products_by_group(it_group.group_id)
            product_markup = types.ReplyKeyboardMarkup()
            for b in products:
                product_markup.row(types.KeyboardButton(b.name))
            bot.send_message(chat_id=message.chat.id,
                             text=bot_texts.dp_get_product,
                             parse_mode="Markdown",
                             reply_markup=product_markup)
            bot.register_next_step_handler(message, dp_get_product)
        else:
            # Потреба у користувача ввести коректно
            bot.send_message(chat_id=message.chat.id,
                             text=bot_texts.none_in_menu,
                             reply_markup=group_markup,
                             parse_mode="Markdown")
            bot.register_next_step_handler(message, dp_get_group)

    # Дія відмінена
    else:
        bot.send_message(chat_id=message.chat.id,
                         text=bot_texts.return_to_menu,
                         parse_mode="Markdown",
                         reply_markup=admin_markup)


# Вибір продукту що видаляється
def dp_get_product(message):
    if message.text != bot_texts.cance:
        if extend_product(message.text):
            # Перехід до delete_product
            s_product = get_product_by_name(message.text)
            photo = open(f"{settings.IMG_FOLDER + s_product.prev_img}", 'rb')
            bot.send_photo(chat_id=message.chat.id,
                           photo=photo,
                           caption=bot_texts.product_send(s_product),
                           parse_mode="Markdown", )
            bot.send_message(chat_id=message.chat.id,
                             text=bot_texts.dp_confirm,
                             parse_mode="Markdown",
                             reply_markup=yn_markup)
            bot.register_next_step_handler(message, delete_product, s_product.product_id)
        else:
            # Потреба у користувача ввести коректно
            bot.send_message(chat_id=message.chat.id,
                             text=bot_texts.none_in_menu,
                             parse_mode="Markdown")
            bot.register_next_step_handler(message, dp_get_group)

    # Дія відмінена
    else:
        bot.send_message(chat_id=message.chat.id,
                         text=bot_texts.return_to_menu,
                         parse_mode="Markdown",
                         reply_markup=admin_markup)


# Видалення продукту
def delete_product(message, product_id):
    # Видалення продукту
    if message.text == bot_texts.yes:
        get_product(product_id).delete()
        log(f"{message.from_user.id} видалив продукт ID{product_id}")
        bot.send_message(chat_id=message.chat.id,
                         text=bot_texts.dp_succes,
                         parse_mode="Markdown",
                         reply_markup=admin_markup)

    # Дія відмінена
    else:
        bot.send_message(chat_id=message.chat.id,
                         text=bot_texts.return_to_menu,
                         parse_mode="Markdown",
                         reply_markup=admin_markup)


# Вибір групи для видалення
def dg_get_group(message):
    if message.text != bot_texts.cance:
        if extend_group(message.text):
            # Перехід до delete_group
            group_id = get_group_id(message.text)
            s_group = get_group(group_id)
            photo = open(f"{settings.IMG_FOLDER + s_group.prev_img}", 'rb')
            bot.send_photo(chat_id=message.chat.id,
                           photo=photo,
                           caption=bot_texts.group_send(s_group),
                           parse_mode="Markdown", )
            bot.send_message(chat_id=message.chat.id,
                             text=bot_texts.dg_confirm,
                             parse_mode="Markdown",
                             reply_markup=yn_markup)
            bot.register_next_step_handler(message, delete_group, group_id)
        else:
            # Потреба у користувача ввести коректно
            bot.send_message(chat_id=message.chat.id,
                             text=bot_texts.none_in_menu,
                             reply_markup=group_markup,
                             parse_mode="Markdown")
            bot.register_next_step_handler(message, dg_get_group)

    # Дія відмінена
    else:
        bot.send_message(chat_id=message.chat.id,
                         text=bot_texts.return_to_menu,
                         parse_mode="Markdown",
                         reply_markup=admin_markup)


# Видалення групи
def delete_group(message, group_id):
    if message.text == bot_texts.yes:
        get_group(group_id).delete()
        log(f"{message.from_user.id} видалив групу ID{group_id} та всі її продукти")

        # Оновлення глобальної клавіатури груп
        global group_markup
        group_markup = get_group_markup()

        bot.send_message(chat_id=message.chat.id,
                         text=bot_texts.dg_succes,
                         parse_mode="Markdown",
                         reply_markup=admin_markup)
    # Дія відмінена
    else:
        bot.send_message(chat_id=message.chat.id,
                         text=bot_texts.return_to_menu,
                         parse_mode="Markdown",
                         reply_markup=admin_markup)


# Обробка інлайн кнопок
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):

    # IF ADMIN
    if call.from_user.username in settings.ADMINS:
        log(call.data)
        data_mass = call.data.split("|")
        all_status = get_all_status()
        status_mass = []
        for b in all_status:
            status_mass.append(b.name)

        # Якщо цей запит має тип command
        if data_mass[0] == bot_texts.command:

            # Зміна статусу
            if data_mass[1] == bot_texts.change_status:
                log(f"{call.from_user.id} ініціював зміну статуса")
                it_order_id = int(data_mass[2])
                keyboard = types.InlineKeyboardMarkup()
                for c in all_status:
                    status_name = c.name
                    data_mass = [bot_texts.command, status_name, str(it_order_id)]
                    data_str = "|".join(data_mass)
                    keyboard.add(types.InlineKeyboardButton(text=status_name,
                                                            callback_data=data_str))
                it_order = get_order(it_order_id)

                bot.edit_message_text(chat_id=call.message.chat.id,
                                      message_id=call.message.message_id,
                                      text=bot_texts.order_text_admin(it_order),
                                      parse_mode="Markdown",
                                      reply_markup=keyboard)

            # Зміна статусу на статус на розгляді
            elif data_mass[1] == status_start.name:
                it_order_id = int(data_mass[2])
                keyboard = types.InlineKeyboardMarkup()
                data_mass = [bot_texts.command, bot_texts.change_status, str(it_order_id)]
                data_str = "|".join(data_mass)
                keyboard.add(types.InlineKeyboardButton(text=bot_texts.change_status,
                                                        callback_data=data_str))

                it_order = get_order(it_order_id)
                it_order.status = status_start
                it_order.update()
                log(f"{call.from_user.id} змінив статус на {data_mass[1]}")

                bot.edit_message_text(chat_id=call.message.chat.id,
                                      message_id=call.message.message_id,
                                      text=bot_texts.order_text_admin(it_order),
                                      parse_mode="Markdown",
                                      reply_markup=keyboard)
                bot.send_message(chat_id=it_order.user.user_id,
                                 text=bot_texts.status_start_set,
                                 parse_mode="Markdown")

            # Зміна статусу на статус на завершений
            elif data_mass[1] == status_close.name:
                it_order_id = int(data_mass[2])
                keyboard = types.InlineKeyboardMarkup()
                data_mass = [bot_texts.command, bot_texts.change_status, str(it_order_id)]
                data_str = "|".join(data_mass)
                keyboard.add(types.InlineKeyboardButton(text=bot_texts.change_status,
                                                        callback_data=data_str))

                it_order = get_order(it_order_id)
                it_order.status = status_close
                it_order.close_date = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
                it_order.update()
                log(f"{call.from_user.id} змінив статус на {data_mass[1]}")

                bot.edit_message_text(chat_id=call.message.chat.id,
                                      message_id=call.message.message_id,
                                      text=bot_texts.order_text_admin(it_order),
                                      parse_mode="Markdown",
                                      reply_markup=keyboard)
                bot.send_message(chat_id=it_order.user.user_id,
                                 text=bot_texts.status_close_set,
                                 parse_mode="Markdown")

            # Зміна статусу на статус на виконується
            elif data_mass[1] == status_work.name:
                it_order_id = int(data_mass[2])
                keyboard = types.InlineKeyboardMarkup()
                data_mass = [bot_texts.command, bot_texts.change_status, str(it_order_id)]
                data_str = "|".join(data_mass)
                keyboard.add(types.InlineKeyboardButton(text=bot_texts.change_status,
                                                        callback_data=data_str))

                it_order = get_order(it_order_id)
                it_order.status = status_work
                it_order.update()
                log(f"{call.from_user.id} змінив статус на {data_mass[1]}")

                bot.edit_message_text(chat_id=call.message.chat.id,
                                      message_id=call.message.message_id,
                                      text=bot_texts.order_text_admin(it_order),
                                      parse_mode="Markdown",
                                      reply_markup=keyboard)
                bot.send_message(chat_id=it_order.user.user_id,
                                 text=bot_texts.status_work_set,
                                 parse_mode="Markdown")

            # Зміна статусу на статус на доставляється
            elif data_mass[1] == status_delivery.name:
                it_order_id = int(data_mass[2])
                keyboard = types.InlineKeyboardMarkup()
                data_mass = [bot_texts.command, bot_texts.change_status, str(it_order_id)]
                data_str = "|".join(data_mass)
                keyboard.add(types.InlineKeyboardButton(text=bot_texts.change_status,
                                                        callback_data=data_str))

                it_order = get_order(it_order_id)
                it_order.status = status_delivery
                it_order.update()
                log(f"{call.from_user.id} змінив статус на {data_mass[1]}")

                bot.edit_message_text(chat_id=call.message.chat.id,
                                      message_id=call.message.message_id,
                                      text=bot_texts.order_text_admin(it_order),
                                      parse_mode="Markdown",
                                      reply_markup=keyboard)
                bot.send_message(chat_id=it_order.user.user_id,
                                 text=bot_texts.status_delivery_set,
                                 parse_mode="Markdown")

            # Зміна статусу на статус на готовий
            elif data_mass[1] == status_complete.name:
                it_order_id = int(data_mass[2])
                keyboard = types.InlineKeyboardMarkup()
                data_mass = [bot_texts.command, bot_texts.change_status, str(it_order_id)]
                data_str = "|".join(data_mass)
                keyboard.add(types.InlineKeyboardButton(text=bot_texts.change_status,
                                                        callback_data=data_str))

                it_order = get_order(it_order_id)
                it_order.status = status_complete
                it_order.update()
                log(f"{call.from_user.id} змінив статус на {data_mass[1]}")

                bot.edit_message_text(chat_id=call.message.chat.id,
                                      message_id=call.message.message_id,
                                      text=bot_texts.order_text_admin(it_order),
                                      parse_mode="Markdown",
                                      reply_markup=keyboard)
                bot.send_message(chat_id=it_order.user.user_id,
                                 text=bot_texts.status_complete_set,
                                 parse_mode="Markdown")
            else:
                log(f"{call.from_user.id} викликав callback у якого немає обробника")
