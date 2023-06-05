from PyQt5.QtGui import QColor, QFont
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QMainWindow, QLineEdit, QTextEdit, QScrollArea, QPushButton, QSpinBox, \
    QDoubleSpinBox, QComboBox, QProgressBar, QTabWidget

basic_theme = {
    'Identifier': Qt.black,
    'Preprocessor': Qt.darkYellow,
    'Comment': Qt.darkGreen,
    'Keyword': Qt.darkBlue,
    'Number': Qt.blue,
    'String': QColor(255, 50, 120),
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
    'Directory': QColor('#2F7519'),
    'FontFamily': "Calibri",
    'CodeFontFamily': "Courier",
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
                    'Identifier': QColor('#DFDFDF'),
                    'Preprocessor': QColor('#BBB529'),
                    'Comment': QColor('#74797B'),
                    'Keyword': QColor('#CC7832'),
                    'Number': QColor('#5191A6'),
                    'String': QColor('#5F864C'),

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
                    'CFile': QColor('#F790F7'),
                    'HFile': QColor('#BBB529'),
                    'TxtFile': QColor('#D6D6D6'),
                    'Directory': QColor('#95D68C')
                }),
            'ocean':
                Theme({
                    'Identifier': QColor('#142836'),
                    'Preprocessor': QColor('#8A3199'),
                    'Comment': QColor('#B57831'),
                    'Keyword': QColor('#0816B5'),
                    'Number': QColor('#5191A6'),
                    'String': QColor('#DE435C'),

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
                    'Directory': QColor('#1BBDD4')
                }),
            'fresh':
                Theme({
                    'Identifier': QColor('#473333'),
                    'Preprocessor': QColor('#1FBA8B'),
                    'Comment': QColor('#525252'),
                    'Keyword': QColor('#2F8023'),
                    'Number': QColor('#D93115'),
                    'String': QColor('#8A5959'),

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
                    'Identifier': QColor('#E031DD'),
                    'Preprocessor': QColor('#5C67E0'),
                    'Comment': QColor('#E0691A'),
                    'Keyword': QColor('#24AED4'),
                    'Number': QColor('#72961B'),
                    'String': QColor('#E0282B'),

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
                    'Identifier': QColor('#5C3D2E'),
                    'Preprocessor': QColor('#4B6587'),
                    'Comment': QColor('#4F0E0E'),
                    'Keyword': QColor('#FF8303'),
                    'Number': QColor('#38470B'),
                    'String': QColor('#911F27'),

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
                    'Identifier': QColor('#F9FA9D'),
                    'Preprocessor': QColor('#A3DEA0'),
                    'Comment': QColor('#1F1F1F'),
                    'Keyword': QColor('#A9CBDE'),
                    'Number': QColor('#DEDEDE'),
                    'String': QColor('#DEABD3'),

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
                    'Identifier': QColor('#DFDFDF'),
                    'Preprocessor': QColor('#BBB529'),
                    'Comment': QColor('#74797B'),
                    'Keyword': QColor('#D767FF'),
                    'Number': QColor('#5191A6'),
                    'String': QColor('#5F864C'),

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
            'orange':
                Theme({
                    'Identifier': QColor('#000000'),
                    'Preprocessor': QColor('#C31FC7'),
                    'Comment': QColor('#909090'),
                    'Keyword': QColor('#F06D26'),
                    'Number': QColor('#3392C2'),
                    'String': QColor('#5CA123'),

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
                    'Directory': QColor('#2E8217')
                }),
            'flamingo':
                Theme({
                    'Identifier': QColor('#3B2C3B'),
                    'Preprocessor': QColor('#3B9629'),
                    'Comment': QColor('#A19F26'),
                    'Keyword': QColor('#CB45F0'),
                    'Number': QColor('#2D62F2'),
                    'String': QColor('#C2451A'),

                    'Paper': QColor('#F7DDF4'),
                    'CaretLineBackgroundColor': QColor('#F5BFF7'),
                    'BraceColor': QColor('#CB45F0'),
                    'MainColor': '#F0C6F2',
                    'BgColor': '#FFFFFF',
                    'BorderColor': '#93699E',
                    'TextColor': '#2F1233',
                    'ColorSelected': '#D6A0D5',
                    'ColorHover': '#E6ACE5',
                    'TestPassed': QColor('#2D9124'),
                    'TestFailed': QColor('#F82525'),
                    'TestInProgress': QColor('#9D70A0'),
                    'TestCrashed': QColor('A01010'),
                    'MainC': QColor('#1933E3'),
                    'CFile': QColor('#2D62F2'),
                    'HFile': QColor('#3B9629'),
                    'TxtFile': QColor('#2065D4'),
                    'Directory': QColor('#F74A15')
                }),
            'cyan':
                Theme({
                    'Identifier': QColor('#263330'),
                    'Preprocessor': QColor('#28871A'),
                    'Comment': QColor('#A6A424'),
                    'Keyword': QColor('#D92C2C'),
                    'Number': QColor('#AF27D4'),
                    'String': QColor('#247FD9'),

                    'Paper': QColor('#DCF2EC'),
                    'CaretLineBackgroundColor': QColor('#B4F2E5'),
                    'BraceColor': QColor('#FF8831'),
                    'MainColor': '#BBDED0',
                    'BgColor': '#E8E8E8',
                    'BorderColor': '#4FDEAF',
                    'TextColor': '#0C3326',
                    'ColorSelected': '#66F2CB',
                    'ColorHover': '#8CF2D8',
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
            'space':
                Theme({
                    'Identifier': QColor('#DFDFDF'),
                    'Preprocessor': QColor('#D494CF'),
                    'Comment': QColor('#AD9381'),
                    'Keyword': QColor('#19A7D9'),
                    'Number': QColor('#28D49C'),
                    'String': QColor('#84D434'),

                    'Paper': QColor('#222333'),
                    'CaretLineBackgroundColor': QColor('#323232'),
                    'BraceColor': QColor('#F0DA4A'),
                    'MainColor': '#292E3D',
                    'BgColor': '#0C0C1C',
                    'BorderColor': '#07093B',
                    'TextColor': '#F0F0F0',
                    'ColorSelected': '#20204D',
                    'ColorHover': '#23233D',
                    'TestPassed': QColor('#CBF742'),
                    'TestFailed': QColor('#FC6921'),
                    'TestInProgress': QColor('#A0A0A0'),
                    'TestCrashed': QColor('#A01010'),
                    'MainC': QColor('#28D49C'),
                    'CFile': QColor('#19A7D9'),
                    'HFile': QColor('#D494CF'),
                    'TxtFile': QColor('#D6D6D6'),
                    'Directory': QColor('#95D68C')
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

    def set_theme_to_list_widget(self, widget, font=None):
        widget.setStyleSheet(self.list_widget_style_sheet)
        for i in range(widget.count()):
            widget.item(i).setFont(font if font else self.font_small)

    def auto_css(self, widget: QWidget, code_font=False):
        if code_font:
            widget.setFont(self.code_font)
        else:
            widget.setFont(self.font_small)

        if isinstance(widget, QMainWindow):
            widget.setStyleSheet(self.bg_style_sheet)
        elif isinstance(widget, QLineEdit):
            widget.setStyleSheet(self.style_sheet)
        elif isinstance(widget, QTextEdit):
            widget.setStyleSheet(self.text_edit_style_sheet)
        elif isinstance(widget, QScrollArea):
            widget.setStyleSheet(self.scroll_area_style_sheet)
        elif isinstance(widget, QPushButton):
            widget.setStyleSheet(self.buttons_style_sheet)
        elif isinstance(widget, QSpinBox):
            widget.setStyleSheet(self.spin_box_style_sheet)
        elif isinstance(widget, QDoubleSpinBox):
            widget.setStyleSheet(self.double_spin_box_style_sheet)
        elif isinstance(widget, QComboBox):
            widget.setStyleSheet(self.combo_box_style_sheet)
        elif isinstance(widget, QProgressBar):
            widget.setStyleSheet(self.progress_bar_style_sheet)
        elif isinstance(widget, QTabWidget):
            widget.setStyleSheet(self.tab_widget_style_sheet)

    def css_to_options_widget(self, widget):
        widget.setFont(self.font_small)
        for el in widget.widgets.values():
            self.auto_css(el)
        for el in widget.labels.values():
            self.auto_css(el)

    def set_theme(self, theme_name):
        self.theme_name = theme_name
        if theme_name not in self.themes:
            self.theme_name = ThemeManager.BASIC_THEME
        self.theme = self.themes.get(theme_name, self.themes[ThemeManager.BASIC_THEME])
        self.font_small = QFont(self.get('FontFamily'), 11)
        self.font_medium = QFont(self.get('FontFamily'), 14)
        self.font_big = QFont(self.get('FontFamily'), 18)
        self.code_font_std = QFont(self.get('CodeFontFamily'), 10)
        self.code_font = QFont(self.get('CodeFontFamily'), 11)
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
        self.scroll_area_style_sheet = f"""
QScrollArea {{
    {self.style_sheet}
}}
QScrollArea QScrollBar:vertical {{
    background: {self['BgColor']};
    border-top-right-radius: 4px;
    border-bottom-right-radius: 4px;
    width: 12px;
    margin: 0px;
}}
QScrollArea QScrollBar:horizontal {{
    background: {self['BgColor']};
    border-bottom-left-radius: 4px;
    border-bottom-right-radius: 4px;
    height: 12px;
    margin: 0px;
}}
QScrollArea QScrollBar::handle::vertical {{
    background-color: {self['BorderColor']};
    margin: 2px 2px 2px 6px;
    border-radius: 2px;
    min-height: 20px;
}}
QScrollArea QScrollBar::handle::vertical:hover {{
    margin: 2px;
    border-radius: 4px;
}}
QScrollArea QScrollBar::handle::horizontal {{
    background-color: {self['BorderColor']};
    margin: 6px 2px 2px 2px;
    border-radius: 2px;
    min-width: 20px;
}}
QScrollArea QScrollBar::handle::horizontal:hover {{
    margin: 2px;
    border-radius: 4px;
}}
QScrollArea QScrollBar::sub-page, QScrollBar::add-page {{
    background: none;
}}
QScrollArea QScrollBar::sub-line, QScrollBar::add-line {{
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
        self.progress_bar_style_sheet = f"""
QProgressBar {{
color: {self['TextColor']};
background-color: {self['BgColor']};
border: 1px solid {self['BorderColor']};
border-radius: 4px;
text-align: center;
}}
QProgressBar::chunk {{
background-color: {self['MainColor']};
}}
"""

        self.tab_widget_style_sheet = f"""
QTabWidget::pane {{
    color: {self['BgColor']};
    }}
QTabBar::tab {{
    color: {self['TextColor']};
    background-color: {self['MainColor']};
    border-bottom-color: {self['TextColor']};
    border-top-left-radius: 5px;
    border-top-right-radius: 5px;
    border: 1px solid {self['BorderColor']};
    width: 50px;
    padding: 4px;
    }}
QTabBar::tab:hover {{
background-color: {self['ColorHover']};
}}
QTabBar::tab:selected {{
background-color: {self['ColorSelected']};
}}
"""

    def add_custom_theme(self, theme_name, theme_data):
        self.themes[theme_name] = Theme(theme_data)
