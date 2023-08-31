from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import  QLineEdit, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, \
    QDialog, QDialogButtonBox

from binary_redactor.redactor import RedactorWidget
from ui.button import Button


class TestEditWidget(QWidget):
    test_edited = pyqtSignal()

    def __init__(self, tm):
        super(TestEditWidget, self).__init__()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        self.tm = tm
        self.labels = []

        h_layout1 = QHBoxLayout()
        layout.addLayout(h_layout1)
        h_layout1.addWidget(label := QLabel("Описание теста"))
        self.labels.append(label)
        self.test_name_edit = QLineEdit()
        h_layout1.addWidget(self.test_name_edit)

        h_layout2 = QHBoxLayout()
        layout.addLayout(h_layout2)
        h_layout2.addWidget(label := QLabel("Аргументы"))
        self.labels.append(label)
        self.cmd_args_edit = QLineEdit()
        h_layout2.addWidget(self.cmd_args_edit)

        h_layout2.addWidget(label := QLabel("Код возврата"))
        self.labels.append(label)
        self.exit_code_edit = QLineEdit()
        self.exit_code_edit.setMaximumWidth(80)
        self.exit_code_edit_text = ""
        self.exit_code_edit.textChanged.connect(self.exit_code_edit_triggered)
        h_layout2.addWidget(self.exit_code_edit)

        h_layout3 = QHBoxLayout()
        layout.addLayout(h_layout3)

        h_layout3.addWidget(label := QLabel("Препроцессор:"))
        self.preprocessor_label = label
        self.labels.append(label)
        self.preprocessor_line = QLineEdit()
        h_layout3.addWidget(self.preprocessor_line)

        h_layout3.addWidget(label := QLabel("Постпроцессор:"))
        self.postprocessor_label = label
        self.labels.append(label)
        self.postprocessor_line = QLineEdit()
        h_layout3.addWidget(self.postprocessor_line)

        h_layout = QHBoxLayout()
        layout.addLayout(h_layout)

        layout1 = QVBoxLayout()
        h_layout.addLayout(layout1, 1)
        # layout_h1 = QHBoxLayout()
        # layout_h1.addWidget(label := QLabel("Входные данные"))
        # self.labels.append(label)
        # 
        # self.in_combo_box = QComboBox()
        # self.in_combo_box.addItems(['STDIN'])
        # self.in_combo_box.setFixedHeight(20)
        # layout_h1.addWidget(self.in_combo_box)
        # 
        # self.button_add_in = Button(self.tm, 'plus')
        # self.button_add_in.setFixedSize(22, 22)
        # layout_h1.addWidget(self.button_add_in)
        # 
        # self.button_delete_in = Button(self.tm, 'delete')
        # self.button_delete_in.setFixedSize(22, 22)
        # layout_h1.addWidget(self.button_delete_in)
        # 
        # layout1.addLayout(layout_h1)
        self.test_in_edit = RedactorWidget(self.tm)
        layout1.addWidget(self.test_in_edit)

        layout2 = QVBoxLayout()
        h_layout.addLayout(layout2, 1)
        # layout_h2 = QHBoxLayout()
        # layout2.addLayout(layout_h2)
        # layout_h2.addWidget(label := QLabel("Выходные данные"))
        # self.labels.append(label)
        # 
        # self.out_combo_box = QComboBox()
        # self.out_combo_box.addItems(['STDOUT'])
        # self.out_combo_box.setFixedHeight(20)
        # layout_h2.addWidget(self.out_combo_box)
        # 
        # self.button_add_out = Button(self.tm, 'plus')
        # self.button_add_out.setFixedSize(22, 22)
        # layout_h2.addWidget(self.button_add_out)
        # 
        # self.button_delete_out = Button(self.tm, 'delete')
        # self.button_delete_out.setFixedSize(22, 22)
        # layout_h2.addWidget(self.button_delete_out)

        self.test_out_edit = RedactorWidget(self.tm)
        layout2.addWidget(self.test_out_edit)

        self.data = dict()
        self.test_name_edit.textEdited.connect(self.set_test_name)
        self.test_in_edit.textChanged.connect(self.set_test_in)
        self.test_out_edit.textChanged.connect(self.set_test_out)
        self.cmd_args_edit.textEdited.connect(self.set_test_args)
        self.exit_code_edit.textEdited.connect(self.set_test_exit)
        self.test_in_edit.addTab.connect(self.add_in_file)
        self.test_in_edit.tabCloseRequested.connect(self.delete_in)
        self.test_in_edit.currentChanged.connect(self.test_in_selected)
        self.test_out_edit.addTab.connect(self.add_out_file)
        self.test_out_edit.tabCloseRequested.connect(self.delete_out)
        self.test_out_edit.currentChanged.connect(self.test_out_selected)

        self.set_disabled()

    def exit_code_edit_triggered(self):
        if not self.exit_code_edit.text().strip():
            self.exit_code_edit.setText("")
            self.exit_code_edit_text = ""
        else:
            try:
                int(self.exit_code_edit.text().strip())
            except ValueError:
                self.exit_code_edit.setText(self.exit_code_edit_text)
            else:
                self.exit_code_edit_text = self.exit_code_edit.text()

    def open_test(self, data: dict):
        self.data = data
        current_in, current_out = data.get('current_in', 0), data.get('current_out', 0)
        self.test_name_edit.setText(data.get('desc', '-'))
        self.cmd_args_edit.setText(data.get('args', ''))
        self.exit_code_edit.setText(str(data.get('exit', '')))
        self.test_in_edit.clear()
        self.test_in_edit.add_tab('STDIN', data['in'])
        self.test_out_edit.clear()
        self.test_out_edit.add_tab('STDOUT', data['out'])
        
        if not isinstance(data.get('in_files'), list):
            data['in_files'] = []
        if not isinstance(data.get('out_files'), list):
            data['out_files'] = []
        try:
            for key, item in data['check_files'].items():
                data['in_files'][int(key) - 1]['check'] = item['text']
            data.pop('check_files')
        except KeyError:
            pass
        except ValueError:
            pass
        except IndexError:
            pass
            
        for i, el in enumerate(data['in_files']):
            self.test_in_edit.add_tab(f"in_file_{i + 1}.{el['type']}", el['text'])
            if 'check' in el:
                self.test_out_edit.add_tab(f"check_file_{i + 1}.{el['type']}", el['check'])

        for i, el in enumerate(data['out_files']):
            self.test_out_edit.add_tab(f"out_file_{i + 1}.{el['type']}", el['text'])

        self.test_in_edit.select_tab(current_in)
        self.test_out_edit.select_tab(current_out)

        self.test_in_edit.setDisabled(False)
        self.test_out_edit.setDisabled(False)
        self.test_name_edit.setDisabled(False)
        self.cmd_args_edit.setDisabled(False)
        self.exit_code_edit.setDisabled(False)

    def set_disabled(self):
        self.test_in_edit.setDisabled(True)
        self.test_out_edit.setDisabled(True)
        self.test_name_edit.setDisabled(True)
        self.cmd_args_edit.setDisabled(True)
        self.exit_code_edit.setDisabled(True)
        self.test_in_edit.clear()
        self.test_out_edit.clear()
        self.test_name_edit.setText("")
        self.preprocessor_line.setText("")
        self.postprocessor_line.setText("")
        self.exit_code_edit.setText("")

    def set_theme(self):
        for el in [self.test_name_edit, self.exit_code_edit]:
            self.tm.auto_css(el)
        for el in [self.cmd_args_edit, self.preprocessor_line, self.postprocessor_line]:
            self.tm.auto_css(el, code_font=True)
        for el in [self.test_in_edit, self.test_out_edit]:
            el.set_theme()
        for label in self.labels:
            label.setFont(self.tm.font_small)

    def set_test_name(self, name):
        self.data['desc'] = name
        self.test_edited.emit()

    def test_in_selected(self, index):
        self.data['current_in'] = index
        self.test_edited.emit()

    def test_out_selected(self, index):
        self.data['current_out'] = index
        self.test_edited.emit()

    def set_test_in(self, name, text):
        if name == 'STDIN':
            self.data['in'] = text
        else:
            try:
                index = int(name.lstrip('in_file_').rstrip('.txt.bin'))
            except ValueError:
                return 
            self.data['in_files'][index - 1]['text'] = text
        self.test_edited.emit()

    def set_test_out(self, name, text):
        if name == 'STDOUT':
            self.data['out'] = text
        elif name.startswith('out_file_'):
            try:
                index = int(name.lstrip('out_file_').rstrip('.txt.bin'))
                self.data['out_files'][index - 1]['text'] = text
            except ValueError:
                return
        elif name.startswith('check_file_'):
            try:
                index = int(name.lstrip('check_file_').rstrip('.txt.bin'))
                self.data['in_files'][index - 1]['check'] = text
            except ValueError:
                return
        else:
            return
        self.test_edited.emit()

    def delete_in(self, index):
        if index <= 0:
            pass
        else:
            self.data['in_files'].pop(index - 1)
            self.open_test(self.data)

            self.test_edited.emit()

    def delete_out(self, index):
        if index <= 0:
            return
        name = self.test_out_edit.tab_text(index)
        if name.startswith('check_file_'):
            try:
                index = int(name.lstrip('check_file_').rstrip('.txt.bin'))
                self.data['in_files'][index - 1].pop('check')
            except Exception as ex:
                print(f"{ex.__class__.__name__}: {ex}")
                return
        elif name.startswith('out_file_'):
            try:
                index = int(name.lstrip('out_file_').rstrip('.txt.bin'))
                self.data['out_files'].pop(index - 1)
            except Exception as ex:
                print(f"{ex.__class__.__name__}: {ex}")
                return
        else:
            return
        self.open_test(self.data)
        self.test_edited.emit()

    def set_test_args(self, data):
        self.data['args'] = data
        self.test_edited.emit()

    def set_test_exit(self, code):
        self.data['exit'] = code
        self.test_edited.emit()

    def add_in_file(self):
        dialog = NewInFileDialog(self.tm)
        if dialog.exec():
            file_type = 'txt' if dialog.combo_box.currentIndex() == 0 else 'bin'
            self.data['in_files'].append({'type': file_type, 'text': ''})
            self.test_in_edit.add_tab(f"in_file_{self.test_in_edit.count()}.{file_type}", "")
        self.test_edited.emit()

    def add_out_file(self):
        dialog = NewOutFileDialog(self.tm, self.data['in_files'])
        if dialog.exec():
            if dialog.combo_box.currentIndex() == 0:
                file_type = 'txt' if dialog.type_combo_box.currentIndex() == 0 else 'bin'
                self.data['out_files'].append({'type': file_type, 'text': ''})
                self.test_out_edit.add_tab(f"out_file_{self.test_out_edit.count()}.{file_type}")
            else:
                index = dialog.file_combo_box.currentIndex()
                self.data['in_files'][index]['check'] = ""
                self.test_out_edit.add_tab(dialog.file_combo_box.currentText().replace('in', 'check', 1))
        self.test_edited.emit()


