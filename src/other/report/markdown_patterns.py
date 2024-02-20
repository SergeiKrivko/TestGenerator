from PyQt6.QtWidgets import QVBoxLayout, QPushButton

from src.backend.commands import write_file
from src.config import APP_NAME
from src.ui.custom_dialog import CustomDialog


class MarkdownPatternsDialog(CustomDialog):
    def __init__(self, sm, tm, file):
        super().__init__(tm, "Шаблоны", True, True)
        self._sm = sm
        self._file = file

        layout = QVBoxLayout()
        self.setLayout(layout)
        self._buttons = dict()

        for key, desc, func in [('Empty', "Пустой файл", self._empty_pattern),
                          ('Readme', "Краткое описание проекта", self._readme_pattern),
                          ('Report', "Отчет", self._report_pattern)]:
            button = QPushButton(desc)
            button.setFixedSize(225, 40)
            button.clicked.connect(func)
            layout.addWidget(button)
            self._buttons[key] = button

        self.set_theme()

    def _empty_pattern(self):
        write_file(self._file, "")
        self.accept()

    def _readme_pattern(self):
        write_file(self._file, f"""
[author]: <> ({APP_NAME})

# {self._sm.project.name()}

{self._sm.project.get_data('description', '')}
""")
        self.accept()

    def _report_pattern(self):
        write_file(self._file, f"""
[author]: <> ({APP_NAME})
[page-size]: <> (210 297)

[table-of-content]: <>
[page-break]: <>

# Описание условия задачи

{self._sm.project.get_data('description', '')}

# Техническое задание

## Входные данные

- ???

## Выходные данные

- ???

## Способ обращения

Способ обращения: при запуске программы из консоли входные данные передаются через стандартный поток ввода.

## Аварийные ситуации

- ???

# Описание внутренних структур данных

```{self._sm.get('language', 'C').lower()}
Some code
```

# Описание алгоритма

???

# Тесты

[tests]: <> (EXPECTED_OUTPUT REAL_OUTPUT STATUS)

# Вывод

???

# Контрольные вопросы

1. Вопрос?

    Ответ

2. Вопрос?

    Ответ
""")
        self.accept()

    def set_theme(self):
        super().set_theme()
        for el in self._buttons.values():
            self.tm.auto_css(el)
