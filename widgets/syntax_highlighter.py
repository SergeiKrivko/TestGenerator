from PyQt5.QtGui import QFont, QColor, QFontMetrics
from PyQt5.Qsci import QsciScintilla, QsciLexerCPP, QsciAPIs
from other.code_autocompletion import CodeAutocompletionManager


class CodeEditor(QsciScintilla):
    ARROW_MARKER_NUM = 8

    def __init__(self, sm, tm, parent=None):
        super(CodeEditor, self).__init__(parent)

        # Set the default font
        font = QFont()
        font.setFamily('Courier')
        font.setFixedPitch(True)
        font.setPointSize(10)
        self.setFont(font)
        self.setMarginsFont(font)
        self.sm = sm
        self.tm = tm

        # Margin 0 is used for line numbers
        fontmetrics = QFontMetrics(font)
        self.setMarginsFont(font)
        self.setMarginWidth(0, fontmetrics.width("00000") + 6)
        self.setMarginLineNumbers(0, True)

        # Clickable margin 1 for showing markers
        self.setMarginSensitivity(1, True)
        self.markerDefine(QsciScintilla.RightArrow,
                          self.ARROW_MARKER_NUM)

        # Brace matching: enable for a brace immediately before or after
        # the current position
        #
        self.setBraceMatching(QsciScintilla.SloppyBraceMatch)

        # Current line visible with special background color
        self.setCaretLineVisible(True)

        self._lexer = QsciLexerCPP(None)
        self._lexer.setDefaultFont(font)
        self.setLexer(self._lexer)

        self.setAutoCompletionSource(QsciScintilla.AcsAPIs)
        self.setAutoCompletionThreshold(1)
        self.setAutoCompletionCaseSensitivity(True)
        self.setAutoCompletionReplaceWord(True)
        self.setCallTipsStyle(QsciScintilla.CallTipsContext)
        self.setCallTipsPosition(QsciScintilla.CallTipsAboveText)

        self.setIndentationsUseTabs(False)
        self.setTabWidth(4)
        self.setIndentationGuides(True)
        self.setTabIndents(True)
        self.setAutoIndent(True)

        text = bytearray(str.encode("Courier"))
        self.SendScintilla(QsciScintilla.SCI_STYLESETFONT, 1, text)

        self.SendScintilla(QsciScintilla.SCI_SETHSCROLLBAR, 0)

        self.setCallTipsVisible(0)

        self.path = ""
        self.current_file = ""
        self.current_row = 0
        self.am = CodeAutocompletionManager(self.sm, self.path)
        self.textChanged.connect(self.set_text_changed)
        self.cursorPositionChanged.connect(lambda: self.update_api(self.getCursorPosition()))
        self.text_changed = False

    def set_text_changed(self):
        self.text_changed = True

    def set_theme(self):
        self.setMarkerBackgroundColor(QColor(self.tm['TextColor']), self.ARROW_MARKER_NUM)
        self.setMarginsBackgroundColor(QColor(self.tm['BgColor']))
        for key, item in self.tm.code_colors():
            self._lexer.setColor(item, QsciLexerCPP.__dict__[key])
        self._lexer.setPaper(self.tm['Paper'])
        self.setCaretLineBackgroundColor(self.tm['CaretLineBackgroundColor'])
        self.setMatchedBraceBackgroundColor(self.tm['CaretLineBackgroundColor'])
        self.setMatchedBraceForegroundColor(self.tm['BraceColor'])
        self.setStyleSheet(f"""
                QsciScintilla {{
                {self.tm.style_sheet}
                }}
                QsciScintilla QScrollBar:vertical {{
                background: rgba{self.tm['Paper'].getRgb()};
                border-top-right-radius: 5px;
                border-bottom-right-radius: 5px;
                width: 12px;
                margin: 0px;
                }}
                QsciScintilla QScrollBar::handle::vertical {{
                background-color: {self.tm['BorderColor']};
                margin: 2px;
                border-radius: 4px;
                min-height: 20px;
                }}
                QsciScintilla QScrollBar::sub-page, QScrollBar::add-page {{
                background: none;
                }}
                QsciScintilla QScrollBar::sub-line, QScrollBar::add-line {{
                background: none;
                height: 0px;
                subcontrol-position: left;
                subcontrol-origin: margin;
                }}
                """)

    def on_margin_clicked(self, nmargin, nline, modifiers):
        # Toggle marker for the line the margin was clicked on
        if self.markersAtLine(nline) != 0:
            self.markerDelete(nline, self.ARROW_MARKER_NUM)
        else:
            self.markerAdd(nline, self.ARROW_MARKER_NUM)

    def open_file(self, path, file_name):
        self.path = path
        self.current_file = file_name
        self.am.dir = path
        self.setText(open(f"{self.path}/{self.current_file}", encoding='utf-8').read())
        self.update_api(self.getCursorPosition())

    def update_api(self, pos):
        row = pos[0]
        if row != self.current_row and self.text_changed:
            self.am.full_update(self.text(), pos)
            self.text_changed = False
        self._api = QsciAPIs(self._lexer)
        try:
            lst, code = self.am.get(self.text(), pos)
            for el in lst:
                self._api.add(str(el))
        except Exception as ex:
            # raise ex
            print(f"main_func: {ex.__class__.__name__}: {ex}")
            pass
        self._api.prepare()
        self._lexer.setAPIs(self._api)
