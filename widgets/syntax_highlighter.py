import os

from PyQt5.QtGui import QFont, QColor, QFontMetrics
from PyQt5.Qsci import QsciScintilla, QsciLexerCPP, QsciAPIs
from other.lib import words, types


headers_list = []


class CodeEditor(QsciScintilla):
    ARROW_MARKER_NUM = 8

    def __init__(self, q_settings, parent=None):
        super(CodeEditor, self).__init__(parent)

        # Set the default font
        font = QFont()
        font.setFamily('Courier')
        font.setFixedPitch(True)
        font.setPointSize(10)
        self.setFont(font)
        self.setMarginsFont(font)
        self.q_settings = q_settings

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

        headers_list.clear()
        self.apis = {
            'words': [words, True],
            'types': [types, True]
        }
        self.libs = tuple(self.get_lib())
        for lib_name, lib_data in self.libs:
            self.apis[lib_name] = [tuple(self.parse_header_str(lib_data)), False]

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
                self.apis[lib[0]][1] = False

            headers_list.clear()
            for line in file:
                line = line.strip()
                for lib in self.libs:
                    if line == f"#include <{lib[0]}>":
                        self.apis[lib[0]][1] = True
                else:
                    if line.startswith("#include \"") and line.endswith("\""):
                        f = line.split()[1].strip('\"')
                        if os.path.isfile(f"{path}/{f}"):
                            self.apis[f] = [tuple(self.parse_header_file(f"{path}/{f}")), True]

        self.apis2 = parse_main_file(f"{path}/{file_name}")
        self.set_api()

    def update_api(self, pos):
        try:
            headers_list.clear()
            for lib in self.libs:
                self.apis[lib[0]][1] = False
            if pos != self.current_row and self.current_file:
                self.current_row = pos
                for line in self.text().split("\n"):
                    for lib in self.libs:
                        if line == f"#include <{lib[0]}>":
                            self.apis[lib[0]][1] = True
                    else:
                        if line.startswith("#include \"") and line.endswith("\""):
                            f = line.split()[1].strip('\"')
                            if os.path.isfile(f"{self.path}/{f}"):
                                if f in self.apis:
                                    self.apis[f][1] = True
                                else:
                                    self.apis[f] = [tuple(self.parse_header_file(f"{self.path}/{f}")), True]
                self.apis2 = parse_main_file(f"{self.path}/{self.current_file}")
                self.set_api()
                self.autoCompleteFromAPIs()
        except Exception:
            pass

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
        except Exception:
            pass
        self.api.prepare()
        self.lexer.setAPIs(self.api)

    def create_api(self, lst):
        api = QsciAPIs(self.lexer)
        for el in lst:
            api.add(el)
        api.prepare()
        return api

    def parse_header_file(self, path):
        with open(path, encoding='utf-8') as header_file:
            for line in header_file:
                res = self.parse_header(line, path)
                if res:
                    yield res

    def parse_header_str(self, string: str):
        for line in string.split('\n'):
            res = self.parse_header(line)
            if res:
                yield res

    def parse_header(self, line, path=""):
        line = line.strip()
        for lib in self.libs:
            if line == f"#include <{lib}>":
                self.apis[lib][1] = True
        else:
            if line.startswith("#include \"") and line.endswith("\""):
                f = line.split()[1].strip('\"')
                if f not in headers_list:
                    headers_list.append(f)
                    for el in self.parse_header_file(f"{os.path.split(path)[0]}/{f}"):
                        return el
            if line.startswith('#define') and len(s := line.split()) == 3:
                return s[1]
            elif line.startswith('typedef') and len(s := line.split()) >= 3:
                s = s[2]
                if '[' in s:
                    return s[:s.index('[')]
                else:
                    return s
            else:
                for func_type in types:
                    func_type = func_type.strip()
                    if line.startswith(func_type) and line.count('(') == line.count(')') and line.endswith(');'):
                        return line.replace(func_type, '', 1)

    def get_lib(self):
        # for lib in os.listdir("lib"):
        #     if lib not in ("words", "types") and lib.endswith(".txt"):
        #         yield lib.replace(".txt", ".h")
        lib_list = self.q_settings.value('lib')
        if isinstance(lib_list, str):
            for lib_info in lib_list.split(';'):
                lib_name, _ = lib_info.split(':')
                lib_data = self.q_settings.value(lib_name)
                yield lib_name, lib_data


def parce_file(path):
    with open(path, encoding='utf-8') as file:
        for line in file:
            yield line


def parse_main_file(path):
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
                    for func_type in types:
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
                for var_type in types:
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
    return res_dict

