import os

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QDialog, QListWidget, \
    QLineEdit

from backend.commands import read_json
from side_tabs.console import Console
from ui.message_box import MessageBox
from main_tabs.code_tab.syntax_highlighter import CodeEditor
from ui.side_panel_widget import SidePanelWidget


class GeneratorTab(SidePanelWidget):
    complete = pyqtSignal()

    def __init__(self, sm, bm, tm):
        super().__init__(sm, tm, 'Генерация тестов', ['delete', 'load', 'save', 'run', 'close'])
        self.setWindowTitle("TestGenerator")
        self.resize(600, 400)

        self.bm = bm
        self.test_type = 'pos'

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.code_edit = CodeEditor(self.sm, self.tm, language='Python', border=True)
        main_layout.addWidget(self.code_edit)

        self.console = Console(self.sm, self.tm, self.bm)
        self.console.hide()
        self.console.processFinished.connect(self.load_tests)
        main_layout.addWidget(self.console)

        self.setLayout(main_layout)

        self.buttons['load'].clicked.connect(self.open_code)
        self.buttons['save'].clicked.connect(self.save_code)
        self.buttons['delete'].clicked.connect(self.show_info)
        self.buttons['close'].clicked.connect(self.close_console)
        self.buttons['run'].clicked.connect(self.run_code)

        self.set_autocompletion()

        self.dialog = None
        self.scripts_dir = f"{self.sm.app_data_dir}/scripts"

    def set_theme(self):
        super().set_theme()
        self.code_edit.set_theme()
        self.console.set_theme()

    def open_code(self):
        self.dialog = FileDialog(self.tm, 'open', self.scripts_dir)
        if self.dialog.exec():
            try:
                with open(os.path.join(self.scripts_dir, self.dialog.list_widget.currentItem().text()),
                          encoding='utf-8') as f:
                    self.code_edit.set_text(f.read())
            except Exception as ex:
                print(f"{ex.__class__.__name__}: {ex}")

    def save_code(self):
        self.dialog = FileDialog(self.tm, 'save', self.scripts_dir)
        if self.dialog.exec():
            try:
                name = self.dialog.line_edit.text()
                if not name.endswith('.py'):
                    name += '.py'
                file = open(f"{self.scripts_dir}/{name}", 'w', encoding='utf-8',
                            newline=self.sm.line_sep)
                file.write(self.code_edit.text())
                file.close()
            except Exception as ex:
                print(f"{ex.__class__.__name__}: {ex}")

    def load_tests(self):
        file = f"{self.sm.temp_dir()}/tests.txt"
        data = read_json(file)
        if data.get('clear', False):
            pass
        for el in data.get('pos', []):
            test = self.bm.func_tests.new('pos', data=el)
        for el in data.get('neg', []):
            test = self.bm.func_tests.new('neg', data=el)
        try:
            os.remove(file)
        except FileNotFoundError:
            pass

    def set_autocompletion(self):
        self.code_edit.autocomplitions = ["open_in_file(test_num, mode='w', **kwargs)",
                                          "open_out_file(test_num, mode='w', **kwargs)",
                                          "open_args_file(test_num, mode='w', **kwargs)",
                                          "write_in(test_num, data, mode='w', **kwargs)",
                                          "write_out(test_num, data, mode='w', **kwargs)",
                                          "write_args(test_num, data, mode='w', **kwargs)",
                                          "test_count",
                                          "set_desc(test_num, desc)",
                                          "add_test(in_data='', out_data='', args='', desc='-', index=None)",
                                          "path: str"]

    def run_code(self):
        os.makedirs(f"{self.sm.project.data_path()}/func_tests/{self.test_type}", exist_ok=True)
        file = open(f'{self.sm.app_data_dir}/temp.py', 'w', encoding='utf-8', newline=self.sm.line_sep)
        file.write(self.previous_code())
        file.write(self.code_edit.text())
        file.write(self.end_code())
        file.close()

        self.code_edit.hide()
        self.buttons['load'].hide()
        self.buttons['save'].hide()
        self.buttons['run'].hide()
        self.buttons['close'].show()
        self.console.show()
        self.console.run_python(f'{self.sm.app_data_dir}/temp.py')

        # self.looper = self.cm.cmd_command_looper([self.sm.get_general('python'), f'{self.sm.app_data_dir}/temp.py'])
        # self.looper.complete.connect(self.run_complete)
        # self.looper.run()

    def close_console(self):
        self.console.hide()
        self.code_edit.show()
        self.buttons['close'].hide()
        self.buttons['load'].show()
        self.buttons['save'].show()
        self.buttons['run'].show()

    def show_info(self):
        MessageBox(MessageBox.Icon.Information, "Генерация тестов",
                   f"class Test:\n"
                   f"    def __init__(self, type, desc='', in_data='', out_data='', args='', exit='')\n"
                   f"    def set_desc(self, desc)\n"
                   f"    def set_in(self, in_data)\n"
                   f"    def set_in(self, text)\n"
                   f"    def set_out(self, text)\n"
                   f"    def set_args(self, args)\n"
                   f"    def set_exit(self, exit='')\n"
                   f"    def add_in_file(self, type='txt', text='')\n"
                   f"    def add_out_file(self, type='txt', text='')\n"
                   f"    def add_check_file(self, index: int, type='txt', text='')\n\n"
                   f""
                   f"def add_test(test: Test)", self.tm)

    def previous_code(self):
        return f"""
import json

__pos_tests__ = []
__neg_tests__ = []
__clear_tests__ = False


def clear_tests():
    __pos_tests__.clear()
    __neg_tests__.clear()
    __clear_tests__ = True


class Test:
    POS = 0
    NEG = 1

    def __init__(self, test_type, desc='', in_data='', out_data='', args='', exit=''):
        self.type = test_type
        self.dict = {{'desc': desc, 'in': in_data, 'out': out_data, 'args': args, 'exit': exit, 'in_files': [],
                      'out_files': [], 'check_files': dict()}}

    def __getitem__(self, item):
        return self.dict[item]

    def __setitem__(self, item, value):
        self.dict[item] = value

    def set_desc(self, desc):
        self.dict['desc'] = str(desc)

    def set_in(self, text):
        self.dict['in'] = str(text)

    def set_out(self, text):
        self.dict['out'] = str(text)

    def set_args(self, args):
        self.dict['args'] = str(args)

    def set_exit(self, exit=''):
        self.dict['exit'] = str(exit)
        
    def add_in_file(self, type='txt', text=''):
        self.dict['in_files'].append({{'type': type, 'text': text}})
        
    def add_out_file(self, type='txt', text=''):
        self.dict['out_files'].append({{'type': type, 'text': text}})
        
    def add_check_file(self, index: int, type='txt', text=''):
        self.dict['check_files'][index] = {{'type': type, 'text': text}}
        

path = r"{self.sm.project.path()}"
data_path = r"{self.sm.project.data_path()}"


def add_test(test: Test):
    if test.type == Test.POS:
        __pos_tests__.append(test)
    else:
        __neg_tests__.append(test)
"""

    def end_code(self):
        return f"""
with open(\"{self.sm.temp_dir()}/tests.txt\", 'w') as f:
    f.write(json.dumps({{'clear': __clear_tests__, 
         'pos': [test.dict for test in __pos_tests__], 
         'neg': [test.dict for test in __neg_tests__]}}))
"""

    def show(self) -> None:
        self.setDisabled(False)
        super().show()


