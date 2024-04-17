import asyncio
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

from adapters.telegram.context import GroupSelectionContext
from adapters.telegram.middlewares.aioinject_ import (
    AioinjectMiddleware,
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
from core.domain.group.queries.get_groups_by_title import SearchGroupsByTitleQuery
from core.domain.lesson.dtos import GetLessonsReportDto
from core.domain.lesson.queries.lessons_report import LessonsReportQuery
from core.domain.lesson.report_renderer import ReportRenderer
from core.domain.user.commands.set_selected_group import SetSelectedGroupCommand
from core.domain.user.dtos import SetSelectedGroupDto
from core.errors import EntityNotFoundError, Never
from core.models.educational_level import EducationalLevelId
from core.models.group import GroupId
from core.models.user import User
from di import create_container
from lib.dates import utc_now

dispatcher = Dispatcher()
dispatcher.message.middleware(AioinjectMiddleware(container=create_container()))
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
) -> None:
    builder = ReplyKeyboardBuilder()
    builder.button(text="Показать расписание")
    builder.button(text="Выбрать группу")
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
        await bot.send_message(message.chat.id, "Группа не выбрана")
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
    level_id = EducationalLevelId(uuid.UUID(callback.data))
    groups = await query.execute(GetGroupsByEducationalLevelDto(level_id=level_id))
    if len(groups) == 0:
        await callback.answer(
            "Не удалось найти ни одной группы...",
            show_alert=True,
        )
        return
    builder = InlineKeyboardBuilder()
    for group in groups:
        builder.button(text=group.title, callback_data=str(group.id))
    builder.adjust(2)
    if callback.message is None:
        raise Never

    if isinstance(callback.message, InaccessibleMessage):
        return

    reply_message = await callback.message.answer(
        "Выберите одну из групп\nЕсли отправить сообщение с названием группы, то я постараюсь ее найти",
        reply_markup=builder.as_markup(),
    )
    if isinstance(callback.message, Message):
        await callback.message.delete()
    await asyncio.gather(
        state.set_state(GroupSelectionState.group_selection),
        state.set_data(
            GroupSelectionContext(
                before_group_search_message_id=reply_message.message_id,
                educational_level_id=level_id,
            ).model_dump(mode="python"),
        ),
    )


@dispatcher.callback_query(GroupSelectionState.group_selection)
@inject
async def handle_group_clicked_callback(
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
    if isinstance(callback.message, Message):
        await callback.message.delete()


@dispatcher.message(GroupSelectionState.group_selection)
@inject
async def handle_group_search_message(
    message: Message,
    state: FSMContext,
    query: Annotated[SearchGroupsByTitleQuery, Inject],
    bot: Annotated[Bot, Inject],
) -> None:
    context_data = GroupSelectionContext.model_validate(await state.get_data())
    groups = await query.execute(search_term=message.text or "", level_id=context_data.educational_level_id)

    if len(groups) == 0:
        await message.answer(
            "Не удалось найти ни одной группы...",
            show_alert=True,
        )
        return

    builder = InlineKeyboardBuilder()
    for group in groups:
        builder.button(text=group.title, callback_data=str(group.id))
    builder.adjust(2)

    reply_message = await message.answer(
        "Выберите одну из групп\nЕсли отправить сообщение с названием группы, то я постараюсь ее найти",
        reply_markup=builder.as_markup(),
    )

    await state.set_data(
        GroupSelectionContext(
            before_group_search_message_id=reply_message.message_id,
            educational_level_id=context_data.educational_level_id,
        ).model_dump(mode="python"),
    )

    if context_data.before_group_search_message_id is not None:
        await bot.delete_message(
            message.chat.id,
            message_id=context_data.before_group_search_message_id,
        )
