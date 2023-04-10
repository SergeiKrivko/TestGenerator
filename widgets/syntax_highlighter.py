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

        self.setAutoCompletionSource(QsciScintilla.AcsAPIs)
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

        self.apis = {
            'words': [tuple(parce_file("lib/words.txt")), True],
            'types': [tuple(parce_file("lib/types.txt")), True]
        }
        self.libs = tuple(get_lib())
        for lib in self.libs:
            self.apis[lib] = [tuple(parce_header(f"lib/{lib.replace('.h', '.txt')}")), True]

        self.apis2 = dict()
        self.path = ""
        self.current_file = ""
        self.current_row = 0
        self.cursorPositionChanged.connect(self.update_api)

    def on_margin_clicked(self, nmargin, nline, modifiers):
        # Toggle marker for the line the margin was clicked on
        if self.markersAtLine(nline) != 0:
            self.markerDelete(nline, self.ARROW_MARKER_NUM)
        else:
            self.markerAdd(nline, self.ARROW_MARKER_NUM)

    def open_file(self, path, file_name):
        self.path = path
        self.current_file = file_name
        with open(f"{path}/{file_name}") as file:
            self.setText(file.read())
            file.seek(0)

            for lib in self.libs:
                self.apis[lib][1] = False

            for line in file:
                line = line.strip()
                for lib in self.libs:
                    if line == f"#include <{lib}>":
                        self.apis[lib][1] = True
                else:
                    if line.startswith("#include \"") and line.endswith("\""):
                        f = line.split()[1].strip('\"')
                        if os.path.isfile(f"{path}/{f}"):
                            self.apis[f] = [tuple(parce_header(f"{path}/{f}")), True]

        self.apis2 = parce_main_file(f"{path}/{file_name}")
        self.set_api()

    def update_api(self, pos):
        try:
            if pos != self.current_row and self.current_file:
                self.current_row = pos
                for line in self.text().split("\n"):
                    for lib in self.libs:
                        if line == f"#include <{lib}>":
                            self.apis[lib][1] = True
                    else:
                        if line.startswith("#include \"") and line.endswith("\""):
                            f = line.split()[1].strip('\"')
                            if os.path.isfile(f"{self.path}/{f}"):
                                if f in self.apis:
                                    self.apis[f][1] = True
                                else:
                                    self.apis[f] = [tuple(parce_header(f"{self.path}/{f}")), True]
                self.apis2 = parce_main_file(f"{self.path}/{self.current_file}")
                self.set_api()
                self.autoCompleteFromAPIs()
        except Exception as ex:
            print(f"{ex.__class__.__name__}: {ex}")

    def set_api(self):
        self.api = QsciAPIs(self.lexer)
        try:
            for api in self.apis.values():
                if api[1]:
                    for el in api[0]:
                        self.api.add(el)
            for api in self.apis2.values():
                if api[1] < self.getCursorPosition()[0] <= api[2]:
                    for el in api[0]:
                        self.api.add(el)
        except Exception as ex:
            print(f"{ex.__class__.__name__}: {ex}")
        self.api.prepare()
        self.lexer.setAPIs(self.api)

    def create_api(self, lst):
        api = QsciAPIs(self.lexer)
        for el in lst:
            api.add(el)
        api.prepare()
        return api


def parce_header(path):
    types_txt = open("lib/types.txt", encoding='utf-8')
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
                types_txt.seek(0)
                for func_type in types_txt:
                    func_type = func_type.strip()
                    if line.startswith(func_type) and line.count('(') == line.count(')') and line.endswith(');'):
                        yield line.replace(func_type, '', 1)
                        break
    types_txt.close()


def parce_file(path):
    with open(path, encoding='utf-8') as file:
        for line in file:
            yield line


def parce_main_file(path):
    types_txt = open("lib/types.txt", encoding='utf-8')
    current_func = ""
    i = 0
    res_dict = {'__general__': ([], 0, 0)}
    with open(path, encoding='utf-8') as main_file:
        for line in main_file:
            if not current_func:
                line = line.strip()
                if line.startswith('#define') and len(s := line.split()) == 3:
                    res_dict['__general__'][0].append(s[1])
                elif line.startswith('typedef') and len(s := line.split()) >= 3:
                    s = s[2]
                    if '[' in s:
                        res_dict['__general__'][0].append(s[:s.index('[')])
                    else:
                        res_dict['__general__'][0].append(s)
                else:
                    types_txt.seek(0)
                    for func_type in types_txt:
                        func_type = func_type.strip()
                        if line.startswith(func_type) and line.count('(') == line.count(')') and \
                                (line.endswith(');') or line.endswith(")")):
                            header = line.replace(func_type, '', 1)
                            res_dict['__general__'][0].append(header)
                            if "(" in header and ")" in header:
                                params = header[header.index("(") + 1:header.rindex(")")].split(",")
                                lst = []
                                for p in params:
                                    if ' ' in p:
                                        lst.append(p.split()[1].lstrip("*"))
                                res_dict[header] = lst, i, i
                                if not header.endswith(";"):
                                    current_func = header
                            break
            elif line.startswith('}'):
                res_dict[current_func] = res_dict[current_func][0], res_dict[current_func][1], i
                current_func = ""
            else:
                line = line.strip()
                types_txt.seek(0)
                for var_type in types_txt:
                    if line.startswith(var_type.strip()) and ' ' in line and line.endswith(";"):
                        lst = line[line.index(' ') + 1:-1].split(',')
                        for el in lst:
                            el = el.strip().lstrip("*").replace('=', ' ')
                            el = el.replace('[', ' ')
                            if ' ' in el:
                                res_dict[current_func][0].append(el[:el.index(' ')])
                            else:
                                res_dict[current_func][0].append(el)
            i += 1
    res_dict['__general__'] = res_dict['__general__'][0], res_dict['__general__'][1], i
    types_txt.close()
    return res_dict


def get_lib():
    for lib in os.listdir("lib"):
        if lib not in ("words", "types") and lib.endswith(".txt"):
            yield lib.replace(".txt", ".h")

