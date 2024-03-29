import os
import platform
import subprocess

from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QTabBar, QFileDialog, QLabel, QComboBox, QCheckBox, \
    QPushButton

from src.backend.commands import is_text_file
from src.backend.managers import BackendManager
from src.backend.settings_manager import SettingsManager
from src.language.languages import languages
from src.main_tabs.code_tab.preview_widgets import PreviewWidget
from src.main_tabs.code_tab.search_panel import SearchPanel
from src.main_tabs.code_tab.syntax_highlighter import CodeEditor
from src.ui.button import Button
from src.ui.custom_dialog import CustomDialog
from src.ui.main_tab import MainTab


class CodeWidget(MainTab):
    testing_signal = pyqtSignal()

    def __init__(self, sm: SettingsManager, bm: BackendManager, tm):
        super(CodeWidget, self).__init__()
        self.sm = sm
        self.bm = bm
        self.tm = tm
        self.current_file = ''

        self.bm.finishChangingProject.connect(self.first_open)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        self.setLayout(main_layout)

        self.top_panel = TopPanelWidget(self.sm, self.tm)
        self.top_panel.tabSelected.connect(self.select_tab)
        self.top_panel.tabClosed.connect(self.close_tab)
        self.top_panel.tab_bar.tabMoved.connect(self.move_tab)
        # self.top_panel.button_run.clicked.connect(self.run_file)
        self.top_panel.button_preview.clicked.connect(self.show_preview)
        main_layout.addWidget(self.top_panel)

        self.search_panel = SearchPanel(self.sm, self.tm)
        self.search_panel.hide()
        self.top_panel.button_open.clicked.connect(self.open_non_project_file)
        self.top_panel.button_search.clicked.connect(lambda flag:
                                                     self.search_panel.show() if flag else self.search_panel.hide())
        self.search_panel.selectText.connect(self.select_text)
        self.search_panel.button_replace.clicked.connect(self.replace)
        self.search_panel.button_replace_all.clicked.connect(self.replace_all)
        main_layout.addWidget(self.search_panel)

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addLayout(self.layout)

        self.files = []
        self.code_widgets = dict()
        self.preview_widgets = dict()
        self.buttons = dict()

        self.empty_widget = QWidget()
        self.layout.addWidget(self.empty_widget)

        self.test_count = 0
        self.file_update_time = 0

    def rename_file(self, name):
        self.current_file = name

    def command(self, file, *args, **kwargs):
        if len(args) >= 2:
            self.open_code(file, args[0], args[1])
        else:
            self.open_code(file)

    def first_open(self):
        if self.sm.project.path() not in self.sm.all_projects:
            return

        self.top_panel.clear()
        for el in self.code_widgets.values():
            el.setParent(None)
        self.code_widgets.clear()
        for el in self.preview_widgets.values():
            el.setParent(None)
        self.preview_widgets.clear()
        self.files.clear()

        self.files = self.sm.get('opened_files', [])
        if not self.files:
            self.empty_widget.show()
        else:
            for el in self.files:
                self.open_code(el)

    def save_files_list(self):
        self.sm.set('opened_files', list(set(self.files)))

    def update_todo(self):
        pass

    def select_tab(self, path):
        self.empty_widget.hide()
        for el in self.code_widgets.values():
            el.hide()
        for el in self.preview_widgets.values():
            el.hide()
        if path in self.code_widgets:
            self.code_widgets[path].show()
        elif path in self.preview_widgets:
            self.preview_widgets[path].show()
        else:
            self.empty_widget.show()
        self.current_file = path
        self._on_text_changed()

        if self.buttons[path] == 1:
            self.top_panel.button_preview.hide()
            self.top_panel.button_run.show()
        elif self.buttons[path] in [2, 3]:
            self.top_panel.button_run.hide()
            self.top_panel.button_preview.show()
            if self.buttons[path] == 3:
                self.top_panel.button_preview.setChecked(True)
                self.code_widgets[path].hide()
                self.preview_widgets[path].show()
            else:
                self.top_panel.button_preview.setChecked(False)
        else:
            self.top_panel.button_run.hide()
            self.top_panel.button_preview.hide()
        if self.current_file in self.code_widgets:
            self.top_panel.button_search.show()
        else:
            self.top_panel.button_search.hide()

    def move_tab(self, ind1, ind2):
        self.files[ind1], self.files[ind2] = self.files[ind2], self.files[ind1]
        self.save_files_list()

    def close_tab(self, path):
        if path in self.code_widgets:
            self.code_widgets[path].setParent(None)
            self.code_widgets.pop(path)
        if path in self.preview_widgets:
            self.preview_widgets[path].setParent(None)
            self.preview_widgets.pop(path)
        if path in self.files:
            self.files.remove(path)
            self.save_files_list()
        if path == self.current_file:
            self.empty_widget.show()
            self.top_panel.button_run.hide()
            self.top_panel.button_preview.hide()
            self.current_file = ""

    def open_non_project_file(self):
        path = QFileDialog.getOpenFileName(caption="Выберите файл", directory=self.sm.project.path())[0]
        if os.path.isfile(path):
            self.open_code(path)

    def open_code(self, path, line=None, pos=None, flags=None):
        path = os.path.abspath(path)
        if pos is None:
            pos = 0
        if path in self.code_widgets or path in self.preview_widgets:
            self.top_panel.select_tab(path)
            if line is not None and self.current_file in self.code_widgets:
                self.code_widgets[self.current_file].setCursorPosition(line - 1, pos - 1)
            return
        if not os.path.isfile(path):
            return
        self.buttons[path] = 0

        for language in languages.values():
            if not language.get('open_files', True):
                continue
            for el in language['files']:
                if path.endswith(el):
                    self._open_file_with_language(path, language)
                    return

        if is_text_file(path):
            self._open_file_with_language(path, languages['txt'])
        else:
            self.open_by_system(path)

    def _open_file_with_language(self, path, language):
        self.files.append(path)
        self.save_files_list()
        if 'lexer' in language:
            code_edit = CodeEditor(self.sm, self.tm, path=path)
            code_edit.hide()
            code_edit.textChanged.connect(self._on_text_changed)
            code_edit.cursorPositionChanged.connect(self._on_pos_changed)
            self.layout.addWidget(code_edit)
            code_edit.set_theme()
            self.code_widgets[path] = code_edit
        if language.get('preview', False):
            preview_widget = PreviewWidget(self.sm, self.tm, path)
            preview_widget.hide()
            self.layout.addWidget(preview_widget)
            preview_widget.set_theme()
            self.preview_widgets[path] = preview_widget
            self.buttons[path] = 2 if 'lexer' in language else 0
            if language.get('show_preview', False):
                self.buttons[path] = 3
        elif language.get('fast_run', False):
            self.buttons[path] = 1
        self.top_panel.open_tab(path)

    @staticmethod
    def open_by_system(filepath):
        if platform.system() == 'Darwin':  # macOS
            subprocess.call(('open', filepath))
        elif platform.system() == 'Windows':  # Windows
            os.startfile(filepath)
        else:  # linux variants
            subprocess.call(('xdg-open', filepath))

    def show_preview(self, flag):
        if flag:
            self.code_widgets[self.current_file].hide()
            self.preview_widgets[self.current_file].show()
        else:
            self.code_widgets[self.current_file].show()
            self.preview_widgets[self.current_file].hide()

    def select_text(self, a, b, c, d):
        if self.current_file in self.code_widgets:
            self.code_widgets[self.current_file].setSelection(a, b, c, d)

    def _on_text_changed(self):
        if self.current_file in self.code_widgets:
            self.search_panel.text = self.code_widgets[self.current_file].text()

    def _on_pos_changed(self):
        if self.current_file in self.code_widgets:
            self.search_panel.pos = self.code_widgets[self.current_file].getCursorPosition()

    def replace(self):
        if self.current_file in self.code_widgets:
            code_edit = self.code_widgets[self.current_file]
            if code_edit.selectedText() == self.search_panel.search_line_edit.text():
                code_edit.replaceSelectedText(self.search_panel.replace_line_edit.text())
                if not self.search_panel.search_next():
                    self.search_panel.search_previous()

    def replace_all(self):
        if self.current_file in self.code_widgets:
            code_edit = self.code_widgets[self.current_file]
            code_edit.setText(code_edit.text().replace(self.search_panel.search_line_edit.text(),
                                                       self.search_panel.replace_line_edit.text()))

    def set_theme(self):
        for el in self.code_widgets.values():
            el.set_theme()
        for el in self.preview_widgets.values():
            el.set_theme()
        self.search_panel.set_theme()
        self.top_panel.set_theme()


