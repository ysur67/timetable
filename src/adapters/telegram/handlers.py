from typing import Annotated

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aioinject import Inject, inject

from adapters.telegram.middlewares.current_user import CurrentUserMiddleware
from core.models.user import User

dispatcher = Dispatcher()
dispatcher.message.middleware(CurrentUserMiddleware())


@dispatcher.message(CommandStart())
@inject
async def handle_command_start(
    message: Message,
    bot: Annotated[Bot, Inject],
    user: User,
) -> None:
    builder = ReplyKeyboardBuilder()
    builder.button(text="Показать расписание", callback_data="get-schedule")
    select_group_title = "Выбрать группу"
    if (group := user.preferences.selected_group) is not None:
        select_group_title = f"Выбрать группу ({group.title})"
    builder.button(text=select_group_title, callback_data="set-group")
    builder.button(text="Настройки", callback_data="set-settings")
    builder.adjust(1)
    await bot.send_message(
        message.chat.id,
        "Выберите один из пунктов",
        reply_markup=builder.as_markup(),
    )
