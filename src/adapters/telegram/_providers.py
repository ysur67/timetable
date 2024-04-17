from typing import Any

import aioinject

from adapters.telegram.controllers.group_selection_controller import (
    GroupSelectionController,
)

providers: list[aioinject.Provider[Any]] = [aioinject.Scoped(GroupSelectionController)]