class TopPanelWidget(QWidget):
    tabSelected = pyqtSignal(str)
    tabClosed = pyqtSignal(str)

    def __init__(self, sm, tm):
        super().__init__()
        self.sm = sm
        self.tm = tm
        self.setFixedHeight(27)

        strange_layout = QVBoxLayout()
        strange_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(strange_layout)
        strange_widget = QWidget()
        strange_layout.addWidget(strange_widget)

        main_layout = QHBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.setContentsMargins(0, 0, 5, 1)
        main_layout.setSpacing(5)
        strange_widget.setLayout(main_layout)

        self.tab_bar = QTabBar()
        self.tab_bar.currentChanged.connect(self.tab_selected)
        self.tab_bar.tabCloseRequested.connect(self.tab_closed)
        self.tab_bar.tabMoved.connect(self.tab_moved)
        self.tab_bar.setMovable(True)
        self.tab_bar.setTabsClosable(True)
        main_layout.addWidget(self.tab_bar, 1000, Qt.AlignmentFlag.AlignLeft)

        self.button_open = Button(self.tm, 'buttons/plus', css='Bg', tooltip='Открыть файл')
        self.button_open.setFixedSize(20, 20)
        main_layout.addWidget(self.button_open, 1, Qt.AlignmentFlag.AlignLeft)

        self.button_search = Button(self.tm, 'buttons/search', css='Bg', tooltip='Поиск')
        self.button_search.setFixedSize(20, 20)
        self.button_search.setCheckable(True)
        main_layout.addWidget(self.button_search, 1, Qt.AlignmentFlag.AlignRight)

        self.button_run = Button(self.tm, 'buttons/run', css='Bg', tooltip='Запустить')
        self.button_run.setFixedSize(20, 20)
        main_layout.addWidget(self.button_run, 1, Qt.AlignmentFlag.AlignRight)

        self.button_preview = Button(self.tm, 'buttons/button_preview', css='Bg', tooltip='Предпросмотр')
        self.button_preview.setFixedSize(20, 20)
        self.button_preview.setCheckable(True)
        main_layout.addWidget(self.button_preview, 1, Qt.AlignmentFlag.AlignRight)

        self.tabs = []

    def tab_selected(self, ind):
        try:
            self.tabSelected.emit(self.tabs[ind])
        except IndexError:
            pass

    def select_tab(self, path):
        if path not in self.tabs:
            return
        self.tab_bar.setCurrentIndex(self.tabs.index(path))

    def tab_closed(self, ind):
        try:
            self.tab_bar.removeTab(ind)
            self.tabClosed.emit(self.tabs[ind])
            self.tabs.pop(ind)
            self.tabSelected.emit(self.tabs[self.tab_bar.currentIndex()])
        except IndexError:
            pass

    def tab_moved(self, ind1, ind2):
        self.tabs[ind1], self.tabs[ind2] = self.tabs[ind2], self.tabs[ind1]

    def open_tab(self, path):
        name = os.path.basename(path)
        if '.' in name and (ind := name.rindex('.')):
            file_type = name[ind + 1:]
        else:
            file_type = 'icons/unknown_file'
        self.tab_bar.addTab(QIcon(self.tm.get_image('files/' + file_type, 'icons/unknown_file')), name)
        self.tabs.append(path)
        self.tab_bar.setCurrentIndex(self.tab_bar.count() - 1)
        self.tabSelected.emit(path)

    def clear(self):
        for i in range(self.tab_bar.count() - 1, -1, -1):
            self.tab_bar.removeTab(i)
        self.tabs.clear()

    def set_theme(self):
        self.setStyleSheet(f"background-color: {self.tm['BgColor']};"
                           f"border-bottom: 1px solid {self.tm['BorderColor']};")
        self.tab_bar.setStyleSheet(f"""
QTabBar:tab {{
color: {self.tm['TextColor']};
background-color: {self.tm['BgColor']};
border-radius: 0px;
min-width: 8ex;
padding: 5px;
}}
QTabBar:tab:hover {{
background-color: {self.tm['BgHoverColor']};
}}
QTabBar:tab:selected {{
background-color: {self.tm['BgSelectedColor']};
}}
QTabBar::close-button {{
    image: url({self.tm.get_image('buttons/button_close_tab')});
}}
QTabBar::close-button:hover {{
    image: url({self.tm.get_image('buttons/button_close_tab_hover')});
}}
QTabBar QToolButton {{
    background-color: {self.tm['BgColor']};
    border: 0px solid {self.tm['BorderColor']};
}}
QTabBar QToolButton::hover {{
    background-color: {self.tm['BgHoverColor']};
}}
QTabBar QToolButton::right-arrow {{
    image: url({self.tm.get_image('buttons/right_arrow')});
}}
QTabBar QToolButton::left-arrow {{
    image: url({self.tm.get_image('buttons/left_arrow')});
}}
""")
        self.button_open.set_theme()
        self.button_run.set_theme()
        self.button_preview.set_theme()
        self.button_search.set_theme()
        for i, el in enumerate(self.tabs):
            name = os.path.basename(el)
            if '.' in name and (ind := name.rindex('.')):
                file_type = name[ind + 1:]
            else:
                file_type = 'icons/unknown_file'
            self.tab_bar.setTabIcon(i, QIcon(self.tm.get_image(file_type, 'icons/unknown_file')))


