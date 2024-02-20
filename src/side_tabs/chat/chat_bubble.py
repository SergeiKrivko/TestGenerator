from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFontMetrics, QIcon
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QTextEdit, QMenu, QVBoxLayout, QSizePolicy

from src.side_tabs.chat.render_latex import render_latex
from src.side_tabs.chat.reply_widget import ReplyList
from src.side_tabs.chat.message import GPTMessage


class ChatBubble(QWidget):
    SIDE_LEFT = 0
    SIDE_RIGHT = 1

    _BORDER_RADIUS = 10

    deleteRequested = pyqtSignal()
    replyRequested = pyqtSignal()
    scrollRequested = pyqtSignal(int)

    def __init__(self, sm, tm, chat, message: GPTMessage):
        super().__init__()
        self._sm = sm
        self._tm = tm
        self._chat = chat
        self._message = message
        self._side = ChatBubble.SIDE_RIGHT if message.role == 'user' else ChatBubble.SIDE_LEFT

        layout = QHBoxLayout()
        layout.setDirection(QHBoxLayout.Direction.LeftToRight if self._side == ChatBubble.SIDE_LEFT
                            else QHBoxLayout.Direction.RightToLeft)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop |
                            Qt.AlignmentFlag.AlignLeft if self._side == ChatBubble.SIDE_LEFT else Qt.AlignmentFlag.AlignRight)
        self.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)

        self._bubble_widget = QWidget()
        self._bubble_widget.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed))
        self._bubble_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self._bubble_widget.customContextMenuRequested.connect(
            lambda pos: self.run_context_menu(self._bubble_widget.mapToGlobal(pos)))
        layout.addWidget(self._bubble_widget, 10)

        bubble_layout = QVBoxLayout()
        bubble_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        bubble_layout.setContentsMargins(4, 4, 4, 4)
        self._bubble_widget.setLayout(bubble_layout)

        self._reply_widget = ReplyList(self._tm, self._chat, 2)
        self._reply_widget.scrollRequested.connect(self.scrollRequested.emit)
        self._reply_widget.hide()
        bubble_layout.addWidget(self._reply_widget)
        for el in self._message.replys:
            self._reply_widget.add_message(el)

        self._font_metrics = QFontMetrics(self._tm.font_medium)

        self._text_edit = QTextEdit()
        self._text_edit.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self._text_edit.customContextMenuRequested.connect(
            lambda pos: self.run_context_menu(self._text_edit.mapToGlobal(pos)))
        self._bubble_widget.setMaximumWidth(self._font_metrics.size(0, self._message.content).width() + 20)
        self._text_edit.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._text_edit.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._text_edit.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByMouse)
        self._set_html()
        self._text_edit.setReadOnly(True)
        self._text_edit.textChanged.connect(self._resize)
        bubble_layout.addWidget(self._text_edit)

        self._widget = QWidget()
        layout.addWidget(self._widget, 1)

    def _set_html(self):
        self._text_edit.setMarkdown(self.parse_latex())

    def parse_latex(self):
        lst = []

        text = self._message.content.replace('\\(', '\\[').replace('\\)', '\\]')
        while '\\[' in text:
            ind = text.index('\\[')
            lst.append(text[:ind])
            text = text[ind + 2:]

            if '\\]' in text:
                ind = text.index('\\]')
                formula = text[:ind]
                try:
                    lst.append(f"![image.svg]({render_latex(self._sm, self._tm, formula)})")
                except Exception:
                    lst.append(f"\\[ {formula} \\]")
                text = text[ind + 2:]

        lst.append(text)

        return ''.join(lst)

    def run_context_menu(self, pos):
        menu = ContextMenu(self._tm)
        menu.move(pos)
        menu.exec()
        match menu.action:
            case ContextMenu.DELETE_MESSAGE:
                self.deleteRequested.emit()
            case ContextMenu.REPLY:
                self.replyRequested.emit()
            case ContextMenu.COPY_AS_TEXT:
                self._sm.copy_text(self._text_edit.toPlainText())
            case ContextMenu.COPY_AS_MARKDOWN:
                self._sm.copy_text(self._text_edit.toMarkdown())
            case ContextMenu.SELECT_ALL:
                self._text_edit.selectAll()
                self._text_edit.setFocus()
            case ContextMenu.SEND_TO_TELEGRAM:
                self._bm.side_tab_command('telegram', self._message.content)

    def resizeEvent(self, a0) -> None:
        super().resizeEvent(a0)
        self._resize()

    def showEvent(self, a0) -> None:
        super().showEvent(a0)
        self._resize()

    def _resize(self):
        self._text_edit.setFixedHeight(10)
        self._text_edit.setFixedHeight(10 + self._text_edit.verticalScrollBar().maximum())
        self._widget.setFixedHeight(self._text_edit.height())

    def add_text(self, text: str):
        self._message.add_text(text)
        self._text_edit.setMarkdown(self._message.content)
        self._bubble_widget.setMaximumWidth(self._font_metrics.size(0, self._message.content).width() + 20)

    @property
    def text(self):
        return self._message.content

    @property
    def message(self):
        return self._message

    def set_theme(self):
        css = f"""color: {self._tm['TextColor']}; 
            background-color: {self._tm['MenuColor']};
            border: 1px solid {self._tm['BorderColor']};
            border-top-left-radius: {ChatBubble._BORDER_RADIUS}px;
            border-top-right-radius: {ChatBubble._BORDER_RADIUS}px;
            border-bottom-left-radius: {0 if self._side == ChatBubble.SIDE_LEFT else ChatBubble._BORDER_RADIUS}px;
            border-bottom-right-radius: {0 if self._side == ChatBubble.SIDE_RIGHT else ChatBubble._BORDER_RADIUS}px;"""
        self._bubble_widget.setStyleSheet(css)

        self._tm.auto_css(self._text_edit, palette='Menu', border=False)


class ContextMenu(QMenu):
    DELETE_MESSAGE = 1
    COPY_AS_TEXT = 2
    SELECT_ALL = 3
    SEND_TO_TELEGRAM = 4
    COPY_AS_MARKDOWN = 5
    REPLY = 6

    def __init__(self, tm):
        super().__init__()
        self.action = None

        action = self.addAction(QIcon(tm.get_image('buttons/reply')), 'Ответить')
        action.triggered.connect(lambda: self.set_action(ContextMenu.REPLY))

        self.addSeparator()

        action = self.addAction('Выделить все')
        action.triggered.connect(lambda: self.set_action(ContextMenu.SELECT_ALL))

        action = self.addAction(QIcon(tm.get_image('buttons/copy')), 'Копировать как текст')
        action.triggered.connect(lambda: self.set_action(ContextMenu.COPY_AS_TEXT))

        action = self.addAction(QIcon(tm.get_image('files/md')), 'Копировать как Markdown')
        action.triggered.connect(lambda: self.set_action(ContextMenu.COPY_AS_MARKDOWN))

        self.addSeparator()

        action = self.addAction(QIcon(tm.get_image('buttons/button_delete')), 'Удалить')
        action.triggered.connect(lambda: self.set_action(ContextMenu.DELETE_MESSAGE))

        # self.addSeparator()
        #
        # action = self.addAction('Переслать в Telegram')
        # action.triggered.connect(lambda: self.set_action(ContextMenu.SEND_TO_TELEGRAM))

        self.setStyleSheet(tm.menu_css(palette='Menu'))

    def set_action(self, action):
        self.action = action
