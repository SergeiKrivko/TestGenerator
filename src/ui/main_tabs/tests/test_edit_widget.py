from PyQt6.QtCore import pyqtSignal
from PyQtUIkit.widgets import *

from src.backend.backend_types.func_test import FuncTest
from src.other.binary_redactor.redactor import RedactorWidget


class TestEditWidget(KitVBoxLayout):
    testEdited = pyqtSignal()
    testNameChanged = pyqtSignal()

    def __init__(self):
        super(TestEditWidget, self).__init__()

        self.spacing = 6

        layout = KitHBoxLayout()
        layout.spacing = 6
        self.addWidget(layout)
        layout.addWidget(KitLabel("Описание теста"))

        self.test_name_edit = KitLineEdit()
        layout.addWidget(self.test_name_edit)

        layout = KitHBoxLayout()
        layout.spacing = 6
        self.addWidget(layout)
        layout.addWidget(KitLabel("Аргументы"))

        self.cmd_args_edit = KitLineEdit()
        self.cmd_args_edit.font = 'mono'
        layout.addWidget(self.cmd_args_edit)

        layout.addWidget(KitLabel("Код возврата"))

        self.exit_code_edit = KitLineEdit()
        self.exit_code_edit.setMaximumWidth(80)
        self.exit_code_edit_text = ""
        self.exit_code_edit.on_text_edited = self.exit_code_edit_triggered
        layout.addWidget(self.exit_code_edit)

        layout = KitHBoxLayout()
        layout.spacing = 12
        self.addWidget(layout)

        self.test_in_edit = RedactorWidget()
        layout.addWidget(self.test_in_edit)

        self.test_out_edit = RedactorWidget()
        layout.addWidget(self.test_out_edit)

        self._test: FuncTest | None = None
        self.test_name_edit.on_text_edited = self.set_test_name
        self.test_in_edit.textChanged.connect(self.set_test_in)
        self.test_out_edit.textChanged.connect(self.set_test_out)
        self.cmd_args_edit.on_text_edited = self.set_test_args
        self.exit_code_edit.on_text_edited = self.set_test_exit
        self.test_in_edit.addTab.connect(self.add_in_file)
        self.test_in_edit.tabCloseRequested.connect(self.delete_in)
        self.test_in_edit.currentChanged.connect(self.test_in_selected)
        self.test_out_edit.addTab.connect(self.add_out_file)
        self.test_out_edit.tabCloseRequested.connect(self.delete_out)
        self.test_out_edit.currentChanged.connect(self.test_out_selected)

        self.set_disabled(True)

    def exit_code_edit_triggered(self):
        if not self.exit_code_edit.text.strip():
            self.exit_code_edit.setText("")
            self.exit_code_edit_text = ""
        else:
            try:
                int(self.exit_code_edit.text.strip())
            except ValueError:
                self.exit_code_edit.setText(self.exit_code_edit_text)
            else:
                self.exit_code_edit_text = self.exit_code_edit.text

    def open_test(self, test: FuncTest):
        self._test = test
        self.test_name_edit.setText(test.description or '-')
        self.cmd_args_edit.setText(test.args)
        self.exit_code_edit.setText(test.exit)

        self.test_in_edit.clear()
        self.test_in_edit.add_tab('STDIN', test.stdin)
        self.test_out_edit.clear()
        self.test_out_edit.add_tab('STDOUT', test.stdout)
            
        for i, el in enumerate(test.in_files):
            self.test_in_edit.add_tab(f"in_file_{i + 1}.{el.type}", el.data)
            if el.check:
                self.test_out_edit.add_tab(f"check_file_{i + 1}.{el.type}", el.check)

        for i, el in enumerate(test.out_files):
            self.test_out_edit.add_tab(f"out_file_{i + 1}.{el.type}", el.data)

        self.test_in_edit.select_tab(test.current_in)
        self.test_out_edit.select_tab(test.current_out)

        self.set_disabled(False)

    def set_disabled(self, flag):
        self.test_in_edit.setDisabled(flag)
        self.test_out_edit.setDisabled(flag)
        self.test_name_edit.setDisabled(flag)
        self.cmd_args_edit.setDisabled(flag)
        self.exit_code_edit.setDisabled(flag)
        
    def close_test(self):
        self._test = None
        self.set_disabled(True)
        self.test_in_edit.clear()
        self.test_out_edit.clear()
        self.test_name_edit.setText("")
        self.exit_code_edit.setText("")

    def set_test_name(self, name):
        self._test.description = name
        self.testEdited.emit()
        self.testNameChanged.emit()

    def test_in_selected(self, index):
        self._test.current_in = index
        self.testEdited.emit()

    def test_out_selected(self, index):
        self._test.current_out = index
        self.testEdited.emit()

    def set_test_in(self, name, text):
        text = text.replace('\r\n', '\n')
        if name == 'STDIN':
            self._test.stdin = text
        else:
            try:
                index = int(name.lstrip('in_file_').rstrip('.txt.bin'))
            except ValueError:
                return 
            self._test.in_files[index - 1].data = text
        self.testEdited.emit()

    def set_test_out(self, name, text):
        text = text.replace('\r\n', '\n')
        if name == 'STDOUT':
            self._test.stdout = text
        elif name.startswith('out_file_'):
            try:
                index = int(name.lstrip('out_file_').rstrip('.txt.bin'))
                self._test.out_files[index - 1].data = text
            except ValueError:
                return
        elif name.startswith('check_file_'):
            try:
                index = int(name.lstrip('check_file_').rstrip('.txt.bin'))
                self._test.in_files[index - 1].check = text
            except ValueError:
                return
        else:
            return
        self.testEdited.emit()

    def delete_in(self, index):
        if index <= 0:
            pass
        else:
            self._test.in_files.pop(index - 1)
            self.open_test(self._test)

            self.testEdited.emit()

    def delete_out(self, index):
        if index <= 0:
            return
        name = self.test_out_edit.tab_text(index)
        if name.startswith('check_file_'):
            try:
                index = int(name.lstrip('check_file_').rstrip('.txt.bin'))
                self._test.in_files[index - 1].pop('check')
            except Exception as ex:
                print(f"{ex.__class__.__name__}: {ex}")
                return
        elif name.startswith('out_file_'):
            try:
                index = int(name.lstrip('out_file_').rstrip('.txt.bin'))
                self._test.out_files.pop(index - 1)
            except Exception as ex:
                print(f"{ex.__class__.__name__}: {ex}")
                return
        else:
            return
        self.open_test(self._test)
        self.testEdited.emit()

    def set_test_args(self, data):
        self._test.args = data
        self.testEdited.emit()

    def set_test_exit(self, code):
        self._test.exit = code
        self.testEdited.emit()

    def add_in_file(self):
        dialog = NewInFileDialog(self)
        if dialog.exec():
            file_type = 'txt' if dialog.combo_box.currentIndex() == 0 else 'bin'
            self._test.in_files.append({'type': file_type, 'text': ''})
            self.test_in_edit.add_tab(f"in_file_{self.test_in_edit.count()}.{file_type}", "")
        self.testEdited.emit()

    def add_out_file(self):
        dialog = NewOutFileDialog(self, self._test.in_files)
        if dialog.exec():
            if dialog.combo_box.currentIndex() == 0:
                file_type = 'txt' if dialog.type_combo_box.currentIndex() == 0 else 'bin'
                self._test.out_files.append({'type': file_type, 'text': ''})
                self.test_out_edit.add_tab(f"out_file_{self.test_out_edit.count()}.{file_type}")
            else:
                index = dialog.file_combo_box.currentIndex()
                self._test.in_files[index].check = ""
                self.test_out_edit.add_tab(dialog.file_combo_box.currentText().replace('in', 'check', 1))
        self.testEdited.emit()
