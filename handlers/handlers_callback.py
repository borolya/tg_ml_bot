from aiogram import Router, F
from aiogram.types import CallbackQuery

from keyboards.keyboards import generation_inline_keyboard
from lexicon.lexicon_en import SET_EPOCH_KB, SET_PARAMS_KB, SET_RESOLUTION_KB
from database.images_db import users, User, Parameters


rt_callbacks = Router()


@rt_callbacks.callback_query(F.data == 'set_epoch')
async def set_epoch_kb(cb: CallbackQuery):
    await cb.message.edit_text(
        text='Choose epoch numbers',
        reply_markup=generation_inline_keyboard(3, SET_EPOCH_KB)
    )


@rt_callbacks.callback_query(F.data == 'set_resolution')
async def set_params_kb(cb: CallbackQuery):
    await cb.message.edit_text(
        text='Choose photo resolution',
        reply_markup=generation_inline_keyboard(3, SET_RESOLUTION_KB)
    )


@rt_callbacks.callback_query(F.data[:5] == 'epoch')
async def set_epoch(cb: CallbackQuery):
    user_id = cb.from_user.id
    epoch = int(cb.data[5:])
    if user_id not in users:
        users[user_id] = User(
            user_id=user_id,
            params=Parameters(epochs=epoch)
        )
    else:
        users[user_id].params.epochs = epoch
    await cb.message.edit_text(
        text='Epoch is set.\n' + str(users[user_id].params)
             + '\nUpdate another parameter or press Cancel.',
        reply_markup=generation_inline_keyboard(2, SET_PARAMS_KB)
    )


@rt_callbacks.callback_query(F.data[:11] == 'resolution_')
async def set_resolution(cb: CallbackQuery):
    user_id = cb.from_user.id
    resolution_dict = Parameters().resolution_dict
    if user_id not in users:
        users[user_id] = User(
            user_id=user_id,
            params=Parameters(resolution=resolution_dict[cb.data[11:]])
        )
    else:
        users[user_id].params.resolution = resolution_dict[cb.data[11:]]
    await cb.message.edit_text(
        text='Resolution is set.\n' + str(users[user_id].params)
             + '\nUpdate another parameter or press Cancel.',
        reply_markup=generation_inline_keyboard(2, SET_PARAMS_KB)
    )


@rt_callbacks.callback_query(F.data == 'cancel_keyboard')
async def cancel_keyboard(cb: CallbackQuery):
    await cb.message.edit_text(
        text='Out of parameters setting.'
    )


@rt_callbacks.callback_query(F.data == 'back_2setparams')
async def back_2setparams(cb: CallbackQuery):
    await cb.message.edit_text(
        text='Set parameters as you wish. by it depends on working time',
        reply_markup=generation_inline_keyboard(2, SET_PARAMS_KB)
    )
