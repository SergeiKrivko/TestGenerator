from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt

basic_theme = {
    'QsciLexerCPP':
        {
            'Identifier': Qt.black,
            'PreProcessor': Qt.darkYellow,
            'Comment': Qt.darkGreen,
            'CommentLine': Qt.darkGreen,
            'CommentDoc': Qt.darkGreen,
            'Keyword': Qt.darkBlue,
            'Number': Qt.blue,
            'Operator': Qt.black,
            'DoubleQuotedString': QColor(255, 50, 120),
            'SingleQuotedString': QColor(255, 50, 120),
        },
    'QsciLexerPython':
        {
            'Identifier': Qt.black,
            'Comment': Qt.darkGreen,
            'CommentBlock': Qt.darkGreen,
            'Keyword': Qt.darkBlue,
            'Number': Qt.blue,
            'Operator': Qt.black,
            'ClassName': Qt.darkBlue,
            'Decorator': Qt.blue,
            'FunctionMethodName': Qt.darkBlue,
            'DoubleQuotedString': QColor(255, 50, 120),
            'SingleQuotedString': QColor(255, 50, 120),
            'DoubleQuotedFString': QColor(255, 50, 120),
            'SingleQuotedFString': QColor(255, 50, 120),
            'TripleDoubleQuotedString': QColor(255, 50, 120),
            'TripleSingleQuotedString': QColor(255, 50, 120),
            'TripleDoubleQuotedFString': QColor(255, 50, 120),
            'TripleSingleQuotedFString': QColor(255, 50, 120),
        },
    'Paper': QColor(Qt.white),
    'CaretLineBackgroundColor': QColor('#E5F3FF'),
    'BraceColor': QColor('#373EF0'),
    'MainColor': '#FFFFFF',
    'BgColor': '#F0F0F0',
    'BorderColor': '#A0A0A0',
    'TextColor': '#000000',
    'ColorSelected': '#CCE8FF',
    'ColorHover': '#E5F3FF',
    'TestPassed': QColor('#12A013'),
    'TestFailed': QColor('#F82525'),
    'TestInProgress': QColor('#A0A0A0'),
    'TestCrashed': QColor('#A01010'),
    'MainC': QColor('#A01010'),
    'CFile': QColor('#F82525'),
    'HFile': QColor('#99922C'),
    'TxtFile': QColor('#2065D4'),
    'MdFile': QColor('#1BBDD4')
}


class Theme:
    def __init__(self, theme_data):
        self.theme_data = theme_data

    def get(self, key):
        return self.theme_data.get(key, basic_theme[key])

    def __getitem__(self, item):
        return self.get(item)

    def code_colors(self, lexer):
        if lexer in self.theme_data:
            for key, item in basic_theme[lexer].items():
                yield key, self.theme_data[lexer].get(key, item)
        else:
            return basic_theme[lexer].items()


