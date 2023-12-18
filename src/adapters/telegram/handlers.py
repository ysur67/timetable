import uuid
from typing import Annotated

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart, or_f
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aioinject import Inject, inject

from adapters.telegram.middlewares.current_user import CurrentUserMiddleware
from adapters.telegram.states import GroupSelectionState
from core.domain.educational_level.queries.get_all import GetAllEducationalLevelsQuery
from core.domain.group.dtos import GetGroupsByEducationalLevelDto
from core.domain.group.queries.get_by_educational_level import (
    GetGroupsByEducationalLevelQuery,
)
from core.errors import Never
from core.models.user import User

dispatcher = Dispatcher()
dispatcher.message.middleware(CurrentUserMiddleware())


@dispatcher.message(or_f(CommandStart(), F.text == "меню"))
@inject
async def handle_command_start(
    message: Message,
    bot: Annotated[Bot, Inject],
    user: User,
) -> None:
    builder = ReplyKeyboardBuilder()
    builder.button(text="Показать расписание")
    select_group_title = "Выбрать группу"
    if (group := user.preferences.selected_group) is not None:
        select_group_title = f"Выбрать группу ({group.title})"
    builder.button(text=select_group_title)
    builder.button(text="Настройки")
    builder.adjust(1)
    await bot.send_message(
        message.chat.id,
        "Выберите один из пунктов",
        reply_markup=builder.as_markup(),
    )


@dispatcher.message(
    or_f(
        F.text == "Показать расписание",
        Command("/get_schedule"),
    ),
)
@inject
async def handle_get_schedule(
    message: Message,
    bot: Annotated[Bot, Inject],
    user: User,
) -> None:
    if (group := user.preferences.selected_group) is None:
        await bot.send_message(
            message.chat.id,
            "Группа не выбрана",
        )
        return
    await bot.send_message(
        message.chat.id,
        f"Группа {group.title}",
    )


@dispatcher.message(
    or_f(
        F.text == "Выбрать группу",
        Command("/set_group"),
    ),
)
@inject
async def handle_set_group(
    message: Message,
    bot: Annotated[Bot, Inject],
    state: FSMContext,
    query: Annotated[GetAllEducationalLevelsQuery, Inject],
) -> None:
    await state.set_state(GroupSelectionState.educational_level_selection)
    educational_levels = await query.execute()
    if len(educational_levels) == 0:
        await bot.send_message(
            message.chat.id,
            "Не удалось найти уровни образования...",
        )
        return
    builder = InlineKeyboardBuilder()
    for level in educational_levels:
        builder.button(text=level.title.capitalize(), callback_data=str(level.id))
    builder.adjust(1)
    await bot.send_message(
        message.chat.id,
        "Выберите один из пунктов",
        reply_markup=builder.as_markup(),
    )


@dispatcher.callback_query(GroupSelectionState.educational_level_selection)
@inject
async def handle_educational_level_selection(
    callback: CallbackQuery,
    state: FSMContext,
    query: Annotated[GetGroupsByEducationalLevelQuery, Inject],
) -> None:
    if callback.data is None:
        raise Never
    groups = await query.execute(
        GetGroupsByEducationalLevelDto(level_id=uuid.UUID(callback.data)),
    )
    if len(groups) == 0:
        await callback.answer(
            "Не удалось найти ни одной группы...",
            show_alert=True,
        )
        return
    await state.set_state(GroupSelectionState.group_selection)
    builder = ReplyKeyboardBuilder()
    for group in groups:
        builder.button(text=group.title)
    builder.adjust(2)
    await callback.answer(
        "Выберите одну из групп",
        reply_markup=builder.as_markup(),
    )
