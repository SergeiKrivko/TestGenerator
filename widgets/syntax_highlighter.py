import os

from PyQt5.QtGui import QFont, QColor, QFontMetrics
from PyQt5.Qsci import QsciScintilla, QsciLexerCPP, QsciAPIs


class CodeEditor(QsciScintilla):
    ARROW_MARKER_NUM = 8

    def __init__(self, parent=None):
        super(CodeEditor, self).__init__(parent)

        # Set the default font
        font = QFont()
        font.setFamily('Courier')
        font.setFixedPitch(True)
        font.setPointSize(10)
        self.setFont(font)
        self.setMarginsFont(font)

        # Margin 0 is used for line numbers
        fontmetrics = QFontMetrics(font)
        self.setMarginsFont(font)
        self.setMarginWidth(0, fontmetrics.width("00000") + 6)
        self.setMarginLineNumbers(0, True)
        self.setMarginsBackgroundColor(QColor("#cccccc"))

        # Clickable margin 1 for showing markers
        self.setMarginSensitivity(1, True)
        #        self.connect(self,
        #            SIGNAL('marginClicked(int, int, Qt::KeyboardModifiers)'),
        #            self.on_margin_clicked)
        self.markerDefine(QsciScintilla.RightArrow,
                          self.ARROW_MARKER_NUM)
        self.setMarkerBackgroundColor(QColor("#ee1111"),
                                      self.ARROW_MARKER_NUM)

        # Brace matching: enable for a brace immediately before or after
        # the current position
        #
        self.setBraceMatching(QsciScintilla.SloppyBraceMatch)

        # Current line visible with special background color
        self.setCaretLineVisible(True)
        self.setCaretLineBackgroundColor(QColor("#ffe4e4"))

        # Set Python lexer
        # Set style for Python comments (style number 1) to a fixed-width
        # courier.
        #

        self.lexer = QsciLexerCPP(None)
        self.lexer.setDefaultFont(font)
        self.setLexer(self.lexer)

        self.setAutoCompletionSource(QsciScintilla.AcsAll)
        self.setAutoCompletionThreshold(1)
        self.setAutoCompletionCaseSensitivity(True)
        self.setAutoCompletionReplaceWord(True)
        self.setCallTipsStyle(QsciScintilla.CallTipsNoContext)

        self.setIndentationsUseTabs(False)
        self.setTabWidth(4)
        self.setIndentationGuides(True)
        self.setTabIndents(True)
        self.setAutoIndent(True)

        text = bytearray(str.encode("Courier"))
        self.SendScintilla(QsciScintilla.SCI_STYLESETFONT, 1, text)

        # Don't want to see the horizontal scrollbar at all
        # Use raw message to Scintilla here (all messages are documented
        # here: http://www.scintilla.org/ScintillaDoc.html)
        self.SendScintilla(QsciScintilla.SCI_SETHSCROLLBAR, 0)

        # not too small
        self.setMinimumSize(600, 450)

        self.setCallTipsVisible(0)

    def on_margin_clicked(self, nmargin, nline, modifiers):
        # Toggle marker for the line the margin was clicked on
        if self.markersAtLine(nline) != 0:
            self.markerDelete(nline, self.ARROW_MARKER_NUM)
        else:
            self.markerAdd(nline, self.ARROW_MARKER_NUM)

    def open_file(self, path, file):
        with open(f"{path}/{file}") as file:
            self.setText(file.read())
            file.seek(0)

            self.api = QsciAPIs(self.lexer)

            for line in file:
                line = line.strip()
                if line.startswith("#include \"") and line.endswith("\""):
                    f = line.split()[1].strip('\"')
                    if os.path.isfile(f"{path}/{f}"):
                        for el in parce_header(f"{path}/{f}"):
                            self.api.add(el)

            self.api.prepare()
            self.lexer.setAPIs(self.api)


def parce_header(path):
    func_types = 'int', 'char', 'void', 'double', 'float'
    with open(path, encoding='utf-8') as header_file:
        for line in header_file:
            line = line.strip()
            if line.startswith('#define') and len(s := line.split()) == 3:
                yield s[1]
            elif line.startswith('typedef') and len(s := line.split()) >= 3:
                s = s[2]
                if '[' in s:
                    yield s[:s.index('[')]
                else:
                    yield s
            else:
                for func_type in func_types:
                    if line.startswith(func_type) and line.count('(') == line.count(')') and line.endswith(');'):
                        yield line.replace(func_type, '', 1)
                        break
