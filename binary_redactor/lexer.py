import sys

from PyQt5.Qsci import QsciLexerCustom, QsciScintilla
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QFrame, QApplication, QStyleFactory, QMainWindow

from tests.convert_binary import get_expected_values, get_defines


class LexerBin(QsciLexerCustom):
    Mask = 0
    Value = 1
    PreProcessor = 2
    InvalidMask = 3
    InvalidValue = 4
    Default = 5

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

        self.defines = dict()
        self.bin_code = False

    def language(self):
        return "ConverBinaryLanguage"

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
        return ""

    def styleText(self, start, end):
        self.startStyling(start)
        if not self.bin_code:
            self.startStyling(end - start, LexerBin.Default)
            return

        text = self.parent().text()[start:end]
        for line in text.split('\n'):
            split_line = line.split()
            if line.startswith('#'):
                self.setStyling(len(line), LexerBin.PreProcessor)
                self.setStyling(1, LexerBin.Value)
            elif line.strip():
                self.setStyling(len(line) - len(line := line.lstrip()), LexerBin.Value)
                mask = split_line[0]
                line = line.lstrip(mask)
                if mask in self.defines:
                    mask = self.defines[mask]

                try:
                    expected_values = get_expected_values(mask)
                except Exception:
                    self.setStyling(len(line) + 1, LexerBin.Value)
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
                        if value_type == str and len(split_line[i].encode('utf-8')) > maximum:
                            raise ValueError
                        elif value_type != str and not(minimum <= value_type(split_line[i]) <= maximum):
                            raise ValueError
                        self.setStyling(len(split_line[i]), LexerBin.Value)
                    except ValueError:
                        self.setStyling(len(split_line[i]), LexerBin.InvalidValue)
                    except IndexError:
                        self.setStyling(len(split_line[i]), LexerBin.InvalidValue)
                self.setStyling(len(line) + 1, LexerBin.Value)

    def set_defines(self, dct):
        self.defines = dct


myCodeSample = r"""#define STUDENT 26s11s3x4I
STUDENT Serysheva Dar'ya 6 1 5 5
STUDENT Onishchuk Ivan 3 5 6 3
STUDENT Parfenov Arsenij 5 3 4 2
STUDENT Tarasenko Egor 2 1 1 1
STUDENT Suhilina Aleksandra 6 2 1 2
STUDENT Krivko Sergej 5 3 2 1
STUDENT Soshnin Nikita 6 6 1 5
STUDENT Kozin Mihail 1 3 4 2
STUDENT Bugakov Ivan 5 6 6 3
STUDENT SHirokov Andrej 6 1 2 2
STUDENT Enikeev Timur 1 5 1 5
STUDENT Sal'nikov Mihail 2 2 1 5
STUDENT Slinyakov Mihail 6 4 5 3
STUDENT Timofeev Daniil 3 5 3 2
STUDENT YAkovlev Roman 1 4 2 1
STUDENT Vavilova Varvara 1 1 1 5
STUDENT Paramonova Ekaterina 5 2 5 5
STUDENT Orlov Aleksej 5 1 5 1
STUDENT Asadullin Tagir 2 3 6 2
STUDENT ZHilyaev Anton 2 6 2 3
STUDENT Volov Aleksandr 4 3 2 3
""".replace("\n", "\r\n")


class CustomMainWindow(QMainWindow):
    def __init__(self):
        super(CustomMainWindow, self).__init__()

        # -------------------------------- #
        #           Window setup           #
        # -------------------------------- #

        # 1. Define the geometry of the main window
        # ------------------------------------------
        self.setGeometry(300, 300, 800, 400)
        self.setWindowTitle("QScintilla Test")

        # 2. Create frame and layout
        # ---------------------------
        self.__frm = QFrame(self)
        self.__frm.setStyleSheet("QWidget { background-color: #ffeaeaea }")
        self.__lyt = QVBoxLayout()
        self.__frm.setLayout(self.__lyt)
        self.setCentralWidget(self.__frm)
        self.__myFont = QFont()
        self.__myFont.setPointSize(14)

        # 3. Place a button
        # ------------------
        self.__btn = QPushButton("Qsci")
        self.__btn.setFixedWidth(50)
        self.__btn.setFixedHeight(50)
        self.__btn.clicked.connect(self.__btn_action)
        self.__btn.setFont(self.__myFont)
        self.__lyt.addWidget(self.__btn)

        # -------------------------------- #
        #     QScintilla editor setup      #
        # -------------------------------- #

        # ! Make instance of QSciScintilla class!
        # ----------------------------------------


        # ! Add editor to layout !
        # -------------------------
        self.__lyt.addWidget(self.__editor)
        self.show()

    def __btn_action(self):
        print("Hello World!")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    QApplication.setStyle(QStyleFactory.create('Fusion'))
    myGUI = CustomMainWindow()
    sys.exit(app.exec_())
