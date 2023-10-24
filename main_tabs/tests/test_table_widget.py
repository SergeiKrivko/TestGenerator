import typing

import docx
from PyQt6 import QtGui
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QListWidget, QLabel, QComboBox, QLineEdit, QDialog, \
    QPushButton

from side_tabs.builds.commands_list import CommandsList, ScenarioBox
from main_tabs.tests.in_data_window import InDataWindow
from ui.button import Button
from ui.options_window import OptionsWidget

BUTTONS_MAX_WIDTH = 30


class TestTableWidget(QWidget):
    copyTests = pyqtSignal(str)
    pasteTests = pyqtSignal(str)
    deleteTests = pyqtSignal(str)

    def __init__(self, tm, sm, bm, cm):
        super(TestTableWidget, self).__init__()
        self.tm = tm
        self.sm = sm
        self.bm = bm
        self.cm = cm
        self.labels = []
        self._windows = []

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        # Positive tests

        pos_layout = QVBoxLayout()
        layout.addLayout(pos_layout)

        in_data_layout = QHBoxLayout()
        pos_layout.addLayout(in_data_layout)
        in_data_layout.addWidget(label := QLabel("Вход:"))
        self.labels.append(label)

        self.in_data_edit = QLineEdit()
        in_data_layout.addWidget(self.in_data_edit)

        self._build_box = ScenarioBox(self.sm, self.bm, self.tm)
        self._build_box.currentIndexChanged.connect(self._on_build_changed)
        self.sm.projectChanged.connect(lambda: self._build_box.load(self.sm.get('build')))
        in_data_layout.addWidget(self._build_box)

        pos_buttons_layout = QHBoxLayout()
        pos_layout.addLayout(pos_buttons_layout)
        pos_buttons_layout.addWidget(label := QLabel("Позитивные тесты"))
        self.labels.append(label)

        self.pos_add_button = Button(self.tm, 'plus', css='Bg')
        self.pos_add_button.setFixedHeight(22)
        self.pos_add_button.setMaximumWidth(BUTTONS_MAX_WIDTH)
        pos_buttons_layout.addWidget(self.pos_add_button)

        self.pos_delete_button = Button(self.tm, 'delete', css='Bg')
        self.pos_delete_button.setFixedHeight(22)
        self.pos_delete_button.setMaximumWidth(BUTTONS_MAX_WIDTH)
        self.pos_delete_button.clicked.connect(lambda: self.deleteTests.emit('pos'))
        pos_buttons_layout.addWidget(self.pos_delete_button)

        self.pos_button_up = Button(self.tm, 'button_up', css='Bg')
        self.pos_button_up.setFixedHeight(22)
        self.pos_button_up.setMaximumWidth(BUTTONS_MAX_WIDTH)
        pos_buttons_layout.addWidget(self.pos_button_up)

        self.pos_button_down = Button(self.tm, 'button_down', css='Bg')
        self.pos_button_down.setFixedHeight(22)
        self.pos_button_down.setMaximumWidth(BUTTONS_MAX_WIDTH)
        pos_buttons_layout.addWidget(self.pos_button_down)

        self.pos_button_copy = Button(self.tm, 'copy', css='Bg')
        self.pos_button_copy.setFixedHeight(22)
        self.pos_button_copy.setMaximumWidth(BUTTONS_MAX_WIDTH)
        self.pos_button_copy.clicked.connect(lambda: self.copyTests.emit('pos'))
        pos_buttons_layout.addWidget(self.pos_button_copy)

        self.pos_button_paste = Button(self.tm, 'paste', css='Bg')
        self.pos_button_paste.setFixedHeight(22)
        self.pos_button_paste.setMaximumWidth(BUTTONS_MAX_WIDTH)
        self.pos_button_paste.clicked.connect(lambda: self.pasteTests.emit('pos'))
        pos_buttons_layout.addWidget(self.pos_button_paste)

        # self.pos_button_generate = Button(self.tm, 'generate')
        # self.pos_button_generate.setFixedHeight(22)
        # self.pos_button_generate.setMaximumWidth(BUTTONS_MAX_WIDTH)
        # pos_buttons_layout.addWidget(self.pos_button_generate)

        self.pos_test_list = QListWidget()
        self.pos_test_list.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)
        pos_layout.addWidget(self.pos_test_list)

        pos_comparator_layout = QHBoxLayout()
        pos_comparator_layout.addWidget(label := QLabel('Компаратор:'))
        self.pos_comparator_label = label
        self.labels.append(label)
        self.pos_comparator_widget = QComboBox()
        self.pos_comparator_widget.addItems(['По умолчанию', 'Числа', 'Числа как текст', 'Текст после подстроки',
                                             'Слова после подстроки', 'Текст', 'Слова'])
        self.pos_comparator_widget.setMaximumWidth(200)
        self.pos_comparator_widget.currentIndexChanged.connect(self.save_pos_comparator)
        pos_comparator_layout.addWidget(self.pos_comparator_widget)
        pos_layout.addLayout(pos_comparator_layout)

        # Negative tests

        neg_layout = QVBoxLayout()
        layout.addLayout(neg_layout)

        out_data_layout = QHBoxLayout()
        neg_layout.addLayout(out_data_layout)

        self.in_data_window = InDataWindow(self.sm, self.tm)

        self.in_data_button = Button(self.tm, 'plus', css='Bg')
        self.in_data_button.setFixedHeight(22)
        self.in_data_button.clicked.connect(self.in_data_window.exec)
        out_data_layout.addWidget(self.in_data_button)

        self._export_dialog = ExportDialog(self.sm, self.cm, self.tm)

        self.export_button = Button(self.tm, 'button_export', css='Bg')
        self.export_button.setFixedHeight(22)
        self.export_button.clicked.connect(self.run_export)
        out_data_layout.addWidget(self.export_button)

        out_data_layout.addWidget(label := QLabel("Выход:"))
        self.labels.append(label)

        self.out_data_edit = QLineEdit()
        out_data_layout.addWidget(self.out_data_edit)

        neg_buttons_layout = QHBoxLayout()
        neg_layout.addLayout(neg_buttons_layout)
        neg_buttons_layout.addWidget(label := QLabel("Негативные тесты"))
        self.labels.append(label)

        self.neg_add_button = Button(self.tm, 'plus', css='Bg')
        self.neg_add_button.setFixedHeight(22)
        self.neg_add_button.setMaximumWidth(BUTTONS_MAX_WIDTH)
        neg_buttons_layout.addWidget(self.neg_add_button)

        self.neg_delete_button = Button(self.tm, 'delete', css='Bg')
        self.neg_delete_button.setFixedHeight(22)
        self.neg_delete_button.setMaximumWidth(BUTTONS_MAX_WIDTH)
        self.neg_delete_button.clicked.connect(lambda: self.deleteTests.emit('neg'))
        neg_buttons_layout.addWidget(self.neg_delete_button)

        self.neg_button_up = Button(self.tm, 'button_up', css='Bg')
        self.neg_button_up.setFixedHeight(22)
        self.neg_button_up.setMaximumWidth(BUTTONS_MAX_WIDTH)
        neg_buttons_layout.addWidget(self.neg_button_up)

        self.neg_button_down = Button(self.tm, 'button_down', css='Bg')
        self.neg_button_down.setFixedHeight(22)
        self.neg_button_down.setMaximumWidth(BUTTONS_MAX_WIDTH)
        neg_buttons_layout.addWidget(self.neg_button_down)

        self.neg_button_copy = Button(self.tm, 'copy', css='Bg')
        self.neg_button_copy.setFixedHeight(22)
        self.neg_button_copy.setMaximumWidth(BUTTONS_MAX_WIDTH)
        self.neg_button_copy.clicked.connect(lambda: self.copyTests.emit('neg'))
        neg_buttons_layout.addWidget(self.neg_button_copy)

        self.neg_button_paste = Button(self.tm, 'paste', css='Bg')
        self.neg_button_paste.setFixedHeight(22)
        self.neg_button_paste.setMaximumWidth(BUTTONS_MAX_WIDTH)
        self.neg_button_paste.clicked.connect(lambda: self.pasteTests.emit('neg'))
        neg_buttons_layout.addWidget(self.neg_button_paste)

        self.neg_button_generate = Button(self.tm, 'generate', css='Bg')
        self.neg_button_generate.setFixedHeight(22)
        self.neg_button_generate.setMaximumWidth(BUTTONS_MAX_WIDTH)
        neg_buttons_layout.addWidget(self.neg_button_generate)

        # self.neg_button_generate = Button(self.tm, 'generate')
        # self.neg_button_generate.setFixedHeight(22)
        # self.neg_button_generate.setMaximumWidth(BUTTONS_MAX_WIDTH)
        # neg_buttons_layout.addWidget(self.neg_button_generate)

        self.neg_test_list = QListWidget()
        self.neg_test_list.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)
        neg_layout.addWidget(self.neg_test_list)

        neg_comparator_layout = QHBoxLayout()
        neg_comparator_layout.addWidget(label := QLabel('Компаратор:'))
        self.neg_comparator_label = label
        self.labels.append(label)
        self.neg_comparator_widget = QComboBox()
        self.neg_comparator_widget.addItems(
            ['По умолчанию', 'Нет', 'Числа', 'Числа как текст', 'Текст после подстроки',
             'Слова после подстроки', 'Текст', 'Слова'])
        self.neg_comparator_widget.setMaximumWidth(200)
        self.neg_comparator_widget.currentIndexChanged.connect(self.save_neg_comparator)
        neg_comparator_layout.addWidget(self.neg_comparator_widget)
        neg_layout.addLayout(neg_comparator_layout)

        self.ctrl_pressed = False
        self.shift_pressed = False

    def _on_build_changed(self):
        self.sm.set('build', self._build_box.current_scenario())

    def save_pos_comparator(self):
        self.sm.get('pos_comparator', self.pos_comparator_widget.currentIndex() - 1)

    def save_neg_comparator(self):
        self.sm.get('neg_comparator', self.neg_comparator_widget.currentIndex() - 1)

    def move_selection(self, test_type, direction, index):
        list_widget = self.pos_test_list if test_type == 'pos' else self.neg_test_list
        # index = list_widget.currentRow()
        if direction == 'up':
            index = max(0, index - 1)
        else:
            index = min(list_widget.count() - 1, index + 1)
        list_widget.setCurrentRow(index)

    def run_export(self):
        self._export_dialog.tests = []
        # for i in range(self.pos_test_list.count()):
        #     self._export_dialog.tests.append(Test(self.pos_test_list.item(i).path, f"pos{i}", 'pos'))
        # for i in range(self.neg_test_list.count()):
        #     self._export_dialog.tests.append(Test(self.neg_test_list.item(i).path, f"neg{i}", 'neg'))
        self._export_dialog.exec()

    def set_theme(self):
        self.tm.set_theme_to_list_widget(self.pos_test_list)
        self.tm.set_theme_to_list_widget(self.neg_test_list)
        for el in [self.pos_add_button, self.pos_delete_button, self.pos_button_up, self.pos_button_down,
                   self.pos_button_copy, self.pos_button_paste, self.in_data_edit,
                   self.neg_add_button, self.neg_delete_button,
                   self.neg_button_up, self.neg_button_down, self.neg_button_copy, self.neg_button_paste,
                   self.out_data_edit,
                   self.pos_comparator_widget, self.neg_comparator_widget, self.in_data_button,
                   self.neg_button_generate, self.export_button]:
            self.tm.auto_css(el)
        for label in self.labels:
            label.setFont(self.tm.font_medium)
        self._build_box.set_theme()
        for el in self._windows:
            if hasattr(el, 'set_theme'):
                el.set_theme()

    def keyPressEvent(self, a0: typing.Optional[QtGui.QKeyEvent]) -> None:
        match a0.key():
            case Qt.Key.Key_C:
                if self.ctrl_pressed:
                    self.copyTests.emit('')
            case Qt.Key.Key_V:
                if self.ctrl_pressed:
                    self.pasteTests.emit('')
            case Qt.Key.Key_Control:
                self.ctrl_pressed = True
            case Qt.Key.Key_Shift:
                self.shift_pressed = True
            case Qt.Key.Key_Delete:
                self.deleteTests.emit('')

    def keyReleaseEvent(self, a0: typing.Optional[QtGui.QKeyEvent]) -> None:
        if a0.key() == Qt.Key.Key_Control:
            self.ctrl_pressed = False
        if a0.key() == Qt.Key.Key_Shift:
            self.shift_pressed = False