class NewInFileDialog(QDialog):
    def __init__(self, tm):
        super(NewInFileDialog, self).__init__()
        self.tm = tm

        self.setWindowTitle("Копировать тесты")

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.button(QDialogButtonBox.Ok).setStyleSheet(self.tm.button_css())
        self.buttonBox.button(QDialogButtonBox.Ok).setFixedSize(80, 24)
        self.buttonBox.button(QDialogButtonBox.Cancel).setStyleSheet(self.tm.button_css())
        self.buttonBox.button(QDialogButtonBox.Cancel).setFixedSize(80, 24)

        layout = QVBoxLayout()

        label = QLabel("Тип файла:")
        label.setFont(self.tm.font_small)
        layout.addWidget(label)

        self.combo_box = QComboBox()
        self.combo_box.addItems(['Текстовый', 'Бинарный'])
        self.combo_box.setStyleSheet(tm.combobox_css('Main'))
        self.combo_box.setFont(tm.font_small)

        layout.addWidget(self.combo_box)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)


class NewOutFileDialog(QDialog):
    def __init__(self, tm, files: list):
        super(NewOutFileDialog, self).__init__()
        self.tm = tm

        self.setWindowTitle("Копировать тесты")

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.tm.auto_css(self.buttonBox.button(QDialogButtonBox.Ok))
        self.buttonBox.button(QDialogButtonBox.Ok).setFixedSize(80, 24)
        self.tm.auto_css(self.buttonBox.button(QDialogButtonBox.Cancel))
        self.buttonBox.button(QDialogButtonBox.Cancel).setFixedSize(80, 24)

        layout = QVBoxLayout()

        self.combo_box = QComboBox()
        self.combo_box.addItems(['Выходной файл', 'Проверка состояния входного файла'])
        self.tm.auto_css(self.combo_box)
        self.combo_box.currentIndexChanged.connect(self.combo_box_triggered)
        layout.addWidget(self.combo_box)

        self.type_label = QLabel("Тип файла:")
        self.type_label.setFont(self.tm.font_small)
        layout.addWidget(self.type_label)

        self.type_combo_box = QComboBox()
        self.type_combo_box.addItems(['Текстовый', 'Бинарный'])
        self.tm.auto_css(self.type_combo_box)
        layout.addWidget(self.type_combo_box)

        self.file_label = QLabel("Проверяемый файл:")
        self.file_label.setFont(self.tm.font_small)
        layout.addWidget(self.file_label)
        self.file_label.hide()

        self.file_combo_box = QComboBox()
        self.file_combo_box.addItems([f"in_file_{i + 1}.{el['type']}"
                                      for i, el in enumerate(files)])
        self.tm.auto_css(self.file_combo_box)
        layout.addWidget(self.file_combo_box)
        self.file_combo_box.hide()

        layout.addWidget(self.buttonBox)
        self.setLayout(layout)

    def combo_box_triggered(self):
        if self.combo_box.currentIndex() == 0:
            self.file_combo_box.hide()
            self.file_label.hide()
            self.type_combo_box.show()
            self.type_label.show()
        else:
            self.type_combo_box.hide()
            self.type_label.hide()
            self.file_combo_box.show()
            self.file_label.show()
