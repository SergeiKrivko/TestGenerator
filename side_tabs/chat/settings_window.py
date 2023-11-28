import datetime

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QSpinBox, \
    QDoubleSpinBox, QComboBox

from side_tabs.chat import gpt
from side_tabs.chat.gpt_dialog import GPTDialog
from ui.custom_dialog import CustomDialog


class ChatSettingsWindow(CustomDialog):
    def __init__(self, sm, tm, dialog: GPTDialog):
        super().__init__(tm, "Настройки", True, True)
        self._dialog = dialog
        self.sm = sm

        self._labels = []
        self.setFixedWidth(300)

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        main_layout.addLayout(layout)

        # self._separator = QWidget()
        # self._separator.setFixedHeight(1)
        # main_layout.addWidget(self._separator)

        label = QLabel("Название диалога")
        self._labels.append(label)
        main_layout.addWidget(label)

        self._name_label = QLineEdit()
        main_layout.addWidget(self._name_label)

        self._time_label = QLabel()
        self._labels.append(self._time_label)
        main_layout.addWidget(self._time_label)

        label = QLabel("Модель")
        self._labels.append(label)
        main_layout.addWidget(label)

        self._model_box = QComboBox()
        self._model_box.addItems(gpt.get_models())
        main_layout.addWidget(self._model_box)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        main_layout.addLayout(layout)

        label = QLabel("Используемые сообщения:")
        self._labels.append(label)
        layout.addWidget(label)

        self._used_messages_box = QSpinBox()
        self._used_messages_box.setMinimum(0)
        self._used_messages_box.setMaximum(20)
        layout.addWidget(self._used_messages_box)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        main_layout.addLayout(layout)

        label = QLabel("Максимум сообщений:")
        self._labels.append(label)
        layout.addWidget(label)

        self._saved_messages_box = QSpinBox()
        self._saved_messages_box.setMinimum(0)
        self._saved_messages_box.setMaximum(200)
        layout.addWidget(self._saved_messages_box)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        main_layout.addLayout(layout)

        label = QLabel("Temperature:")
        self._labels.append(label)
        layout.addWidget(label)

        self._temperature_box = QDoubleSpinBox()
        self._temperature_box.setMinimum(0)
        self._temperature_box.setMaximum(1)
        self._temperature_box.setSingleStep(0.01)
        layout.addWidget(self._temperature_box)

        if self._dialog is not None:
            self._model_box.setCurrentText(self._dialog.model)
            self._temperature_box.setValue(self._dialog.temperature)
            self._saved_messages_box.setValue(self._dialog.saved_messages)
            self._used_messages_box.setValue(self._dialog.used_messages)
            self._time_label.setText(f"Создан: {datetime.datetime.fromtimestamp(self._dialog.time).strftime('%D %H:%M')}")
            self._name_label.setText(self._dialog.name)
        else:
            self._temperature_box.hide()
            self._saved_messages_box.hide()
            self._used_messages_box.hide()
            self._model_box.hide()
            self._time_label.hide()
            self._name_label.hide()
            for el in self._labels[1:]:
                el.hide()

    def save(self):
        if self._dialog is not None:
            self._dialog.name = self._name_label.text()
            self._dialog.used_messages = self._used_messages_box.value()
            self._dialog.saved_messages = self._saved_messages_box.value()
            self._dialog.temperature = self._temperature_box.value()
            self._dialog.model = self._model_box.currentText()

    def showEvent(self, a0) -> None:
        super().showEvent(a0)
        self.set_theme()

    def set_theme(self):
        super().set_theme()
        for el in self._labels:
            self.tm.auto_css(el)
        for el in [self._name_label, self._used_messages_box, self._saved_messages_box, self._temperature_box,
                   self._model_box]:
            self.tm.auto_css(el)
        # self._separator.setStyleSheet(f"background-color: {self.tm['BorderColor']};")

