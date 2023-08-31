from PyQt5.Qsci import QsciLexerCustom
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont

from tests.convert_binary import BinaryConverter


class LexerBin(QsciLexerCustom):
    Mask = 0
    Value = 1
    PreProcessor = 2
    InvalidMask = 3
    InvalidValue = 4
    Default = 5
    Comment = 6

    def __init__(self, parent=None):
        super().__init__(parent)
        # Default text settings
        # ----------------------
        self.setDefaultColor(QColor("#ff000000"))
        self.setDefaultPaper(QColor("#ffffffff"))
        self.setDefaultFont(QFont("Consolas", 11))

        # Initialize colors per style
        # ----------------------------
        self.setColor(QColor(Qt.blue), LexerBin.Mask)
        self.setColor(QColor(Qt.black), LexerBin.Value)
        self.setColor(QColor(Qt.darkYellow), LexerBin.PreProcessor)
        self.setColor(QColor(Qt.red), LexerBin.InvalidMask)
        self.setColor(QColor(Qt.red), LexerBin.InvalidValue)
        self.setColor(QColor(Qt.black), LexerBin.Default)
        self.setColor(QColor(Qt.gray), LexerBin.Comment)

        self.defines = dict()
        self.bin_code = True
        self.encoder = BinaryConverter('')

    def language(self):
        return "ConvertBinaryLanguage"

    def description(self, style):
        if style == 0:
            return "mask"
        elif style == 1:
            return "value"
        elif style == 2:
            return "preprocessor"
        elif style == 3:
            return "invalid_mask"
        elif style == 4:
            return "invalid_value"
        elif style == 6:
            return "comment"
        return ""

    def styleText(self, start, end):
        self.set_defines()
        if not self.bin_code:
            self.startStyling(end, LexerBin.Default)
            return

        self.startStyling(start)

        text = self.parent().text()[start:end]
        for line in text.split('\n'):
            if '//' in line:
                comment_len = len(line) - (ind := line.rindex('//'))
                line = line[:ind]
            else:
                comment_len = 0

            split_line = line.split()
            if line.startswith('#'):
                self.setStyling(len(line), LexerBin.PreProcessor)
            elif line.strip():
                self.setStyling(len(line) - len(line := line.lstrip()), LexerBin.Value)
                mask = split_line[0]
                line = line.lstrip(mask)
                if mask in self.defines:
                    mask = self.defines[mask]

                try:
                    expected_values = BinaryConverter.get_expected_values(mask)
                except Exception:
                    self.setStyling(len(split_line[0]), LexerBin.InvalidMask)
                    self.setStyling(len(line), LexerBin.Value)
                    continue

                if len(expected_values) != len(split_line) - 1:
                    self.setStyling(len(split_line[0]), LexerBin.InvalidMask)
                else:
                    self.setStyling(len(split_line[0]), LexerBin.Mask)

                for i in range(1, len(split_line)):
                    self.setStyling(len(line) - len(line := line.lstrip()), LexerBin.Value)
                    line = line.lstrip(split_line[i])
                    try:
                        value_type, minimum, maximum = expected_values[i - 1]
                        if value_type == str and len(split_line[i].encode(self.encoder.encoding)) > maximum:
                            raise ValueError
                        elif value_type != str and not(minimum <= value_type(split_line[i]) <= maximum):
                            raise ValueError
                        self.setStyling(len(split_line[i]), LexerBin.Value)
                    except ValueError:
                        self.setStyling(len(split_line[i]), LexerBin.InvalidValue)
                    except IndexError:
                        self.setStyling(len(split_line[i]), LexerBin.InvalidValue)
                self.setStyling(len(line), LexerBin.Value)

            self.setStyling(comment_len + 1, LexerBin.Comment)

    def set_defines(self):
        self.encoder.text = self.parent().text()
        self.defines = self.encoder.get_defines()
