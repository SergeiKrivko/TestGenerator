import json
import os

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QTabBar

from code_tab.preview_widgets import PreviewWidget
from code_tab.search_panel import SearchPanel
from language.languages import languages
from code_tab.syntax_highlighter import CodeEditor
from ui.button import Button
from ui.side_bar import SidePanel, SideBar
from tests.convert_binary import convert


class CodeWidget(QWidget):
    testing_signal = pyqtSignal()

    def __init__(self, sm, cm, tm, side_bar: SideBar, side_panel: SidePanel):
        super(CodeWidget, self).__init__()
        self.sm = sm
        self.cm = cm
        self.tm = tm
        self.side_bar = side_bar
        self.side_panel = side_panel
        self.current_file = ''

        self.sm.finish_change_task.connect(self.first_open)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        self.setLayout(main_layout)

        self.top_panel = TopPanelWidget(self.sm, self.tm)
        self.top_panel.tabSelected.connect(self.select_tab)
        self.top_panel.tabClosed.connect(self.close_tab)
        self.top_panel.tab_bar.tabMoved.connect(self.move_tab)
        self.top_panel.button_run.clicked.connect(self.run_file)
        self.top_panel.button_preview.clicked.connect(self.show_preview)
        main_layout.addWidget(self.top_panel)

        self.search_panel = SearchPanel(self.sm, self.tm)
        self.search_panel.hide()
        self.top_panel.button_search.clicked.connect(lambda flag:
                                                     self.search_panel.show() if flag else self.search_panel.hide())
        self.search_panel.selectText.connect(self.select_text)
        self.search_panel.button_replace.clicked.connect(self.replace)
        self.search_panel.button_replace_all.clicked.connect(self.replace_all)
        main_layout.addWidget(self.search_panel)

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addLayout(self.layout)

        self.files_widget = self.side_panel.tabs['files']

        self.files_widget.openFile.connect(self.open_code)
        self.files_widget.renameFile.connect(self.rename_file)

        self.files = []
        self.code_widgets = dict()
        self.preview_widgets = dict()
        self.buttons = dict()

        self.empty_widget = QWidget()
        self.layout.addWidget(self.empty_widget)

        self.path = ''
        self.test_count = 0
        self.file_update_time = 0

    def get_path(self):
        self.path = self.sm.lab_path()

    def rename_file(self, name):
        self.current_file = name

    def first_open(self):
        if self.sm.project not in self.sm.projects:
            return
        self.files_widget.open_task()

        self.top_panel.clear()
        for el in self.code_widgets.values():
            el.setParent(None)
        self.code_widgets.clear()
        for el in self.preview_widgets.values():
            el.setParent(None)
        self.preview_widgets.clear()
        self.files.clear()

        files = self.load_files_list()
        if not files:
            self.empty_widget.show()
        else:
            for el in files:
                self.open_code(el)

    def load_files_list(self):
        try:
            with open(f"{self.sm.data_lab_path()}/files.json", encoding='utf-8') as f:
                lst = json.loads(f.read())
                if not isinstance(lst, list):
                    lst = []
                return lst
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            return []

    def save_files_list(self):
        path = self.sm.data_lab_path()
        os.makedirs(path, exist_ok=True)
        with open(f"{self.sm.data_lab_path()}/files.json", 'w', encoding='utf-8') as f:
            f.write(json.dumps(self.files))

    def update_todo(self):
        pass

    def jump_by_todo(self):
        item = 0
        for i in range(self.files_widget.files_list.count()):
            if self.files_widget.files_list.item(i).text() == item.path:
                self.files_widget.files_list.setCurrentRow(i)
                self.code_edit.setCursorPosition(item.line, 0)
                break

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
        elif self.buttons[path] == 2:
            self.top_panel.button_run.hide()
            self.top_panel.button_preview.show()
            self.top_panel.button_preview.setChecked(False)
        else:
            self.top_panel.button_run.hide()
            self.top_panel.button_preview.hide()

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

    def open_code(self, path):
        if path in self.code_widgets or path in self.preview_widgets:
            self.top_panel.select_tab(path)
            return
        if not os.path.isfile(path):
            return
        self.get_path()
        self.files.append(path)
        self.save_files_list()
        self.buttons[path] = 0

        for language in languages.values():
            for el in language['files']:
                if path.endswith(el):
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
                    elif language.get('fast_run', False):
                        self.buttons[path] = 1
                    self.top_panel.open_tab(path)
                    return
        code_edit = CodeEditor(self.sm, self.tm, path=path)
        code_edit.hide()
        self.layout.addWidget(code_edit)
        code_edit.set_theme()
        self.code_widgets[path] = code_edit
        self.top_panel.open_tab(path)

    def show_preview(self, flag):
        if flag:
            self.code_widgets[self.current_file].hide()
            self.preview_widgets[self.current_file].show()
        else:
            self.code_widgets[self.current_file].show()
            self.preview_widgets[self.current_file].hide()

    def run_file(self):
        if self.current_file.endswith('.t2b'):
            convert(in_path=self.current_file)
            self.files_widget.update_files_list()
        else:
            self.side_panel.tabs['run'].run_file(self.current_file)
            self.side_bar.select_tab('run')

    def parse_gcov_file(self):
        path = self.current_file + '.gcov'

        if os.path.isfile(path):
            file = open(path, encoding='utf-8')
            i = 0
            for line in file:
                line = line.split(':')
                if int(line[1]) > 0:
                    i += 1
                    if line[0].startswith('#'):
                        line[0] = '0'
                    self.code_edit.setMarginLineNumbers(i, False)
                    self.code_edit.setMarginText(i, f"{line[0].strip():3} {line[1].strip():3}", 0)

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
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setContentsMargins(0, 0, 5, 1)
        main_layout.setSpacing(5)
        strange_widget.setLayout(main_layout)

        self.tab_bar = QTabBar()
        self.tab_bar.currentChanged.connect(self.tab_selected)
        self.tab_bar.tabCloseRequested.connect(self.tab_closed)
        self.tab_bar.tabMoved.connect(self.tab_moved)
        self.tab_bar.setMovable(True)
        self.tab_bar.setTabsClosable(True)
        main_layout.addWidget(self.tab_bar, 100, Qt.AlignLeft)

        self.button_search = Button(self.tm, 'search', css='Bg', tooltip='Поиск')
        self.button_search.setFixedSize(20, 20)
        self.button_search.setCheckable(True)
        main_layout.addWidget(self.button_search, 1, Qt.AlignRight)

        self.button_run = Button(self.tm, 'run', css='Bg', tooltip='Запустить')
        self.button_run.setFixedSize(20, 20)
        main_layout.addWidget(self.button_run, 1, Qt.AlignRight)

        self.button_preview = Button(self.tm, 'button_preview', css='Bg', tooltip='Предпросмотр')
        self.button_preview.setFixedSize(20, 20)
        self.button_preview.setCheckable(True)
        main_layout.addWidget(self.button_preview, 1, Qt.AlignRight)

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
            file_type = 'unknown_file'
        self.tab_bar.addTab(QIcon(self.tm.get_image(file_type, 'unknown_file')), name)
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
    image: url({self.tm.get_image('button_close_tab')});
}}
QTabBar::close-button:hover {{
    image: url({self.tm.get_image('button_close_tab_hover')});
}}
""")
        self.button_run.set_theme()
        self.button_preview.set_theme()
        self.button_search.set_theme()
        for i, el in enumerate(self.tabs):
            name = os.path.basename(el)
            if '.' in name and (ind := name.rindex('.')):
                file_type = name[ind + 1:]
            else:
                file_type = 'unknown_file'
            self.tab_bar.setTabIcon(i, QIcon(self.tm.get_image(file_type, 'unknown_file')))
