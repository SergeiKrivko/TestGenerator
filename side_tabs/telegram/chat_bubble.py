import shutil

from PyQt6 import QtGui
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFontMetrics, QPixmap
from PyQt6.QtWidgets import QLabel, QHBoxLayout, QWidget, QVBoxLayout, QFileDialog

from side_tabs.telegram.telegram_api import types
from side_tabs.telegram.telegram_manager import TelegramManager
from ui.button import Button
from ui.message_box import MessageBox


class TelegramChatBubble(QWidget):
    _BORDER_RADIUS = 10

    def __init__(self, tm, message: types.TgMessage, manager: TelegramManager):
        super().__init__()
        self._tm = tm
        self._message = message
        self._manager = manager
        self._right_side = isinstance(message.sender_id, types.TgMessageSenderUser) and message.sender_id.user_id == \
                           self._manager.get('my_id')

        if isinstance(message.content, types.TgMessageText):
            self._text = message.content.text.text
        elif isinstance(message.content, (types.TgMessageDocument, types.TgMessagePhoto, types.TgMessageVideo)):
            self._text = message.content.caption.text
        else:
            self._text = ''

        main_layout = QHBoxLayout()
        main_layout.setDirection(QHBoxLayout.Direction.RightToLeft if self._right_side else
                                 QHBoxLayout.Direction.LeftToRight)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignLeft if self._right_side else Qt.AlignmentFlag.AlignRight)
        self.setLayout(main_layout)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self._main_widget = QWidget()
        main_layout.addWidget(self._main_widget)

        self._layout = QVBoxLayout()
        self._layout.setSpacing(0)
        self._layout.setContentsMargins(1, 1, 1, 1)
        self._main_widget.setLayout(self._layout)

        if isinstance(self._message.sender_id, types.TgMessageSenderUser):
            user = self._manager.get_user(self._message.sender_id.user_id)
            user_name = f"{user.first_name} {user.last_name}"
        elif isinstance(self._message.sender_id, types.TgMessageSenderChat):
            chat = self._manager.get_chat(self._message.sender_id.chat_id)
            user_name = chat.title
        else:
            user_name = ""
        self._sender_label = QLabel(user_name)
        self._sender_label.setContentsMargins(10, 2, 10, 2)
        self._layout.addWidget(self._sender_label)

        if isinstance(self._message.content, types.TgMessagePhoto):
            self._photo_label = _PhotoLabel(self._tm, self._message.content.photo.sizes[-1].photo)
            self._manager.updateFile.connect(self._photo_label.update_image)
            self._layout.addWidget(self._photo_label)

        if isinstance(self._message.content, types.TgMessageDocument):
            self._document_widget = _DocumentWidget(self._tm, self._message.content.document, self._manager)
            self._layout.addWidget(self._document_widget)

        font_metrics = QFontMetrics(self._tm.font_medium)

        self._label = QLabel(self._text)
        self._label.setContentsMargins(7, 4, 7, 7)
        self._label.setWordWrap(True)
        self._label.setMaximumWidth(font_metrics.size(0, self._text).width() + 20)
        self._label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse |
                                            Qt.TextInteractionFlag.TextSelectableByKeyboard)
        self._layout.addWidget(self._label, 10)

        widget = QWidget()
        main_layout.addWidget(widget, 1)

    def hide_sender(self):
        self._sender_label.hide()
        self._layout.setContentsMargins(1, 7, 1, 1)

    def set_read(self):
        self._manager.view_messages(self._message.chat_id, [self._message.id])

    def set_max_width(self, width):
        self._main_widget.setMaximumWidth(width)
        if hasattr(self, '_photo_label'):
            self._photo_label.setMaximumWidth(width)
            self._photo_label.resize_pixmap()

    def set_theme(self):
        css = f"""color: {self._tm['TextColor']}; 
            background-color: {self._tm['BgColor']};
            border: 1px solid {self._tm['BorderColor']};
            border-top-left-radius: {TelegramChatBubble._BORDER_RADIUS}px;
            border-top-right-radius: {TelegramChatBubble._BORDER_RADIUS}px;
            border-bottom-left-radius: {0 if not self._right_side else TelegramChatBubble._BORDER_RADIUS}px;
            border-bottom-right-radius: {0 if self._right_side else TelegramChatBubble._BORDER_RADIUS}px;"""
        self._main_widget.setStyleSheet(css)
        self._main_widget.setFont(self._tm.font_medium)
        self._label.setStyleSheet("border: none;")
        self._label.setFont(self._tm.font_medium)
        self._sender_label.setStyleSheet(f"color: {self._tm['TestPassed'].name()}; border: none;")
        self._sender_label.setFont(self._tm.font_small)
        if hasattr(self, '_photo_label'):
            self._photo_label.setStyleSheet("border: none;")
        if hasattr(self, '_document_widget'):
            self._document_widget.set_theme()


