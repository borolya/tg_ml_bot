from aiogram import Bot
from aiogram.types import BotCommand, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from lexicon.lexicon_en import MENU_COMMANDS


def generation_inline_keyboard(width: int, keyboard_dict: dict[str, str]):
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = list()

    for key, item in keyboard_dict.items():
        button = InlineKeyboardButton(
            callback_data=key,
            text=item)
        buttons.append(button)
    kb_builder.row(*buttons, width=width)
    return kb_builder.as_markup()


async def set_menu(bot: Bot):
    commands_list = list()
    for command, description in MENU_COMMANDS.items():
        commands_list.append(
            BotCommand(
                command=command,
                description=description
            )
        )
    await bot.set_my_commands(commands_list)
