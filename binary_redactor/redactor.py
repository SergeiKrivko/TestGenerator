from PyQt5.Qsci import QsciScintilla
from PyQt5.QtGui import QColor

from binary_redactor.lexer import LexerBin


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
        self.setStyleSheet(self.tm.scintilla_style_sheet)
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

