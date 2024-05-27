from PyQt6.QtCore import Qt, pyqtSignal
from PyQtUIkit.widgets import *


class SearchPanel(KitVBoxLayout):
    textSearched = pyqtSignal(int, int, int, int)

    def __init__(self, editor: KitScintilla):
        super().__init__()

        self._editor = editor
        self._editor.textChanged.connect(self._on_text_edited)

        self._lines = []
        self._results = []
        self.__replacing = False

        main_layout = KitHBoxLayout()
        self.addWidget(main_layout)

        line_edit_layout = KitVBoxLayout()
        line_edit_layout.setContentsMargins(0, 0, 0, 0)
        line_edit_layout.setSpacing(0)
        line_edit_layout.setMaximumWidth(400)
        main_layout.addWidget(line_edit_layout)

        self.search_line_edit = KitLineEdit()
        self.search_line_edit.setFixedHeight(30)
        self.search_line_edit.border = 0
        self.search_line_edit.main_palette = 'Bg'
        self.search_line_edit.font = 'mono'
        self.search_line_edit.radius = 0
        self.search_line_edit.on_text_changed = self._search_all
        line_edit_layout.addWidget(self.search_line_edit)

        line_edit_layout.addWidget(KitHSeparator())

        self.replace_line_edit = KitLineEdit()
        self.replace_line_edit.setFixedHeight(30)
        self.replace_line_edit.border = 0
        self.replace_line_edit.main_palette = 'Bg'
        self.replace_line_edit.font = 'mono'
        self.replace_line_edit.radius = 0
        line_edit_layout.addWidget(self.replace_line_edit)

        main_layout.addWidget(KitVSeparator())

        right_layout = KitVBoxLayout()
        right_layout.spacing = 3
        right_layout.setContentsMargins(8, 3, 8, 3)
        main_layout.addWidget(right_layout)

        top_layout = KitHBoxLayout()
        top_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        top_layout.spacing = 6
        right_layout.addWidget(top_layout)

        self.label = KitLabel()
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        top_layout.addWidget(self.label)
        self.label.setFixedWidth(120)

        self.button_up = KitIconButton('line-arrow-up')
        self.button_up.border = 0
        self.button_up.main_palette = 'Bg'
        self.button_up.size = 22
        self.button_up.on_click = self.search_previous
        top_layout.addWidget(self.button_up)

        self.button_down = KitIconButton('line-arrow-down')
        self.button_down.border = 0
        self.button_down.main_palette = 'Bg'
        self.button_down.size = 22
        self.button_down.on_click = self.search_next
        top_layout.addWidget(self.button_down)

        bottom_layout = KitHBoxLayout()
        bottom_layout.spacing = 6
        bottom_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        right_layout.addWidget(bottom_layout)

        self.button_replace = KitButton("Заменить")
        self.button_replace.main_palette = 'Bg'
        self.button_replace.on_click = self._replace
        bottom_layout.addWidget(self.button_replace)

        self.button_replace_all = KitButton("Заменить все")
        self.button_replace_all.main_palette = 'Bg'
        self.button_replace_all.on_click = self._replace_all
        bottom_layout.addWidget(self.button_replace_all)

        self.addWidget(KitHSeparator())

        self._on_text_edited()

    def _on_text_edited(self):
        text = self._editor.text()
        self._lines.clear()
        length = 0
        for line in text.split('\n'):
            self._lines.append(length)
            length += len(line) + 1
        self._search_all()

    def _search_all(self):
        if self.__replacing:
            return
        word = self.search_line_edit.text
        self._results.clear()
        if not word:
            return
        text = self._editor.text()
        length = 0
        while True:
            try:
                index = text.index(word)
            except ValueError:
                break
            length += index
            self._results.append(length)
            length += len(word)
            text = text[index + len(word):]
        self.search_any()

    def _line_to_pos(self, line, pos):
        return self._lines[line] + pos

    def _pos_to_line(self, pos):
        i = 0
        while pos > self._lines[i + 1]:
            i += 1
        return i, pos - self._lines[i]

    def search_any(self):
        word = self.search_line_edit.text
        cursor_pos = self._current_pos()
        for i, res in enumerate(self._results):
            if res >= cursor_pos:
                self._editor.setSelection(*self._pos_to_line(res), *self._pos_to_line(res + len(word)))
                self.update_label(i)
                return True
        if not self.search_previous():
            self.update_label()
        
    def search_next(self):
        word = self.search_line_edit.text
        cursor_pos = self._current_pos() + 1
        for i, res in enumerate(self._results):
            if res >= cursor_pos:
                self._editor.setSelection(*self._pos_to_line(res), *self._pos_to_line(res + len(word)))
                self.update_label(i)
                return True
        return False

    def search_previous(self):
        word = self.search_line_edit.text
        cursor_pos = self._current_pos() - 1
        for i, res in enumerate(reversed(self._results)):
            if res < cursor_pos:
                self._select_text(res, res + len(word))
                self.update_label(len(self._results) - i - 1)
                return True
        return False

    def _current_pos(self):
        if self._editor.hasSelectedText():
            l, p, _, _ = self._editor.getSelection()
        else:
            l, p = self._editor.getCursorPosition()
        return self._line_to_pos(l, p)

    def _select_text(self, pos1, pos2):
        self._editor.setSelection(*self._pos_to_line(pos1), *self._pos_to_line(pos2))

    def update_label(self, index=0):
        if not self._results:
            self.label.text = "Нет результатов"
            self.label.main_palette = 'Danger'
            self.label._apply_theme()
        else:
            self.label.text = f"{index + 1} / {len(self._results)}"
            self.label.main_palette = 'Main'
            self.label._apply_theme()

    def _replace(self):
        word = self.search_line_edit.text
        new_word = self.replace_line_edit.text
        if word and new_word and self._editor.selectedText() == word:
            self.__replacing = True
            self._editor.replaceSelectedText(new_word)
            self.__replacing = False
            self._search_all()

    def _replace_all(self):
        word = self.search_line_edit.text
        new_word = self.replace_line_edit.text
        if word and new_word:
            text = self._editor.text().replace(word, new_word)
            self._editor.setText(text)

    def search(self, word):
        self.search_line_edit.text = word
