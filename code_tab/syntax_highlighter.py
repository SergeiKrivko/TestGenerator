import os

from PyQt5.QtGui import QColor, QFontMetrics
from PyQt5.Qsci import QsciScintilla, QsciAPIs, QsciLexerCPP, QsciLexerBash
from language.autocomplition.abstract import CodeAutocompletionManager
from language.languages import languages


class CodeEditor(QsciScintilla):
    ARROW_MARKER_NUM = 8

    def __init__(self, sm, tm, border=False):
        super(CodeEditor, self).__init__(None)

        self.sm = sm
        self.tm = tm
        self.border = border

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
        self.textChanged.connect(self.save_file)
        self.cursorPositionChanged.connect(lambda: self.update_api(self.getCursorPosition()))
        self.text_changed = False
        self.language_data = dict()
        self.theme_apply = False

    def set_text_changed(self):
        self.text_changed = True

    def set_theme(self):
        if self.isHidden():
            return
        self.theme_apply = True
        self.setStyleSheet(self.tm.scintilla_css(border=self.border))

        self.setFont(self.tm.code_font)
        self.setMarginsFont(self.tm.code_font)
        fontmetrics = QFontMetrics(self.tm.code_font)
        self.setMarginsFont(self.tm.code_font)
        self._lexer.setDefaultFont(self.tm.code_font)
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

        for key, item in self.language_data.get('colors', dict()).items():
            self._lexer.setColor(self.tm[item], key)
            self._lexer.setFont(self.tm.code_font, key)

    def on_margin_clicked(self, nmargin, nline, modifiers):
        # Toggle marker for the line the margin was clicked on
        if self.markersAtLine(nline) != 0:
            self.markerDelete(nline, self.ARROW_MARKER_NUM)
        else:
            self.markerAdd(nline, self.ARROW_MARKER_NUM)

    def set_lexer(self, data: dict):
        self.language_data = data
        if data.get('lexer') is None:
            self._lexer = QsciLexerCPP(self)
            self._lexer.setDefaultFont(self.tm.code_font_std)
            for key in languages['C']['colors'].keys():
                self._lexer.setColor(self.tm['Identifier'], key)
                self._lexer.setFont(self.tm.code_font, key)
        else:
            self._lexer = data['lexer'](self)
            self._lexer.setDefaultFont(self.tm.code_font_std)
            self._lexer.setDefaultPaper(self.tm['Paper'])
            for key, item in data.get('colors', dict()).items():
                self._lexer.setColor(self.tm[item], key)
                self._lexer.setFont(self.tm.code_font, key)

        self.setLexer(self._lexer)
        if hasattr(self.am, 'terminate'):
            self.am.terminate()
        self.am = data.get('autocompletion', CodeAutocompletionManager)(self.sm, self.path)

    def open_file(self, path):
        self.path, self.current_file = os.path.split(path)

        for language, data in languages.items():
            for f in data.get('files', []):
                if self.current_file.endswith(f):
                    self.set_lexer(data)

                    self.am.dir = self.path
                    self.setText(open(f"{self.path}/{self.current_file}", encoding='utf-8').read())
                    self.update_api(self.getCursorPosition())
                    return

        self.set_lexer(dict())

        self.am.dir = self.path
        try:
            self.setText(open(f"{self.path}/{self.current_file}", encoding='utf-8').read())
        except UnicodeDecodeError:
            self.setText("")
            self.setDisabled(True)
        self.update_api(self.getCursorPosition())

    def save_file(self):
        path = os.path.join(self.path, self.current_file)
        if os.path.isfile(path):
            try:
                with open(path, 'w', encoding='utf-8', newline=self.sm.get_general('line_sep', '\n')) as f:
                    f.write(self.text())
            except FileNotFoundError:
                pass
            except PermissionError:
                pass

    def set_text(self, text):
        self.setText(text)
        self.update_api(self.getCursorPosition())

    def update_api(self, pos):
        row = pos[0]
        if row != self.current_row and self.text_changed:
            self.current_row = row
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

    def show(self) -> None:
        super().show()
        self.set_theme()
        try:
            with open(os.path.join(self.path, self.current_file), encoding='utf-8') as f:
                self.setText(f.read())
        except FileNotFoundError:
            pass
        except UnicodeDecodeError:
            pass
