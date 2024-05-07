from enum import Enum
from typing import Type, Callable

from PyQtUIkit.themes.languages import _languages, _names, _Language

from src.backend.language.autocomplition.abstract import CodeAutocompletionManager as AcMAbstract


class Language:
    class PreviewType(Enum):
        NONE = 0
        SIMPLE = 1
        ACTIVE = 2
        ONLY = 3

    def __init__(self,
                 name: str,
                 extensions: list,
                 icon: str,
                 kit_language: str | tuple[Type, dict[str: str]] = None,
                 autocompletion: Type = AcMAbstract,
                 fast_run: list[tuple[str, str, Callable]] = None,
                 preview=PreviewType.NONE):
        self.name = name
        self.icon = icon
        if isinstance(kit_language, tuple):
            lang = _Language(name, extensions, kit_language[0], kit_language[1])
            _languages[name] = lang
            _names[name] = lang
            self.kit_language = name
        else:
            self.kit_language = name if kit_language is None else kit_language
        self.extensions = extensions
        self.autocompletion = autocompletion
        self.fast_run = fast_run or []
        self.preview = preview
