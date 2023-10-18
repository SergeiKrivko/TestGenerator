from pathlib import Path

from borb.io.read.types import Decimal
from borb.pdf import Document
from borb.pdf import Page
from borb.pdf import SingleColumnLayout
from borb.pdf import Paragraph
from borb.pdf import PDF
from borb.pdf import OrderedList, UnorderedList, Image

from other.report import types


class PdfConverter:
    def __init__(self, document: types.Document, dist):
        self.document = document
        self.dist = dist
        self.file = Document()

        self.page = Page()
        self.file.add_page(self.page)

        self.layout = SingleColumnLayout(self.page)

    def convert(self):
        for obj in self.document.objects:
            match obj.__class__:
                case types.Paragraph:
                    self.add_paragraph(obj)
                case types.Heading:
                    self.add_heading(obj)
                case types.List:
                    self.add_list(obj)
                case types.Picture:
                    self.add_picture(obj)
                case _:
                    print(obj)
        self.save_file()

    def add_paragraph(self, paragraph: types.Paragraph):
        self.layout.add(Paragraph(''.join(run.text for run in paragraph.runs),
                                  font_size=Decimal(14), font='Times-Roman'))

    def add_heading(self, heading: types.Heading):
        self.layout.add(Paragraph(''.join(run.text for run in heading.runs),
                                  font_size=Decimal(16), font='Times-Roman'))

    def add_list(self, lst: types.List):
        if lst.num:
            ordered_list = OrderedList()
            for paragraph in lst.paragraphs:
                print(repr(''.join(run.text for run in paragraph.runs)))
                ordered_list.add(Paragraph(''.join(run.text for run in paragraph.runs),
                                           font_size=Decimal(14), font='Times-Roman'))
            self.layout.add(ordered_list)
        else:
            unordered_list = UnorderedList()
            for paragraph in lst.paragraphs:
                unordered_list.add(Paragraph(''.join(run.text for run in paragraph.runs),
                                             font_size=Decimal(14), font='Times-Roman'))
            self.layout.add(unordered_list)

    def add_picture(self, picture: types.Picture):
        self.layout.add(Image(Path(picture.path), width=Decimal(picture.width), height=Decimal(picture.height)))

    def save_file(self):
        with open(self.dist, "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, self.file)
