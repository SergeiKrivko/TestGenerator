from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QVBoxLayout, QLineEdit, QTextEdit, QHBoxLayout, QPushButton, QLabel, QFileDialog, QWidget, \
    QMenu

from backend.backend_manager import BackendManager
from side_tabs.telegram.telegram_api import tg
from ui.button import Button
from ui.custom_dialog import CustomDialog


class SendMessageDialog(CustomDialog):
    TEXT_ONLY = 0
    FILE = 1
    IMAGE = 2
    PROJECT = 3
    VIDEO = 4

    def __init__(self, bm: BackendManager, tm, chat: tg.Chat, text='', option=0):
        super().__init__(tm, "Отправка сообщения")
        self._bm = bm
        self._tm = tm
        self._chat = chat
        self._option = option
        super().set_theme()

        self.setFixedSize(400, 300)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self._chat_label = QLabel(chat.title)
        layout.addWidget(self._chat_label)

        match self._option:
            case SendMessageDialog.FILE:
                path, _ = QFileDialog.getOpenFileName(caption="Выберите файл для отправки")
                if not path:
                    self.reject()
                    return
                self.specific_widget = QLineEdit()
                self.specific_widget.setText(path)
                self.specific_widget.setReadOnly(True)
                layout.addWidget(self.specific_widget)
            case SendMessageDialog.PROJECT:
                self.specific_widget = ProjectWidget(self._bm, self._tm)
                layout.addWidget(self.specific_widget)

        self.text_area = QTextEdit()
        self.text_area.setText(text)
        layout.addWidget(self.text_area)

        buttons_layout = QHBoxLayout()
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        layout.addLayout(buttons_layout)

        self._button_cancel = QPushButton("Отмена")
        self._button_cancel.clicked.connect(self.reject)
        buttons_layout.addWidget(self._button_cancel)

        self._button_add = QPushButton("Добавить")
        self._button_add.clicked.connect(self.reject)
        buttons_layout.addWidget(self._button_add)
        self._button_add.hide()

        self._button_send = QPushButton("Отправить")
        # self._button_send.clicked.connect(self.accept)
        self._button_send.clicked.connect(self._send)
        buttons_layout.addWidget(self._button_send)

        for el in [self._chat_label, self.text_area, self._button_add, self._button_send, self._button_cancel]:
            self._tm.auto_css(el, padding=True)
        if hasattr(self.specific_widget,'set_theme'):
            self.specific_widget.set_theme()
        else:
            self._tm.auto_css(self.specific_widget)

    def _send(self):
        match self._option:
            case SendMessageDialog.FILE:
                tg.sendMessage(self._chat.id, input_message_content=tg.InputMessageDocument(
                    document=tg.InputFileLocal(path=self.specific_widget.text()),
                    caption=tg.FormattedText(text=self.text_area.toPlainText())))
            case SendMessageDialog.PROJECT:
                path = f"{self._bm.sm.temp_dir()}/{self._bm.sm.project.name()}.TGProject.7z"
                self._bm.project_to_zip(path).finished.connect(
                    lambda: tg.sendMessage(self._chat.id, input_message_content=tg.InputMessageDocument(
                        document=tg.InputFileLocal(path=path),
                        caption=tg.FormattedText(text=self.text_area.toPlainText()))))
        self.accept()


class ProjectWidget(QWidget):
    def __init__(self, bm, tm):
        super().__init__()
        self._bm = bm
        self._tm = tm

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)

        self._button = Button(self._tm, 'buttons/button_projects')
        self._button.setFixedSize(32, 32)
        main_layout.addWidget(self._button)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addLayout(layout)

        self._label1 = QLabel("Проект")
        layout.addWidget(self._label1)

        self._label2 = QLabel(self._bm.sm.project.name())
        layout.addWidget(self._label2)

    def set_theme(self):
        for el in [self._button, self._label1, self._label2]:
            self._tm.auto_css(el)


class MessageTypeMenu(QMenu):
    def __init__(self, tm):
        super().__init__()
        self._tm = tm
        self.selected_type = 0

        action = self.addAction(QIcon(self._tm.get_image('icons/telegram_document')), "Файл")
        action.triggered.connect(lambda: self.set_type(SendMessageDialog.FILE))

        action = self.addAction(QIcon(self._tm.get_image('buttons/button_preview')), "Изображение")
        action.triggered.connect(lambda: self.set_type(SendMessageDialog.IMAGE))

        action = self.addAction(QIcon(self._tm.get_image('icons/projects')), "Текущий проект")
        action.triggered.connect(lambda: self.set_type(SendMessageDialog.PROJECT))

        self._tm.auto_css(self)

    def set_type(self, t):
        self.selected_type = t
