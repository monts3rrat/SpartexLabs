import os
import re
import sys
import asyncio
from random import randint
import datetime
import mimetypes
from csv import DictReader
from loguru import logger
from math import ceil

from aiogram import Bot, Dispatcher, types, F, Router, BaseMiddleware
from aiogram.types import Message, FSInputFile
from aiogram.filters.command import CommandObject, Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.filters.state import StatesGroup
from aiogram.client.default import DefaultBotProperties

import modules.functions.price_func as price
import modules.functions.antiflood as antiflood
import modules.functions.payment as pay
import modules.config.config as config
from modules.functions import texts
from modules.functions import validator
from modules.functions import draw_img
from checker import checker
import modules.keyboards.reply_kb as reply_kb
import modules.keyboards.inline_kb as inline_kb
from modules.database import db_api as db
from machine import setup

# configuration

db_ref = db.ReferalSystem()

bot = Bot(config.TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
dp = Dispatcher(storage=MemoryStorage())
storage = MemoryStorage()
router = Router()

admin_ids = config.ADMIN

logger.add("./logs/log.txt",
           format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <7}</level> | <green>{message}</green>",
           level="DEBUG",
           rotation="00:00",
           compression="zip")


# classes

class DataWaiting(StatesGroup):
    waiting_for_xlsx = State()
    processing_data = State()
    results_ready = State()


class HlDataWaiting(StatesGroup):
    waiting_for_xlsx = State()


class CheckerFuncDataWaiting(StatesGroup):
    waiting_for_txt = State()


class WaitingUrlForMint(StatesGroup):
    waiting_for_url = State()


class InvoiceAmountWaiting(StatesGroup):
    waiting_for_amount = State()


class BanMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Message, data):
        user_id = event.from_user.id

        if await db.is_user_banned(user_id) == "1":
            await event.answer("Вы заблокированы и не можете пользоваться ботом.")
            return

        return await handler(event, data)


dp.message.middleware(BanMiddleware())


# handlers

