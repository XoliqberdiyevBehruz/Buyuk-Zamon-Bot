from aiogram import Router, types, filters, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

import config
import utils.bot_text as bot_text
from utils import request, utils
from keyboards import reply, inlines
from main import bot
from tasks import update_user, change_user_group_joined, create_telegram_group, set_student_to_tg_group

router = Router()


class Register(StatesGroup):
    phone = State()
    full_name = State()
    contract_number = State()


@router.callback_query(F.data == "ha")
async def remove_keyboard(callback: types.CallbackQuery):
    await callback.message.answer(request.create_invite_link(config.BOT_TOKEN, config.CHANNEL_ID, callback.message.from_user.id))
    set_student_to_tg_group.delay(config.CHANNEL_ID, res_data.get('id'))
    await callback.answer()


@router.callback_query(F.data == "yoq")
async def remove_keyboard(callback: types.CallbackQuery):
    await callback.message.answer(bot_text.callback_no)
    await callback.answer()


@router.message(filters.CommandStart())
async def say_hello(message: types.Message, state: FSMContext):
    await message.answer(bot_text.start_text)
    await state.set_state(Register.phone)
    await message.answer("Telefon raqamni yuboring", reply_markup=reply.phone_number)


@router.message(Register.phone)
async def get_full_name(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.contact.phone_number)
    await state.set_state(Register.full_name)
    await message.answer("Ism Familiyani kiriting", reply_markup=ReplyKeyboardRemove())


@router.message(Register.full_name)
async def get_contract_number(message: types.Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    await state.set_state(Register.contract_number)
    await message.answer("Shartnoma raqamini kiriting")


@router.message(Register.contract_number)
async def get_user_in_crm(message: types.Message, state: FSMContext):
    await state.update_data(contract_number=message.text)
    data = await state.get_data()
    global res_data
    res_data = request.get_user(data.get('phone'), data.get('full_name'), data.get('contract_number'))
    if "type" in res_data and res_data.get('type') != "graduate":
        update_user.delay(
            res_data.get('id'), message.from_user.id, message.from_user.username, message.from_user.full_name
        )
        change_user_group_joined.delay(res_data.get('id'))
        if res_data.get('status') != "completed":
            is_joined = await utils.get_chat_member(bot, config.FIRST_CHANNEL_ID, message.from_user.id)
            if not is_joined:
                await message.answer(
                    f"{bot_text.status_not_complited(res_data.get('id'))}\n\n{request.create_invite_link(token=config.BOT_TOKEN,chat_id=config.FIRST_CHANNEL_ID, user_id=message.from_user.id)}" 
                )
                set_student_to_tg_group.delay(config.FIRST_CHANNEL_ID, res_data.get('id'))
            else:
                await message.answer(bot_text.status_not_complited(res_data.get('id')))

        else:
            is_joined = await utils.get_chat_member(bot, config.SECOND_CHANNEL_ID, message.from_user.id)
            if not is_joined:
                await message.answer(
                    f"{bot_text.status_complited(res_data.get('id'))}\n\n{request.create_invite_link(token=config.BOT_TOKEN,chat_id=config.SECOND_CHANNEL_ID, user_id=message.from_user.id)}" 
                )
                set_student_to_tg_group.delay(config.SECOND_CHANNEL_ID, res_data.get('id'))

            else:
                await message.answer(bot_text.status_complited(res_data.get('id')))
    elif res_data.get('type') == 'graduate':
        await message.answer(bot_text.graduate_text(), reply_markup=inlines.yes_or_no)
    else:
        await message.answer(bot_text.register_failed)


@router.message(filters.Command("chat_id"))
async def get_chat_id(message: types.Message):
    if message.chat.type in ["group", 'supergroup']:
        create_telegram_group.delay(message.chat.title, message.chat.id)
        await message.delete()
