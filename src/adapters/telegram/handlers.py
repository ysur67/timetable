import uuid
from datetime import timedelta
from typing import Annotated, assert_never

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart, or_f
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InaccessibleMessage, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aioinject import Inject, inject
from result import Err

from adapters.telegram.middlewares.aioinject_ import (
    AioinjectMiddlware,
    CallbackAioinjectMiddleware,
)
from adapters.telegram.middlewares.current_user import (
    CallbackCurrentUserMiddleware,
    ChatCurrentUserMiddleware,
)
from adapters.telegram.states import GroupSelectionState
from core.domain.educational_level.queries.get_all import GetAllEducationalLevelsQuery
from core.domain.group.dtos import GetGroupsByEducationalLevelDto
from core.domain.group.queries.get_by_educational_level import (
    GetGroupsByEducationalLevelQuery,
)
from core.domain.lesson.dtos import GetLessonsReportDto
from core.domain.lesson.queries.lessons_report import LessonsReportQuery
from core.domain.lesson.report_renderer import ReportRenderer
from core.domain.user.commands.set_selected_group import SetSelectedGroupCommand
from core.domain.user.dtos import SetSelectedGroupDto
from core.errors import EntityNotFoundError, Never
from core.models.group import GroupId
from core.models.user import User
from di import create_container
from lib.dates import utc_now

dispatcher = Dispatcher()
dispatcher.message.middleware(AioinjectMiddlware(container=create_container()))
dispatcher.callback_query.middleware(
    CallbackAioinjectMiddleware(container=create_container()),
)
dispatcher.message.middleware(ChatCurrentUserMiddleware())
dispatcher.callback_query.middleware(CallbackCurrentUserMiddleware())


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
    query: Annotated[LessonsReportQuery, Inject],
    renderer: Annotated[ReportRenderer, Inject],
    user: User,
) -> None:
    if user.preferences.selected_group is None:
        await bot.send_message(
            message.chat.id,
            "Группа не выбрана",
        )
        return
    current_date = utc_now().date()
    report = await query.execute(
        GetLessonsReportDto(
            group=user.preferences.selected_group,
            start_date=current_date,
            end_date=current_date + timedelta(days=user.preferences.report_days_offset),
        ),
    )
    result = await renderer.render(report)
    await bot.send_message(message.chat.id, result, parse_mode="HTML")


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
    builder = InlineKeyboardBuilder()
    for group in groups:
        builder.button(text=group.title, callback_data=str(group.id))
    builder.adjust(2)
    if callback.message is None:
        raise Never

    if isinstance(callback.message, InaccessibleMessage):
        return

    await callback.message.answer(
        "Выберите одну из групп",
        reply_markup=builder.as_markup(),
    )


@dispatcher.callback_query(GroupSelectionState.group_selection)
@inject
async def handle_group_selection(
    callback: CallbackQuery,
    state: FSMContext,
    command: Annotated[SetSelectedGroupCommand, Inject],
    user: User,
) -> None:
    result = await command.execute(
        SetSelectedGroupDto(
            group_id=GroupId(uuid.UUID(callback.data)),
            user=user,
        ),
    )
    if isinstance(result, Err):
        err = result.err_value
        match err:
            case EntityNotFoundError():
                await callback.answer(
                    "Не удалось найти выбранную группу...",
                    show_alert=True,
                )
                return
            case _ as never:
                assert_never(never)
    group = result.ok_value
    await state.clear()
    await callback.answer(f"Группа {group.title} успешно выбрана")
