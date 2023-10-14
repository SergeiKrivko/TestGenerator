from time import sleep

import docx
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.oxml import OxmlElement, ns
from docx.shared import Pt, RGBColor, Mm
from docx.oxml.ns import qn
from htmldocx import HtmlToDocx
from requests import post

DEFAULT_STILES = {
    'Normal': {'font': 'Times New Roman', 'size': 14, 'color': (0, 0, 0)},
    'Title': {'font': 'Times New Roman', 'size': 22, 'color': (0, 0, 0)},
    'Heading 1': {'font': 'Times New Roman', 'size': 16, 'bold': True, 'color': (0, 0, 0)},
    'Heading 2': {'font': 'Times New Roman', 'size': 15, 'bold': True, 'color': (0, 0, 0)},
    'Heading 3': {'font': 'Times New Roman', 'size': 14, 'bold': True, 'underline': True, 'color': (0, 0, 0)},
    'Heading 4': {'font': 'Times New Roman', 'size': 14, 'bold': True, 'color': (0, 0, 0)},
    'Heading 5': {'font': 'Times New Roman', 'size': 14, 'italic': True, 'underline': True, 'color': (0, 0, 0)},
    'Heading 6': {'font': 'Times New Roman', 'size': 14, 'italic': True, 'color': (0, 0, 0)},
    'Body Text': {'font': 'Courier', 'size': 11, 'color': (0, 0, 0)},
}

DEFAULT_PROPERTIES = {
    'margins': (30, 20, 10, 20)
}