class _PhotoLabel(QLabel):
    MAX_HEIGHT = 600

    def __init__(self, tm, file: types.TgFile):
        super().__init__()
        self._tm = tm
        self._photo = file
        self._pixmap = None
        if self._photo.local.is_downloading_completed:
            self._pixmap = QPixmap(self._photo.local.path)
            self.resize_pixmap()
        else:
            self._photo.download()

    def update_image(self, image: types.TgFile):
        if isinstance(self._photo, types.TgFile) and image.id == self._photo.id and \
                self._photo.local.is_downloading_completed:
            self._pixmap = QPixmap(self._photo.local.path)
            self.resize_pixmap()

    def resize_pixmap(self):
        if isinstance(self._pixmap, QPixmap):
            pixmap = self._pixmap
            if self._pixmap.width() > self.maximumWidth() or self._pixmap.height() > self.MAX_HEIGHT:
                pixmap = self._pixmap.scaled(self.maximumWidth(), _PhotoLabel.MAX_HEIGHT,
                                             Qt.AspectRatioMode.KeepAspectRatio)
            self.setPixmap(pixmap)

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        super().resizeEvent(a0)
        self.resize_pixmap()


class _DocumentWidget(QWidget):
    def __init__(self, tm, document: types.TgDocument, manager):
        super().__init__()
        self._tm = tm
        self._document = document
        self._manager = manager
        self._saving = False
        self._path = ''
        self._importing = False

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self._button_save = Button(self._tm, "telegram_save", css='Bg')
        self._button_save.setFixedSize(40, 40)
        self._button_save.clicked.connect(self.save)
        layout.addWidget(self._button_save)

        self._button_import = Button(self._tm, "telegram_import", css='Bg')
        self._button_import.setFixedSize(40, 40)
        layout.addWidget(self._button_import)

        self._name_label = QLabel(self._document.file_name)
        layout.addWidget(self._name_label)
        self._name_label.setMinimumWidth(100)

        self._manager.updateFile.connect(self._on_file_updated)

    def set_theme(self):
        self.setStyleSheet("border: none;")
        for el in [self._button_save, self._button_import, self._name_label]:
            self._tm.auto_css(el)

    def save(self):
        if '.' in self._document.file_name:
            extension = '.' + self._document.file_name.split('.')[-1]
        else:
            extension = ''
        self._path = QFileDialog.getSaveFileName(caption="Сохранение файла", filter=extension)[0]
        if not self._path.endswith(extension):
            self._path += extension
        if self._path:
            if self._document.document.local.is_downloading_completed:
                self._continue_saving()
            else:
                self._saving = True
                if not self._document.document.local.is_downloading_active:
                    self._document.document.download()

    def _on_file_updated(self, file: types.TgFile):
        if file.id == self._document.document.id and self._document.document.local.is_downloading_completed:
            if self._saving:
                self._continue_saving()

    def _continue_saving(self):
        self._saving = False
        try:
            shutil.copy(self._document.document.local._path, self._path)
        except Exception as ex:
            MessageBox(MessageBox.Warning, "Ошибка", f"Не удалось сохранить файл {self._document.file_name}:\n"
                                                          f"{ex.__class__.__name__}: {ex}", self._tm)
