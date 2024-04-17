from datetime import timedelta
from typing import Annotated

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart, or_f
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aioinject import Inject, inject

from adapters.telegram.controllers.group_selection_controller import (
    GroupSelectionController,
)
from adapters.telegram.middlewares.aioinject_ import (
    AioinjectMiddleware,
    CallbackAioinjectMiddleware,
)
from adapters.telegram.middlewares.current_user import (
    CallbackCurrentUserMiddleware,
    ChatCurrentUserMiddleware,
)
from adapters.telegram.states import GroupSelectionState
from core.domain.lesson.dtos import GetLessonsReportDto
from core.domain.lesson.queries.lessons_report import LessonsReportQuery
from core.domain.lesson.report_renderer import ReportRenderer
from core.models.user import User
from di import create_container
from lib.dates import utc_now

dispatcher = Dispatcher()
dispatcher.message.middleware(AioinjectMiddleware(container=create_container()))
dispatcher.callback_query.middleware(CallbackAioinjectMiddleware(container=create_container()))
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
        batch_size=10,
    )
    result = await renderer.render(report)
    for msg in result:
        await bot.send_message(message.chat.id, msg, parse_mode="HTML")


@dispatcher.message(or_f(F.text == "Выбрать группу", Command("/set_group")))
@inject
async def handle_set_group(
    message: Message,
    state: FSMContext,
    controller: Annotated[GroupSelectionController, Inject],
) -> None:
    await controller.offer_educational_level_selection(message=message, state=state)


@dispatcher.callback_query(GroupSelectionState.educational_level_selection)
@inject
async def handle_educational_level_selection(
    callback: CallbackQuery,
    state: FSMContext,
    controller: Annotated[GroupSelectionController, Inject],
) -> None:
    await controller.select_educational_level(callback=callback, state=state)


@dispatcher.callback_query(GroupSelectionState.group_selection)
@inject
async def handle_group_clicked_callback(
    callback: CallbackQuery,
    state: FSMContext,
    user: User,
    controller: Annotated[GroupSelectionController, Inject],
) -> None:
    await controller.set_selected_group(callback=callback, state=state, user=user)


@dispatcher.message(GroupSelectionState.group_selection)
@inject
async def handle_group_search_message(
    message: Message,
    state: FSMContext,
    controller: Annotated[GroupSelectionController, Inject],
) -> None:
    await controller.search_groups(message=message, state=state)
