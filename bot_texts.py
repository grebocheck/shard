import settings

none_addres = "Адреса не вказана 👀"
command = "command"

moderators = ""
for a in range(len(settings.FEEDBACK_MODERATORS)):
    if a <= len(settings.FEEDBACK_MODERATORS)-1:
        moderators += "@" + settings.FEEDBACK_MODERATORS[a] +", "
    else:
        moderators += "@" + settings.FEEDBACK_MODERATORS[a]


if settings.LANGUAGE == "UA":
    # Кнопки
    reg_start_button = "Розпочати реєстрацію🔥"
    reg_pass_addres = "Пропустити⏳"

    cance = "Відмінити✖️"
    back = "Назад🔙"
    yes = "Так✅"
    no = "Ні❌"

    my_orders = "Мої замовлення✨"
    shop = "Магазин🛒"
    feedback = "Зворотній зв`язок☎️"
    about = "Про нас🗒"

    start_order = "⭐Оформити замовлення⭐️"
    continue_buy = "Продовжити покупки🐾"

    pass_text = "Пропустити⏳"
    create_comment = "Написати відгук🗒"

    none_close_date = "Замовлення не завершене🕘"
    change_status = "Змінити статус⚡️"

    all_open_orders = "Всі відкриті замовлення🌪"
    add_product = "Додати товар📕"
    add_group = "Додати групу📒"
    change_product = "Змінити дані продукту📗"
    change_group = "Змінити дані групи📘"
    del_product = "Видалити продукт📙"
    del_group = "Видалити групу📓"

    change_product_name = "Назву🖨"
    change_product_price = "Ціну💵"
    change_product_description = "Опис📃"
    change_product_img = "Зображення🖼"
    change_product_group = "Групу товару💎️"

    change_group_name = "Назву🖨"
    change_group_img = "Зображення🖼"

    # Статуси
    status_start_name = "В обробці🖥"
    status_start_description = "Ваше замовлення `в обробці`🖥, очікуйте поки з вами зв'яжеться *оператор*👨‍💻"
    status_start_set = "Ваше замовлення набуло статусу `в обробці`🖥"

    status_close_name = "Завершено✅"
    status_close_description = "Це замовлення вже було `завершено`✅"
    status_close_set = "Ваше замовлення `завершено`✅, дякуємо що скористались ботом🥳"

    status_work_name = "Виконується🕊"
    status_work_description = "Ваше замовлення на стадії `приготування`🕊"
    status_work_set = "Ваше замовлення вже `виконується`🕊"

    status_delivery_name = "Доставляється🚛"
    status_delivery_description = "Курєр вже везе🚛 ваше замовлення"
    status_delivery_set = "Ваше замовлення вже `доставляється`🚛"

    status_complete_name = "Готове💡"
    status_complete_description = "Ваше замовлення вже готове💡 та очікує вас😋"
    status_complete_set = "Ваше замовлення готове💡 до того щоб ви його забрали😋"

    # Тексти
    return_to_menu = "Ви повернулись в *меню*🎯"
    p_send_feedback = "Відправте свій відгук *одним повідомленням*☝️, воно також може включати в собі медіа🖼"
    s_send_feedback = "Вітаю, відгук успішно відправлено✅"
    welcome = "Вітаємо в *боті*🤖, оберіть в *меню*🎯 що бажаєте"
    first_start = "Вітаємо в нашому боті🤖, будь-ласка пройдіть *реєстрацію* щоб комфортно продовжити " \
                  "користування⚡️ нашим ботом🤖 "
    h_your_name = "Введіть як *до вас звертатися*?💻"
    h_your_phone = "Введіть свій *номер телефону*📞"
    h_your_addres = "Введіть *адресу*🏠 на котру буде йти доставка, натисність *пропустити⏳* якщо не бажаєте."
    h_correct = "Піддтвердіть чи все введено *вірно*✅, якщо ні то почнемо *реєстрацію* заново🔙"
    reg_succes = "Вітаємо, реєстрацію *завершенно*✅, якщо ви захочете змінити дані, ви зможете зробити це в " \
                 "*налаштуваннях*"
    reg_restart = "Почнімо тоді *реєстрацію* спочатку🔙, введіть як до вас звертатися"

    about_text = "Бота🤖 розроблено @heridium для формування та обслуговування замовлень"

    choice_group = "Виберіть *категорію*💎 товару котрий вас цікавить"
    choice_product = "Виберіть *продукт*🍔 що вас цікавить"
    choice_amount = "Введіть *кількість* котру бажаєте додати до корзини🛒"
    choice_succes = "Чудово✅, товар додано до корзини🛒!"
    shop_comment = "Якщо є якісь побажання до замовлення то введіть *коментар*💡"
    succes_create_order = "Вітаємо✅, ось ваше *замовлення*:"
    unsucces_order = "Формування замовлення *відмінено*❌"

    ban_succes = "Користувач *заблокований*🔫"
    ban_unsucces = "Користувач вже був *заблокований*🔫"
    unban_succes = "Користувач *розблокований*💊"
    unban_unsucces = "Користувач не був *заблокований*💊"

    add_product_group = "Оберіть *групу*💎 в котру буде додано *товар*🍔"
    add_product_name = "Введіть *назву🖨 товару*🍔"
    add_product_img = "Відправте *зображення🖼 товару🍔*"
    add_product_description = "Введіть *опис📃 товару🍔*"
    add_product_price = "Введіть *ціну💵* за *1шт.*"
    add_product_succes = "*Продукт*🍔 додано✅"
    add_product_unsucces = "Додавання відмінено❌"

    correct = "Все вірно?⚖️"

    add_group_name = "Введіть *назву🖨* *групи*💎 яку хочете створити"
    add_group_img = "Відправте *зображення🖼* для *групи*💎"
    add_group_succes = "*Групу*💎 додано✅"
    add_group_unsucces = "Додавання відмінено❌"

    change_text = "Оберіть що хочете змінити🔦"

    cp_get_group = "Виберіть *групу*💎 товару"
    cp_get_product = "Виберіть *товар*🍔 який бажаєте змінити"
    change_product_name_text = "Введіть нову *назву🖨*"
    change_product_price_text = "Введіть *ціну💵* за *1шт.*"
    change_product_desc_text = "Введіть *опис📃 товару🍔*"
    change_product_img_text = "Відправте *зображення🖼 товару🍔*"
    change_product_group_text = "Оберіть нову *групу*💎"

    cg_get_group = "Виберіть *групу*💎"
    change_group_name_text = "Введіть нову *назву🖨*"
    change_group_img_text = "Відправте *зображення🖼 💎групи💎*"

    dp_get_group = "Виберіть *групу*💎 товару"
    dp_get_product = "Виберіть *товар*🍔 який хочете *видалити*💣"
    dp_confirm = "Ви впевнені що хочете *видалити*💣 цей *товар*🍔?"
    dp_succes = "*Товар*🍔 видалено✅"

    dg_get_group = "Виберіть *групу*💎 котру хочете *видалити*💣"
    dg_confirm = "Ви впевнені що хочете *видалити*💣 цю групу разом з всіма її *товарами*🍔?"
    dg_succes = "*Групу*💎 та її *товари*🍔 видалено✅"

    write_correct = "Введіть будь-ласка *коректно*👓"

    change_succes = "Зміни успішно внесені✅"

    you_have_ban = "Ви *заблоковані*🔫 в цьому боті"

    none_in_menu = "Такого немає в *меню*🎯, будь-ласка оберіть те що є в *меню*🎯"

    non_comment = "Коментар відсутній"

    cance_reg = "Реєстрація відмінена❌. Введіть /start якщо бажаєте почати✅"

    unknown_err = "Виникла невідома *помилка*😬"

    forward_err = "Не вдалось переслати *📨повідомлення📨*, перегляньте налаштування *приватності*🕵️‍♀️"

    image_err = "Бот не зміг прийняти це *зображення🖼*, надішліть його без стиснення"

    active_orders = "Ваші активні *замовлення🔍*:"
    none_active_orders = "У вас немає активних *замовлень🔍*"
    none_active_orders_admin = "Активних *замовлень🔍* немає"

    go_start = "Почніть з реєстрації /start"

    feed_text = f"Ви можете звернутись в приватні повідомлення до {moderators}. " \
                f"Якщо хочете лишити *відгук📨*, то натисніть клавішу щоб продовжити."

    # Функції виводу форматування тексту
    def user_correct_info(name, username, phone, addres):
        text = f"""{h_correct}

*Звати вас:* `{name}`
*Юзернейм:* `{username}`
*Номер телефону:* `{phone}`
*Адреса:* `{addres}`

Все вірно?✅"""
        return text


    def pid_addres(addres):
        text = f"""Бажаєте замовити з *доставкою*🚛?
Доставка коштує `{settings.DELIVERY_PRICE}`грн.💵
Бажаєте замовити на цю *адресу*🏠: `{addres}`?
Якщо бажаєте замовити на іншу *адресу*🏠, то *напишіть* її сюди.👇"""
        return text


    def order_text(ORDER):
        text = f"""*Замовлення🗒 №{ORDER.order_id}*

{ORDER.content}

{ORDER.status.description}

*Створено🕘:* _{ORDER.create_date}_
*Завершено🕞:* _{ORDER.close_date}_
"""
        return text

    def order_text_admin(ORDER):
        text = f"""*Замовлення🗒 №{ORDER.order_id}*

*ID:* `{ORDER.user.user_id}`
*Юзернейм:* `@{ORDER.user.username}`
*Номер телефону:* `{ORDER.user.phone_number}`
*Ім'я:* `{ORDER.user.name}`

{ORDER.content}

{ORDER.status.description}

*Створено🕘:* _{ORDER.create_date}_
*Завершено🕞:* _{ORDER.close_date}_
"""
        return text


    def cart_text(list_products, list_amounts):
        text = ""
        for a in range(len(list_products)):
            text = text + f"`{list_products[a].name}` {list_amounts[a]} шт. " \
                          f"- `{list_products[a].price * list_amounts[a]}`" \
                          f" грн." + "\n"

        return text

    def con_text(cart_text):
        if cart_text == "":
            text = choice_succes
        else:
            text = f"""*Ваша корзина🛒:*
{cart_text}

{choice_succes}"""
        return text

    def pid_order(list_products, list_amounts, delivery, comment):
        order_list_products = ""
        for a in range(len(list_products)):
            order_list_products = order_list_products + f"`{list_products[a].name}` {list_amounts[a]} шт " \
                          f"- `{list_products[a].price * list_amounts[a]}` грн" + "\n"
        if delivery != none_addres:
            order_list_products = order_list_products + f"`Доставка {settings.DELIVERY_PRICE}` грн"
        prices = get_price(list_products, list_amounts, delivery)
        text = f"""*Все вірно?✅:*
        
*Чек-лист:*
{order_list_products}

*Загальна вартість💵:* `{prices}` грн.
*Адреса доставки🏠:* `{delivery}` 
Ваш *коментар*💡 до замовлення:
_{comment}_
"""
        return text

    def order_content(list_products, list_amounts, delivery, comment):
        order_list_products = ""
        for a in range(len(list_products)):
            order_list_products = order_list_products + f"`{list_products[a].name}` {list_amounts[a]} шт " \
                                                        f"- `{list_products[a].price * list_amounts[a]}` грн" + "\n"
        prices = get_price(list_products, list_amounts, delivery)
        if delivery != none_addres:
            order_list_products = order_list_products + f"`Доставка {settings.DELIVERY_PRICE}` грн"
        text = f"""*Чек-лист:*
{order_list_products}

*Загальна вартість💵:* `{prices}` грн.
*Адреса доставки🏠:* `{delivery}` 
Ваш *коментар*💡 до замовлення:
_{comment}_"""
        return text

    def product_send(PRODUCT):
        text = f"""*{PRODUCT.name}*
*Категорія💎:* _{PRODUCT.group.name}_
*Ціна💵:* `{PRODUCT.price} грн.`
*Опис📃:* _{PRODUCT.description}_
"""
        return text

    def group_send(GROUP):
        return f"*Назва🖨:* `{GROUP.name}`"

    # підрахунок ціни замовлення
    def get_price(list_products, list_amounts, delivery):
        prices = 0
        for a in range(len(list_products)):
            prices += list_products[a].price * list_amounts[a]
        if delivery != none_addres:
            prices += settings.DELIVERY_PRICE
        return prices