class FileDialog(QDialog):
    def __init__(self, tm, mode='open', scripts_dir=''):
        super(FileDialog, self).__init__()
        self.mode = mode
        self.tm = tm

        os.makedirs(scripts_dir, exist_ok=True)

        main_layout = QVBoxLayout()

        self.list_widget = QListWidget()
        self.list_widget.addItems(filter(lambda s: s.endswith('.py'), os.listdir(scripts_dir)))

        if self.mode == 'save':
            self.line_edit = QLineEdit()
            main_layout.addWidget(self.line_edit)
            self.list_widget.currentItemChanged.connect(lambda item: self.line_edit.setText(item.text()))
        self.list_widget.doubleClicked.connect(lambda: self.accept() if self.list_widget.currentItem() else None)

        main_layout.addWidget(self.list_widget)

        buttons_layout = QHBoxLayout()
        buttons_layout.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.button_cancel = QPushButton("Отмена")
        buttons_layout.addWidget(self.button_cancel)
        self.button_cancel.clicked.connect(self.reject)
        self.button_cancel.setFixedSize(80, 24)
        self.button_ok = QPushButton("Ок")
        buttons_layout.addWidget(self.button_ok)
        self.button_ok.clicked.connect(self.accept)
        self.button_ok.setFixedSize(80, 24)

        main_layout.addLayout(buttons_layout)
        self.setLayout(main_layout)

        self.set_theme()

    def set_theme(self):
        self.setStyleSheet(self.tm.bg_style_sheet)
        for el in [self.button_cancel, self.button_ok, self.list_widget]:
            self.tm.auto_css(el)
        if self.mode == 'save':
            self.tm.auto_css(self.line_edit)