class ThemeManager:
    BASIC_THEME = 'basic'

    def __init__(self, theme_name='basic'):
        self.themes = {
            ThemeManager.BASIC_THEME: Theme(basic_theme),
            'darcula':
                Theme({
                    'QsciLexerCPP':
                        {
                            'Identifier': QColor('#DFDFDF'),
                            'PreProcessor': QColor('#BBB529'),
                            'Comment': QColor('#74797B'),
                            'CommentLine': QColor('#74797B'),
                            'CommentDoc': QColor('#74797B'),
                            'Keyword': QColor('#CC7832'),
                            'Number': QColor('#5191A6'),
                            'Operator': QColor('#DFDFDF'),
                            'DoubleQuotedString': QColor('#5F864C'),
                            'SingleQuotedString': QColor('#5F864C')
                        },
                    'QsciLexerPython':
                        {
                            'Identifier': QColor('#DFDFDF'),
                            'Comment': QColor('#74797B'),
                            'CommentBlock': QColor('#74797B'),
                            'Keyword': QColor('#CC7832'),
                            'Number': QColor('#5191A6'),
                            'Operator': QColor('#DFDFDF'),
                            'ClassName': QColor('#F5BA56'),
                            'Decorator': QColor('#DEDB22'),
                            'FunctionMethodName': QColor('#F5BA56'),
                            'DoubleQuotedString': QColor('#5F864C'),
                            'SingleQuotedString': QColor('#5F864C'),
                            'DoubleQuotedFString': QColor('#5F864C'),
                            'SingleQuotedFString': QColor('#5F864C'),
                            'TripleDoubleQuotedString': QColor('#5F864C'),
                            'TripleSingleQuotedString': QColor('#5F864C'),
                            'TripleDoubleQuotedFString': QColor('#5F864C'),
                            'TripleSingleQuotedFString': QColor('#5F864C'),
                        },
                    'Paper': QColor('#2B2B2B'),
                    'CaretLineBackgroundColor': QColor('#323232'),
                    'BraceColor': QColor('#F0DA4A'),
                    'MainColor': '#606060',
                    'BgColor': '#303030',
                    'BorderColor': '#101010',
                    'TextColor': '#F0F0F0',
                    'ColorSelected': '#909090',
                    'ColorHover': '#777777',
                    'TestPassed': QColor('#CBF742'),
                    'TestFailed': QColor('#F82525'),
                    'TestInProgress': QColor('#A0A0A0'),
                    'TestCrashed': QColor('#A01010'),
                    'MainC': QColor('#0735C2'),
                    'CFile': QColor('#F716E8'),
                    'HFile': QColor('#BBB529'),
                    'TxtFile': QColor('#D6D6D6'),
                    'MdFile': QColor('#95D68C')
                }),
            'ocean':
                Theme({
                    'QsciLexerCPP':
                        {
                            'Identifier': QColor('#142836'),
                            'PreProcessor': QColor('#8A3199'),
                            'Comment': QColor('#B57831'),
                            'CommentLine': QColor('#B57831'),
                            'CommentDoc': QColor('#B57831'),
                            'Keyword': QColor('#0816B5'),
                            'Number': QColor('#5191A6'),
                            'Operator': QColor('#142836'),
                            'DoubleQuotedString': QColor('#DE435C'),
                            'SingleQuotedString': QColor('#5F864C')
                        },
                    'QsciLexerPython':
                        {
                            'Identifier': QColor('#142836'),
                            'Comment': QColor('#B57831'),
                            'CommentBlock': QColor('#B57831'),
                            'Keyword': QColor('#0816B5'),
                            'Number': QColor('#5191A6'),
                            'Operator': QColor('#142836'),
                            'ClassName': QColor('#E673D8'),
                            'Decorator': QColor('#E673D8'),
                            'FunctionMethodName': QColor('#E673D8'),
                            'DoubleQuotedString': QColor('#DE435C'),
                            'SingleQuotedString': QColor('#DE435C'),
                            'DoubleQuotedFString': QColor('#DE435C'),
                            'SingleQuotedFString': QColor('#DE435C'),
                            'TripleDoubleQuotedString': QColor('#DE435C'),
                            'TripleSingleQuotedString': QColor('#DE435C'),
                            'TripleDoubleQuotedFString': QColor('#DE435C'),
                            'TripleSingleQuotedFString': QColor('#DE435C'),
                        },
                    'Paper': QColor('#E7F6F2'),
                    'CaretLineBackgroundColor': QColor('#C1EDF5'),
                    'BraceColor': QColor('#EB6BD3'),
                    'MainColor': '#E7F6F2',
                    'BgColor': '#A5C9CA',
                    'BorderColor': '#395B64',
                    'TextColor': '#2C3333',
                    'ColorSelected': '#A2D7E5',
                    'ColorHover': '#C1EDF5',
                    'TestPassed': QColor('#449C38'),
                    'TestFailed': QColor('#F82525'),
                    'TestInProgress': QColor('#A0A0A0'),
                    'TestCrashed': QColor('#A01010'),
                    'MainC': QColor('#A01010'),
                    'CFile': QColor('#F82525'),
                    'HFile': QColor('#99922C'),
                    'TxtFile': QColor('#2065D4'),
                    'MdFile': QColor('#1BBDD4')
                }),
            'fresh':
                Theme({
                    'QsciLexerCPP':
                        {
                            'Identifier': QColor('#473333'),
                            'PreProcessor': QColor('#1FBA8B'),
                            'Comment': QColor('#525252'),
                            'CommentLine': QColor('#525252'),
                            'CommentDoc': QColor('#525252'),
                            'Keyword': QColor('#2F8023'),
                            'Number': QColor('#D93115'),
                            'Operator': QColor('#473333'),
                            'DoubleQuotedString': QColor('#8A5959'),
                            'SingleQuotedString': QColor('#8A5959')
                        },
                    'QsciLexerPython':
                        {
                            'Identifier': QColor('#473333'),
                            'Comment': QColor('#525252'),
                            'CommentBlock': QColor('#525252'),
                            'Keyword': QColor('#2F8023'),
                            'Number': QColor('#D93115'),
                            'Operator': QColor('#473333'),
                            'ClassName': QColor('#1FBA8B'),
                            'Decorator': QColor('#1FBA8B'),
                            'FunctionMethodName': QColor('#8A5959'),
                            'DoubleQuotedString': QColor('#8A5959'),
                            'SingleQuotedString': QColor('#8A5959'),
                            'DoubleQuotedFString': QColor('#8A5959'),
                            'SingleQuotedFString': QColor('#8A5959'),
                            'TripleDoubleQuotedString': QColor('#8A5959'),
                            'TripleSingleQuotedString': QColor('#8A5959'),
                            'TripleDoubleQuotedFString': QColor('#8A5959'),
                            'TripleSingleQuotedFString': QColor('#8A5959'),
                        },
                    'Paper': QColor('#D2D79F'),
                    'CaretLineBackgroundColor': QColor('#BAD78C'),
                    'BraceColor': QColor('#FF8831'),
                    'MainColor': '#D2D79F',
                    'BgColor': '#90B77D',
                    'BorderColor': '#42855B',
                    'TextColor': '#483838',
                    'ColorSelected': '#A3CF63',
                    'ColorHover': '#BAD78C',
                    'TestPassed': QColor('#327329'),
                    'TestFailed': QColor('#F82525'),
                    'TestInProgress': QColor('#A0A0A0'),
                    'TestCrashed': QColor('A01010'),
                    'MainC': QColor('#A01010'),
                    'CFile': QColor('#F82525'),
                    'HFile': QColor('#99922C'),
                    'TxtFile': QColor('#2065D4'),
                    'MdFile': QColor('#1BBDD4')
                }),
            'neon':
                Theme({
                    'QsciLexerCPP':
                        {
                            'Identifier': QColor('#E031DD'),
                            'PreProcessor': QColor('#5C67E0'),
                            'Comment': QColor('#E0691A'),
                            'CommentLine': QColor('#E0691A'),
                            'CommentDoc': QColor('#E0691A'),
                            'Keyword': QColor('#24AED4'),
                            'Number': QColor('#72961B'),
                            'Operator': QColor('#E031DD'),
                            'DoubleQuotedString': QColor('#E0282B'),
                            'SingleQuotedString': QColor('#E0282B')
                        },
                    'QsciLexerPython':
                        {
                            'Identifier': QColor('#E031DD'),
                            'Comment': QColor('#E0691A'),
                            'CommentBlock': QColor('#E0691A'),
                            'Keyword': QColor('#24AED4'),
                            'Number': QColor('#72961B'),
                            'Operator': QColor('#E031DD'),
                            'ClassName': QColor('#5C67E0'),
                            'Decorator': QColor('#5C67E0'),
                            'FunctionMethodName': QColor('#5C67E0'),
                            'DoubleQuotedString': QColor('#E0282B'),
                            'SingleQuotedString': QColor('#E0282B'),
                            'DoubleQuotedFString': QColor('#E0282B'),
                            'SingleQuotedFString': QColor('#E0282B'),
                            'TripleDoubleQuotedString': QColor('#E0282B'),
                            'TripleSingleQuotedString': QColor('#E0282B'),
                            'TripleDoubleQuotedFString': QColor('#E0282B'),
                            'TripleSingleQuotedFString': QColor('#E0282B'),
                        },
                    'Paper': QColor('#F9FFD0'),
                    'CaretLineBackgroundColor': QColor('#EEC1F0'),
                    'BraceColor': QColor('#E61B1B'),
                    'MainColor': '#F9FFD0',
                    'BgColor': '#F5EA5A',
                    'BorderColor': '#39B5E0',
                    'TextColor': '#A31ACB',
                    'ColorSelected': '#CFA0D9',
                    'ColorHover': '#EEC1F0',
                    'TestPassed': QColor('#327329'),
                    'TestFailed': QColor('#F82525'),
                    'TestInProgress': QColor('#A0A0A0'),
                    'TestCrashed': QColor('A01010'),
                    'MainC': QColor('#A01010'),
                    'CFile': QColor('#F82525'),
                    'HFile': QColor('#99922C'),
                    'TxtFile': QColor('#2065D4'),
                    'MdFile': QColor('#1BBDD4')
                }),
            'coffee':
                Theme({
                    'QsciLexerCPP':
                        {
                            'Identifier': QColor('#5C3D2E'),
                            'PreProcessor': QColor('#4B6587'),
                            'CommentLine': QColor('#4F0E0E'),
                            'CommentDoc': QColor('#4F0E0E'),
                            'Keyword': QColor('#FF8303'),
                            'Number': QColor('#38470B'),
                            'Operator': QColor('#5C3D2E'),
                            'DoubleQuotedString': QColor('#911F27'),
                            'SingleQuotedString': QColor('#911F27')
                        },
                    'QsciLexerPython':
                        {
                            'Identifier': QColor('#5C3D2E'),
                            'Comment': QColor('#4F0E0E'),
                            'CommentBlock': QColor('#4F0E0E'),
                            'Keyword': QColor('#FF8303'),
                            'Number': QColor('#38470B'),
                            'Operator': QColor('#5C3D2E'),
                            'ClassName': QColor('#4B6587'),
                            'Decorator': QColor('#4B6587'),
                            'FunctionMethodName': QColor('#4B6587'),
                            'DoubleQuotedString': QColor('#911F27'),
                            'SingleQuotedString': QColor('#911F27'),
                            'DoubleQuotedFString': QColor('#911F27'),
                            'SingleQuotedFString': QColor('#911F27'),
                            'TripleDoubleQuotedString': QColor('#911F27'),
                            'TripleSingleQuotedString': QColor('#911F27'),
                            'TripleDoubleQuotedFString': QColor('#911F27'),
                            'TripleSingleQuotedFString': QColor('#911F27'),
                        },
                    'Paper': QColor('#FFDCC5'),
                    'CaretLineBackgroundColor': QColor('#F2CEB1'),
                    'BraceColor': QColor('#FC8817'),
                    'MainColor': '#D9B28D',
                    'BgColor': '#D7B19D',
                    'BorderColor': '#865439',
                    'TextColor': '#402218',
                    'ColorSelected': '#E8C3B0',
                    'ColorHover': '#E0BB9D',
                    'TestPassed': QColor('#327329'),
                    'TestFailed': QColor('#F82525'),
                    'TestInProgress': QColor('#A0A0A0'),
                    'TestCrashed': QColor('A01010'),
                    'MainC': QColor('#A01010'),
                    'CFile': QColor('#F82525'),
                    'HFile': QColor('#99922C'),
                    'TxtFile': QColor('#2065D4'),
                    'MdFile': QColor('#1BBDD4')
                }),
            'fire':
                Theme({
                    'QsciLexerCPP':
                        {
                            'Identifier': QColor('#F9FA9D'),
                            'PreProcessor': QColor('#A3DEA0'),
                            'Comment': QColor('#1F1F1F'),
                            'CommentLine': QColor('#1F1F1F'),
                            'CommentDoc': QColor('#1F1F1F'),
                            'Keyword': QColor('#A9CBDE'),
                            'Number': QColor('#DEDEDE'),
                            'Operator': QColor('#F9FA9D'),
                            'DoubleQuotedString': QColor('#DEABD3'),
                            'SingleQuotedString': QColor('#DEABD3')
                        },
                    'QsciLexerPython':
                        {
                            'Identifier': QColor('#F9FA9D'),
                            'Comment': QColor('#1F1F1F'),
                            'CommentBlock': QColor('#1F1F1F'),
                            'Keyword': QColor('#A9CBDE'),
                            'Number': QColor('#DEDEDE'),
                            'Operator': QColor('#F9FA9D'),
                            'ClassName': QColor('#A3DEA0'),
                            'Decorator': QColor('#A3DEA0'),
                            'FunctionMethodName': QColor('#A3DEA0'),
                            'DoubleQuotedString': QColor('#DEABD3'),
                            'SingleQuotedString': QColor('#DEABD3'),
                            'DoubleQuotedFString': QColor('#DEABD3'),
                            'SingleQuotedFString': QColor('#DEABD3'),
                            'TripleDoubleQuotedString': QColor('#DEABD3'),
                            'TripleSingleQuotedString': QColor('#DEABD3'),
                            'TripleDoubleQuotedFString': QColor('#DEABD3'),
                            'TripleSingleQuotedFString': QColor('#DEABD3'),
                        },
                    'Paper': QColor('#B23925'),
                    'CaretLineBackgroundColor': QColor('#B24E26'),
                    'BraceColor': QColor('#FC8817'),
                    'MainColor': '#B22222',
                    'BgColor': '#7C0A02',
                    'BorderColor': '#E25822',
                    'TextColor': '#F1BC31',
                    'ColorSelected': '#CF0E04',
                    'ColorHover': '#DB4016',
                    'TestPassed': QColor('#2496C9'),
                    'TestFailed': QColor('#ED8029'),
                    'TestInProgress': QColor('#B8BD65'),
                    'TestCrashed': QColor('470707'),
                    'MainC': QColor('#F7F410'),
                    'CFile': QColor('#F7A524'),
                    'HFile': QColor('#E562E6'),
                    'TxtFile': QColor('#4262E5'),
                    'MdFile': QColor('#33B7E5')
                }),
            'night':
                Theme({
                    'QsciLexerCPP':
                        {
                            'Identifier': QColor('#DFDFDF'),
                            'PreProcessor': QColor('#BBB529'),
                            'Comment': QColor('#74797B'),
                            'CommentLine': QColor('#74797B'),
                            'CommentDoc': QColor('#74797B'),
                            'Keyword': QColor('#D767FF'),
                            'Number': QColor('#5191A6'),
                            'Operator': QColor('#DFDFDF'),
                            'DoubleQuotedString': QColor('#5F864C'),
                            'SingleQuotedString': QColor('#5F864C')
                        },
                    'QsciLexerPython':
                        {
                            'Identifier': QColor('#DFDFDF'),
                            'Comment': QColor('#74797B'),
                            'CommentBlock': QColor('#74797B'),
                            'Keyword': QColor('#D767FF'),
                            'Number': QColor('#5191A6'),
                            'Operator': QColor('#DFDFDF'),
                            'ClassName': QColor('#F5BA56'),
                            'Decorator': QColor('#DEDB22'),
                            'FunctionMethodName': QColor('#F5BA56'),
                            'DoubleQuotedString': QColor('#5F864C'),
                            'SingleQuotedString': QColor('#5F864C'),
                            'DoubleQuotedFString': QColor('#5F864C'),
                            'SingleQuotedFString': QColor('#5F864C'),
                            'TripleDoubleQuotedString': QColor('#5F864C'),
                            'TripleSingleQuotedString': QColor('#5F864C'),
                            'TripleDoubleQuotedFString': QColor('#5F864C'),
                            'TripleSingleQuotedFString': QColor('#5F864C'),
                        },
                    'Paper': QColor('#42324A'),
                    'CaretLineBackgroundColor': QColor('#574261'),
                    'BraceColor': QColor('#F0DA4A'),
                    'MainColor': '#634378',
                    'BgColor': '#250230',
                    'BorderColor': '#8B33A8',
                    'TextColor': '#EDBFF2',
                    'ColorSelected': '#3E5378',
                    'ColorHover': '#4E4378',
                    'TestPassed': QColor('#62DB26'),
                    'TestFailed': QColor('#E54E13'),
                    'TestInProgress': QColor('#DEABDC'),
                    'TestCrashed': QColor('#5F097D'),
                    'MainC': QColor('#CE62F0'),
                    'CFile': QColor('#686DF0'),
                    'HFile': QColor('#4CF09C'),
                    'TxtFile': QColor('#D2F056'),
                    'MdFile': QColor('#F0AC5C')
                }),
            'orange': Theme({
                'QsciLexerCPP':
                    {
                        'Identifier': QColor('#000000'),
                        'PreProcessor': QColor('#C31FC7'),
                        'Comment': QColor('#909090'),
                        'CommentLine': QColor('#909090'),
                        'CommentDoc': QColor('#909090'),
                        'Keyword': QColor('#F06D26'),
                        'Number': QColor('#3392C2'),
                        'Operator': QColor('#000000'),
                        'DoubleQuotedString': QColor('#5CA123'),
                        'SingleQuotedString': QColor('#5CA123')
                    },
                'QsciLexerPython':
                    {
                        'Identifier': QColor('#000000'),
                        'Comment': QColor('#909090'),
                        'CommentBlock': QColor('#909090'),
                        'Keyword': QColor('#F06D26'),
                        'Number': QColor('#3392C2'),
                        'Operator': QColor('#000000'),
                        'ClassName': QColor('#C31FC7'),
                        'Decorator': QColor('#C31FC7'),
                        'FunctionMethodName': QColor('#C31FC7'),
                        'DoubleQuotedString': QColor('#5CA123'),
                        'SingleQuotedString': QColor('#5CA123'),
                        'DoubleQuotedFString': QColor('#5CA123'),
                        'SingleQuotedFString': QColor('#5CA123'),
                        'TripleDoubleQuotedString': QColor('#5CA123'),
                        'TripleSingleQuotedString': QColor('#5CA123'),
                        'TripleDoubleQuotedFString': QColor('#5CA123'),
                        'TripleSingleQuotedFString': QColor('#5CA123'),
                    },
                'Paper': QColor('#F0DEC4'),
                'CaretLineBackgroundColor': QColor('#F0D6B4'),
                'BraceColor': QColor('#FF8831'),
                'MainColor': '#F2D7AD',
                'BgColor': '#F0F0F0',
                'BorderColor': '#F27317',
                'TextColor': '#000000',
                'ColorSelected': '#FFCB99',
                'ColorHover': '#F2CE9C',
                'TestPassed': QColor('#3BA126'),
                'TestFailed': QColor('#F82525'),
                'TestInProgress': QColor('#A0A0A0'),
                'TestCrashed': QColor('A01010'),
                'MainC': QColor('#A01010'),
                'CFile': QColor('#F82525'),
                'HFile': QColor('#9C783C'),
                'TxtFile': QColor('#2065D4'),
                'MdFile': QColor('#1BBDD4')
            }),
        }

        self.theme_name = ''
        self.theme = None
        self.style_sheet = ''
        self.bg_style_sheet = ''
        self.set_theme(theme_name)

    def __getitem__(self, item):
        return self.theme.get(item)

    def get(self, item):
        return self.theme.get(item)

    def code_colors(self, lexer):
        return self.theme.code_colors(lexer)

    def set_theme(self, theme_name):
        self.theme_name = theme_name
        if theme_name not in self.themes:
            self.theme_name = ThemeManager.BASIC_THEME
        self.theme = self.themes.get(theme_name, self.themes[ThemeManager.BASIC_THEME])
        self.bg_style_sheet = f"color: {self['TextColor']};\n" \
                              f"background-color: {self['BgColor']};"
        self.style_sheet = f"color: {self['TextColor']};\n" \
                           f"background-color: {self['MainColor']};\n" \
                           f"border: 1px solid {self['BorderColor']};\n" \
                           f"border-radius: 4px;"
        self.scintilla_style_sheet = f"""
            QsciScintilla {{
                {self.style_sheet}
            }}
            QsciScintilla QScrollBar:vertical {{
                background: rgba{self['Paper'].getRgb()};
                border-top-right-radius: 5px;
                border-bottom-right-radius: 5px;
                width: 12px;
                margin: 0px;
            }}
            QsciScintilla QScrollBar::handle::vertical {{
                background-color: {self['BorderColor']};
                margin: 2px 2px 2px 6px;
                border-radius: 2px;
                min-height: 20px;
            }}
            QsciScintilla QScrollBar::handle::vertical:hover {{
                margin: 2px;
                border-radius: 4px;
            }}
            QsciScintilla QScrollBar::sub-page, QScrollBar::add-page {{
                background: none;
            }}
            QsciScintilla QScrollBar::sub-line, QScrollBar::add-line {{
                background: none;
                height: 0px;
                subcontrol-position: left;
                subcontrol-origin: margin;
            }}"""
        self.list_widget_style_sheet = f"""
        QListWidget {{
            {self.style_sheet}
        }}
        QListWidget::item {{
            border-radius: 6px;
        }}
        QListWidget::item:hover {{
            background-color: {self['ColorHover']};
            border: none;
        }}
        QListWidget::item:selected {{
            color: {self['TextColor']};
            background-color: {self['ColorSelected']};
            border: none;
            border-radius: 6px;
        }}
        QListWidget QScrollBar:vertical {{
            background: {self['MainColor']};
            border-top-right-radius: 4px;
            border-bottom-right-radius: 4px;
            width: 12px;
            margin: 0px;
        }}
        QListWidget QScrollBar:horizontal {{
            background: {self['MainColor']};
            border-bottom-left-radius: 4px;
            border-bottom-right-radius: 4px;
            height: 12px;
            margin: 0px;
        }}
        QListWidget QScrollBar::handle::vertical {{
            background-color: {self['BorderColor']};
            margin: 2px 2px 2px 6px;
            border-radius: 2px;
            min-height: 20px;
        }}
        QListWidget QScrollBar::handle::vertical:hover {{
            margin: 2px;
            border-radius: 4px;
        }}
        QListWidget QScrollBar::handle::horizontal {{
            background-color: {self['BorderColor']};
            margin: 6px 2px 2px 2px;
            border-radius: 2px;
            min-width: 20px;
        }}
        QListWidget QScrollBar::handle::horizontal:hover {{
            margin: 2px;
            border-radius: 4px;
        }}
        QListWidget QScrollBar::sub-page, QScrollBar::add-page {{
            background: none;
        }}
        QListWidget QScrollBar::sub-line, QScrollBar::add-line {{
            background: none;
            height: 0px;
            subcontrol-position: left;
            subcontrol-origin: margin;
        }}
        """
        self.text_edit_style_sheet = f"""
        QTextEdit {{
        {self.style_sheet}
        }}
        QTextEdit QScrollBar:vertical {{
            background: {self['MainColor']};
            border-top-right-radius: 5px;
            border-bottom-right-radius: 5px;
            width: 12px;
            margin: 0px;
        }}
        QTextEdit QScrollBar:horizontal {{
            background: {self['MainColor']};
            border-bottom-left-radius: 5px;
            border-bottom-right-radius: 5px;
            height: 12px;
            margin: 0px;
        }}
        QTextEdit QScrollBar::handle::horizontal {{
            background-color: {self['BorderColor']};
            margin: 6px 2px 2px 2px;
            border-radius: 2px;
            min-width: 20px;
        }}
        QTextEdit QScrollBar::handle::horizontal:hover {{
            margin: 2px;
            border-radius: 4px;
        }}
        QTextEdit QScrollBar::handle::vertical {{
            background-color: {self['BorderColor']};
            margin: 2px 2px 2px 6px;
            border-radius: 2px;
            min-height: 20px;
        }}
        QTextEdit QScrollBar::handle::vertical:hover {{
            margin: 2px;
            border-radius: 4px;
        }}
        QTextEdit QScrollBar::sub-page, QScrollBar::add-page {{
            background: none;
        }}
        QTextEdit QScrollBar::sub-line, QScrollBar::add-line {{
            background: none;
            height: 0px;
            subcontrol-position: left;
            subcontrol-origin: margin;
        }}
        """
        self.buttons_style_sheet = f"""
        QPushButton {{ {self.style_sheet} }}
        QPushButton::hover {{
            background-color: {self['ColorHover']};
        }}
        QPushButton::disabled {{
            color: {self['BgColor']};
            border-color: {self['MainColor']};
        }}
        """
        self.combo_box_style_sheet = f"""
        QComboBox {{
        {self.style_sheet}
        }}
        QComboBox::hover {{
        background-color: {self['ColorHover']};
        }}
        QComboBox::drop-down:button {{
        border-radius: 5px;
        }}
        QComboBox QAbstractItemView {{
        color: {self['TextColor']};
        background-color: {self['MainColor']};
        border: 1px solid {self['BorderColor']};
        selection-color: {self['TextColor']};
        selection-background-color: {self['ColorHover']};
        border-radius: 4px;
        }}
        """
        self.spin_box_style_sheet = f"""
        QSpinBox {{
            {self.style_sheet}
        }}
        QSpinBox::up-button {{
            color: {self['TextColor']};
            background-color: {self['MainColor']};
            border-left: 1px solid {self['BorderColor']};
            border-bottom: 1px solid {self['BorderColor']};
            border-top-right-radius: 3px;
        }}
        QSpinBox::up-button::disabled {{
            border: 0px solid {self['BorderColor']};
        }}
        QSpinBox::up-button::hover {{
            background-color: {self['ColorHover']};
        }}
        QSpinBox::down-button {{
            color: {self['TextColor']};
            background-color: {self['MainColor']};
            border-left: 1px solid {self['BorderColor']};
            border-top: 1px solid {self['BorderColor']};
            border-bottom-right-radius: 3px;
        }}
        QSpinBox::down-button::disabled {{
            border: 0px solid {self['BorderColor']};
        }}
        QSpinBox::down-button::hover {{
            background-color: {self['ColorHover']};
        }}
        QSpinBox::disabled {{
            color: {self['BgColor']};
            border-color: {self['MainColor']};
        }}
        """
        self.double_spin_box_style_sheet = self.spin_box_style_sheet.replace('QSpinBox', 'QDoubleSpinBox')

    def add_custom_theme(self, theme_name, theme_data):
        self.themes[theme_name] = Theme(theme_data)
