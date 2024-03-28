from collections.abc import Iterable
from typing import Any

import aioinject

from core.domain.user.commands.get_or_create_user import GetOrCreateUserCommand
from core.domain.user.commands.set_selected_group import SetSelectedGroupCommand

providers: Iterable[aioinject.Provider[Any]] = [
    aioinject.Scoped(GetOrCreateUserCommand),
    aioinject.Scoped(SetSelectedGroupCommand),
]
