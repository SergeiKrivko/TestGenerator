from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFontMetrics
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QTextEdit, QMenu


class ChatBubble(QWidget):
    SIDE_LEFT = 0
    SIDE_RIGHT = 1

    _BORDER_RADIUS = 10

    deleteRequested = pyqtSignal()

    def __init__(self, bm, tm, text, side):
        super().__init__()
        self._tm = tm
        self._bm = bm
        self._side = side
        self._text = text
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.run_context_menu)

        layout = QHBoxLayout()
        layout.setDirection(QHBoxLayout.Direction.LeftToRight if self._side == ChatBubble.SIDE_LEFT
                            else QHBoxLayout.Direction.RightToLeft)
        layout.setAlignment(
            Qt.AlignmentFlag.AlignLeft if self._side == ChatBubble.SIDE_LEFT else Qt.AlignmentFlag.AlignRight)
        self.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)

        self._font_metrics = QFontMetrics(self._tm.font_medium)

        self._text_edit = QTextEdit()
        self._text_edit.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        self._text_edit.setMaximumWidth(self._font_metrics.size(0, self._text).width() + 20)
        self._text_edit.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._text_edit.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByMouse)
        self._text_edit.setMarkdown(text)
        self._text_edit.setReadOnly(True)
        self._text_edit.textChanged.connect(self._resize)
        layout.addWidget(self._text_edit, 10)

        widget = QWidget()
        layout.addWidget(widget, 1)

    def run_context_menu(self, pos):
        menu = ContextMenu(self._tm)
        menu.move(self.mapToGlobal(pos))
        menu.exec()
        match menu.action:
            case ContextMenu.DELETE_MESSAGE:
                self.deleteRequested.emit()
            case ContextMenu.COPY_AS_TEXT:
                pass
            case ContextMenu.SELECT_ALL:
                self._text_edit.selectAll()
                self._text_edit.setFocus()

    def resizeEvent(self, a0) -> None:
        super().resizeEvent(a0)
        self._resize()

    def showEvent(self, a0) -> None:
        super().showEvent(a0)
        self._resize()

    def _resize(self):
        self._text_edit.setFixedHeight(10)
        self._text_edit.setFixedHeight(10 + self._text_edit.verticalScrollBar().maximum())

    def add_text(self, text: str):
        self._text += text
        self._text_edit.setMarkdown(self._text)
        self._text_edit.setMaximumWidth(self._font_metrics.size(0, self._text).width() + 20)

    def text(self):
        return self._text

    def set_theme(self):
        css = f"""color: {self._tm['TextColor']}; 
            background-color: {self._tm['BgColor']};
            border: 1px solid {self._tm['BorderColor']};
            border-top-left-radius: {ChatBubble._BORDER_RADIUS}px;
            border-top-right-radius: {ChatBubble._BORDER_RADIUS}px;
            border-bottom-left-radius: {0 if self._side == ChatBubble.SIDE_LEFT else ChatBubble._BORDER_RADIUS}px;
            border-bottom-right-radius: {0 if self._side == ChatBubble.SIDE_RIGHT else ChatBubble._BORDER_RADIUS}px;
            padding: 4px;"""
        self._text_edit.setStyleSheet(css)
        self._text_edit.setFont(self._tm.font_medium)


class ContextMenu(QMenu):
    DELETE_MESSAGE = 1
    COPY_AS_TEXT = 2
    SELECT_ALL = 3

    def __init__(self, tm):
        super().__init__()
        self.action = None

        action = self.addAction('Выделить все')
        action.triggered.connect(lambda: self.set_action(ContextMenu.SELECT_ALL))

        action = self.addAction('Копировать как текст')
        action.triggered.connect(lambda: self.set_action(ContextMenu.COPY_AS_TEXT))

        self.addSeparator()

        action = self.addAction('Удалить')
        action.triggered.connect(lambda: self.set_action(ContextMenu.DELETE_MESSAGE))

        self.setStyleSheet(tm.menu_css())

    def set_action(self, action):
        self.action = action
