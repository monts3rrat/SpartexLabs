from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder

# services

services_kb = ReplyKeyboardBuilder()
services_kb.row(types.KeyboardButton(text="В Главное Меню"))

start_kb = ReplyKeyboardBuilder()
start_kb.row(
    types.KeyboardButton(text="Запуск Софта"),
    types.KeyboardButton(text="Профиль")
)

# admin

start_kb_admin = ReplyKeyboardBuilder()
start_kb_admin.row(
    types.KeyboardButton(text="Запуск Софта"),
    types.KeyboardButton(text="Профиль")
)
start_kb_admin.row(
    types.KeyboardButton(text="Админ Панель"),
)

menu_kb_admin = ReplyKeyboardBuilder()
menu_kb_admin.row(
    types.KeyboardButton(text="Бан"),
    types.KeyboardButton(text="Рассылка")
)
menu_kb_admin.row(
    types.KeyboardButton(text="Балансы"),
    types.KeyboardButton(text="Статистика")
)
menu_kb_admin.row(
    types.KeyboardButton(text="В Главное Меню"),
)

# profile

profile_kb = ReplyKeyboardBuilder()
profile_kb.row(
    types.KeyboardButton(text="Баланс"),
    types.KeyboardButton(text="Сессии")
)
profile_kb.row(
    types.KeyboardButton(text="FAQ/Поддержка"),
    types.KeyboardButton(text="Реф.Система")
)
profile_kb.row(
    types.KeyboardButton(text="В Главное Меню"),
)

balance_kb = ReplyKeyboardBuilder()
balance_kb.row(
    types.KeyboardButton(text="Пополнить Баланс"),
    types.KeyboardButton(text="Назад")
)

# start software

start_soft_kb = ReplyKeyboardBuilder()
start_soft_kb.row(
    types.KeyboardButton(text="Пополнить Баланс"),
    types.KeyboardButton(text="Услуги")
)
start_soft_kb.row(types.KeyboardButton(text="В Главное Меню"))
