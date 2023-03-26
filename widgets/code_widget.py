import os
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QTextEdit, QListWidget, QListWidgetItem
from widgets.options_window import OptionsWidget


class CodeWidget(QWidget):
    testing_signal = pyqtSignal()

    def __init__(self, settings):
        super(CodeWidget, self).__init__()
        self.settings = settings

        layout = QHBoxLayout()
        self.setLayout(layout)
        layout_left = QVBoxLayout()
        layout.addLayout(layout_left)

        self.options_widget = OptionsWidget({
            'Номер лабы:': {'type': int, 'min': 1, 'initial': self.settings.get('lab', 1)},
            'Номер задания:': {'type': int, 'min': 1, 'initial': self.settings.get('task', 1)},
            'Номер варианта:': {'type': int, 'min': -1, 'initial': self.settings.get('var', 0)},
            'Тестировать': {'type': 'button', 'text': 'Тестировать', 'name': OptionsWidget.NAME_SKIP}
        })
        self.options_widget.clicked.connect(self.option_changed)
        layout_left.addWidget(self.options_widget)

        self.test_res_widget = QListWidget()
        self.test_res_widget.setMaximumWidth(175)
        layout_left.addWidget(self.test_res_widget)

        self.code_edit = QTextEdit()
        self.code_edit.setFont(QFont("Courier", 10))
        layout.addWidget(self.code_edit)
        self.path = ''

    def option_changed(self, key):
        if key in ('Номер лабы:', 'Номер задания:'):
            self.settings['lab'] = self.options_widget["Номер лабы:"]
            self.settings['task'] = self.options_widget["Номер задания:"]
            if os.path.isdir(self.settings['path'] + f"/lab_{self.options_widget['Номер лабы:']:0>2}_"
                                                     f"{self.options_widget['Номер задания:']:0>2}"):
                self.options_widget.set_value('Номер варианта:', -1)
            else:
                for i in range(100):
                    if os.path.isdir(self.settings['path'] + f"/lab_{self.options_widget['Номер лабы:']:0>2}_"
                                                             f"{self.options_widget['Номер задания:']:0>2}_{i:0>2}"):
                        self.options_widget.set_value('Номер варианта:', i)
                        break
            self.settings['var'] = self.options_widget["Номер варианта:"]
            self.open_code()
        elif key == 'Номер варианта:':
            self.settings['var'] = self.options_widget["Номер варианта:"]
            self.open_code()
        elif key == 'Тестировать':
            self.save_code()
            self.testing_signal.emit()

    def update_options(self):
        self.options_widget.set_value('Номер лабы:', self.settings.get('lab', self.options_widget['Номер лабы:']))
        self.options_widget.set_value('Номер задания:',
                                      self.settings.get('task', self.options_widget['Номер задания:']))
        self.options_widget.set_value('Номер варианта:',
                                      self.settings.get('var', self.options_widget['Номер варианта:']))

    def get_path(self, from_settings=False):
        if from_settings:
            if self.settings['var'] == -1:
                self.path = self.settings['path'] + f"/lab_{self.settings['lab']:0>2}_" \
                                                    f"{self.settings['task']:0>2}"
            else:
                self.path = self.settings['path'] + f"/lab_{self.settings['lab']:0>2}_" \
                                                    f"{self.settings['task']:0>2}_" \
                                                    f"{self.settings['var']:0>2}"
        elif self.options_widget['Номер варианта:'] == -1:
            self.path = self.settings['path'] + f"/lab_{self.options_widget['Номер лабы:']:0>2}_" \
                                                f"{self.options_widget['Номер задания:']:0>2}"
        else:
            self.path = self.settings['path'] + f"/lab_{self.options_widget['Номер лабы:']:0>2}_" \
                                                f"{self.options_widget['Номер задания:']:0>2}_" \
                                                f"{self.options_widget['Номер варианта:']:0>2}"

    def open_code(self):
        self.get_path()
        try:
            self.code_edit.setText("")
            file = open(f"{self.path}/main.c")
            self.code_edit.setText(file.read())
            file.close()
        except Exception:
            pass

    def save_code(self):
        code = self.code_edit.toPlainText()
        if code:
            os.makedirs(self.path, exist_ok=True)
            file = open(f"{self.path}/main.c", 'w', encoding='utf=8')
            file.write(code)
            file.close()

    def update_test_info(self, test_list):
        self.test_res_widget.clear()
        for test in test_list:
            self.test_res_widget.addItem(QListWidgetItem(f"{test[4]} \t{'PASSED' if test[0] else 'FAILED'}"))

    def show(self) -> None:
        self.update_options()
        self.open_code()
        super(CodeWidget, self).show()

    def hide(self):
        self.save_code()
        super(CodeWidget, self).hide()