@logger.catch
async def start_command(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    referrer_id = message.text[7:] if message.text[7:] != str(user_id) else None

    if not db_ref.user_exists(user_id):
        await state.update_data(id=user_id)
        await _add_user(message, referrer_id)
    else:
        await state.update_data(id=user_id)
        await _update_user(message)

    if user_id in admin_ids:
        current_directory = os.path.dirname(os.path.realpath(__file__)).split("\\")
        path = f"{'/'.join(current_directory)}/modules/data/photos"

        img = FSInputFile(f"{path}/hello.png")
        await message.answer_photo(photo=img,
                                   caption=texts.hello(),
                                   reply_markup=reply_kb.start_kb_admin.as_markup(resize_keyboard=True))
    else:
        current_directory = os.path.dirname(os.path.realpath(__file__)).split("\\")
        path = f"{'/'.join(current_directory)}/modules/data/photos"

        img = FSInputFile(f"{path}/hello.png")
        await message.answer_photo(photo=img,
                                   caption=texts.hello(),
                                   reply_markup=reply_kb.start_kb.as_markup(resize_keyboard=True))


async def _add_user(message: types.Message, referrer_id: str):
    if referrer_id:
        await db.add_user(message, referrer_id)
        await notify_referrer(referrer_id)
        logger.info(f"New User with id: {message.from_user.id}. Referrer: {referrer_id}")
    else:
        await db.add_user(message, "")
        logger.info(f"New User with id: {message.from_user.id}")


async def _update_user(message: types.Message):
    await db.update_data(message)


@logger.catch
async def notify_referrer(referrer_id):
    try:
        await bot.send_message(
            referrer_id,
            "По Вашей ссылке зарегистрировался новый пользователь, Ваш баланс пополнен на 1!",
        )
        await db.refill_balance(referrer_id, 1)

    except Exception as e:
        logger.warning(f"Error when sending a message about a new referral to the user {referrer_id}")
        logger.warning(e)


# admin functions
@logger.catch
async def admin_menu(message: types.Message):
    await message.answer(
        "Админ меню. Выберите нужную функцию в клавиатуре.",
        reply_markup=reply_kb.menu_kb_admin.as_markup(resize_keyboard=True),
    )


@logger.catch
async def admin_ban_menu(message: types.Message):
    if message.from_user.id not in admin_ids:
        await message.answer("У вас нет прав на выполнение этой команды.")
        return
    else:
        await message.answer(
            "Чтобы заблокировать человека в боте, нужно ввести (без скобок!): /ban {id человека}\n"
            "Тоже самое с разбаном: /unban {id человека}"
            "Можете использовать эту команду даже не заходя в это меню."
        )


@logger.catch
async def admin_ban(message: types.Message, command: CommandObject):
    if message.from_user.id not in admin_ids:
        await message.answer("У вас нет прав на выполнение этой команды.")
        return
    try:
        user_id_to_ban = int(command.args)
    except ValueError:
        await message.answer("Пожалуйста, укажите корректный ID пользователя.")
        return

    if user_id_to_ban in admin_ids:
        await message.answer("Нельзя заблокировать админа.")
    else:
        await db.ban_user(user_id_to_ban)
        await message.answer(f"Пользователь с ID {user_id_to_ban} был заблокирован.")
        logger.info(f"User with id {message.from_user.id} banned")


@logger.catch
async def admin_unban(message: types.Message, command: CommandObject):
    if message.from_user.id not in admin_ids:
        await message.answer("У вас нет прав на выполнение этой команды.")
        return
    try:
        user_id_to_unban = int(command.args)
    except ValueError:
        await message.answer("Пожалуйста, укажите корректный ID пользователя.")
        return

    else:
        await db.unban_user(user_id_to_unban)
        await message.answer(f"Пользователь с ID {user_id_to_unban} был разблокирован.")
        logger.info(f"User with id {message.from_user.id} unbanned")


@logger.catch
async def admin_mailing_menu(message: types.Message):
    if message.from_user.id not in admin_ids:
        await message.answer("У вас нет прав на выполнение этой команды.")
        return
    else:
        await message.answer(
            "Чтобы произвести рассылку, нужно ввести (без скобок!): /mail {текст}\n"
            "Можете использовать эту команду даже не заходя в это меню."
        )


@logger.catch
async def admin_mailing(message: types.Message, command: CommandObject):
    if message.from_user.id not in admin_ids:
        await message.answer("У вас нет прав на выполнение этой команды.")
        return
    else:
        text = command.args

        user_ids = await db.get_all_users()
        for user_id in user_ids:
            try:
                await bot.send_message(chat_id=user_id, text=text)
            except Exception as e:
                logger.error(f"Failed to send message to {user_id}: {e}")
        logger.info(f"The message was sent: `{text}` to all users")


@logger.catch
async def admin_balance_menu(message: types.Message):
    if message.from_user.id not in admin_ids:
        await message.answer("У вас нет прав на выполнение этой команды.")
        return
    else:
        await message.answer(
            "Чтобы <b>пополнить</b> баланс человеку, нужно ввести (без скобок!): /balance {id человека} {на какую сумму}\n"
            "Чтобы <b>уменьшить</b> баланс человеку, нужно ввести (без скобок!): /steal_balance {id человека} {на какую сумму}"
            "Можете использовать эти команды даже не заходя в это меню."
        )


@logger.catch
async def admin_balance(message: types.Message, command: CommandObject):
    if message.from_user.id not in admin_ids:
        await message.answer("У вас нет прав на выполнение этой команды.")
        return
    else:
        qq = command.args.split()
        user = qq[0]
        amount = qq[1]
        await db.refill_balance(int(user), int(amount))
        await message.answer(
            f"Баланс пользователя {message.from_user.id} пополнен на {amount}$."
        )

        logger.info(
            f"The balance of the user with id {message.from_user.id} is replenished by {amount}"
        )


@logger.catch
async def admin_steal_balance(message: types.Message, command: CommandObject):
    if message.from_user.id not in admin_ids:
        await message.answer("У вас нет прав на выполнение этой команды.")
        return
    else:
        qq = command.args.split()
        user = qq[0]
        amount = qq[1]
        await db.reduce_balance(int(user), int(amount))
        await message.answer(
            f"Баланс пользователя {message.from_user.id} уменьшен на {amount}$."
        )

        logger.info(
            f"The balance of the user with id {message.from_user.id} is reduced by {amount}$"
        )


@logger.catch
async def admin_stat(message: types.Message):
    users_qq = await db.get_all_users()
    users = len(users_qq)
    users_balance_qq = await db.get_all_users_with_balance()
    users_balance = len(users_balance_qq)
    avg_balance = await db.get_avg_balance()
    avg_session = await db.check_avg_sessions_count()
    all_session = await db.check_all_sessions_count()
    avg_wallets = await db.check_avg_wallets_count()
    procent_project = await db.check_project_count()
    procent_function = await db.check_function_count()

    if procent_project == 0 and procent_function == 0:
        await message.answer(
            f"Статистика по сервису:\n\n"
            f"Кол-во юзеров:   {users}\n"
            f"Кол-во с балансом:   {users_balance}\n"
            f"Средний баланс:   {avg_balance}\n"
            f"Кол-во сессий:   {all_session}\n\n\n"
            f"Характеристика сессий:\n\n"
            f"• Процент выбранных проектов: \n"
            f"   -Base:                          0 %\n"
            f"   -Scroll:                         0 %\n"
            f"   -Zora:                           0 %\n"
            f"   -Linea:                         0 %\n"
            f"   -Hyperlane:               0 %\n\n"
            f"• Процент выбранных функций: \n"
            f"   -Бридж:                0 %\n"
            f"   -Обьемы:            0 %\n"
            f"   -Протоколы:      0 %\n"
            f"   -Коллектор:        0 %\n"
            f"   -Готовый маршрут:   0 %\n\n"
            f"• Cреднее количество кошельков: \n{avg_wallets}\n\n"
            f"• Cреднее количество сессий на человека: \n{avg_session}"
        )
    else:
        await message.answer(
            f"Статистика по сервису:\n\n"
            f"Кол-во юзеров:   {users}\n"
            f"Кол-во с балансом:   {users_balance}\n"
            f"Средний баланс:   {avg_balance}\n"
            f"Кол-во сессий:   {all_session}\n\n\n"
            f"Характеристика сессий:\n\n"
            f"• Процент выбранных проектов: \n"
            f"   -Base:  {procent_project.get('base', 'default')} %\n"
            f"   -Scroll:  {procent_project.get('scroll', 'default')} %\n"
            f"   -Zora:  {procent_project.get('zora', 'default')} %\n"
            f"   -Linea:  {procent_project.get('linea', 'default')} %\n"
            f"   -Hyperlane:  {procent_project.get('hyperlane', 'default')} %\n\n"
            f"• Процент выбранных функций: \n"
            f"   -Бридж:    {procent_function.get('bridge', 'default')} %\n"
            f"   -Обьемы:  {procent_function.get('swap', 'default')} %\n"
            f"   -Протоколы:   {procent_function.get('protocol', 'default')} %\n"
            f"   -Коллектор:   {procent_function.get('collector', 'default')} %\n"
            f"   -Готовый маршрут: {procent_function.get('route', 'default')} %\n\n"
            f"• Cреднее количество кошельков: \n{avg_wallets}\n\n"
            f"• Cреднее количество сессий на человека: \n{avg_session}"
        )


# profile

@logger.catch
async def profile(message: types.Message):
    balance = await db.check_balance(message.from_user.id)
    
    img_path = await draw_img.draw_profile(message.from_user.id, round(balance, 2))
    img = FSInputFile(img_path)
    await message.answer_photo(photo=img, caption=f"Ваш профиль, альфа ретрохантер! 🧑‍🦽\n\n"
                                                  f"🧿  ID: <i>{message.from_user.id}</i>\n"
                                                  f"🧢  Nick: <i>{message.from_user.full_name[:32]}</i>\n"
                                                  f"🩻  Username: <i>{message.from_user.username}</i>\n\n"
                                                  f"🪙  Баланс: <i>{round(balance, 2)}$</i>\n\n",
                               reply_markup=reply_kb.profile_kb.as_markup(resize_keyboard=True))
    await asyncio.sleep(2)

    try:
        await draw_img.delete_photo(img_path)

    except Exception:
        return


@logger.catch
async def balance_menu(message: types.Message):
    balance = await db.check_balance(message.from_user.id)

    current_directory = os.path.dirname(os.path.realpath(__file__)).split("\\")
    path = f"{'/'.join(current_directory)}/modules/data/photos"

    gif = FSInputFile(f"{path}/balance.gif")

    await message.answer_animation(animation=gif,
                                   caption=f"🪙 Ваш баланс: <i>{round(balance, 2)}$.</i>\n\n"
                                           f"<blockquote>Казна пуста, милорд,\nНужно больше золота!</blockquote>\n\n"
                                           f"<tg-spoiler>Нажимай Пополнить и летсго крутить ретро.</tg-spoiler>",
                                   reply_markup=reply_kb.balance_kb.as_markup(resize_keyboard=True))


async def session_hueta(id):
    sessions = await db.check_sessions(id)
    session_count = await db.check_sessions_count(id)

    try:
        qq = sessions.split("\n")
    except:
        pass
    updated_sessions = []

    for x in range(int(session_count)):
        session_details = (
            qq[x].split(":")[1].strip() if x < len(qq) else "Unknown session"
        )
        status = (
            "Работает"
            if os.path.isdir(f"./machine/SpartexSoft{id}_{x}")
            else "Завершено"
        )
        updated_sessions.append(f"{x + 1}: {session_details}: {status}\n")

    for x in range(int(session_count)):
        session_details = (
            qq[x].split(":")[1].strip() if x < len(qq) else "Unknown session"
        )
        status = (
            "Работает"
            if os.path.isdir(f"./machine/SpartexSoft{id}_{x}")
            else "Завершено"
        )
        updated_sessions.append(f"{x + 1}: {session_details}: {status}\n")

    sessions = await db.check_sessions(id)
    session_count = await db.check_sessions_count(id)

    try:
        qq = sessions.split("\n")
    except:
        pass
    updated_sessions = []

    for x in range(int(session_count)):
        session_details = (qq[x].split(":")[1].strip() if x < len(qq) else "Unknown session")
        status = 0
        if os.path.isdir(f"./machine/SpartexSoft{id}_{x}"):
            status = "Работает"
        else:
            status = "Завершен"
        updated_sessions.append(f"{x + 1}: {session_details}: {status}\n")

    img_sessions = []
    for q in range(int(session_count)):
        session_details = (
            qq[q].split(":")[1].strip() if q < len(qq) else "Unknown session"
        )
        status = 0
        if os.path.isdir(f"./machine/SpartexSoft{id}_{q}"):
            pass
        else:
            status = 1

        if status == 1:
            img_sessions.append(f"{q + 1}: {session_details}: Заверш\n")

    session = "".join(updated_sessions)
    await db.update_sessions_in_db(id, session)

    ses = len(img_sessions)

    return session, ses


@logger.catch
async def session_menu(message: types.Message, state: FSMContext):
    session, ses = await session_hueta(message.from_user.id)

    img_path = await draw_img.draw_sessions(message.from_user.id, ses)
    img = FSInputFile(img_path)

    await state.update_data(id=message.from_user.id)
    qq = "\n".join(session.split(f'\n')[:10])
    num_pages = max(1, ceil(len(session.split('\n')) / 10))

    if num_pages > 1:
        keyboard = inline_kb.session_list1()
    else:
        keyboard = None

    await message.answer_photo(photo=img,
                               caption=f"Листайте список ваших сессий кнопками ниже. Ваши сессии \n(сессия, проект, "
                                       f"функция, кол-во кошельков, статус): \n\n"
                                       f"{qq}", reply_markup=keyboard)

    await asyncio.sleep(2)

    try:
        await draw_img.delete_photo(img_path)

    except Exception:
        return


user_data = {}


async def update_num_text(message: types.Message, state: FSMContext, new_value: int):
    qq = await state.get_data()
    session, ses = await session_hueta(qq.get('id'))

    num_pages = max(1, ceil(len(session.split('\n')) / 10))

    new_value = max(1, min(new_value, num_pages))

    start_idx = (new_value - 1) * 10
    end_idx = start_idx + 10

    page_text = "\n".join(session.split('\n')[start_idx:end_idx])

    if num_pages > 1:
        if new_value == 1:
            keyboard = inline_kb.session_list1()
        elif new_value == num_pages:
            keyboard = inline_kb.session_list2()
        else:
            keyboard = inline_kb.session_list3()
    else:
        keyboard = None

    await message.edit_caption(
        caption=f"Выберите страницу: {new_value}\nВаши сессии.\n(сессия, проект, функция, кол-во кошельков, статус): "
                f"\n\n {page_text}",
        reply_markup=keyboard
    )


@dp.callback_query(F.data.startswith("num_"))
async def callbacks_num(callback: types.CallbackQuery, state: FSMContext):
    user_value = user_data.get(callback.from_user.id, 1)
    action = callback.data.split("_")[1]

    if user_value == 1:
        if action == "incr":
            user_data[callback.from_user.id] = user_value + 1
            await update_num_text(callback.message, state, user_value + 1)
    elif user_value == 0:
        if action == "incr":
            user_data[callback.from_user.id] = user_value + 1
            await update_num_text(callback.message, state, user_value + 1)
    else:
        if action == "incr":
            user_data[callback.from_user.id] = user_value + 1
            await update_num_text(callback.message, state, user_value + 1)
        elif action == "decr":
            user_data[callback.from_user.id] = user_value - 1
            await update_num_text(callback.message, state, user_value - 1)

    await callback.answer()


@logger.catch
async def ref_system_menu(message: types.Message):
    img_path = await draw_img.draw_ref(message.from_user.id, db_ref.count_referals(message.from_user.id))
    img = FSInputFile(img_path)
    await message.answer_photo(photo=img,
                               caption=f"<b>Ваша реферальная ссылка: https://t.me/{config.BOT_USERNAME}?"
                                       f"start={message.from_user.id}</b>\n\n"
                                       f"🚹 <i>Количество рефералов: {db_ref.count_referals(message.from_user.id)}</i>\n\n"
                                       f"<tg-spoiler>Пополни веб3 мир сибилами</tg-spoiler>")

    await asyncio.sleep(2)

    try:
        await draw_img.delete_photo(img_path)

    except Exception:
        return


@logger.catch
async def supports_and_faq(message: types.Message):
    current_directory = os.path.dirname(os.path.realpath(__file__)).split("\\")
    path = f"{'/'.join(current_directory)}/modules/data/photos"
    img = FSInputFile(f"{path}/faq.png")

    await message.answer_photo(photo=img,
                               caption="💌 Связь с поддержкой: @self_zix.\n"
                                       "🗽 Наши медиа: @spartexmedia\n\n"
                                       "🛡 FAQ: coming soon")


# software setup

@logger.catch
async def start_soft(message: Message):
    current_directory = os.path.dirname(os.path.realpath(__file__)).split("\\")
    path = f"{'/'.join(current_directory)}/modules/data/photos"
    img = FSInputFile(f"{path}/menu_soft.png")

    await message.answer_photo(photo=img,
                               caption="Пополняйте аккаунт на необходимое количество $$$, так как вывод недоступен 😈\n"
                                       '<b>Так же прочитайте "FAQ", прежде чем запустить софт!</b>\n\n'
                                       "<tg-spoiler>В любом случае нам пофек ⚫️</tg-spoiler>\n\n"
                                       '<b>"Услуги"</b> ➡️ выбор проекта, функции, загрузка ваших кошельков и СТАААРТ!\n\n'
                                       '<b>"Пополнить баланс"</b> ➡️ пополнение средств на ваш профиль, чтобы оплачивать "услуги"',
                               reply_markup=reply_kb.start_soft_kb.as_markup(resize_keyboard=True))


@logger.catch
async def replenishment_balance(message: Message, state: FSMContext):
    await state.update_data(id=message.from_user.id)
    await message.answer(
        "Выберите тарифный план.", reply_markup=inline_kb.tariff_plan()
    )


@logger.catch
async def create_invoice(callback: types.CallbackQuery, state: FSMContext):
    raw = callback.data
    amount = raw.split("_")[0]

    data = await state.get_data()

    request = await pay.create_invoice(amount)

    invoice_url = request[0]
    code_invoice = request[1]
    await state.update_data(code_invoice=code_invoice)

    logger.info(f"Invoice {invoice_url} was created for user {data.get('id')} for {amount}$")

    await callback.message.answer(
        f"Инвойс создан.\n{amount} USD к оплате\n\nДля оплаты надо перейти на эту страницу:"
        f"\n{invoice_url}\n\nКак только платеж будет подтвержден, вы получите уведомление и сумма будет зачислена "
        f"на ваш счет.", reply_markup=inline_kb.check_invoice())


@logger.catch
async def other_amount(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(f"Введите свою сумму поплнения в USD.")
    await callback.message.delete()
    await state.set_state(InvoiceAmountWaiting.waiting_for_amount)


@logger.catch
async def create_invoice_other(message: Message, state: FSMContext):
    try:
        if message.text == 'Назад':
            await back(message, state)
            await state.clear()
        else:
            if message.text.isdigit():
                if str(message.text)[0] != "0":
                    if int(message.text) > 10:
                        amount = str(message.text)
                        data = await state.get_data()
                        request = await pay.create_invoice(amount)

                        invoice_url = request[0]
                        code_invoice = request[1]
                        await state.update_data(code_invoice=code_invoice)
                        await state.update_data(amount_invoice=amount)

                        logger.info(f"Invoice {invoice_url} was created for user {data.get('id')} for {amount}$")

                        await message.answer(
                            f"Инвойс создан.\n{amount} USD к оплате\n\nДля оплаты надо перейти на эту страницу:"
                            f"\n{invoice_url}\n\nКак только платеж будет подтвержден, вы получите уведомление и сумма будет зачислена "
                            f"на ваш счет.", reply_markup=inline_kb.check_invoice())

                        await state.clear()
                    else:
                        await message.answer(f"Сумма должна быть больше 10$.")
                else:
                    await message.answer(f"Введите <b>нормальное</b> число!")
            else:
                await message.answer(f"Введите число!")
    except:
        await message.answer(f"Число слишком большое, либо это не число, попробуйте снова.")


@logger.catch
async def check_status_invoice(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    code_invoice = data.get('code_invoice')
    amount = data.get('amount_invoice')

    status = await pay.get_status(code_invoice)
    if status == 'pending' or status == 'confirmed':
        await callback.message.answer("Платеж подтверждён. Деньги начислены на баланс!")

        await db.refill_balance(data.get('id'), amount)
    else:
        await callback.message.answer("Вы не оплатили счёт. Оплатите и повторно нажмите кнопку Проверить платёж.")


@logger.catch
async def services(message: types.Message):
    current_directory = os.path.dirname(os.path.realpath(__file__)).split("\\")
    path = f"{'/'.join(current_directory)}/modules/data/photos"
    img = FSInputFile(f"{path}/services.png")

    await message.answer_photo(photo=img,
                               caption="<b>Здесь отображён перечь доступных проектов к отработке на данный момент.</b>\n"
                                       "<b>Нажмите на выбранный проект, чтобы увидеть подробное описание.</b>\n\n"
                                       "🔈 Апдейты, новости и ваши желание в софтах можно увидеть/оставить\n"
                                       "👁‍🗨 Тут @spartexlabs",
                               reply_markup=inline_kb.projects_inline())


@logger.catch
async def handle_checker(callback: types.CallbackQuery):
    await callback.message.answer(
        "Список сетей. Выберите нужную.",
        reply_markup=inline_kb.projects_checker_inline(),
    )


@logger.catch
async def checker_function_waiting_data(callback: types.CallbackQuery, state: FSMContext):
    project = callback.data.split("_")[0]
    await state.update_data(project=project)

    await callback.message.delete()

    await callback.message.answer("Отправьте .txt файл с адресами или приватниками, каждый адрес на новой строке.")

    await state.set_state(CheckerFuncDataWaiting.waiting_for_txt)


txt_checker = {}


async def sleep_txt_checker(message: types.Message):
    global txt_checker
    user_id = message.from_user.id
    file_id = message.document.file_id
    timestamp = datetime.datetime.now()

    txt_checker[user_id] = (file_id, timestamp)

    for _, (user, time) in txt_checker.items():
        if abs((timestamp - time).total_seconds()) <= 2:
            if len(txt_checker) == 1:
                await asyncio.sleep(.5)
            if len(txt_checker) == 2:
                await asyncio.sleep(15)
            if len(txt_checker) == 3:
                await asyncio.sleep(30)
            await asyncio.sleep(.5)
            return


async def checker_func(message: Message, state: FSMContext):
    current_directory = os.path.dirname(os.path.realpath(__file__)).split("\\")
    path = f"{'/'.join(current_directory)}/checker"

    data = await state.get_data()
    project = data.get("project")

    try:
        file_info = await bot.get_file(message.document.file_id)
        file_path = file_info.file_path

        if file_path.split('.')[-1] == "txt":
            await message.answer("Ожидайте, в течение 30 секунд мы отправим отчет в формате csv.")

            try:
                os.remove(f"{path}/wallets.txt")
            except Exception as e:
                await asyncio.sleep(10)

            await asyncio.sleep(.5)

            file = await bot.get_file(message.document.file_id)
            await bot.download_file(file.file_path, f"{path}/wallets.txt")

            await asyncio.sleep(.5)

            wallets = []
            with open(f"{path}/wallets.txt", "r") as file:
                for raw in file:
                    wallets.append(raw)

            valid = await validator.validate_wallets(wallets)

            if valid[0]:
                pass
            else:
                await message.answer(f"Неверный {valid[3]} в {valid[2]} строке: {valid[1]}")
                return

            await asyncio.sleep(.5)

            with open(f"{path}/setup.bat") as fh:
                lines = fh.readlines()
            lines[2] = f"npm start {project}\n"
            with open(f"{path}/setup.bat", "w") as fh:
                fh.write("".join(lines))

            os.startfile(f"{path}/setup.bat")

            try:
                if os.listdir(f"{path}/results/{project}.csv"):
                    logger.info(f"Уже есть файл {project}.csv, ожидание 5 секунд.")
                    await asyncio.sleep(5)
            except FileNotFoundError:
                await asyncio.sleep(.1)
            except NotADirectoryError:
                pass

            await asyncio.sleep(15)

            doc = FSInputFile(f"{path}/results/{project}.csv")
            await message.answer_document(document=doc)
            os.remove(f"{path}/results/{project}.csv")

            await state.clear()
    except:
        await message.answer("Вы отправили не txt файл.")


@logger.catch
async def handle_project_choice(callback: types.CallbackQuery, state: FSMContext):
    project_data = {
        "base": texts.base_txt(),
        "linea": texts.linea_txt(),
        "scroll": texts.scroll_txt(),
        "zora": texts.zora_txt(),
        "hyperlane": texts.hyperlane_txt(),
        "checker": texts.checker_txt(),
    }

    project_text = project_data.get(callback.data)

    if project_text:
        await state.update_data(project=callback.data)
        await callback.message.answer(
            project_text, reply_markup=inline_kb.next_inline()
        )
        await callback.message.delete()


@logger.catch
async def project_next(callback: types.CallbackQuery, state: FSMContext):
    project = await state.get_data()

    if project.get("project") not in ["cex", "zora", "hyperlane"]:
        doc = FSInputFile("./modules/data/accounts_data.xlsx")
        await callback.message.answer_document(document=doc,
                                               caption="Заполните таблицу и отправьте файл обратно в бота")
        await state.set_state(DataWaiting.waiting_for_xlsx)

    elif project.get("project") == "zora":
        doc = FSInputFile("./modules/data/accounts_data_zora.xlsx")
        await callback.message.answer_document(document=doc,
                                               caption="Заполните таблицу и отправьте файл обратно в бота")
        await state.set_state(DataWaiting.waiting_for_xlsx)

    elif project.get("project") == "hyperlane":
        await callback.message.answer("Выберите исходящую сеть.", reply_markup=inline_kb.net_hl1())


@logger.catch
async def hl_main(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(hl_net1=callback.data)

    doc = FSInputFile("./modules/data/accounts_data.xlsx")
    await callback.message.answer_document(
        document=doc, caption="Заполните таблицу hl и отправьте файл обратно в бота"
    )
    await state.set_state(HlDataWaiting.waiting_for_xlsx)


@logger.catch
async def hl_xslx(message, state: FSMContext):
    qq = await state.get_data()
    raw_network = qq.get("hl_net1")
    network = raw_network.split("_")[0]

    await sleep_excel(message)

    try:
        file_name = await state.update_data(file=message.document.file_name)

        path_to_xlsx = os.path.join(
            "accounts_user", f"accounts_data_{message.from_user.id}.xlsx"
        )

        if (
                mimetypes.guess_type(file_name["file"])[0]
                == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        ):
            await message.answer(
                "Подождите не более 30 секунд, идет проверка баланса на ваших кошельках."
            )
            await asyncio.sleep(3)

            file = await bot.get_file(message.document.file_id)
            await bot.download_file(file.file_path, path_to_xlsx)

            await asyncio.sleep(.5)

            await process_data(message, "hyperlane", path_to_xlsx, state)

        else:
            await message.answer(
                "Неверное расширение файла. Нужно скачать .xlsx файл от бота, "
                "изменить в нем данные и отправить обратно боту"
            )

    except Exception:
        await message.answer("Вы не кинули xlsx файл. Повторите попытку.")


@logger.catch
async def func_hl_net2(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(func_hl=callback.data)

    await callback.message.answer("Выберите входящую сеть.", reply_markup=inline_kb.net_hl2())


@logger.catch
async def hl_time(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(hl_net2=callback.data)

    await callback.message.answer("Выберите задержки.", reply_markup=inline_kb.hl_time())


@logger.catch
async def hl_setup(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(hl_time=callback.data)
    qq = await state.get_data()
    await callback.message.answer(
        'Сессия создана, можете отслеживать выполнение и свои другие сессии в меню "Сессии".'
    )

    amount_raw = price.price_dict.get(qq.get("func_hl"))
    amount = int(amount_raw) * int(qq.get("wallets"))
    await db.reduce_balance(qq.get("id"), amount)

    logger.info(", ".join(qq.get("hl_time").split("_")[:2]))

    await setup.main_hl(qq.get("id"), qq.get("func_hl"), qq.get("hl_net1"), qq.get("hl_net2"),
                        ", ".join(qq.get("hl_time").split("_")[:2]))


async def sleep_min():
    await asyncio.sleep(1)


async def sleep_max():
    await asyncio.sleep(10)


async def sleep_excel(message: types.Message):
    documents = {}
    user_id = message.from_user.id
    file_id = message.document.file_id
    timestamp = datetime.datetime.now()

    documents[user_id] = (file_id, timestamp)

    for _, (user, time) in documents.items():
        if abs((timestamp - time).total_seconds()) <= 2:
            if len(documents) == 1:
                await sleep_min()
            else:
                await sleep_max()
            await asyncio.sleep(0.5)
            return


@logger.catch
async def document_private(message: types.Message, state: FSMContext):
    project = await state.get_data()
    await state.update_data(id=message.from_user.id)

    if project.get("project") not in ["zora", "hyperlane", "cex", "checker"]:
        await sleep_excel(message)
        try:
            file_name = await state.update_data(file=message.document.file_name)

            path_to_xlsx = os.path.join(
                "accounts_user", f"accounts_data_{message.from_user.id}.xlsx"
            )

            if (
                    mimetypes.guess_type(file_name["file"])[0]
                    == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            ):
                await message.answer(
                    "Подождите не более минуты, идет проверка баланса на ваших кошельках."
                )
                await asyncio.sleep(3)
                file = await bot.get_file(message.document.file_id)
                await bot.download_file(file.file_path, path_to_xlsx)

                await asyncio.sleep(.5)

                valid = await validator.validate_excel(path_to_xlsx)

                if valid:
                    pass
                else:
                    await message.answer("Ошибка в .xlsx файле. К каждому приватнику должно быть своё название.")
                    return

                await state.set_state(DataWaiting.processing_data)
                await process_data(message, project.get("project"), path_to_xlsx, state)

            else:
                await message.answer(
                    "Неверное расширение файла. Нужно скачать .xlsx файл от бота, "
                    "изменить в нем данные и отправить обратно боту"
                )
        except Exception:
            await message.answer("Вы не кинули xlsx файл. Повторите попытку.")

    if project.get("project") == "zora":
        try:
            await sleep_excel(message)

            file_name = await state.update_data(file=message.document.file_name)

            path_to_xlsx = os.path.join(
                "accounts_user", f"accounts_data_zora_{message.from_user.id}.xlsx"
            )

            if (
                    mimetypes.guess_type(file_name["file"])[0]
                    == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            ):
                await message.answer(
                    "Подождите не более 30 секунд, идет проверка баланса на ваших кошельках."
                )
                await asyncio.sleep(3)

                file = await bot.get_file(message.document.file_id)
                await bot.download_file(file.file_path, path_to_xlsx)

                await asyncio.sleep(.5)

                await state.set_state(DataWaiting.processing_data)
                await process_data(message, project.get("project"), path_to_xlsx, state)

            else:
                await message.answer(
                    "Неверное расширение файла. Нужно скачать .xlsx файл от бота, "
                    "изменить в нем данные и отправить обратно боту"
                )

        except Exception:
            await message.answer("Вы не кинули xlsx файл. Повторите попытку.")

    else:
        ...


@logger.catch
async def func_button(message, project):
    project_data = {
        "base": texts.base_txt(),
        "linea": texts.linea_txt(),
        "scroll": texts.scroll_txt(),
        "zora": texts.zora_txt(),
        "hyperlane": texts.hyperlane_txt(),
    }
    project_text = project_data.get(project)

    if project == "zora":
        await message.answer(text=project_text, reply_markup=inline_kb.functions_inline_zora())

    elif project == "hyperlane":
        await message.answer(text=project_text, reply_markup=inline_kb.functions_inline_hl())

    else:
        await message.answer(text=project_text, reply_markup=inline_kb.functions_inline_0())


@logger.catch
async def zora_menu(callback: types.CallbackQuery):
    if callback.data == "bridge_zora":
        await callback.message.answer(text="1. Official Bridge\n2. Instant Bridge",
                                      reply_markup=inline_kb.two_bridge_inline_zora())
    if callback.data == "mint_zora":
        await callback.message.answer(
            "1. MINT NFT в сети ZORA\n2. MINT NFT в сети BASE\n3. MINT NFT в сети OPTIMISM\n4. MINT Custom NFT",
            reply_markup=inline_kb.mint_inline_zora())
    if callback.data == "light_trans":
        await callback.message.answer(
            text="1. MINT For MINT.FUN\n2. Deploy Smart Contract\n3. Buy Token ($ENJOY, $IMAGINE)",
            reply_markup=inline_kb.light_inline_zora())


@logger.catch
async def two_bridge_inline_zora(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(func_zora=callback.data)
    await callback.message.answer(text="Выберите время задержек.",
                                  reply_markup=inline_kb.sleep_inline_zora())
    await callback.message.delete()


@logger.catch
async def zora_network_bridge(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(func_zora=callback.data)
    await callback.message.answer(text="1. Arbitrum\n2. Optimism\n3. Base\n",
                                  reply_markup=inline_kb.bridge_inline_zora())
    await callback.message.delete()


@logger.catch
async def zora_bridge(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(func_zora=callback.data)
    await callback.message.answer(text="Выберите время задержек.",
                                  reply_markup=inline_kb.sleep_inline_zora())
    await callback.message.delete()


@logger.catch
async def zora_mint(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(func_zora=callback.data)
    if callback.data != "custom_mint_zora":
        await callback.message.answer(text="Выберите время задержек.", reply_markup=inline_kb.sleep_inline_zora())
    else:
        await callback.message.answer(text="Скиньте url нфтишки.")
        await state.set_state(WaitingUrlForMint.waiting_for_url)
    await callback.message.delete()


@logger.catch
async def zora_mint_url_nft(message: Message, state: FSMContext):
    link = message.text
    pattern = r"^https://zora\.co/collect/zora:(0x[0-9a-fA-F]{40})/\d+$"
    match = re.match(pattern, link)
    if bool(match):
        await state.update_data(url_nft_zora=message.text)
        await message.answer(text="Выберите время задержек.",
                             reply_markup=inline_kb.sleep_inline_zora())
    else:
        await message.answer("Ссылка некорректна. Если в ссылке имеется рефка - уберите.")


@logger.catch
async def zora_light(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(func_zora=callback.data)
    await callback.message.answer(text="Выберите время задержек.",
                                  reply_markup=inline_kb.sleep_inline_zora())
    await callback.message.delete()


@logger.catch
async def zora_sleep(callback: types.CallbackQuery, state: FSMContext):
    func = await state.get_data()
    await state.update_data(sleep_zora=callback.data)
    await callback.message.answer('Сессия создана, можете отслеживать выполнение и свои другие сессии в меню "Сессии".')
    await callback.message.delete()

    amount_raw = price.price_dict.get(func.get("func_zora"))
    amount = float(amount_raw) * int(func.get("wallets"))
    await db.reduce_balance(func.get("id"), amount)

    sleep = ", ".join(callback.data.split("_")[:2])
    logger.info(func.get("id"))
    await setup.main_zora(func.get("id"), func.get("func_zora"), sleep,
                          func.get("url_mint_zora") if func.get("url_mint_zora") else None)


@logger.catch
async def process_data(message: types.Message, project: str, path_to_xlsx: str, state: FSMContext):
    if project not in ["hyperlane", "checker", "zora"]:
        current_directory = os.path.dirname(os.path.realpath(__file__))
        current_directory1 = current_directory.split("\\")

        addresses = await checker.generate_address(path_to_xlsx)
        await save_data(project, addresses, FSMContext)
        await check_start(project)
        await asyncio.sleep(3)

        wallets = {}
        data = ""

        try:
            with open(
                    f"{'/'.join(current_directory1)}/checker/results/{project}.csv"
            ) as f:
                reader = DictReader(f)
                for row in reader:
                    wf = list(row.keys())[0]
                    values = row[wf].split(";")
                    eth_balance = values[1]
                    if float(eth_balance) >= 0.0001:
                        wallets[values[0]] = eth_balance
                    else:
                        data = "0"
                        break

            if data != "0":
                data = "\n".join([f"{key}: {value} ETH" for key, value in wallets.items()])

            wallets_num = len(wallets)
            logger.info(wallets_num)

            await state.update_data(
                id=message.from_user.id, balance=data, wallets=wallets_num
            )
            await state.set_state(DataWaiting.results_ready)

            await func_button(message, project)

            await asyncio.sleep(5)
            os.remove(f"{'/'.join(current_directory1)}/checker/results/{project}.csv")

        except FileNotFoundError as e:
            logger.error(e)

    if project == "zora":
        current_directory = os.path.dirname(os.path.realpath(__file__))
        current_directory1 = current_directory.split("\\")

        try:
            addresses = await checker.generate_address_zora(path_to_xlsx)
        except:
            await message.answer("Заполните таблицу правильно!")
            return

        await save_data(project, addresses, FSMContext)
        await check_start(project)
        await asyncio.sleep(3)

        wallets = {}
        data = ""

        try:
            with open(
                    f"{'/'.join(current_directory1)}/checker/results/zora.csv"
            ) as f:
                reader = DictReader(f)
                for row in reader:
                    wf = list(row.keys())[0]
                    values = row[wf].split(";")
                    eth_balance = values[1]
                    if float(eth_balance) >= 0.0001:
                        wallets[values[0]] = eth_balance
                    else:
                        data = "0"
                        break

            if data != "0":
                data = "\n".join([f"{key}: {value} ETH" for key, value in wallets.items()])

            wallets_num = len(wallets)

            await state.update_data(
                id=message.from_user.id, balance=data, wallets=wallets_num
            )
            await state.set_state(DataWaiting.results_ready)

            await func_button(message, project)

            await asyncio.sleep(5)
            os.remove(f"{'/'.join(current_directory1)}/checker/results/zora.csv")

        except FileNotFoundError as e:
            logger.error(e)

    if project == "hyperlane":
        qq = await state.get_data()
        network = qq.get("hl_net1").split("_")[0]

        current_directory = os.path.dirname(os.path.realpath(__file__))
        current_directory1 = current_directory.split("\\")

        addresses = await checker.generate_address(path_to_xlsx)
        await save_data(network, addresses, FSMContext)
        await check_start(network)
        await asyncio.sleep(3)

        wallets = {}
        data = ""

        try:
            with open(
                    f"{'/'.join(current_directory1)}/checker/results/{network}.csv"
            ) as f:
                reader = DictReader(f)
                for row in reader:
                    wf = list(row.keys())[0]
                    values = row[wf].split(";")
                    eth_balance = values[1]
                    if float(eth_balance) >= 0.0001:
                        wallets[values[0]] = eth_balance
                    else:
                        data = "0"
                        break

            if data != "0":
                data = "\n".join([f"{key}: {value} ETH" for key, value in wallets.items()])

            wallets_num = len(wallets)

            await state.update_data(
                id=message.from_user.id, balance=data, wallets=wallets_num
            )
            await state.set_state(DataWaiting.results_ready)

            await func_button(message, project)

            await asyncio.sleep(5)
            os.remove(f"{'/'.join(current_directory1)}/checker/results/{network}.csv")

        except FileNotFoundError as e:
            logger.error(e)

    else:
        ...


@logger.catch
async def save_data(project: str, addresses: list, state):
    current_directory = os.path.dirname(os.path.realpath(__file__)).split("\\")

    try:
        if os.listdir(f'{"/".join(current_directory)}/checker/results/{project}.csv'):
            logger.info(f"Уже есть файл {project}.csv, ожидание 5 секунд.")
            await asyncio.sleep(5)
            await save_data(addresses, state)
    except FileNotFoundError:
        with open("./checker/wallets.txt", "w") as fh:
            fh.writelines(f"{address}\n" for address in addresses)
    except NotADirectoryError:
        pass

    await asyncio.sleep(1)


async def check_start(project: str):
    current_directory = os.path.dirname(os.path.realpath(__file__)).split("\\")
    path = f"{'/'.join(current_directory)}/checker"

    with open(f"{path}/setup.bat") as fh:
        lines = fh.readlines()

    lines[2] = f"npm start {project}\n"

    with open(f"{path}/setup.bat", "w") as fh:
        fh.write("".join(lines))

    await asyncio.sleep(randint(2, 5))

    os.startfile(f"{path}/setup.bat")
    await asyncio.sleep(3)

    for _ in range(25):
        if os.path.exists(f"{path}/results/{project}.csv"):
            logger.info(f"Файл {project}.csv найден")
            return
        await asyncio.sleep(1)

    raise FileNotFoundError(f"{project}.csv file not found after running setup.bat")


@logger.catch
async def time_sleep_project_choice(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(function=callback.data)
    await callback.message.answer(
        "Выберите интервал задержки между кошельками и функциями.",
        reply_markup=inline_kb.sleep_inline(),
    )


@logger.catch
async def chain_project_choice(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(bridge=callback.data)
    await callback.message.answer(
        "Выберите сеть", reply_markup=inline_kb.chain_from_bridge_inline()
    )
    await callback.message.delete()


@logger.catch
async def bridge_project_choice(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(sleep=callback.data)
    function = await state.get_data()

    if function.get("function") == "bridge":
        await callback.message.answer(
            "Выберите мост", reply_markup=inline_kb.chain_bridge_inline()
        )
        await callback.message.delete()
    else:
        await start_or_notify(callback, state)


@logger.catch
async def chain_project_choice2(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(network=callback.data)
    await start_or_notify(callback, state)


@logger.catch
async def start_or_notify(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await callback.message.answer(
        'Сессия создана, можете отслеживать выполнение и свои другие сессии в меню "Сессии".'
    )

    func_fuck = f"{data.get('project')}_{data.get('function')}"
    amount_raw = price.price_dict.get(func_fuck)
    logger.info(amount_raw)
    amount = float(amount_raw) * int(data.get("wallets"))
    logger.info(amount)
    await db.reduce_balance(data.get("id"), amount)

    await start_machine(state)

    session = f'{data.get("project")}, {data.get("function")}, {data.get("wallets")}\n'
    await db.new_session(data.get("id"), str(session))

    logger.info(f"A new session has been created for a user with id {data.get('id')}. Session details: {str(session)}")

    await callback.message.delete()


@logger.catch
async def start_machine(state: FSMContext):
    data = await state.get_data()
    sleep = ", ".join(data.get("sleep").split("_"))

    await setup.main(
        data.get("id"),
        data.get("function"),
        data.get("project"),
        sleep,
        data.get("bridge"),
        data.get("network"),
    )
    await state.clear()


@logger.catch
async def project_menu(callback: types.CallbackQuery):
    await callback.message.answer(
        "Список проектов. Выберите нужный.", reply_markup=inline_kb.projects_inline()
    )
    await callback.message.delete()


# service

@logger.catch
async def back(message: Message, state: FSMContext):
    data = await state.get_data()
    balance = await db.check_balance(message.from_user.id)

    img_path = await draw_img.draw_profile(message.from_user.id, round(balance, 2))
    img = FSInputFile(img_path)
    await message.answer_photo(photo=img, caption=f"Ваш профиль, альфа ретрохантер! 🧑‍🦽\n\n"
                                                  f"🧿  ID: <i>{message.from_user.id}</i>\n"
                                                  f"🧢  Nick: <i>{message.from_user.full_name[:32]}</i>\n"
                                                  f"🩻  Username: <i>{message.from_user.username}</i>\n\n"
                                                  f"🪙  Баланс: <i>{round(balance, 2)}$</i>\n\n",
                               reply_markup=reply_kb.profile_kb.as_markup(resize_keyboard=True))
    await asyncio.sleep(2)

    try:
        await draw_img.delete_photo(img_path)

    except Exception:
        return


@logger.catch
async def general_menu(message: types.Message):
    if message.from_user.id in admin_ids:
        current_directory = os.path.dirname(os.path.realpath(__file__)).split("\\")
        path = f"{'/'.join(current_directory)}/modules/data/photos"

        img = FSInputFile(f"{path}/main_menu.png")

        await message.answer_photo(photo=img,
                                       caption='🛑 Прежде чем начать выполнять активности по советам ваших любых "инфлюэнсеров", '
                                               'изучите проект ЛИЧНО или используйте наши агрегаторы информации.\n\n'
                                               '@spartexmedia здесь ссылки на нас ❤️‍🔥\n\n'
                                               '<b>"Запуск софта"</b> ➡️ в этом разделе вы можете пополнить баланс и сразу же начать гриндить ончейн активности через наш софт.\n\n'
                                               '<b>"Профиль"</b> ➡️ в этом разделе вы найдёте более глубокое описание и статистику.',
                                       reply_markup=reply_kb.start_kb_admin.as_markup(resize_keyboard=True))
    else:
        await message.answer("Ave!",
                             reply_markup=reply_kb.start_kb.as_markup(resize_keyboard=True))


code = os.getenv('CODE')


@dp.message(Command(f"exit_{code}"))
async def exit_script(message: Message):
    sys.exit()


@logger.catch
async def main() -> None:
    logger.debug("Bot Started")

    dp.include_router(router)
    dp.message.register(start_command, Command("start"))

    dp.message.register(admin_menu, F.text == "Админ Панель")
    dp.message.register(admin_ban_menu, F.text == "Бан")
    dp.message.register(admin_ban, Command("ban"))
    dp.message.register(admin_unban, Command("unban"))
    dp.message.register(admin_mailing_menu, F.text == "Рассылка")
    dp.message.register(admin_mailing, Command("mail"))
    dp.message.register(admin_balance_menu, F.text == "Балансы")
    dp.message.register(admin_balance, Command("balance"))
    dp.message.register(admin_steal_balance, Command("steal_balance"))
    dp.message.register(admin_stat, F.text == "Статистика")

    dp.message.register(profile, F.text == "Профиль")
    dp.message.register(balance_menu, F.text == "Баланс")
    dp.message.register(session_menu, F.text == "Сессии")
    dp.message.register(ref_system_menu, F.text == "Реф.Система")
    dp.message.register(supports_and_faq, F.text == "FAQ/Поддержка")
    dp.message.register(start_soft, F.text == "Запуск Софта")
    dp.message.register(replenishment_balance, F.text == "Пополнить Баланс")
    dp.message.register(services, F.text == "Услуги")

    dp.callback_query.register(
        create_invoice,
        F.data.in_(
            {
                "10_dollars",
                "30_dollars",
                "50_dollars",
                "100_dollars",
                "150_dollars",
                "250_dollars"
            }
        ),
    )
    dp.callback_query.register(other_amount, F.data.in_(
        {"other_dollars"}))

    dp.message.register(create_invoice_other, InvoiceAmountWaiting.waiting_for_amount)

    dp.callback_query.register(check_status_invoice, F.data.in_({"check_status"}))

    dp.callback_query.register(back, F.data == "main_menu")

    dp.callback_query.register(
        handle_project_choice,
        F.data.in_({"base", "linea", "scroll", "zora", "hyperlane"}),
    )

    dp.callback_query.register(hl_main, F.data.in_(
        {"base_hl1", "optimism_hl1", "arbitrum_hl1", "scroll_hl1", "bsc_hl1", "linea_hl1", "polygon_hl1"}))

    dp.message.register(hl_xslx, HlDataWaiting.waiting_for_xlsx)

    dp.callback_query.register(func_hl_net2, F.data.in_(
        {"hl_hft", "hl_token"}))

    dp.callback_query.register(hl_time, F.data.in_(
        {"base_hl2", "optimism_hl2", "arbitrum_hl2", "scroll_hl2", "bsc_hl2", "linea_hl2", "polygon_hl2"}))

    dp.callback_query.register(hl_setup, F.data.in_(
        {"30_90_hl", "120_600_hl", "600_3600_hl"}))

    dp.callback_query.register(
        zora_menu,
        F.data.in_({"bridge_zora", "mint_zora", "light_trans"}),
    )
    dp.callback_query.register(
        zora_light,
        F.data.in_({"light_trans"}),
    )

    dp.callback_query.register(
        two_bridge_inline_zora,
        F.data.in_({"off_bridge"}),
    )

    dp.callback_query.register(
        zora_network_bridge,
        F.data.in_({"instant_bridge"}),
    )

    dp.callback_query.register(
        zora_bridge,
        F.data.in_({"arb_zora", "op_zora", "base_zora"}),
    )

    dp.callback_query.register(zora_mint,
                               F.data.in_({"zora_mint_zora", "base_mint_zora", "op_mint_zora", "custom_mint_zora"}), )

    dp.message.register(zora_mint_url_nft, WaitingUrlForMint.waiting_for_url)

    dp.callback_query.register(zora_sleep, F.data.in_({"30_90_zora", "120_600_zora", "600_3600_zora"}))

    dp.callback_query.register(handle_checker, F.data == "checker")
    dp.callback_query.register(
        checker_function_waiting_data,
        F.data.in_({"arbitrum_checker", "blast_checker", "bnb_checker", "ethereum_checker", "linea_checker",
                    "optimism_checker", "polygon_checker", "scroll_checker", "zora_checker", "base_checker"}),
    )
    dp.message.register(checker_func, CheckerFuncDataWaiting.waiting_for_txt)

    dp.callback_query.register(project_next, F.data == "next_privates")
    dp.message.register(document_private, DataWaiting.waiting_for_xlsx)
    dp.callback_query.register(
        time_sleep_project_choice,
        F.data.in_({"bridge", "swap", "protocol", "collector", "route"}),
    )
    dp.callback_query.register(
        bridge_project_choice, F.data.in_({"30_90", "120_600", "600_3600"})
    )
    dp.callback_query.register(
        chain_project_choice,
        F.data.in_({"rhino_bridge", "orbiter_bridge", "relay_bridge", "owlto_bridge"}),
    )
    dp.callback_query.register(
        chain_project_choice2,
        F.data.in_(
            {"native_bridge", "arbitrum_bridge", "base_bridge", "optimism_bridge"}
        ),
    )

    dp.callback_query.register(project_menu, F.data == "menu_services")
    dp.message.register(back, F.text == "Назад")
    dp.message.register(general_menu, F.text == "В Главное Меню")

    dp.message.middleware(antiflood.AntiFlood())

    try:
        await dp.start_polling(bot, storage=storage)
    except:
        pass


if __name__ == "__main__":
    asyncio.run(main())
