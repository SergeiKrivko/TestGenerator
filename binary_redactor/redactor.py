from PyQt5.Qsci import QsciScintilla
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QTabBar, QWidget, QVBoxLayout, QHBoxLayout

from binary_redactor.lexer import LexerBin
from ui.button import Button


class BinaryRedactor(QsciScintilla):
    def __init__(self, tm):
        super().__init__(None)
        self.setLexer(None)  # We install lexer later
        self.setUtf8(True)  # Set encoding to UTF-8
        self.tm = tm

        # 1. Text wrapping
        # -----------------
        self.setWrapMode(QsciScintilla.WrapWord)
        self.setWrapVisualFlags(QsciScintilla.WrapFlagByText)
        self.setWrapIndentMode(QsciScintilla.WrapIndentIndented)

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
        if bin_code:
            self.__lexer.setColor(self.tm['Keyword'], LexerBin.Mask)
        else:
            self.__lexer.setColor(QColor(self.tm['TextColor']), LexerBin.Mask)
        self.setText(text)

    def set_theme(self):
        self.setStyleSheet(self.tm.scintilla_css(True).replace(self.tm['Paper'].name(), self.tm['MainColor']))
        self.setCaretForegroundColor(QColor(self.tm['TextColor']))
        self.setCaretLineBackgroundColor(QColor(self.tm['MainColor']))
        self.__lexer.setDefaultFont(self.tm.code_font)
        self.__lexer.setDefaultPaper(QColor(self.tm['MainColor']))
        self.__lexer.setColor(self.tm['Keyword'], LexerBin.Mask)
        self.__lexer.setPaper(QColor(self.tm['MainColor']), LexerBin.Mask)
        self.__lexer.setColor(self.tm['Identifier'], LexerBin.Value)
        self.__lexer.setPaper(QColor(self.tm['MainColor']), LexerBin.Value)
        self.__lexer.setColor(self.tm['Preprocessor'], LexerBin.PreProcessor)
        self.__lexer.setPaper(QColor(self.tm['MainColor']), LexerBin.PreProcessor)
        self.__lexer.setColor(self.tm['String'], LexerBin.InvalidMask)
        self.__lexer.setPaper(self.tm['CaretLineBackgroundColor'], LexerBin.InvalidMask)
        self.__lexer.setColor(self.tm['String'], LexerBin.InvalidValue)
        self.__lexer.setPaper(self.tm['CaretLineBackgroundColor'], LexerBin.InvalidValue)
        self.__lexer.setColor(self.tm['Comment'], LexerBin.Comment)
        self.__lexer.setPaper(QColor(self.tm['MainColor']), LexerBin.Comment)
        self.__lexer.setColor(QColor(self.tm['TextColor']), LexerBin.Default)
        self.__lexer.setPaper(QColor(self.tm['MainColor']), LexerBin.Default)


class RedactorWidget(QWidget):
    textChanged = pyqtSignal(str, str)
    tabCloseRequested = pyqtSignal(int)
    currentChanged = pyqtSignal(int)
    addTab = pyqtSignal()

    def __init__(self, tm):
        super().__init__()
        self.tm = tm

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)
        self.setLayout(main_layout)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        top_layout = QHBoxLayout()
        top_layout.setAlignment(Qt.AlignLeft)
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.setSpacing(2)
        main_layout.addLayout(top_layout)

        self._tab_bar = QTabBar()
        self._tab_bar.setTabsClosable(True)
        self._tab_bar.tabCloseRequested.connect(self.tabCloseRequested.emit)
        self._tab_bar.currentChanged.connect(self._on_tab_selected)
        top_layout.addWidget(self._tab_bar)

        self._button = Button(self.tm, 'plus', css='Bg')
        self._button.setFixedSize(20, 20)
        self._button.clicked.connect(self.addTab.emit)
        top_layout.addWidget(self._button)

        self._redactors_layout = QHBoxLayout()
        main_layout.addLayout(self._redactors_layout)

        self.redactors = dict()
        self.current_tab = ''

    def add_tab(self, name, text=''):
        redactor = BinaryRedactor(self.tm)
        redactor.open_text(text, name.endswith('.bin'))
        redactor.textChanged.connect(lambda: self.textChanged.emit(name, redactor.text()))
        self._redactors_layout.addWidget(redactor)
        redactor.hide()
        self.redactors[name] = redactor
        self._tab_bar.addTab(name)

    def remove_tab(self, name):
        if isinstance(name, str):
            for i in range(self._tab_bar.count()):
                if self._tab_bar.tabText(i) == name:
                    self._tab_bar.removeTab(i)
                    break
        else:
            self._tab_bar.removeTab(name)
        self.redactors[name].hide()
        self.redactors.pop(name)

    def select_tab(self, index: int | str):
        if isinstance(index, str):
            for i in range(self._tab_bar.count()):
                if self._tab_bar.tabText(i) == index:
                    index = i
                    break
        self._tab_bar.setCurrentIndex(index)

    def count(self):
        return self._tab_bar.count()

    def _on_tab_selected(self):
        index = self._tab_bar.currentIndex()
        name = self._tab_bar.tabText(index)
        for el in self.redactors.values():
            el.hide()
        if name in self.redactors:
            self.redactors[name].show()
            self.redactors[name].set_theme()
            self.current_tab = name
        self.currentChanged.emit(index)

    def clear(self):
        for i in range(self._tab_bar.count()):
            self._tab_bar.removeTab(0)
        for el in self.redactors.values():
            el.setParent(None)

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

    def set_theme(self):
        self._button.set_theme()
        palette = 'Bg'
        css = f"""
QTabBar::tab {{
    background-color {self.tm[f'{palette}Color']};
    border: 1px solid {  self.tm['BorderColor']};
    min-width: 8px;
    padding: 2px 5px 2px 5px;
}}
QTabBar::tab:first {{
    border-top-left-radius: 8px;
}}
QTabBar::tab:last {{
    border-top-right-radius: 8px;
}}
QTabBar:tab:hover {{
    background-color: {self.tm[f'{palette}HoverColor']};
}}
QTabBar:tab:selected {{
    border-top-left-radius: 3px;
    border-top-right-radius: 3px;
    background-color: {self.tm[f'{palette}SelectedColor']};
}}
QTabBar::tab:first:selected {{
    border-top-left-radius: 8px;
}}
QTabBar::tab:last:selected {{
    border-top-right-radius: 8px;
}}
QTabBar::tab:!selected {{
    margin-top: 3px;
}}
QTabBar::close-button {{
    image: url({self.tm.get_image('button_close_tab')});
}}
QTabBar::close-button:hover {{
    image: url({self.tm.get_image('button_close_tab_hover')});
}}
"""
        self._tab_bar.setFont(self.tm.font_small)
        self._tab_bar.setStyleSheet(css)