class ExportDialog(QDialog):
    def __init__(self, sm, cm, tm):
        super().__init__()
        self._tm = tm
        self._sm = sm
        self._cm = cm
        self.tests = []
        self._looper = None

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        self._options_widget = OptionsWidget({
            "Формат файла:": {'type': 'combo', 'values': ['Txt', 'Docx', "Markdown"], 'name': OptionsWidget.NAME_LEFT},
            "Путь:": {'type': 'file', 'width': 300},
            "Ожидаемый вывод": {'type': bool, 'name': OptionsWidget.NAME_RIGHT},
            "Фактический вывод": {'type': bool, 'name': OptionsWidget.NAME_RIGHT},
            "Результат": {'type': bool, 'name': OptionsWidget.NAME_RIGHT},
            "Запустить тестирование": {'type': bool, 'name': OptionsWidget.NAME_RIGHT},
        })
        main_layout.addWidget(self._options_widget)

        buttons_layout = QHBoxLayout()
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        buttons_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        main_layout.addLayout(buttons_layout)

        self._button_export = QPushButton("Экспортировать")
        self._button_export.setFixedSize(160, 24)
        self._button_export.clicked.connect(self._execute)
        buttons_layout.addWidget(self._button_export)

        self._tm.css_to_options_widget(self._options_widget)
        self._tm.auto_css(self._button_export)
        self.setStyleSheet(self._tm.bg_style_sheet)

    def _execute(self, skip_looper=False):
        if not skip_looper and self._options_widget["Запустить тестирование"]:
            # self._looper = TestingLooper(self._sm, self._cm, self.tests)
            self._looper.finished.connect(lambda: self._execute(skip_looper=True))
            self._looper.start()
            return

        if self._options_widget["Формат файла:"] == 0:
            self._export_txt()
        elif self._options_widget["Формат файла:"] == 1:
            self._export_docx()
        self.accept()

    def _prepare_data(self):
        for test in self.tests:
            flag = test.is_loaded()
            if not flag:
                test.load()
            lst = [test.get('desc', ''), test.get('in', '')]
            if self._options_widget["Ожидаемый вывод"]:
                lst.append(test.get('out', ''))
            if self._options_widget["Фактический вывод"]:
                if self._options_widget["Запустить тестирование"]:
                    lst.append(test.prog_out['STDOUT'])
            if self._options_widget["Результат"]:
                lst.append("OK" if test.res() else "FAIL")
            if not flag:
                test.unload()
            yield lst

    def _export_txt(self):
        with open(self._options_widget["Путь:"], 'w', encoding='utf-8') as f:
            for test in self._prepare_data():
                f.write(' '.join(test) + '\n')

    def _export_docx(self):
        document = docx.Document()

        lst = list(self._prepare_data())

        table = document.add_table(rows=len(lst), cols=len(lst[0]))
        table.style = 'Table Grid'
        for i in range(len(lst)):
            for j in range(len(lst[i])):
                table.cell(i, j).text = str(lst[i][j])

        document.save(self._options_widget["Путь:"])
