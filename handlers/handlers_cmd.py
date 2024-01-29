from aiogram import Router, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ContentType, InputMediaPhoto
from aiogram.exceptions import TelegramServerError
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import or_f
from aiogram.fsm.state import default_state
from PIL import Image
import logging

from keyboards.keyboards import generation_inline_keyboard
from lexicon.lexicon_en import CMD_ANSWER, SET_PARAMS_KB
from database.images_db import (users, User, Parameters,
                                Photos2Transfer, Photo,
                                DEFAULT_STYLE_PATH, DEFAULT_CONTENT_PATH)
from transfer_model.transfer_style import net_transfer_style
from FSM.fsm import FSMState


rt_commands = Router()
storage = MemoryStorage()
logger = logging.getLogger(__name__)


@rt_commands.message(Command(commands='start'))
async def start_answer(msg: Message):
    await msg.answer(CMD_ANSWER['start'])


@rt_commands.message(Command(commands='help'))
async def help_answer(msg: Message):
    await msg.answer(CMD_ANSWER['help'])


@rt_commands.message(Command(commands='default_photos'))
async def set_default(msg: Message):
    logger.info('Set defualt_photos')
    new_user = User(
        user_id=msg.from_user.id,
        params=Parameters(),
        photos=Photos2Transfer(
            style=Photo(img_path=DEFAULT_STYLE_PATH),
            content=Photo(img_path=DEFAULT_CONTENT_PATH)
        )
    )
    users[msg.from_user.id] = new_user
    media = [
        InputMediaPhoto(media=new_user.photos.style.bot_img,
                        caption=CMD_ANSWER['set_default_photos']),
        InputMediaPhoto(media=new_user.photos.content.bot_img)
    ]
    await msg.answer_media_group(media)


@rt_commands.message(Command(commands='cancel'), ~StateFilter(default_state))
async def stop_transfer_style(msg: Message, state: FSMContext):
    my_state = await state.get_state()
    await state.clear()
    logger.info(f'Cancel state = {my_state}')
    if my_state == FSMState.transfer_style:
        await msg.answer(CMD_ANSWER['cancel_transfering_succuses'])
    elif my_state in (FSMState.upload_content, FSMState.upload_style):
        await msg.answer(CMD_ANSWER['cancel_photo_upload'])


@rt_commands.message(or_f(Command('upload_style'),
                          StateFilter(FSMState.upload_style)))
async def upload_style(msg: Message, bot: Bot, state: FSMContext):
    logging.debug(msg.json())
    if msg.content_type == ContentType.PHOTO:
        # Get file information from bot by file_id
        file = await bot.get_file(msg.photo[-1].file_id)
        # Download file from bot by file_path
        down_file_bits = await bot.download_file(file.file_path)
        # Convert file to PIL Image
        img = Image.open(down_file_bits)
        # Add uploded photo to user database
        style_photo = Photo(file_id=msg.photo[-1].file_id, pil_img=img)
        id = msg.from_user.id
        if id in users:
            users[id].photos.style = style_photo
        else:
            users[id] = User(
                user_id=id,
                photos=Photos2Transfer(
                    style=style_photo
                )
            )
        await msg.answer(CMD_ANSWER['upload_style_success'])
        await state.clear()
        logger.info('Uploaded style photo')
    else:
        await state.set_state(FSMState.upload_style)
        await msg.answer(CMD_ANSWER['upload_style_instruction'])


@rt_commands.message(Command('set_parameters'))
async def set_parametrs_keyboard(msg: Message):
    await msg.answer(
        text='Set parameters as you wish. by it depends on working time',
        reply_markup=generation_inline_keyboard(2, SET_PARAMS_KB)
    )


@rt_commands.message(or_f(Command('upload_content'),
                          StateFilter(FSMState.upload_content)))
async def upload_content(msg: Message, bot: Bot,
                         state: FSMContext):
    logging.debug(msg.json())
    if msg.content_type == ContentType.PHOTO:
        # Get file information from bot by file_id
        file = await bot.get_file(msg.photo[-1].file_id)
        # Download file from bot by file_path
        down_file_bits = await bot.download_file(file.file_path)
        # Convert file to PIL Image
        img = Image.open(down_file_bits)
        # Add uploded photo to user database
        content_photo = Photo(file_id=msg.photo[-1].file_id, pil_img=img)
        id = msg.from_user.id
        if id in users:
            users[id].photos.content = content_photo
        else:
            users[id] = User(
                user_id=id,
                photos=Photos2Transfer(
                    content=content_photo
                )
            )
        await state.clear()
        await msg.answer(CMD_ANSWER['upload_content_success'])
    else:
        await state.set_state(FSMState.upload_content)
        await msg.answer(CMD_ANSWER['upload_content_instruction'])


@rt_commands.message(Command(commands='transfer_style'))
async def transfer_style(msg: Message, bot: Bot, state: FSMContext):
    id = msg.from_user.id
    if id not in users or (users[id].photos.style is None
                           and users[id].photos.content is None):
        await msg.answer(CMD_ANSWER['transter_waiting_photos'])
    elif users[id].photos.style is None:
        await msg.answer(CMD_ANSWER['transter_waiting_style'])
    elif users[id].photos.content is None:
        await msg.answer(CMD_ANSWER['transter_waiting_content'])
    else:
        # Show information about transfering before transfer
        media = [
            InputMediaPhoto(media=users[id].photos.style.bot_img,
                            caption=CMD_ANSWER['starting_transfering']),
            InputMediaPhoto(media=users[id].photos.content.bot_img)
        ]
        await msg.answer_media_group(media)
        await msg.answer(str(users[id].params))
        # Set transfer_style state to be able to interrupt process
        # by cancel command
        await state.set_state(FSMState.transfer_style)
        # Show content photo, which will be edited during train
        bot_message = await bot.send_photo(
            chat_id=msg.from_user.id,
            photo=users[id].photos.content.bot_img,
            caption='New image epoch=0'
        )
        try:
            await net_transfer_style(
                users[id].photos.style.pil_img,
                users[id].photos.content.pil_img,
                size=users[id].params.resolution,
                epochs=users[id].params.epochs,
                chat_id=msg.from_user.id,
                bot=bot,
                fsm_state=state,
                last_msg=bot_message
            )
            await msg.answer(CMD_ANSWER['transfering_succses'])
        except TelegramServerError:
            logger.error('Exeption in net_transfer_style', exc_info=True)
            await msg.answer(CMD_ANSWER['transfering_fail'])
