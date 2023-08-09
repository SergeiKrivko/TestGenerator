import os

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QListWidgetItem

from code_tab.preview_widgets import PreviewWidget
from language.languages import languages
from code_tab.syntax_highlighter import CodeEditor
from ui.side_bar import SidePanel


class CodeWidget(QWidget):
    testing_signal = pyqtSignal()

    def __init__(self, sm, cm, tm, side_panel: SidePanel):
        super(CodeWidget, self).__init__()
        self.sm = sm
        self.cm = cm
        self.tm = tm
        self.side_panel = side_panel
        self.current_file = ''

        self.sm.finish_change_task.connect(self.first_open)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self.files_widget = self.side_panel.tabs['files']
        self.files_widget.setMaximumWidth(200)
        self.files_widget.button_down.clicked.connect(self.search_next)
        self.files_widget.button_up.clicked.connect(self.search_previous)
        self.files_widget.button_replace.clicked.connect(self.replace)
        self.files_widget.button_replace_all.clicked.connect(self.replace_all)

        self.files_widget.openFile.connect(self.open_code)
        self.files_widget.renameFile.connect(self.rename_file)

        self.code_edit = CodeEditor(sm, tm)
        self.code_edit.textChanged.connect(self.save_code)
        self.code_edit.cursorPositionChanged.connect(self.check_if_code_changed)
        layout.addWidget(self.code_edit)

        self.preview_widget = PreviewWidget(self.sm, self.tm)
        self.preview_widget.hide()
        self.files_widget.buttons['preview'].clicked.connect(self.show_preview)
        layout.addWidget(self.preview_widget)

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
        self.open_code('')
        # for i in range(self.files_widget.files_list.count()):
        #     if self.files_widget.files_list.item(i) == 'main.c':
        #         self.files_widget.files_list.setCurrentRow(i)
        #         return

    def update_todo(self):
        pass

    def jump_by_todo(self):
        item = 0
        for i in range(self.files_widget.files_list.count()):
            if self.files_widget.files_list.item(i).text() == item.path:
                self.files_widget.files_list.setCurrentRow(i)
                self.code_edit.setCursorPosition(item.line, 0)
                break

    def open_code(self, path):
        self.get_path()
        self.code_edit.setText("")
        try:
            if not os.path.isfile(path):
                raise Exception

            self.current_file = path

            if self.open_preview() != 1:
                self.preview_widget.hide()
                self.code_edit.show()
                self.file_update_time = os.path.getmtime(self.current_file)
                self.code_edit.open_file(*os.path.split(self.current_file))
                self.update_todo()
                self.code_edit.setDisabled(False)
                self.set_theme()
                self.parse_gcov_file()
            else:
                self.code_edit.hide()
                self.preview_widget.show()
        except Exception as ex:
            self.preview_widget.hide()
            self.code_edit.show()
            self.code_edit.setDisabled(True)

    def open_preview(self):
        for language in languages.values():
            if not language.get('preview', False):
                continue
            for el in language.get('files', []):
                if self.current_file.endswith(el):
                    self.preview_widget.open(self.current_file)
                    self.files_widget.buttons['run'].hide()
                    self.files_widget.buttons['preview'].show()

                    self.files_widget.buttons['preview'].setChecked(False)

                    if language.get('lexer'):
                        self.files_widget.buttons['preview'].setDisabled(False)
                        return 0
                    else:
                        self.files_widget.buttons['preview'].setDisabled(True)
                        return 1

        self.files_widget.buttons['preview'].hide()
        self.files_widget.buttons['run'].show()
        return 2

    def show_preview(self, flag):
        if flag:
            self.code_edit.hide()
            self.preview_widget.open(self.current_file)
            self.preview_widget.show()
        else:
            self.preview_widget.hide()
            self.code_edit.show()

    def save_code(self):
        code = self.code_edit.text()
        if code and self.path:
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
        for test in lst:
            item = QListWidgetItem(test)
            item.setForeground(self.tm['TestInProgress'])
            item.setFont(self.tm.code_font)
            item.setIcon(QIcon(self.tm.get_image('running', color=self.tm['TestInProgress'])))
            self.test_res_widget.addItem(item)

    def add_test(self, text, color):
        self.test_res_widget.item(self.test_count).setText(text)
        self.test_res_widget.item(self.test_count).setForeground(color)
        self.test_res_widget.item(self.test_count).setIcon(QIcon(self.tm.get_image(
            'passed' if text.endswith('PASSED') else 'failed', color=color)))
        self.test_count += 1

    def end_testing(self, open_files=False):
        self.parse_gcov_file()

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

    def search_next(self):
        try:
            if word := self.files_widget.search_line.text():
                current_line, current_symbol = self.code_edit.getCursorPosition()
                text = self.code_edit.text().split('\n')
                if word in text[current_line][current_symbol:]:
                    index = text[current_line][current_symbol:].index(word) + current_symbol
                    self.code_edit.setSelection(current_line, index, current_line, index + len(word))
                    return True
                else:
                    for i in range(current_line + 1, len(text)):
                        if word in text[i]:
                            index = text[i].index(word)
                            self.code_edit.setSelection(i, index, i, index + len(word))
                            return True
        except Exception as ex:
            print(f"{ex.__class__.__name__}: {ex}")
        return False

    def search_previous(self):
        try:
            if word := self.files_widget.search_line.text():
                current_line, current_symbol = self.code_edit.getCursorPosition()
                text = self.code_edit.text().split('\n')
                if word in text[current_line][:current_symbol - 1]:
                    index = text[current_line][:current_symbol - 1].rindex(word)
                    self.code_edit.setSelection(current_line, index, current_line, index + len(word))
                    return True
                else:
                    for i in range(current_line - 1, -1, -1):
                        if word in text[i]:
                            index = text[i].rindex(word)
                            self.code_edit.setSelection(i, index, i, index + len(word))
                            return True
        except Exception as ex:
            print(f"{ex.__class__.__name__}: {ex}")
        return False

    def replace(self):
        if self.code_edit.selectedText() == self.files_widget.search_line.text():
            self.code_edit.replaceSelectedText(self.files_widget.replace_line.text())
            if not self.search_next():
                self.search_previous()

    def replace_all(self):
        self.code_edit.setText(self.code_edit.text().replace(self.files_widget.search_line.text(),
                                                             self.files_widget.replace_line.text()))

    def set_theme(self):
        self.code_edit.set_theme()
        self.preview_widget.set_theme()


class CodeTODOItem(QListWidgetItem):
    def __init__(self, path, line, description, tm):
        super(CodeTODOItem, self).__init__()
        self.path = os.path.basename(path)
        self.description = description
        self.line = line
        self.setText(f"    {self.path:20} {line}\n{self.description}")
