from PyQt5.QtGui import QColor, QFontMetrics
from PyQt5.Qsci import QsciScintilla, QsciAPIs, QsciLexerCPP, QsciLexerBash
from code_tab.autocomplition.abstract import CodeAutocompletionManager
from code_tab.languages import languages


class CodeEditor(QsciScintilla):
    ARROW_MARKER_NUM = 8

    def __init__(self, sm, tm):
        super(CodeEditor, self).__init__(None)

        self.sm = sm
        self.tm = tm

        # Set the default font
        self.setFont(self.tm.code_font_std)
        self.setMarginsFont(self.tm.code_font_std)

        # Margin 0 is used for line numbers
        fontmetrics = QFontMetrics(self.tm.code_font_std)
        self.setMarginsFont(self.tm.code_font_std)
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

        self._lexer = QsciLexerBash(None)
        self._lexer.setDefaultFont(self.tm.code_font_std)
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
        print("OK")

    def set_text_changed(self):
        self.text_changed = True

    def set_theme(self):
        self.setStyleSheet(self.tm.scintilla_style_sheet)

        self.setFont(self.tm.code_font_std)
        self.setMarginsFont(self.tm.code_font_std)
        fontmetrics = QFontMetrics(self.tm.code_font_std)
        self.setMarginsFont(self.tm.code_font_std)
        self._lexer.setDefaultFont(self.tm.code_font_std)
        self.setMarginWidth(0, fontmetrics.width("00000") + 6)

        self.setMarkerBackgroundColor(QColor(self.tm['TextColor']), self.ARROW_MARKER_NUM)
        self.setMarginsBackgroundColor(QColor(self.tm['BgColor']))
        self.setMarginsForegroundColor(QColor(self.tm['TextColor']))
        self._lexer.setPaper(self.tm['Paper'])
        self.setCaretLineBackgroundColor(self.tm['CaretLineBackgroundColor'])
        self.setMatchedBraceBackgroundColor(self.tm['CaretLineBackgroundColor'])
        self.setMatchedBraceForegroundColor(self.tm['BraceColor'])
        self.setUnmatchedBraceBackgroundColor(self.tm['CaretLineBackgroundColor'])
        self.setUnmatchedBraceForegroundColor(self.tm['BraceColor'])

    def on_margin_clicked(self, nmargin, nline, modifiers):
        # Toggle marker for the line the margin was clicked on
        if self.markersAtLine(nline) != 0:
            self.markerDelete(nline, self.ARROW_MARKER_NUM)
        else:
            self.markerAdd(nline, self.ARROW_MARKER_NUM)

    def set_lexer(self, data: dict):
        if data.get('lexer') is None:
            self._lexer = QsciLexerCPP(None)
            self._lexer.setDefaultFont(self.tm.code_font_std)
            for key in languages['c']['colors'].keys():
                self._lexer.setColor(self.tm['Identifier'], key)
        else:
            self._lexer = data['lexer'](None)
            self._lexer.setDefaultFont(self.tm.code_font_std)
            for key, item in data.get('colors', dict()).items():
                self._lexer.setColor(self.tm[item], key)

        self.setLexer(self._lexer)
        self.am = data.get('autocompletion', CodeAutocompletionManager)(self.sm, self.path)

    def open_file(self, path, file_name: str):
        self.path = path
        self.current_file = file_name

        for language, data in languages.items():
            for f in data['files']:
                if file_name.endswith(f):
                    self.set_lexer(data)

                    self.am.dir = path
                    self.setText(open(f"{self.path}/{self.current_file}", encoding='utf-8').read())
                    self.update_api(self.getCursorPosition())
                    return

        self.am.dir = path
        self.setText(open(f"{self.path}/{self.current_file}", encoding='utf-8').read())
        self.update_api(self.getCursorPosition())

    def set_text(self, text):
        self.setText(text)
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
