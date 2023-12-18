from collections.abc import Iterable
from typing import Any

import aioinject

from core.domain.user.commands.get_or_create_user import GetOrCreateUserCommand

providers: Iterable[aioinject.Provider[Any]] = [
    aioinject.Callable(GetOrCreateUserCommand),
]
