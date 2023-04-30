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

        self.lexer = QsciLexerCPP(None)
        self.lexer.setDefaultFont(font)
        self.setLexer(self.lexer)

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
        self.cursorPositionChanged.connect(self.update_api)

    def set_theme(self):
        self.setMarkerBackgroundColor(QColor(self.tm['TextColor']), self.ARROW_MARKER_NUM)
        self.setMarginsBackgroundColor(QColor(self.tm['BgColor']))
        for key, item in self.tm.code_colors():
            self.lexer.setColor(item, QsciLexerCPP.__dict__[key])
        self.lexer.setPaper(self.tm['Paper'])
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
        self.update_api(self.getCursorPosition()[0])

    def update_api(self, pos):
        self.api = QsciAPIs(self.lexer)
        try:
            for el in self.am.get(self.text(), pos):
                self.api.add(el)
        except Exception as ex:
            print(f"main_func: {ex.__class__.__name__}: {ex}")
            pass
        self.api.prepare()
        self.lexer.setAPIs(self.api)