class MarkdownParser:
    def __init__(self, bm, text: str, dist: str, styles=None, properties=None):
        self.bm = bm
        self.text = text
        self.dist = dist

        self.document = docx.Document()

        self.html_parser = HtmlToDocx()

        self.styles = dict()
        self._set_styles(styles if styles else DEFAULT_STILES)
        self.properties = properties if properties else DEFAULT_PROPERTIES

    def convert(self):
        paragraph = None
        table = None
        table_columns = 0
        table_rows = 0
        lexer = 'python'
        code_lines = None
        for line in self.text.split('\n'):
            if code_lines is not None:
                code_lines.append(line)
                if line.endswith('```'):
                    code_lines[-1] = line.rstrip('```')
                    self.highlight_code('\n'.join(code_lines), lexer)
                    code_lines = None
            elif line.startswith('#'):
                self.document.add_heading(line.lstrip('#').strip(), count_in_start(line, '#'))
                paragraph = None
            elif line.startswith('- '):
                self.document.add_paragraph(line.lstrip('-').strip(), "List Bullet")
                paragraph = None
            elif line.lstrip('1234567890').startswith('. ') and not line.startswith('.'):
                self.document.add_paragraph(line.lstrip('1234567890.').strip(), "List Number")
                paragraph = None
            elif line.startswith('```'):
                code_lines = []
                lexer = line.lstrip('```').strip()
            elif line.startswith('['):
                self.run_macros(line)
            elif line.startswith('|'):
                if table is None:
                    table_columns = line.strip().count('|') - 1
                    table_rows = 1
                    table = self.document.add_table(rows=1, cols=table_columns, style='Table Grid')
                    for i, text in enumerate(line.strip()[1:-1].split('|')):
                        table.cell(0, i).text = text.strip()
                elif line.strip().strip('-|'):
                    table.add_row()
                    for i, text in enumerate(line.strip()[1:-1].split('|')):
                        table.cell(table_rows, i).text = text.strip()
                    table_rows += 1

            elif not line.strip():
                paragraph = None
            else:
                if paragraph is None:
                    paragraph = self.document.add_paragraph()
                    paragraph.add_run(line.strip())
                else:
                    paragraph.add_run(' ')
                    paragraph.add_run(line.strip())

        self.set_margins()
        self._add_page_numbers()
        self.document.save(self.dist)

    def run_macros(self, line):
        if line.startswith('[tests]: <>'):
            flags = set(map(str.upper, line[len('[tests]: <>'):].strip().strip('()').split()))
            lst = ["Описание", "Входные данные"]
            if 'EXPECTED_OUTPUT' in flags:
                lst.append("Ожидаемый вывод")
            if 'REAL_OUTPUT' in flags:
                lst.append("Фактический вывод")
            if 'STATUS' in flags:
                lst.append("Результат")
            tests = self.bm.func_tests['pos'] + self.bm.func_tests['neg']
            table = self.document.add_table(rows=len(tests) + 1, cols=len(lst), style='Table Grid')
            if 'RUN' in flags:
                looper = self.bm.start_testing()
                while not looper.isFinished():
                    sleep(0.1)
            for i, el in enumerate(lst):
                table.cell(0, i).text = el
            for i, test in enumerate(self._prepare_tests_data(tests, flags)):
                for j, el in enumerate(test):
                    table.cell(i + 1, j).text = el

    @staticmethod
    def _prepare_tests_data(tests, flags):
        for test in tests:
            lst = [test.get('desc', '').strip(), test.get('in', '').strip()]
            if 'EXPECTED_OUTPUT' in flags:
                lst.append(test.get('out', '').strip())
            if 'REAL_OUTPUT' in flags:
                if 'RUN' in flags:
                    lst.append(test.prog_out.get('STDOUT', '').strip())
                else:
                    lst.append(test.get('out', ''))
            if 'STATUS' in flags:
                lst.append("OK" if 'RUN' not in flags or test.res() else "FAIL")
            yield lst

    def set_margins(self):
        sections = self.document.sections
        for section in sections:
            section.left_margin = Mm(self.properties['margins'][0])
            section.top_margin = Mm(self.properties['margins'][1])
            section.right_margin = Mm(self.properties['margins'][2])
            section.bottom_margin = Mm(self.properties['margins'][3])

    def _set_styles(self, data: dict):
        for key, item in data.items():
            style = self.document.styles[key]
            if 'font' in item:
                style.font.name = item['font']
            if 'size' in item:
                style.font.size = Pt(item['size'])
            if 'color' in item:
                style.font.color.rgb = RGBColor(*item.get('color'))
            style.font.italic = item.get('italic', False)
            style.font.bold = item.get('bold', False)
            style.font.underline = item.get('underline', False)
            style.font.strike = item.get('strike', False)

            rFonts = style.element.rPr.rFonts
            rFonts.set(qn("w:asciiTheme"), item['font'])
            rFonts.set(qn("w:hAnsiTheme"), item['font'])

            self.styles[key] = style

    def highlight_code(self, code: str, lexer: str = 'c'):
        req = {
            'code': code.strip(),
            'lexer': lexer,
            'options': [],
            'style': 'colorful',
            'linenos': True
        }
        try:
            if not lexer:
                raise Exception
            res = post('http://hilite.me/api', req)
            if res.status_code >= 400:
                raise Exception(str(res.status_code))
            text = res.text
        except Exception as ex:
            table = self.document.add_table(rows=1, cols=2)
            table.cell(0, 0).paragraphs[0].text = '\n'.join(map(str, range(1, code.strip().count('\n') + 2)))
            table.cell(0, 0).paragraphs[0].style = 'Body Text'
            table.cell(0, 1).paragraphs[0].text = code.strip()
            table.cell(0, 1).paragraphs[0].style = 'Body Text'
        else:
            self.html_parser.add_html_to_document(text, self.document)
            table = self.document.tables[-1]
        table.style = 'Table Grid'
        for row in table.rows:
            row.cells[0].width = Mm(10)
            row.cells[1].width = Mm(150)
        table.cell(0, 1).paragraphs[0].runs[-1].text = table.cell(0, 1).paragraphs[0].runs[-1].text.rstrip()
        for run in table.cell(0, 0).paragraphs[0].runs:
            run.font.size = Pt(11)
        for run in table.cell(0, 1).paragraphs[0].runs:
            run.font.size = Pt(11)

    def _add_page_numbers(self):
        def create_element(name):
            return OxmlElement(name)

        def create_attribute(element, name, value):
            element.set(ns.qn(name), value)

        def add_page_number(paragraph):
            paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.RIGHT

            page_num_run = paragraph.add_run()

            fldChar1 = create_element('w:fldChar')
            create_attribute(fldChar1, 'w:fldCharType', 'begin')

            instrText = create_element('w:instrText')
            create_attribute(instrText, 'xml:space', 'preserve')
            instrText.text = "PAGE"

            fldChar2 = create_element('w:fldChar')
            create_attribute(fldChar2, 'w:fldCharType', 'end')

            page_num_run._r.append(fldChar1)
            page_num_run._r.append(instrText)
            page_num_run._r.append(fldChar2)

        add_page_number(self.document.sections[0].footer.paragraphs[0])


def count_in_start(line, symbol):
    return len(line) - len(line.lstrip(symbol))


if __name__ == '__main__':
    from sys import argv

    with open(argv[1], encoding='utf-8') as f:
        converter = MarkdownParser(None, f.read(), argv[2])
    converter.convert()
