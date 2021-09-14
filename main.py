from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from Shop_bot.FSM import ChoicePay, AddItem
from Shop_bot.YM import get_balance_url, is_success
from Shop_bot.databases import create_tables, check_or_add_user, is_accept, accept_user, send_profile_data, \
    add_balance, count_rows, count_balance
from Shop_bot.keyboards import accept, menu, choice_money, admin_menu

'''
TASK: доделать добавление и удаление товаров
'''
# Создание таблиц user и items
create_tables()
token = ''
admin_id = 726883862
bot = Bot(token=token)
dp = Dispatcher(bot=bot, storage=MemoryStorage())


@dp.message_handler(commands='start')
async def welcome(message):
    user_id = message.from_user.id
    user = message.from_user.first_name
    username = message.from_user.username
    user_values = (user_id, user, username, 0, 0)
    # Добавление пользователя в бд, если его там нет
    check_or_add_user(*user_values)
    if is_accept(user_id):
        await bot.send_message(message.chat.id, f'Рады видеть вас снова, {user.upper()}!', reply_markup=menu)
    else:
        await bot.send_message(message.chat.id, reply_markup=accept,
                               text='Добро пожаловать!\nУчтите, что мы не несём ответственность'
                                    'за незаконное использование наших товаров.')


@dp.message_handler(commands='info')
@dp.message_handler(lambda message: message.text == '❓ Информация')
async def information(message):
    await bot.send_message(message.chat.id, 'Создатель бота — @stanisIaw.')


@dp.message_handler(commands='admin')
async def admin_channel(message):
    if message.from_user.id == admin_id:
        count = count_rows()
        all_balance = count_balance()
        await bot.send_message(message.chat.id, f"Количество пользователей: {count}\nОбщий баланс: {all_balance}",
                               reply_markup=admin_menu)


@dp.message_handler(lambda message: message.text == '📦 Добавить товар')
async def new_item(message):
    if message.from_user.id == admin_id:
        await message.answer('Функционал в разработке.')
        # await bot.send_message(message.chat.id, 'Введите название товара.')
        # await AddItem.name.set()


@dp.message_handler(lambda message: message.text == '🧨 Удалить товар')
async def del_item(message):
    if message.from_user.id == admin_id:
        await message.answer('Функционал в разработке.')


# @dp.message_handler(state=AddItem.name)
# async def set_name(message):
#     global name
#     name = message.text
#     await bot.send_message(message.chat.id, 'Введите описание товара')
#     await AddItem.description.set()


# @dp.message_handler(state=AddItem.description)
# async def set_desc(message):
#     global description
#     description = message.text
#     await bot.send_message(message.chat.id, 'Введите цену товара')
#     await AddItem.price.set()


# @dp.message_handler(state=AddItem.price)
# async def set_price(message):
#     global price
#     try:
#         price = int(message.text)
#     except ValueError:
#         await bot.send_message(message.chat.id, 'Вы ввели не число.')
#     else:
#         await bot.send_message(message.chat.id, 'Отправьте файл к товару.')
#         await AddItem.additem.set()


@dp.message_handler(content_types=['document'], state=AddItem.additem)
async def add_item_file(message):
    pass
    # await bot.download_file(file_path, name)
    # url = get_file_url(name)
    # values = (name, description, price, url)
    # add_item(*values)
    # await bot.send_message(message.chat.id, 'Товар успешно добавлен')
    # await dp.current_state(user=message.from_user.id).reset_state()


@dp.message_handler(lambda message: message.text == '👤 Профиль')
async def profile(message):
    user_id, user, balance = send_profile_data(message)[0]
    await bot.send_message(message.chat.id, f'Здравствуйте, {user}!\nВаш айди — {user_id}.\n'
                                            f'Ваш баланс — {balance} рублей.\n'
                                            f'Спасибо, что пользуетесь ботом!')


@dp.message_handler(lambda message: message.text == '💰 Пополнить баланс')
async def add_money(message):
    await bot.send_message(message.chat.id, 'Выберите способ оплаты.', reply_markup=choice_money)


@dp.callback_query_handler(lambda call: call.data == 'deny')
async def deny_msg(call):
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await bot.send_message(call.message.chat.id, 'Использование магазина недоступно.\n'
                                                 'Для принятия введите команду /start.')


@dp.callback_query_handler(lambda call: call.data == 'accept')
async def accept_msg(call):
    user = call['from'].first_name
    accept_user(call['from'].id)
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await bot.send_message(call.message.chat.id, f'Добро пожаловать, {user}!', reply_markup=menu)


@dp.callback_query_handler(lambda call: call.data == 'yookassa')
async def yoomoney(call):
    await bot.send_message(call.message.chat.id, 'Введите сумму пополнения.\nДля отмены введите "отмена".')
    await ChoicePay.amount.set()


@dp.callback_query_handler(lambda call: call.data == 'ym_check_pay')
async def check_pay(call):
    if is_success()[0] and is_success()[1] > 0:
        add_balance(call['from'].id, is_success()[1])
        await bot.delete_message(call.message.chat.id, message_id=call.message.message_id)
        await bot.send_message(call.message.chat.id, f'Баланс на сумму {is_success()[1]} успешно пополнен.')
        await bot.send_message(726883862, f'Пользователь {call["from"].username} пополнил баланс на сумму '
                                          f'{is_success()[1]} рублей')
    else:
        await bot.send_message(call.message.chat.id, 'Произошла ошибка')
        await dp.current_state(user=call.message.from_user.id).reset_state()


@dp.message_handler(state=ChoicePay.amount)
async def send_pay_url(message):
    try:
        money = int(message.text)
    except ValueError:
        if message.text.lower() == 'отмена':
            await bot.send_message(message.chat.id, 'Действие отменено.')
            await dp.current_state(user=message.from_user.id).reset_state()
        else:
            await bot.send_message(message.chat.id, 'Вы ввели не число')
            await dp.current_state(user=message.from_user.id).reset_state()
            await ChoicePay.amount.set()
    else:
        if money < 2:
            await bot.send_message(message.chat.id, 'Минимальный перевод 2 рубля.')
        else:
            pay = InlineKeyboardMarkup()
            pay.row(InlineKeyboardButton('Оплатить', url=get_balance_url(money)))
            pay.row(InlineKeyboardButton('Проверить оплату', callback_data='ym_check_pay'))

            await bot.send_message(message.chat.id, "Для оплаты нажмите кнопку", reply_markup=pay)
    await dp.current_state(user=message.from_user.id).reset_state()


print('Бот запущен.')
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)
