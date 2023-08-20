import os

from PyQt5.QtGui import QColor, QFontMetrics
from PyQt5.Qsci import QsciScintilla, QsciAPIs, QsciLexer
from language.autocomplition.abstract import CodeAutocompletionManager
from language.languages import languages


class CodeEditor(QsciScintilla):
    ARROW_MARKER_NUM = 8

    def __init__(self, sm, tm, path=None, language=None, border=False):
        super(CodeEditor, self).__init__(None)

        self.sm = sm
        self.tm = tm
        self.path = path
        if self.path is not None:
            self.dir, self.file = os.path.split(self.path)
        else:
            self.dir, self.file = '', ''
        self.language = language
        self.border = border
        self.language_data = dict()
        self.find_language()

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

        if 'lexer' in self.language_data and self.language_data['lexer'] is not None:
            self._lexer = self.language_data['lexer'](self)
            self._lexer.setDefaultFont(self.tm.code_font_std)
            self.setLexer(self._lexer)
        else:
            self._lexer = None

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

        if self.path is not None:
            try:
                with open(self.path, encoding='utf-8') as f:
                    self.setText(f.read())
                self.textChanged.connect(self.save_file)
            except Exception as ex:
                print(f"{ex.__class__.__name__}: {ex}")

        self.current_row = 0
        self.am = self.language_data.get('autocompletion', CodeAutocompletionManager)(self.sm, self.dir)
        self.textChanged.connect(self.set_text_changed)
        self.cursorPositionChanged.connect(lambda: self.update_api(self.getCursorPosition()))
        self.text_changed = False
        self.theme_apply = False

    def find_language(self):
        if self.language is None and self.path is not None:
            for key, item in languages.items():
                for el in item.get('files', []):
                    if self.path.endswith(el):
                        self.language = key
                        self.language_data = item
                        return
        else:
            self.language_data = languages[self.language]

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
        self.setMarginWidth(0, fontmetrics.width("00000") + 6)

        self.setMarkerBackgroundColor(QColor(self.tm['TextColor']), self.ARROW_MARKER_NUM)
        self.setMarginsBackgroundColor(QColor(self.tm['BgColor']))
        self.setMarginsForegroundColor(QColor(self.tm['TextColor']))
        self.setCaretLineBackgroundColor(self.tm['CaretLineBackgroundColor'])
        self.setMatchedBraceBackgroundColor(self.tm['CaretLineBackgroundColor'])
        self.setMatchedBraceForegroundColor(self.tm['BraceColor'])
        self.setUnmatchedBraceBackgroundColor(self.tm['CaretLineBackgroundColor'])
        self.setUnmatchedBraceForegroundColor(self.tm['BraceColor'])

        if self._lexer is not None:
            self._lexer.setDefaultFont(self.tm.code_font)
            self._lexer.setPaper(self.tm['Paper'])
            for key, item in self.language_data.get('colors', dict()).items():
                self._lexer.setColor(self.tm[item], key)
                self._lexer.setFont(self.tm.code_font, key)

    def on_margin_clicked(self, nmargin, nline, modifiers):
        # Toggle marker for the line the margin was clicked on
        if self.markersAtLine(nline) != 0:
            self.markerDelete(nline, self.ARROW_MARKER_NUM)
        else:
            self.markerAdd(nline, self.ARROW_MARKER_NUM)

    def save_file(self):
        if os.path.isfile(self.path):
            try:
                with open(self.path, 'w', encoding='utf-8', newline=self.sm.get_general('line_sep', '\n')) as f:
                    f.write(self.text())
            except FileNotFoundError:
                pass
            except PermissionError:
                pass

    def set_text(self, text):
        self.setText(text)
        self.update_api(self.getCursorPosition())

    def update_api(self, pos):
        if self._lexer is None:
            return
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
            with open(self.path, encoding='utf-8') as f:
                self.setText(f.read())
        except FileNotFoundError:
            pass
        except UnicodeDecodeError:
            pass
