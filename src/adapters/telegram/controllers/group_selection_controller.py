import asyncio
import uuid
from typing import Any, Protocol, assert_never

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InaccessibleMessage, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from result import Err

from adapters.telegram.context import GroupSelectionContext
from adapters.telegram.states import GroupSelectionState
from core.domain.educational_level.queries.get_all import GetAllEducationalLevelsQuery
from core.domain.group.dtos import GetGroupsByEducationalLevelDto
from core.domain.group.queries.get_by_educational_level import (
    GetGroupsByEducationalLevelQuery,
)
from core.domain.group.queries.get_groups_by_title import SearchGroupsByTitleQuery
from core.domain.user.commands.set_selected_group import SetSelectedGroupCommand
from core.domain.user.dtos import SetSelectedGroupDto
from core.errors import EntityNotFoundError, Never
from core.models.educational_level import EducationalLevelId
from core.models.group import GroupId
from core.models.user import User


class SupportsDumpToJsonDict(Protocol):
    def model_dump(self) -> dict[str, Any]: ...


class GroupSelectionController:

    def __init__(  # noqa: PLR0913
        self,
        bot: Bot,
        get_educational_levels_query: GetAllEducationalLevelsQuery,
        get_groups_by_educational_level_query: GetGroupsByEducationalLevelQuery,
        set_selected_group_command: SetSelectedGroupCommand,
        search_groups_query: SearchGroupsByTitleQuery,
    ) -> None:
        self._bot = bot
        self._get_educational_levels_query = get_educational_levels_query
        self._get_groups_by_educational_level_query = get_groups_by_educational_level_query
        self._set_selected_group_command = set_selected_group_command
        self._search_groups_query = search_groups_query

    async def offer_educational_level_selection(self, *, message: Message, state: FSMContext) -> None:
        await state.set_state(GroupSelectionState.educational_level_selection)
        educational_levels = await self._get_educational_levels_query.execute()
        if len(educational_levels) == 0:
            await self._bot.send_message(
                message.chat.id,
                "Не удалось найти уровни образования...",
            )
            return
        builder = InlineKeyboardBuilder()
        for level in educational_levels:
            builder.button(text=level.title.capitalize(), callback_data=str(level.id))
        builder.adjust(1)
        await self._bot.send_message(
            message.chat.id,
            "Выберите один из пунктов",
            reply_markup=builder.as_markup(),
        )

    async def select_educational_level(self, *, callback: CallbackQuery, state: FSMContext) -> None:
        if callback.data is None:
            raise Never
        level_id = EducationalLevelId(uuid.UUID(callback.data))
        groups = await self._get_groups_by_educational_level_query.execute(
            GetGroupsByEducationalLevelDto(level_id=level_id),
        )
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
            self._set_state_context(
                state,
                GroupSelectionContext(
                    before_group_search_message_id=reply_message.message_id,
                    educational_level_id=level_id,
                ),
            ),
        )

    async def search_groups(self, *, message: Message, state: FSMContext) -> None:
        context_data = GroupSelectionContext.model_validate(await state.get_data())
        groups = await self._search_groups_query.execute(
            search_term=message.text or "",
            level_id=context_data.educational_level_id,
        )

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
        await self._set_state_context(
            state,
            GroupSelectionContext(
                before_group_search_message_id=reply_message.message_id,
                educational_level_id=context_data.educational_level_id,
            ),
        )

        if context_data.before_group_search_message_id is not None:
            await self._bot.delete_message(
                message.chat.id,
                message_id=context_data.before_group_search_message_id,
            )

    async def set_selected_group(self, *, callback: CallbackQuery, state: FSMContext, user: User) -> None:
        result = await self._set_selected_group_command.execute(
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

    async def _set_state_context(self, state: FSMContext, context: SupportsDumpToJsonDict) -> None:
        await state.set_data(context.model_dump())
