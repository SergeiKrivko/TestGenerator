class Document:
    def __init__(self):
        self.objects = []

    def add_paragraph(self, text=None, style=''):
        paragraph = Paragraph(text, style)
        self.objects.append(paragraph)
        return paragraph

    def add_heading(self, text, level=1, style=''):
        paragraph = Heading(text, level, style)
        self.objects.append(paragraph)
        return paragraph

    def add_list(self, num=False):
        lst = List(num)
        self.objects.append(lst)
        return lst

    def add_code(self, code, lexer=''):
        code_area = CodeArea(code, lexer)
        self.objects.append(code_area)
        return code_area

    def add_table(self, columns=1, rows=1):
        table = Table(columns, rows)
        self.objects.append(table)
        return table

    def add_picture(self, path, width=None, height=None):
        image = Picture(path, width, height)
        self.objects.append(image)
        return image


class Paragraph:
    def __init__(self, text=None, style=''):
        self.runs = []
        if text:
            self.add_run(text, style)

    def add_run(self, text, style=''):
        run = Run(text, style)
        self.runs.append(run)
        return run


class Heading(Paragraph):
    def __init__(self, text, level=1, style=''):
        super().__init__(text, style)
        self.level = level


class Run:
    def __init__(self, text, style=''):
        self.text = text
        self._style = set(style)

    def set_text(self, text):
        self.text = text

    def set_style(self, style):
        self._style = set(style)


class List:
    def __init__(self, num=False):
        self.num = num
        self.paragraphs = []

    def add_paragraph(self, text=None, style=''):
        paragraph = Paragraph(text, style)
        self.paragraphs.append(paragraph)
        return paragraph


class CodeArea:
    def __init__(self, code, lexer=''):
        self.code = code
        self.lexer = lexer


class Table:
    def __init__(self, columns=1, rows=1):
        self.columns = columns
        self.rows = rows
        self.cells = [Paragraph() for _ in range(rows) for _ in range(columns)]

    def __getitem__(self, item):
        return self.cells[item]

    def cell(self, x, y):
        return self.cells[x][y]


class Picture:
    def __init__(self, path, width=None, height=None):
        self.path = path
        self.width = width
        self.height = height
