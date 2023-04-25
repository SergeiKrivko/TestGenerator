from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt

basic_theme = {
    'CodeColors':
        {
            'Identifier': Qt.black,
            'PreProcessor': Qt.darkYellow,
            'CommentLine': Qt.darkGreen,
            'CommentDoc': Qt.darkGreen,
            'Keyword': Qt.darkBlue,
            'Number': Qt.blue,
            'Operator': Qt.black,
            'DoubleQuotedString': QColor(255, 50, 120),
            'SingleQuotedString': QColor(255, 50, 120)
        },
    'Paper': Qt.white,
    'CaretLineBackgroundColor': QColor('#FFE4E4'),
    'MainColor': '#FFFFFF',
    'BgColor': '#F0F0F0',
    'Border': '2px solid #A0A0A0',
    'TextColor': '#000000'
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
                            'Identifier': QColor('#FFFFFF'),
                            'PreProcessor': QColor('#BBB529'),
                            'CommentLine': QColor('#74797B'),
                            'CommentDoc': QColor('#74797B'),
                            'Keyword': QColor('#CC7832'),
                            'Number': QColor('#5191A6'),
                            'Operator': QColor('#FFFFFF'),
                            'DoubleQuotedString': QColor('#5F864C'),
                            'SingleQuotedString': QColor('#5F864C')
                        },
                    'Paper': QColor('#2B2B2B'),
                    'CaretLineBackgroundColor': QColor('#323232'),
                    'MainColor': '#606060',
                    'BgColor': '#303030',
                    'Border': '2px solid #101010',
                    'TextColor': '#F0F0F0'
                }),
            'theme3':
                Theme({
                    'CodeColors':
                        {
                            'Identifier': QColor('#274D66'),
                            'PreProcessor': QColor('#8A3199'),
                            'CommentLine': QColor('#1F2A40'),
                            'CommentDoc': QColor('#1F2A40'),
                            'Keyword': QColor('#CC7832'),
                            'Number': QColor('#5191A6'),
                            'Operator': QColor('#304070'),
                            'DoubleQuotedString': QColor('#DE435C'),
                            'SingleQuotedString': QColor('#5F864C')
                        },
                    'Paper': QColor('#E7F6F2'),
                    'CaretLineBackgroundColor': QColor('#A5C9CA'),
                    'MainColor': '#E7F6F2',
                    'BgColor': '#A5C9CA',
                    'Border': '2px solid #395B64',
                    'TextColor': '#2C3333'
                }),
            'theme4':
                Theme({
                    'CodeColors':
                        {
                            'Identifier': QColor('#274D66'),
                            'PreProcessor': QColor('#8A3199'),
                            'CommentLine': QColor('#1F2A40'),
                            'CommentDoc': QColor('#1F2A40'),
                            'Keyword': QColor('#CC7832'),
                            'Number': QColor('#5191A6'),
                            'Operator': QColor('#304070'),
                            'DoubleQuotedString': QColor('#DE435C'),
                            'SingleQuotedString': QColor('#5F864C')
                        },
                    'Paper': QColor('#D2D79F'),
                    'CaretLineBackgroundColor': QColor('#90B77D'),
                    'MainColor': '#D2D79F',
                    'BgColor': '#90B77D',
                    'Border': '2px solid #42855B',
                    'TextColor': '#483838'
                }),
        }

        self.theme_name = ''
        self.theme = None
        self.set_theme(theme_name)
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
        self.theme = self.themes.get(theme_name, self.themes[ThemeManager.BASIC_THEME])
        self.bg_style_sheet = f"color: {self['TextColor']};" \
                              f"background-color: {self['BgColor']};"
        self.style_sheet = f"color: {self['TextColor']};" \
                           f"background-color: {self['MainColor']};" \
                           f"border: {self['Border']};" \
                           f"border-radius: 6px;"
        self.combo_box_style_sheet = f"QComboBox{{{self.style_sheet}}}" \
                                     "QComboBox::drop-down:button {border-radius: 5px;}"
        s = ''
        self.spin_box_style_sheet = self.style_sheet

    def add_custom_theme(self, theme_name, theme_data):
        self.themes[theme_name] = Theme(theme_data)
