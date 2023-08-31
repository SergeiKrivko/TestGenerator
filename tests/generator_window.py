import os

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QDialog, QListWidget, \
    QLineEdit

from code_tab.console import Console
from ui.message_box import MessageBox
from code_tab.syntax_highlighter import CodeEditor
from ui.side_panel_widget import SidePanelWidget


class GeneratorTab(SidePanelWidget):
    complete = pyqtSignal()

    def __init__(self, sm, cm, tm):
        super().__init__(sm, tm, 'Генерация тестов', ['load', 'save', 'run', 'close', 'resize'])
        self.setWindowTitle("TestGenerator")
        self.resize(600, 400)

        self.cm = cm
        self.test_type = 'pos'

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.code_edit = CodeEditor(self.sm, self.tm, language='Python', border=True)
        main_layout.addWidget(self.code_edit)

        self.console = Console(self.sm, self.tm, self.cm)
        self.console.hide()
        main_layout.addWidget(self.console)

        self.setLayout(main_layout)

        self.buttons['load'].clicked.connect(self.open_code)
        self.buttons['save'].clicked.connect(self.save_code)
        # self.buttons['documentation'].clicked.connect(self.show_info)
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
                self.code_edit.open_file(os.path.join(self.scripts_dir, self.dialog.list_widget.currentItem().text()))
            except:
                pass

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
            except:
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
                                          "path"]

    def run_code(self):
        os.makedirs(f"{self.sm.data_lab_path()}/func_tests/{self.test_type}", exist_ok=True)
        file = open(f'{self.sm.app_data_dir}/temp.py', 'w', encoding='utf-8', newline=self.sm.line_sep)
        file.write(self.previous_code())
        file.write(self.code_edit.text())
        file.close()

        self.code_edit.hide()
        self.buttons['load'].hide()
        self.buttons['save'].hide()
        self.buttons['run'].hide()
        self.buttons['close'].show()
        self.console.show()
        self.console.run_file(f'{self.sm.app_data_dir}/temp.py')

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
        MessageBox(MessageBox.Information, "Генерация тестов",
                   f"class Test:\n"
                   f"    def __init__(self, desc='', in_data='', out_data='', args='', exit='')\n"
                   f"    def set_desc(self, desc)\n"
                   f"    def set_in(self, in_data)\n"
                   f"    def set_in(self, text)\n"
                   f"    def set_out(self, text)\n"
                   f"    def set_args(self, args)\n"
                   f"    def set_exit(self, exit='')\n"
                   f"    def add_in_file(self, type='txt', text='')\n"
                   f"    def add_out_file(self, type='txt', text='')\n"
                   f"    def add_check_file(self, index: int, type='txt', text='')\n\n"
                   f"def add_test(test: Test, index=None)", self.tm)

    def previous_code(self):
        return f"""
import json

__tests_list__ = []


class Test:
    def __init__(self, desc='', in_data='', out_data='', args='', exit=''):
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
        
        
for el in {os.listdir(f"{self.sm.data_lab_path()}/func_tests/{self.test_type}")}:
    if el.rstrip('.json').isdigit():
        test = Test()
        try:
            with open(f"{self.sm.data_lab_path()}/func_tests/{self.test_type}/{{el}}", encoding='utf-8') as f:
                for key, item in json.loads(f.read()).items():
                    test[key] = item
            __tests_list__.append(test)
        except json.JSONDecodeError:
            pass
        except ValueError:
            pass
test_count = len(__tests_list__)
path = "{self.sm.lab_path()}"
data_path = "{self.sm.data_lab_path()}"


def add_test(test: Test, index=None):
    if index is None:
        index = len(__tests_list__) + 1
        __tests_list__.append(test)
    else:
        __tests_list[index] = test
    with open(f"{{data_path}}/func_tests/{self.test_type}/{{index}}.json", 'w', encoding='utf-8') as f:
        f.write(json.dumps(test.dict))

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
        buttons_layout.setAlignment(Qt.AlignRight)

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
