from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, \
    ReplyKeyboardMarkup, KeyboardButton

accept = InlineKeyboardMarkup(row_width=2)
accept.add(
    InlineKeyboardButton(text='Согласен', callback_data='accept'),
    InlineKeyboardButton(text='Не согласен', callback_data='deny')
)
menu = ReplyKeyboardMarkup(resize_keyboard=True)
menu.row(KeyboardButton('👤 Профиль'), KeyboardButton('💰 Пополнить баланс'))
menu.row(KeyboardButton('❓ Информация'))

choice_money = InlineKeyboardMarkup(row_width=1)
choice_money.add(
    InlineKeyboardButton('ЮКасса (2%)', callback_data='yookassa')
)
back = InlineKeyboardMarkup().add(InlineKeyboardButton(text='<<< Назад', callback_data='accept'))

admin_menu = ReplyKeyboardMarkup(resize_keyboard=True)
admin_menu.row(KeyboardButton('👤 Профиль'), KeyboardButton('💰 Пополнить баланс'))
admin_menu.row(KeyboardButton('❓ Информация'))
admin_menu.row(KeyboardButton('📦 Добавить товар'), KeyboardButton('🧨 Удалить товар'))