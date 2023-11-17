import markdown
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFontMetrics
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QTextEdit, QMenu, QLabel, QVBoxLayout
from PyQt6.QtWebEngineWidgets import QWebEngineView

from backend.commands import read_file


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

        v_layout = QVBoxLayout()
        v_layout.setContentsMargins(0, 0, 0, 0)
        v_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addLayout(v_layout, 10)

        self._font_metrics = QFontMetrics(self._tm.font_medium)

        self._text_edit = QTextEdit()
        self._text_edit.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        self._text_edit.setMaximumWidth(self._font_metrics.size(0, self._text).width() + 20)
        self._text_edit.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._text_edit.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByMouse)
        self._set_html()
        self._text_edit.setReadOnly(True)
        self._text_edit.textChanged.connect(self._resize)
        v_layout.addWidget(self._text_edit)

        self._progress_marker = QLabel("GPT печатает...")
        v_layout.addWidget(self._progress_marker)
        self._progress_marker.hide()

        widget = QWidget()
        layout.addWidget(widget, 1)

    def _set_html(self):
        # html = f"<style>{read_file(r'C:/Users/sergi/AppData/Local/SergeiKrivko/TestGenerator/GPT/dialogs/codehilite.css')}</style>\n{markdown.markdown(self._text, extensions=['fenced_code', 'codehilite'])}"
        # self._text_edit.setHtml(html)
        self._text_edit.setMarkdown(self._text)

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
            case ContextMenu.SEND_TO_TELEGRAM:
                self._bm.side_tab_command('telegram', self._text)

    def resizeEvent(self, a0) -> None:
        super().resizeEvent(a0)
        self._resize()

    def showEvent(self, a0) -> None:
        super().showEvent(a0)
        self._resize()

    def start_progress(self):
        self._progress_marker.show()

    def end_progress(self):
        self._progress_marker.hide()

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
    SEND_TO_TELEGRAM = 4

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

        self.addSeparator()

        action = self.addAction('Переслать в Telegram')
        action.triggered.connect(lambda: self.set_action(ContextMenu.SEND_TO_TELEGRAM))

        self.setStyleSheet(tm.menu_css())

    def set_action(self, action):
        self.action = action
