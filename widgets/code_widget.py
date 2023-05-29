import os

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QListWidget, QListWidgetItem, QTabWidget

from widgets.files_widget import FilesWidget
from widgets.options_window import OptionsWidget
from widgets.syntax_highlighter import CCodeEditor


class CodeWidget(QWidget):
    testing_signal = pyqtSignal()

    def __init__(self, sm, cm, tm):
        super(CodeWidget, self).__init__()
        self.sm = sm
        self.cm = cm
        self.tm = tm
        self.current_file = ''

        layout = QHBoxLayout()
        self.setLayout(layout)
        layout_left = QVBoxLayout()
        layout.addLayout(layout_left)

        self.options_widget = OptionsWidget({
            'Номер лабы:': {'type': int, 'min': 1},
            'Номер задания:': {'type': int, 'min': 1},
            'Номер варианта:': {'type': int, 'min': -1},
            'Тестировать': {'type': 'button', 'text': 'Тестировать', 'name': OptionsWidget.NAME_SKIP}
        })
        self.options_widget.clicked.connect(self.option_changed)
        layout_left.addWidget(self.options_widget)

        self.test_res_widget = QListWidget()
        self.test_res_widget.setMaximumWidth(200)

        self.files_widget = FilesWidget(self.sm, self.tm)
        self.files_widget.setMaximumWidth(200)

        self.files_widget.openFile.connect(self.open_code)
        self.files_widget.renameFile.connect(self.rename_file)

        self.todo_widget = QListWidget()
        self.todo_widget.setMaximumWidth(200)

        self.tab_widget = QTabWidget()
        self.tab_widget.addTab(self.files_widget, "Файлы")
        self.tab_widget.addTab(self.test_res_widget, "Тесты")
        self.tab_widget.addTab(self.todo_widget, "TODO")
        self.tab_widget.setFixedWidth(190)
        self.todo_widget.doubleClicked.connect(self.jump_by_todo)
        layout_left.addWidget(self.tab_widget)

        self.code_edit = CCodeEditor(sm, tm)
        self.code_edit.textChanged.connect(self.save_code)
        self.code_edit.cursorPositionChanged.connect(self.check_if_code_changed)
        layout.addWidget(self.code_edit)
        self.path = ''
        self.test_count = 0
        self.file_update_time = 0

    def option_changed(self, key):
        if key in ('Номер лабы:', 'Номер задания:'):
            self.sm.set('lab', self.options_widget["Номер лабы:"])
            self.sm.set('task', self.options_widget["Номер задания:"])
            if os.path.isdir(self.sm.lab_path(self.options_widget['Номер лабы:'],
                                              self.options_widget['Номер задания:'], -1)):
                self.options_widget.set_value('Номер варианта:', -1)
            else:
                for i in range(100):
                    if os.path.isdir(self.sm.lab_path(self.options_widget['Номер лабы:'],
                                                      self.options_widget['Номер задания:'], i)):
                        self.options_widget.set_value('Номер варианта:', i)
                        break
            self.sm.set('var', self.options_widget["Номер варианта:"])
            self.first_open()
        elif key == 'Номер варианта:':
            self.sm.set('var', self.options_widget["Номер варианта:"])
            self.first_open()
        elif key == 'Тестировать':
            self.save_code()
            self.testing_signal.emit()

    def update_options(self):
        self.options_widget.set_value('Номер лабы:', self.sm.get('lab', self.options_widget['Номер лабы:']))
        self.options_widget.set_value('Номер задания:',
                                      self.sm.get('task', self.options_widget['Номер задания:']))
        self.options_widget.set_value('Номер варианта:',
                                      self.sm.get('var', self.options_widget['Номер варианта:']))

    def get_path(self, from_settings=False):
        if from_settings:
            self.path = self.sm.lab_path()
        else:
            self.path = self.sm.lab_path(self.options_widget['Номер лабы:'], self.options_widget['Номер задания:'],
                                         self.options_widget['Номер варианта:'])

    def rename_file(self, name):
        self.current_file = name

    def first_open(self):
        self.test_res_widget.clear()
        self.files_widget.open_task()
        self.tab_widget.setCurrentIndex(0)
        for i in range(self.files_widget.files_list.count()):
            if self.files_widget.files_list.item(i) == 'main.c':
                self.files_widget.files_list.setCurrentRow(i)
                return

    def update_todo(self):
        self.todo_widget.clear()
        for path, line, text in self.cm.parse_todo_in_code(current_task=True):
            self.todo_widget.addItem(CodeTODOItem(path, line, text, self.tm))

    def jump_by_todo(self):
        item = self.todo_widget.currentItem()
        for i in range(self.files_widget.files_list.count()):
            if self.files_widget.files_list.item(i).text() == item.path:
                self.files_widget.files_list.setCurrentRow(i)
                self.code_edit.setCursorPosition(item.line, 0)
                break
        self.tab_widget.setCurrentIndex(2)

    def open_code(self, path):
        self.tab_widget.setCurrentIndex(0)
        self.get_path()
        self.code_edit.setText("")
        try:
            if not os.path.isfile(path):
                self.code_edit.setDisabled(True)
                return

            self.current_file = path
            self.file_update_time = os.path.getmtime(self.current_file)
            self.code_edit.open_file(*os.path.split(self.current_file))
            self.update_todo()
            self.code_edit.setDisabled(False)
            self.set_theme()
            self.parse_gcov_file()
        except Exception:
            self.code_edit.setDisabled(True)

    def save_code(self):
        code = self.code_edit.text()
        if code:
            os.makedirs(self.path, exist_ok=True)
            file = open(f"{self.current_file}", 'w', encoding='utf=8', newline=self.sm['line_sep'])
            file.write(code)
            file.close()
            self.file_update_time = os.path.getmtime(f"{self.current_file}")

    def check_if_code_changed(self):
        if os.path.isfile(self.current_file) and self.file_update_time != os.path.getmtime(self.current_file):
            pos = self.code_edit.getCursorPosition()
            self.code_edit.setCursorPosition(*pos)

    def testing_start(self, lst):
        self.test_count = 0
        self.test_res_widget.clear()
        self.options_widget.setDisabled(True)
        self.tab_widget.setCurrentIndex(1)
        for test in lst:
            item = QListWidgetItem(test)
            item.setForeground(self.tm['TestInProgress'])
            item.setFont(self.tm.code_font)
            self.test_res_widget.addItem(item)

    def add_test(self, text, color):
        self.test_res_widget.item(self.test_count).setText(text)
        self.test_res_widget.item(self.test_count).setForeground(color)
        self.test_count += 1

    def end_testing(self):
        self.parse_gcov_file()
        self.options_widget.setDisabled(False)

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
                    print(f"{line[0].strip():3} {line[1].strip():3}")
                    self.code_edit.setMarginLineNumbers(i, False)
                    self.code_edit.setMarginText(i, f"{line[0].strip():3} {line[1].strip():3}", 0)

    def set_theme(self):
        tab_style_sheet = f"""
        QTabWidget::pane {{
            color: {self.tm['BgColor']};
            }}
        QTabBar::tab {{
            color: {self.tm['TextColor']};
            background-color: {self.tm['MainColor']};
            border-bottom-color: {self.tm['TextColor']};
            border-top-left-radius: 5px;
            border-top-right-radius: 5px;
            border: 1px solid {self.tm['BorderColor']};
            width: 50px;
            padding: 4px;
            }}
        QTabBar::tab:hover {{
        background-color: {self.tm['ColorHover']};
        }}
        QTabBar::tab:selected {{
        background-color: {self.tm['ColorSelected']};
        }}
        """

        self.tm.set_theme_to_list_widget(self.test_res_widget)
        self.tm.set_theme_to_list_widget(self.todo_widget)
        self.tab_widget.setStyleSheet(tab_style_sheet)
        self.tab_widget.setFont(self.tm.font_small)
        self.code_edit.set_theme()
        self.files_widget.set_theme()
        self.options_widget.set_widget_style_sheet('Номер лабы:', self.tm.spin_box_style_sheet)
        self.options_widget.set_widget_style_sheet('Номер задания:', self.tm.spin_box_style_sheet)
        self.options_widget.set_widget_style_sheet('Номер варианта:', self.tm.spin_box_style_sheet)
        self.options_widget.set_widget_style_sheet('Тестировать', self.tm.buttons_style_sheet)
        self.options_widget.setFont(self.tm.font_small)

    def show(self) -> None:
        if self.isHidden():
            self.update_options()
            self.first_open()
            self.code_edit.am.update_libs()
        super(CodeWidget, self).show()

    def hide(self):
        super(CodeWidget, self).hide()


class CodeTODOItem(QListWidgetItem):
    def __init__(self, path, line, description, tm):
        super(CodeTODOItem, self).__init__()
        self.path = os.path.basename(path)
        self.description = description
        self.line = line
        self.setText(f"    {self.path:20} {line}\n{self.description}")
