from PyQt6.Qsci import QsciScintilla
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QColor
from PyQtUIkit.core import IntProperty, FontProperty, EnumProperty, KitFont
from PyQtUIkit.widgets import *
from PyQtUIkit.widgets._widget import _KitWidget

from src.other.binary_redactor.lexer import LexerBin


class BinaryRedactor(QsciScintilla, _KitWidget):
    border = IntProperty('border', 1)
    radius = IntProperty('radius', 0)
    font = FontProperty('font', 'mono')
    font_size = EnumProperty('font_size', KitFont.Size, KitFont.Size.MEDIUM)

    def __init__(self):
        super().__init__(None)
        self.setLexer(None)  # We install lexer later
        self.setUtf8(True)  # Set encoding to UTF-8

        # 1. Text wrapping
        # -----------------
        self.setWrapMode(QsciScintilla.WrapMode.WrapWord)
        self.setWrapVisualFlags(QsciScintilla.WrapVisualFlag.WrapFlagByText)
        self.setWrapIndentMode(QsciScintilla.WrapIndentMode.WrapIndentIndented)

        # 3. Indentation
        # ---------------
        # self.setIndentationsUseTabs(False)
        # self.setTabWidth(4)
        # self.setIndentationGuides(True)
        # self.setTabIndents(True)
        # self.setAutoIndent(True)

        # 4. Caret
        # ---------
        self.setCaretLineVisible(True)
        self.setCaretWidth(2)

        # 5. Margins
        # -----------
        # Margin 0 = Line nr margin
        self.setMargins(0)
        # self.setMarginType(0, QsciScintilla.NumberMargin)
        # self.setMarginWidth(0, "0000")

        self.__lexer = LexerBin(self)
        self.setLexer(self.__lexer)

    def open_text(self, text: str, bin_code=False):
        self.__lexer.bin_code = bin_code
        if self._tm:
            if bin_code:
                self.__lexer.setColor(self._tm.palette('Keyword'), LexerBin.Mask)
            else:
                self.__lexer.setColor(QColor(self._tm.palette('Main').text), LexerBin.Mask)
        self.setText(text)

    def _apply_theme(self):
        if not self._tm or not self._tm.active:
            return
        self.setStyleSheet(f"""
QsciScintilla {{
    background-color: {self.main_palette.main};
    border: {self.border}px solid {self.border_palette.main};
    border-radius: {self.radius};
}}
QsciScintilla QScrollBar:vertical {{
    background: {self.main_palette.main};
    width: 12px;
    margin: 0px;
}}
QsciScintilla QScrollBar::handle::vertical {{
    background-color: {self.border_palette.main};
    margin: 2px 2px 2px 6px;
    border-radius: 2px;
    min-height: 20px;
}}
QsciScintilla QScrollBar::handle::vertical:hover {{
    margin: 2px;
    border-radius: 4px;
}}
QsciScintilla QScrollBar::sub-page, QScrollBar::add-page {{
    background: none;
}}
QsciScintilla QScrollBar::sub-line, QScrollBar::add-line {{
    background: none;
    height: 0px;
    subcontrol-position: left;
    subcontrol-origin: margin;
}}""")
        self.setCaretForegroundColor(QColor(self._tm.palette('Main').text))
        self.setCaretLineBackgroundColor(QColor(self._tm.palette('Main').main))
        self.__lexer.setDefaultFont(self.font.get(self.font_size))
        self.__lexer.setDefaultPaper(QColor(self._tm.palette('Main').main))
        self.__lexer.setColor(QColor(self._tm.code_color('Keyword')) if self.__lexer.bin_code else QColor(self._tm.palette('Main').text),
                              LexerBin.Mask)
        self.__lexer.setPaper(QColor(self._tm.palette('Main').main), LexerBin.Mask)
        self.__lexer.setColor(self._tm.code_color('Identifier'), LexerBin.Value)
        self.__lexer.setPaper(QColor(self._tm.palette('Main').main), LexerBin.Value)
        self.__lexer.setColor(self._tm.code_color('Preprocessor'), LexerBin.PreProcessor)
        self.__lexer.setPaper(QColor(self._tm.palette('Main').main), LexerBin.PreProcessor)
        self.__lexer.setColor(self._tm.code_color('Danger'), LexerBin.InvalidMask)
        self.__lexer.setPaper(QColor(self._tm.palette('Main').hover), LexerBin.InvalidMask)
        self.__lexer.setColor(self._tm.code_color('Danger'), LexerBin.InvalidValue)
        self.__lexer.setPaper(QColor(self._tm.palette('Main').hover), LexerBin.InvalidValue)
        self.__lexer.setColor(self._tm.code_color('Comment'), LexerBin.Comment)
        self.__lexer.setPaper(QColor(self._tm.palette('Main').main), LexerBin.Comment)
        self.__lexer.setColor(QColor(self._tm.palette('Main').text), LexerBin.Default)
        self.__lexer.setPaper(QColor(self._tm.palette('Main').main), LexerBin.Default)


