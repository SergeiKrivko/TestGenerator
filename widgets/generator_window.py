import os

from PyQt5.QtCore import Qt, pyqtSignal, QThread
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QMainWindow, QDialog, QListWidget, \
    QLineEdit, QMessageBox

from widgets.menu_bar import MenuBar
from widgets.syntax_highlighter import PythonCodeEditor


SCRIPTS_DIR = 'scripts'


class GeneratorWindow(QMainWindow):
    complete = pyqtSignal(list, str)

    def __init__(self, sm, cm, tm):
        super(GeneratorWindow, self).__init__()
        self.setWindowTitle("TestGenerator")
        self.resize(600, 400)

        self.sm = sm
        self.cm = cm
        self.tm = tm
        self.test_type = 'pos'

        central_widget = QWidget()
        main_layout = QVBoxLayout()

        self.menu_bar = MenuBar({
            'Открыть': (self.open_code, None),
            'Сохранить': (self.save_code, None),
            'Протестировать': (lambda: print('test'), None),
            'Запустить': (self.run_code, None)
        })
        self.setMenuBar(self.menu_bar)

        self.code_edit = PythonCodeEditor(self.sm, self.tm, [])

        main_layout.addWidget(self.code_edit)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.set_autocompletion()

        self.tests_list = []
        self.dialog = None

    def set_theme(self):
        self.setStyleSheet(self.tm.bg_style_sheet)
        self.menu_bar.setStyleSheet(f"""
        QMenuBar {{
            color: {self.tm['TextColor']};
            background-color: {self.tm['BgColor']};
        }}
        QMenuBar::item::selected {{
            background-color: {self.tm['MainColor']};
        }}""")
        self.code_edit.set_theme()

    def open_code(self):
        self.dialog = FileDialog(self.tm, 'open')
        if self.dialog.exec():
            try:
                self.code_edit.open_file(SCRIPTS_DIR, self.dialog.list_widget.currentItem().text())
            except:
                pass

    def save_code(self):
        self.dialog = FileDialog(self.tm, 'save')
        if self.dialog.exec():
            try:
                name = self.dialog.line_edit.text()
                if not name.endswith('.py'):
                    name += '.py'
                file = open(f"{SCRIPTS_DIR}/{name}", 'w', encoding='utf-8',
                            newline=self.sm.get_general('line_sep', '\n'))
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
                                          "add_test(in_data='', out_data='', args='', desc='-', index=None)"]

    def run_code(self):
        os.makedirs(f"{self.sm.lab_path()}/func_tests/data", exist_ok=True)
        file = open('temp.py', 'w', encoding='utf-8', newline=self.sm['line_sep'])
        file.write(self.previous_code())
        file.write(self.code_edit.text())
        file.write(self.end_code())
        file.close()

        self.menu_bar.setDisabled(True)

        self.looper = self.cm.cmd_command_looper([self.sm.get_general('python'), 'temp.py'])
        self.looper.complete.connect(self.run_complete)
        self.looper.run()

    def run_complete(self, res):
        self.menu_bar.setDisabled(False)
        if res.stdout:
            QMessageBox.information(None, 'STDOUT', res.stdout)
        if res.stderr:
            QMessageBox.information(None, 'STDERR', res.stderr)
        if os.path.isfile('temp.txt'):
            file = open(f"temp.txt", encoding='utf-8')
            self.complete.emit(list(map(str.strip, file.readlines())), self.test_type)
            file.close()
            os.remove('temp.txt')
        if os.path.isfile('temp.py'):
            os.remove('temp.py')
        if res.returncode == 0:
            self.hide()

    def previous_code(self):
        return f"""
__tests_list__ = {str(self.tests_list)}
test_count = {len(self.tests_list)}
        
        
def open_in_file(test_num, mode='w', **kwargs):
    return open(f"{self.sm.lab_path()}/func_tests/data/{self.test_type}_{{test_num:0>2}}_in.txt", mode, **kwargs)


def open_out_file(test_num, mode='w', **kwargs):
    return open(f"{self.sm.lab_path()}/func_tests/data/{self.test_type}_{{test_num:0>2}}_out.txt", mode, **kwargs)


def open_args_file(test_num, mode='w', **kwargs):
    return open(f"{self.sm.lab_path()}/func_tests/data/{self.test_type}_{{test_num:0>2}}_args.txt", mode, **kwargs)


def write_in(test_num, data, mode='w', **kwargs):
    file = open_in_file(test_num, mode=mode, **kwargs)
    file.write(str(data))
    file.close()


def write_out(test_num, data, mode='w', **kwargs):
    file = open_out_file(test_num, mode=mode, **kwargs)
    file.write(str(data))
    file.close()


def write_args(test_num, data, mode='w', **kwargs):
    file = open_args_file(test_num, mode=mode, **kwargs)
    file.write(str(data))
    file.close()
    
    
def set_desc(test_num, desc):
    while len(__tests_list__) < test_num:
        __tests_list__.append('')
    __tests_list__[test_num - 1] = desc
    

def add_test(in_data='', out_data='', args='', desc='-', index=None):
    if index is None:
        index = len(__tests_list__) + 1
    write_in(index, in_data)
    write_out(index, out_data)
    if args:
        write_args(index, args)
    set_desc(index, desc)

"""

    def end_code(self):
        return f"""
file = open('temp.txt', 'w', encoding='utf-8')
for el in __tests_list__:
    file.write(str(el) + '\\n')
file.close()
"""

    def show(self) -> None:
        self.setDisabled(False)
        super(GeneratorWindow, self).show()


class FileDialog(QDialog):
    def __init__(self, tm, mode='open'):
        super(FileDialog, self).__init__()
        self.mode = mode
        self.tm = tm

        os.makedirs(SCRIPTS_DIR, exist_ok=True)

        main_layout = QVBoxLayout()

        self.list_widget = QListWidget()
        self.list_widget.addItems(filter(lambda s: s.endswith('.py'), os.listdir(SCRIPTS_DIR)))

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
        self.button_cancel.setStyleSheet(self.tm.buttons_style_sheet)
        self.button_ok.setStyleSheet(self.tm.buttons_style_sheet)
        self.list_widget.setStyleSheet(self.tm.list_widget_style_sheet)
        if self.mode == 'save':
            self.line_edit.setStyleSheet(self.tm.style_sheet)

