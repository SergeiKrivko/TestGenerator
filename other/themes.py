from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt

basic_theme = {
    'CodeColors':
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
            'SingleQuotedString': QColor(255, 50, 120)
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

    def code_colors(self):
        if 'CodeColors' in self.theme_data:
            for key, item in basic_theme['CodeColors'].items():
                yield key, self.theme_data['CodeColors'].get(key, item)
        else:
            return basic_theme['CodeColors'].items()


class ThemeManager:
    BASIC_THEME = 'basic'

    def __init__(self, theme_name='basic'):
        self.themes = {
            ThemeManager.BASIC_THEME: Theme(basic_theme),
            'darcula':
                Theme({
                    'CodeColors':
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
                    'CodeColors':
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
                    'CodeColors':
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
                    'CodeColors':
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
                    'CodeColors':
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

    def code_colors(self):
        return self.theme.code_colors()

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
                margin: 2px;
                border-radius: 4px;
                min-height: 20px;
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
            margin: 2px;
            border-radius: 4px;
            min-height: 20px;
        }}
        QListWidget QScrollBar::handle::horizontal {{
            background-color: {self['BorderColor']};
            margin: 2px;
            border-radius: 4px;
            min-width: 20px;
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
        QTextEdit QScrollBar::handle::vertical {{
            background-color: {self['BorderColor']};
            margin: 2px;
            border-radius: 4px;
            min-height: 20px;
        }}
        QTextEdit QScrollBar::handle::horizontal {{
            background-color: {self['BorderColor']};
            margin: 2px;
            border-radius: 4px;
            min-width: 20px;
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
