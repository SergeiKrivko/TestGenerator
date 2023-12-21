import typing

import docx
from PyQt6 import QtGui
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QListWidget, QLabel, QComboBox, QLineEdit, QDialog, \
    QPushButton, QProgressBar

from main_tabs.tests.gpt_generator import GPTTestGenerator
from side_tabs.builds.commands_list import ScenarioBox
from ui.button import Button

BUTTONS_MAX_WIDTH = 30


class TestTableWidget(QWidget):
    cutTests = pyqtSignal(str)
    copyTests = pyqtSignal(str)
    pasteTests = pyqtSignal(str)
    deleteTests = pyqtSignal(str)
    undo = pyqtSignal()

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

        self._build_box = ScenarioBox(self.sm, self.bm, self.tm)
        self._build_box.currentIndexChanged.connect(self._on_build_changed)
        self.sm.projectChanged.connect(lambda: self._build_box.load(self.sm.get('build')))
        pos_layout.addWidget(self._build_box)

        pos_buttons_layout = QHBoxLayout()
        pos_layout.addLayout(pos_buttons_layout)
        pos_buttons_layout.addWidget(label := QLabel("Позитивные тесты"))
        self.labels.append(label)

        self.pos_add_button = Button(self.tm, 'buttons/plus', css='Bg')
        self.pos_add_button.setFixedHeight(22)
        self.pos_add_button.setMaximumWidth(BUTTONS_MAX_WIDTH)
        pos_buttons_layout.addWidget(self.pos_add_button)

        self.pos_delete_button = Button(self.tm, 'buttons/delete', css='Bg')
        self.pos_delete_button.setFixedHeight(22)
        self.pos_delete_button.setMaximumWidth(BUTTONS_MAX_WIDTH)
        self.pos_delete_button.clicked.connect(lambda: self.deleteTests.emit('pos'))
        pos_buttons_layout.addWidget(self.pos_delete_button)

        self.pos_button_up = Button(self.tm, 'buttons/button_up', css='Bg')
        self.pos_button_up.setFixedHeight(22)
        self.pos_button_up.setMaximumWidth(BUTTONS_MAX_WIDTH)
        pos_buttons_layout.addWidget(self.pos_button_up)

        self.pos_button_down = Button(self.tm, 'buttons/button_down', css='Bg')
        self.pos_button_down.setFixedHeight(22)
        self.pos_button_down.setMaximumWidth(BUTTONS_MAX_WIDTH)
        pos_buttons_layout.addWidget(self.pos_button_down)

        self.pos_button_copy = Button(self.tm, 'buttons/copy', css='Bg')
        self.pos_button_copy.setFixedHeight(22)
        self.pos_button_copy.setMaximumWidth(BUTTONS_MAX_WIDTH)
        self.pos_button_copy.clicked.connect(lambda: self.copyTests.emit('pos'))
        pos_buttons_layout.addWidget(self.pos_button_copy)

        self.pos_button_cut = Button(self.tm, 'buttons/cut', css='Bg')
        self.pos_button_cut.setFixedHeight(22)
        self.pos_button_cut.setMaximumWidth(BUTTONS_MAX_WIDTH)
        self.pos_button_cut.clicked.connect(lambda: self.cutTests.emit('pos'))
        pos_buttons_layout.addWidget(self.pos_button_cut)

        self.pos_button_paste = Button(self.tm, 'buttons/paste', css='Bg')
        self.pos_button_paste.setFixedHeight(22)
        self.pos_button_paste.setMaximumWidth(BUTTONS_MAX_WIDTH)
        self.pos_button_paste.clicked.connect(lambda: self.pasteTests.emit('pos'))
        pos_buttons_layout.addWidget(self.pos_button_paste)

        # self.pos_button_generate = Button(self.tm, 'generate', css='Bg')
        # self.pos_button_generate.setFixedHeight(22)
        # self.pos_button_generate.clicked.connect(self._generate_pos_tests)
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

        generator_layout = QHBoxLayout()
        neg_layout.addLayout(generator_layout)
        generator_layout.setContentsMargins(0, 0, 0, 0)

        self.button_generate = QPushButton("Сгенерировать")
        self.button_generate.setFixedHeight(22)
        self.button_generate.clicked.connect(self._generate_pos_tests)
        generator_layout.addWidget(self.button_generate)

        self.generator_progress_bar = QProgressBar()
        self.generator_progress_bar.setFixedHeight(22)
        self.generator_progress_bar.hide()
        generator_layout.addWidget(self.generator_progress_bar)

        self.button_cancel = QPushButton("Отмена")
        self.button_cancel.setFixedSize(100, 22)
        self.button_cancel.hide()
        generator_layout.addWidget(self.button_cancel)

        neg_buttons_layout = QHBoxLayout()
        neg_layout.addLayout(neg_buttons_layout)
        neg_buttons_layout.addWidget(label := QLabel("Негативные тесты"))
        self.labels.append(label)

        self.neg_add_button = Button(self.tm, 'buttons/plus', css='Bg')
        self.neg_add_button.setFixedHeight(22)
        self.neg_add_button.setMaximumWidth(BUTTONS_MAX_WIDTH)
        neg_buttons_layout.addWidget(self.neg_add_button)

        self.neg_delete_button = Button(self.tm, 'buttons/delete', css='Bg')
        self.neg_delete_button.setFixedHeight(22)
        self.neg_delete_button.setMaximumWidth(BUTTONS_MAX_WIDTH)
        self.neg_delete_button.clicked.connect(lambda: self.deleteTests.emit('neg'))
        neg_buttons_layout.addWidget(self.neg_delete_button)

        self.neg_button_up = Button(self.tm, 'buttons/button_up', css='Bg')
        self.neg_button_up.setFixedHeight(22)
        self.neg_button_up.setMaximumWidth(BUTTONS_MAX_WIDTH)
        neg_buttons_layout.addWidget(self.neg_button_up)

        self.neg_button_down = Button(self.tm, 'buttons/button_down', css='Bg')
        self.neg_button_down.setFixedHeight(22)
        self.neg_button_down.setMaximumWidth(BUTTONS_MAX_WIDTH)
        neg_buttons_layout.addWidget(self.neg_button_down)

        self.neg_button_copy = Button(self.tm, 'buttons/copy', css='Bg')
        self.neg_button_copy.setFixedHeight(22)
        self.neg_button_copy.setMaximumWidth(BUTTONS_MAX_WIDTH)
        self.neg_button_copy.clicked.connect(lambda: self.copyTests.emit('neg'))
        neg_buttons_layout.addWidget(self.neg_button_copy)

        self.neg_button_paste = Button(self.tm, 'buttons/paste', css='Bg')
        self.neg_button_paste.setFixedHeight(22)
        self.neg_button_paste.setMaximumWidth(BUTTONS_MAX_WIDTH)
        self.neg_button_paste.clicked.connect(lambda: self.pasteTests.emit('neg'))
        neg_buttons_layout.addWidget(self.neg_button_paste)

        self.neg_button_cut = Button(self.tm, 'buttons/cut', css='Bg')
        self.neg_button_cut.setFixedHeight(22)
        self.neg_button_cut.setMaximumWidth(BUTTONS_MAX_WIDTH)
        self.neg_button_cut.clicked.connect(lambda: self.cutTests.emit('neg'))
        neg_buttons_layout.addWidget(self.neg_button_cut)

        # self.neg_button_generate = Button(self.tm, 'generate', css='Bg')
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

    def _generate_pos_tests(self):
        self.button_generate.hide()
        self.generator_progress_bar.show()
        self.button_cancel.show()

        # for el in [self.po]:
        #     pass

        generator = GPTTestGenerator(self.bm)
        generator.finished.connect(self._on_generation_finished)
        generator.progressChanged.connect(self._on_progress_changed)
        self.bm.run_process(generator, 'gpt_test_generator', self.sm.project.path())

    def _on_progress_changed(self, current_progress, max_progress):
        self.generator_progress_bar.setMaximum(max_progress)
        self.generator_progress_bar.setValue(current_progress)

    def _on_generation_finished(self):
        self.generator_progress_bar.hide()
        self.button_cancel.hide()
        self.button_generate.show()

    def set_theme(self):
        self.tm.set_theme_to_list_widget(self.pos_test_list)
        self.tm.set_theme_to_list_widget(self.neg_test_list)
        for el in [self.pos_add_button, self.pos_delete_button, self.pos_button_up, self.pos_button_down,
                   self.pos_button_copy, self.pos_button_paste, self.pos_button_cut,
                   self.neg_add_button, self.neg_delete_button,
                   self.neg_button_up, self.neg_button_down, self.neg_button_copy, self.neg_button_paste,
                   self.neg_button_cut, self.pos_comparator_widget, self.neg_comparator_widget,
                   self.button_generate, self.generator_progress_bar, self.button_cancel]:
            self.tm.auto_css(el)
        for label in self.labels:
            label.setFont(self.tm.font_medium)
        self._build_box.set_theme()
        for el in self._windows:
            if hasattr(el, 'set_theme'):
                el.set_theme()

    def keyPressEvent(self, a0: typing.Optional[QtGui.QKeyEvent]) -> None:
        match a0.key():
            case Qt.Key.Key_X:
                if self.ctrl_pressed:
                    self.cutTests.emit('')
            case Qt.Key.Key_C:
                if self.ctrl_pressed:
                    self.copyTests.emit('')
            case Qt.Key.Key_V:
                if self.ctrl_pressed:
                    self.pasteTests.emit('')
            case Qt.Key.Key_Z:
                if self.ctrl_pressed:
                    self.undo.emit()
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