class RedactorWidget(KitVBoxLayout):
    textChanged = pyqtSignal(str, str)
    tabCloseRequested = pyqtSignal(int)
    currentChanged = pyqtSignal(int)
    addTab = pyqtSignal()

    def __init__(self):
        super().__init__()

        top_layout = KitHBoxLayout()
        top_layout.setFixedHeight(26)
        top_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        top_layout.setSpacing(2)
        self.addWidget(top_layout)

        self._tab_bar = KitTabBar()
        self._tab_bar.addTab("rehsernn")
        self._tab_bar.setTabsClosable(True)
        self._tab_bar.tabCloseRequested.connect(self.tabCloseRequested.emit)
        # self._tab_bar.currentChanged.connect(print)
        top_layout.addWidget(self._tab_bar)

        self._button = KitIconButton('line-add')
        self._button.setFixedSize(20, 20)
        self._button.clicked.connect(self.addTab.emit)
        top_layout.addWidget(self._button)

        self._redactors_layout = KitTabLayout()
        self._redactors_layout.addWidget(KitHBoxLayout())
        self._redactors_layout.connect(self._tab_bar)
        self.addWidget(self._redactors_layout)

        self._empty_widget = KitHBoxLayout()
        self._empty_widget.border = 1
        self._empty_widget.radius = 0
        # self._redactors_layout.addWidget(self._empty_widget)

        self.redactors = dict()
        self.current_tab = ''
        self._disabled = False

    def add_tab(self, name, text=''):
        redactor = BinaryRedactor()
        self._redactors_layout.addWidget(redactor)
        redactor.open_text(text, name.endswith('.bin'))
        redactor.textChanged.connect(lambda: self.textChanged.emit(name, redactor.text()))
        self.redactors[name] = redactor
        self._tab_bar.addTab(KitTab(name))

    def remove_tab(self, name):
        if isinstance(name, str):
            for i in range(self._tab_bar.count()):
                if self._tab_bar.tabText(i) == name:
                    self._tab_bar.removeTab(i)
                    break
        else:
            self._tab_bar.removeTab(name)
        self._redactors_layout.removeWidget(self.redactors[name])
        self.redactors.pop(name)

    def select_tab(self, index: int | str):
        if isinstance(index, str):
            for i in range(self._tab_bar.count()):
                if self._tab_bar.tab(i).text() == index:
                    index = i
                    break
        if index is None or index > self._tab_bar.tabsCount():
            return
        self._tab_bar.setCurrentTab(index)

    def count(self):
        return self._tab_bar.count()

    def _on_tab_selected(self):
        index = self._tab_bar.currentIndex()
        self._button.setHidden(self._disabled)

        self._redactors_layout.setCurrent(index)

        self.currentChanged.emit(index)

    def clear(self):
        self._tab_bar.clear()
        self._redactors_layout.clear()

    def tab_text(self, index=None):
        if index is None:
            index = self._tab_bar.currentIndex()
        return self._tab_bar.tabText(index)

    def tab_index(self, name: str = None):
        if name is None:
            return self._tab_bar.currentIndex()
        for i in range(self._tab_bar.count()):
            if self._tab_bar.tabText(i) == name:
                return i

    def setDisabled(self, a0: bool) -> None:
        self._disabled = a0
        if a0:
            for el in self.redactors.values():
                el.hide()
            self._empty_widget.show()
            self._button.hide()
        else:
            self._empty_widget.hide()
            self._button.show()
        super().setDisabled(a0)
