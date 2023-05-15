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
                    'MainC': QColor('#000478'),
                    'CFile': QColor('#78176F'),
                    'HFile': QColor('#BBB529'),
                    'TxtFile': QColor('#D6D6D6'),
                    'MdFile': QColor('#95D68C')
                }),
            'ocean':
                Theme({
                    'QsciLexerCPP':
                        {
                            'Identifier': QColor('#274D66'),
                            'PreProcessor': QColor('#8A3199'),
                            'Comment': QColor('#1F2A40'),
                            'CommentLine': QColor('#1F2A40'),
                            'CommentDoc': QColor('#1F2A40'),
                            'Keyword': QColor('#CC7832'),
                            'Number': QColor('#5191A6'),
                            'Operator': QColor('#304070'),
                            'DoubleQuotedString': QColor('#DE435C'),
                            'SingleQuotedString': QColor('#5F864C')
                        },
                    'QsciLexerPython':
                        {
                            'Identifier': QColor('#274D66'),
                            'Comment': QColor('#1F2A40'),
                            'CommentBlock': QColor('#1F2A40'),
                            'Keyword': QColor('#CC7832'),
                            'Number': QColor('#5191A6'),
                            'Operator': QColor('#304070'),
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
                            'Identifier': QColor('#0F9C18'),
                            'PreProcessor': QColor('#1FBA8B'),
                            'Comment': QColor('#26470B'),
                            'CommentLine': QColor('#26470B'),
                            'CommentDoc': QColor('#26470B'),
                            'Keyword': QColor('#782622'),
                            'Number': QColor('#A9C718'),
                            'Operator': QColor('#0F9C18'),
                            'DoubleQuotedString': QColor('#784315'),
                            'SingleQuotedString': QColor('#784315')
                        },
                    'QsciLexerPython':
                        {
                            'Identifier': QColor('#0F9C18'),
                            'Comment': QColor('#1F2A40'),
                            'CommentBlock': QColor('#26470B'),
                            'Keyword': QColor('#782622'),
                            'Number': QColor('#A9C718'),
                            'Operator': QColor('#0F9C18'),
                            'ClassName': QColor('#1FBA8B'),
                            'Decorator': QColor('#1FBA8B'),
                            'FunctionMethodName': QColor('#1FBA8B'),
                            'DoubleQuotedString': QColor('#784315'),
                            'SingleQuotedString': QColor('#784315'),
                            'DoubleQuotedFString': QColor('#784315'),
                            'SingleQuotedFString': QColor('#784315'),
                            'TripleDoubleQuotedString': QColor('#784315'),
                            'TripleSingleQuotedString': QColor('#784315'),
                            'TripleDoubleQuotedFString': QColor('#784315'),
                            'TripleSingleQuotedFString': QColor('#784315'),
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
                    'Paper': QColor('#62077A'),
                    'CaretLineBackgroundColor': QColor('#78088F'),
                    'BraceColor': QColor('#F0DA4A'),
                    'MainColor': '#6A0A8A',
                    'BgColor': '#2D033B',
                    'BorderColor': '#C147E9',
                    'TextColor': '#E8ABF0',
                    'ColorSelected': '#AA0CB3',
                    'ColorHover': '#8D0DB8',
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
            'theme1':
                Theme({
                    'QsciLexerCPP':
                        {
                            'Identifier': QColor('#274D66'),
                            'PreProcessor': QColor('#8A3199'),
                            'Comment': QColor('#1F2A40'),
                            'CommentLine': QColor('#1F2A40'),
                            'CommentDoc': QColor('#1F2A40'),
                            'Keyword': QColor('#CC7832'),
                            'Number': QColor('#5191A6'),
                            'Operator': QColor('#304070'),
                            'DoubleQuotedString': QColor('#DE435C'),
                            'SingleQuotedString': QColor('#5F864C')
                        },
                    'QsciLexerPython':
                        {
                            'Identifier': QColor('#274D66'),
                            'Comment': QColor('#1F2A40'),
                            'CommentBlock': QColor('#1F2A40'),
                            'Keyword': QColor('#CC7832'),
                            'Number': QColor('#5191A6'),
                            'Operator': QColor('#304070'),
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
                    'MainColor': '#FFDEB4',
                    'BgColor': '#FDF7C3',
                    'BorderColor': '#FFB4B4',
                    'TextColor': '#7071F2',
                    'ColorSelected': '#AFB2FF',
                    'ColorHover': '#D4D2FF',
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