class UnknownFileDialog(CustomDialog):
    def __init__(self, tm, path):
        super().__init__(tm, "Неизвестный файл", True, True)
        self.setFixedSize(300, 200)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self._label = QLabel(f"Файл {os.path.basename(path)} имеет неизвестное расширение и, не может быть открыт, "
                             f"так как не является текстовым файлом или имеет другую кодировку. "
                             f"Выберите, что делать с этим файлом")
        self._label.setWordWrap(True)
        layout.addWidget(self._label)

        self._combo_box = QComboBox()
        self._combo_box.addItems(['Открыть системным приложением', 'Выбрать другую кодировку'])
        self._combo_box.currentIndexChanged.connect(
            lambda ind: self._encoding_box.hide() if ind != 1 else self._encoding_box.show())
        layout.addWidget(self._combo_box)

        self._encoding_box = QComboBox()
        self._encoding_box.hide()
        self._encoding_box.addItems(['utf-8', 'utf-16'])
        layout.addWidget(self._encoding_box)

        self._checkbox = QCheckBox()
        self._checkbox.setText("Для всех файлов такого типа")
        layout.addWidget(self._checkbox)

        buttons_layout = QHBoxLayout()
        buttons_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        layout.addLayout(buttons_layout)

        self._button_ok = QPushButton("Ок")
        self._button_ok.setFixedSize(80, 24)
        self._button_ok.clicked.connect(self.accept)
        buttons_layout.addWidget(self._button_ok)

    def showEvent(self, a0) -> None:
        super().showEvent(a0)
        self.set_theme()

    def res(self):
        res = dict()
        match self._combo_box.currentIndex():
            case 0:
                res['system_open'] = True
            case 1:
                res['encoding'] = self._encoding_box.currentText()
        return res, self._checkbox.isChecked()

    def set_theme(self):
        super().set_theme()
        for el in [self._checkbox, self._encoding_box, self._label, self._combo_box, self._button_ok]:
            self.tm.auto_css(el)
