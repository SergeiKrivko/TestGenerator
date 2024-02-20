import os
import shutil
from io import BytesIO
from uuid import uuid4

import PIL.Image as Image
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont
from PyQt6.QtWidgets import QWidget, QMainWindow, QLineEdit, QTextEdit, QScrollArea, QPushButton, QSpinBox, \
    QDoubleSpinBox, QComboBox, QProgressBar, QTabWidget, QListWidget, QCheckBox, QLabel, QTabBar, QTreeWidget, QMenu

from src import config
from src.ui.button import Button
from src.ui.resources import resources

if config.USE_TELEGRAM:
    from src.ui.resources_emoji import resources as r
    resources.update(r)

basic_theme = {
    'Identifier': Qt.GlobalColor.black,
    'Preprocessor': Qt.GlobalColor.darkYellow,
    'Comment': Qt.GlobalColor.darkGreen,
    'Keyword': Qt.GlobalColor.darkBlue,
    'Number': Qt.GlobalColor.blue,
    'String': QColor(255, 50, 120),

    'Paper': QColor(Qt.GlobalColor.white),
    'CaretLineBackgroundColor': QColor('#E5F3FF'),
    'BraceColor': QColor('#373EF0'),

    'MainColor': '#FFFFFF',
    'MainHoverColor': '#E5F3FF',
    'MainSelectedColor': '#CCE8FF',
    'BgColor': '#F0F0F0',
    'BgHoverColor': '#E3E3E3',
    'BgSelectedColor': '#B8E3E3',
    'MenuColor': '#ADADAD',
    'MenuHoverColor': '#8F8F8F',
    'MenuSelectedColor': '#6AA39E',
    'BorderColor': '#969696',
    'TextColor': '#000000',

    'ImageColor': (0, 0, 0),
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
    'CodeFontFamily': "Consolas",
}


class Theme:
    def __init__(self, theme_data):
        self.theme_data = theme_data

    def get(self, key):
        return self.theme_data.get(key, basic_theme.get(key))

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

    def __init__(self, sm, theme_name='basic'):
        self.sm = sm
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
                    'MainHoverColor': '#777777',
                    'MainSelectedColor': '#909090',
                    'BgColor': '#303030',
                    'BgHoverColor': '#474747',
                    'BgSelectedColor': '#575757',
                    'MenuColor': '#1F1F1F',
                    'MenuHoverColor': '#2E2E2E',
                    'MenuSelectedColor': '#3D3D3D',
                    'BorderColor': '#101010',
                    'TextColor': '#F0F0F0',
                    'ImageColor': (250, 250, 250),

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
                    'MainHoverColor': '#C1EDF5',
                    'MainSelectedColor': '#A2D7E5',
                    'BgColor': '#A5C9CA',
                    'BgHoverColor': '#98B9BA',
                    'BgSelectedColor': '#93A3A3',
                    'MenuColor': '#4D7B87',
                    'MenuHoverColor': '#446D78',
                    'MenuSelectedColor': '#3A5D66',
                    'BorderColor': '#3E5875',
                    'TextColor': '#191C42',
                    'ImageColor': (25, 28, 66),

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
                    'MainHoverColor': '#BAD78C',
                    'MainSelectedColor': '#A3CF63',
                    'BgColor': '#90B77D',
                    'BgHoverColor': '#9FC98A',
                    'BgSelectedColor': '#73C978',
                    'MenuColor': '#539667',
                    'MenuHoverColor': '#4C8A5F',
                    'MenuSelectedColor': '#4D8A51',
                    'BorderColor': '#39703A',
                    'TextColor': '#403232',
                    'ImageColor': (64, 50, 50),

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
                    'MainHoverColor': '#EEC1F0',
                    'MainSelectedColor': '#CFA0D9',
                    'BgColor': '#F5EA5A',
                    'BgHoverColor': '#E8DE55',
                    'BgSelectedColor': '#D4CA4E',
                    'MenuColor': '#4EC9CC',
                    'MenuHoverColor': '#48B7BA',
                    'MenuSelectedColor': '#35A8A8',
                    'BorderColor': '#39B5E0',
                    'TextColor': '#A31ACB',
                    'ImageColor': (166, 23, 203),

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
                    'MainHoverColor': '#E0BB9D',
                    'MainSelectedColor': '#E8C3B0',
                    'BgColor': '#D7B19D',
                    'BgHoverColor': '#CCA895',
                    'BgSelectedColor': '#BD9A8A',
                    'MenuColor': '#865439',
                    'MenuHoverColor': '#9C6242',
                    'MenuSelectedColor': '#AB6B49',
                    'BorderColor': '#6B432E',
                    'TextColor': '#402218',
                    'ImageColor': (64, 34, 24),

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

                    'MainColor': '#8C2E0D',
                    'MainHoverColor': '#DB4016',
                    'MainSelectedColor': '#CF0E04',
                    'BgColor': '#7C0A02',
                    'BgHoverColor': '#8F0C02',
                    'BgSelectedColor': '#A30D03',
                    'MenuColor': '#57130B',
                    'MenuHoverColor': '#450F09',
                    'MenuSelectedColor': '#2B0A06',
                    'BorderColor': '#E25822',
                    'TextColor': '#F1BC31',
                    'ImageColor': (241, 188, 49),

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
                    'MainHoverColor': '#4E4378',
                    'MainSelectedColor': '#3E5378',
                    'BgColor': '#250230',
                    'BgHoverColor': '#330342',
                    'BgSelectedColor': '#47045C',
                    'MenuColor': '#470246',
                    'MenuHoverColor': '#570355',
                    'MenuSelectedColor': '#70046E',
                    'BorderColor': '#9C0499',
                    'TextColor': '#EDBFF2',
                    'ImageColor': (237, 191, 242),

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
                    'MainHoverColor': '#F2CE9C',
                    'MainSelectedColor': '#FFCB99',
                    'BgColor': '#F0F0F0',
                    'BgHoverColor': '#E3D2C8',
                    'BgSelectedColor': '#E3C3AE',
                    'MenuColor': '#F28B41',
                    'MenuHoverColor': '#E3823D',
                    'MenuSelectedColor': '#E0651B',
                    'BorderColor': '#F26510',
                    'TextColor': '#000000',
                    'ImageColor': (217, 126, 29),

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
                    'MainHoverColor': '#E6ACE5',
                    'MainSelectedColor': '#D6A0D5',
                    'BgColor': '#FFFFFF',
                    'BgHoverColor': '#F3DEF7',
                    'BgSelectedColor': '#F3C6F7',
                    'MenuColor': '#DEA7F2',
                    'MenuHoverColor': '#DC9CF2',
                    'MenuSelectedColor': '#D67CF2',
                    'BorderColor': '#93699E',
                    'TextColor': '#2F1233',
                    'ImageColor': (47, 18, 51),

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
                    'MainHoverColor': '#8CF2D8',
                    'MainSelectedColor': '#66F2CB',
                    'BgColor': '#E8E8E8',
                    'BgHoverColor': '#CFE8E5',
                    'BgSelectedColor': '#BAE8E2',
                    'MenuColor': '#5BC2A8',
                    'MenuHoverColor': '#4DA38D',
                    'MenuSelectedColor': '#5299A3',
                    'BorderColor': '#93699E',
                    'TextColor': '#0C3326',
                    'ImageColor': (12, 51, 38),

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
                    'MainHoverColor': '#23233D',
                    'MainSelectedColor': '#20204D',
                    'BgColor': '#111129',
                    'BgHoverColor': '#1C1C42',
                    'BgSelectedColor': '#2E2E6B',
                    'MenuColor': '#191B4D',
                    'MenuHoverColor': '#212463',
                    'MenuSelectedColor': '#303491',
                    'BorderColor': '#07093B',
                    'TextColor': '#F0F0F0',
                    'ImageColor': (240, 240, 240),

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
            'summer':
                Theme({
                    'Identifier': QColor('#22420D'),
                    'Preprocessor': QColor('#7A4875'),
                    'Comment': QColor('#702425'),
                    'Keyword': QColor('#162DA8'),
                    'Number': QColor('#289396'),
                    'String': QColor('#8B8C1E'),

                    'Paper': QColor('#A9D696'),
                    'CaretLineBackgroundColor': QColor('#86D673'),
                    'BraceColor': QColor('#162DA8'),

                    'MainColor': '#A0C95E',
                    'MainHoverColor': '#86A84F',
                    'MainSelectedColor': '#B1D12D',
                    'BgColor': '#E8E8E8',
                    'BgHoverColor': '#D3E8C9',
                    'BgSelectedColor': '#C0E8B0',
                    'MenuColor': '#62B854',
                    'MenuHoverColor': '#6AC75A',
                    'MenuSelectedColor': '#80F06D',
                    'BorderColor': '#4F8C25',
                    'TextColor': '#354711',
                    'ImageColor': (57, 71, 17),

                    'TestPassed': QColor('#3F8731'),
                    'TestFailed': QColor('#D96612'),
                    'TestInProgress': QColor('#A0A0A0'),
                    'TestCrashed': QColor('B02424'),
                    'MainC': QColor('#20339E'),
                    'CFile': QColor('#21669E'),
                    'HFile': QColor('#7A4875'),
                    'TxtFile': QColor('#3E733F'),
                }),
            'dark':
                Theme({
                    'Identifier': QColor('#DFDFDF'),
                    'Preprocessor': QColor('#56A8F5'),
                    'Comment': QColor('#74797B'),
                    'Keyword': QColor('#CC7832'),
                    'Number': QColor('#5191A6'),
                    'String': QColor('#5F864C'),

                    'Paper': QColor('#1E1F22'),
                    'CaretLineBackgroundColor': QColor('#26282E'),
                    'BraceColor': QColor('#CC7832'),

                    'MainColor': '#2B2D30',
                    'MainHoverColor': '#3E4145',
                    'MainSelectedColor': '#2E436E',
                    'BgColor': '#141517',
                    'BgHoverColor': '#222345',
                    'BgSelectedColor': '#323466',
                    'MenuColor': '#1F2024',
                    'MenuHoverColor': '#4E5157',
                    'MenuSelectedColor': '#3574F0',
                    'BorderColor': '#474747',
                    'TextColor': '#F0F0F0',
                    'ImageColor': (250, 250, 250),

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
            'christmas':
                Theme({
                    'Identifier': QColor('#000000'),
                    'Preprocessor': QColor('#69803C'),
                    'Comment': QColor('#A87269'),
                    'Keyword': QColor('#ED1F1F'),
                    'Number': QColor('#346AC7'),
                    'String': QColor('#C31FC7'),

                    'Paper': QColor('#F5F5F5'),
                    'CaretLineBackgroundColor': QColor('#F5D1D1'),
                    'BraceColor': QColor('#ED1F1F'),

                    'MainColor': '#FFDBD7',
                    'MainHoverColor': '#E8C7C4',
                    'MainSelectedColor': '#E88C8C',
                    'BgColor': '#FFF5E0',
                    'BgHoverColor': '#FFD6C8',
                    'BgSelectedColor': '#E3968A',
                    'MenuColor': '#E65451',
                    'MenuHoverColor': '#B84643',
                    'MenuSelectedColor': '#BA0F0F',
                    'BorderColor': '#A62121',
                    'TextColor': '#101838',
                    'ImageColor': (16, 24, 56),

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
            'winter':
                Theme({
                    'Identifier': QColor('#142836'),
                    'Preprocessor': QColor('#8A3199'),
                    'Comment': QColor('#B57831'),
                    'Keyword': QColor('#0816B5'),
                    'Number': QColor('#5191A6'),
                    'String': QColor('#DE435C'),

                    'Paper': QColor('#D1D8F5'),
                    'CaretLineBackgroundColor': QColor('#BACDF5'),
                    'BraceColor': QColor('#EB6BD3'),

                    'MainColor': '#B4D2FA',
                    'MainHoverColor': '#93BBFA',
                    'MainSelectedColor': '#4BA7FA',
                    'BgColor': '#EEEEEE',
                    'BgHoverColor': '#D1D1D1',
                    'BgSelectedColor': '#7798C7',
                    'MenuColor': '#7798C7',
                    'MenuHoverColor': '#5787C7',
                    'MenuSelectedColor': '#2971C7',
                    'BorderColor': '#3E5875',
                    'TextColor': '#191C42',
                    'ImageColor': (25, 28, 66),

                    'TestPassed': QColor('#38802E'),
                    'TestFailed': QColor('#F82525'),
                    'TestInProgress': QColor('#A0A0A0'),
                    'TestCrashed': QColor('#A01010'),
                    'MainC': QColor('#A01010'),
                    'CFile': QColor('#F82525'),
                    'HFile': QColor('#99922C'),
                    'TxtFile': QColor('#2065D4'),
                    'Directory': QColor('#1BBDD4')
                }),
            'light':
                Theme({
                    'Identifier': QColor('#101010'),
                    'Preprocessor': QColor('#997509'),
                    'Comment': QColor('#B0B0B0'),
                    'Keyword': QColor('#0057D5'),
                    'Number': QColor('#0057D5'),
                    'String': QColor('#18822C'),

                    'Paper': QColor('#FFFFFF'),
                    'CaretLineBackgroundColor': QColor('#FFFFFF'),
                    'BraceColor': QColor('#0057D5'),

                    'MainColor': '#FFFFFF',
                    'MainHoverColor': '#DFE1E5',
                    'MainSelectedColor': '#CFDEFC',
                    'BgColor': '#DFE1E3',
                    'BgHoverColor': '#CBCDCF',
                    'BgSelectedColor': '#5283C9',
                    'MenuColor': '#F7F8FA',
                    'MenuHoverColor': '#DFE1E5',
                    'MenuSelectedColor': '#3573F0',
                    'BorderColor': '#BFC0C2',
                    'TextColor': '#222222',
                    'ImageColor': (25, 28, 66),

                    'TestPassed': QColor('#38802E'),
                    'TestFailed': QColor('#F82525'),
                    'TestInProgress': QColor('#A0A0A0'),
                    'TestCrashed': QColor('#A01010'),
                    'MainC': QColor('#A01010'),
                    'CFile': QColor('#F82525'),
                    'HFile': QColor('#99922C'),
                    'TxtFile': QColor('#2065D4'),
                    'Directory': QColor('#1BBDD4')
                }),
        }

        self.__emojis = dict()

        self.theme_name = ''
        self.theme = None
        self.style_sheet = ''
        self.bg_style_sheet = ''
        self.set_theme(theme_name)

    def __getitem__(self, item):
        return self.theme.get(item)

    @staticmethod
    def shift(palette):
        if palette == 'Bg':
            return 'Main'
        if palette == 'Main':
            return 'Menu'
        if palette == 'Menu':
            return 'Bg'

    def get(self, item):
        return self.theme.get(item)

    def code_colors(self, lexer):
        return self.theme.code_colors(lexer)

    def set_theme_to_list_widget(self, widget, font=None, palette='Main', border=True, border_radius=True):
        # widget.setFocusPolicy(False)
        widget.setStyleSheet(self.list_widget_css(palette, border, border_radius))
        for i in range(widget.count()):
            item = widget.item(i)
            if hasattr(item, 'set_theme'):
                item.set_theme()
            else:
                item.setFont(font if font else self.font_medium)

    def auto_css(self, widget: QWidget, code_font=False, palette='Main', border=True, border_radius=True, padding=False):
        if code_font:
            widget.setFont(self.code_font)
        else:
            widget.setFont(self.font_medium)

        if isinstance(widget, QMainWindow):
            widget.setStyleSheet(self.bg_style_sheet)
        elif isinstance(widget, Button):
            widget.set_theme(tm=self)
        # elif hasattr(widget, 'set_theme'):
        #     widget.set_theme()
        elif isinstance(widget, QComboBox):
            widget.setStyleSheet(self.combobox_css(palette))
        elif isinstance(widget, QLineEdit):
            widget.setStyleSheet(self.line_edit_css(palette, border, border_radius))
        elif isinstance(widget, QTextEdit):
            widget.setStyleSheet(self.text_edit_css(palette))
        elif isinstance(widget, QTreeWidget):
            widget.setStyleSheet(self.tree_widget_css(palette, border, border_radius))
        elif isinstance(widget, QScrollArea):
            widget.setStyleSheet(self.scroll_area_css(palette, border))
        elif isinstance(widget, QPushButton):
            widget.setStyleSheet(self.button_css(palette, border, border_radius, padding))
        elif isinstance(widget, QLabel):
            widget.setStyleSheet('border: none;')
        elif isinstance(widget, QSpinBox):
            widget.setStyleSheet(self.spinbox_css(palette))
        elif isinstance(widget, QDoubleSpinBox):
            widget.setStyleSheet(self.double_spinbox_css(palette))
        elif isinstance(widget, QProgressBar):
            widget.setStyleSheet(self.progress_bar_css(palette))
        elif isinstance(widget, QTabBar):
            widget.setStyleSheet(self.tab_bar_css(palette))
        elif isinstance(widget, QTabWidget):
            widget.setStyleSheet(self.tab_widget_css(palette))
        elif isinstance(widget, QListWidget):
            self.set_theme_to_list_widget(widget, palette=palette, border=border, border_radius=border_radius)
        elif isinstance(widget, QCheckBox):
            widget.setStyleSheet(self.checkbox_css(palette))
        elif isinstance(widget, QMenu):
            widget.setStyleSheet(self.menu_css(palette))

    def set_theme(self, theme_name):
        self.theme_name = theme_name
        self.clear_images()
        if theme_name not in self.themes:
            self.theme_name = ThemeManager.BASIC_THEME
        self.theme = self.themes.get(theme_name, self.themes[ThemeManager.BASIC_THEME])
        self.font_small = QFont(self.get('FontFamily'), 10)
        self.font_medium = QFont(self.get('FontFamily'), 11)
        self.font_big = QFont(self.get('FontFamily'), 14)
        self.code_font_std = QFont(self.get('CodeFontFamily'), 10)
        self.code_font = QFont(self.get('CodeFontFamily'), 11)
        self.bg_style_sheet = f"color: {self['TextColor']};\n" \
                              f"background-color: {self['BgColor']};"

    def scintilla_css(self, border=False):
        return f"""
QsciScintilla {{
    background-color: {self['Paper'].name()};
    border: {'1' if border else '0'}px solid {self['BorderColor']};
    background-color: {self['Paper'].name()};
}}
QsciScintilla QScrollBar:vertical {{
    background: {self['Paper'].name()};
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
}}
{self.menu_css()}"""

    def list_widget_css(self, palette, border=True, border_radius=True):
        return f"""
QListWidget {{
    {self.base_css(palette, border, border_radius)}
}}
QListWidget::item {{
    border-radius: 6px;
}}
QListWidget::item:hover {{
    background-color: {self[f'{palette}HoverColor']};
}}
QListWidget::item:selected {{
    color: {self['TextColor']};
    background-color: {self[f'{palette}SelectedColor']};
    border-radius: 6px;
}}
QListWidget QScrollBar:vertical {{
    background: {self[f'{palette}Color']};
    border-top-right-radius: 4px;
    border-bottom-right-radius: 4px;
    width: 12px;
    margin: 0px;
}}
QListWidget QScrollBar:horizontal {{
    background: {self[f'{palette}Color']};
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

    def tree_widget_css(self, palette, border=True, border_radius=True):
        return f"""
QTreeWidget {{
    {self.base_css(palette, border, border_radius)}
}}
QTreeView {{
    show-decoration-selected: 1;
}}
QTreeWidget::item {{
    border-top-right-radius: 6px;
    border-bottom-right-radius: 6px;
}}
QTreeWidget::item:hover {{
    background-color: {self[f'{palette}HoverColor']};
}}
QTreeWidget::item:selected {{
    color: {self['TextColor']};
    background-color: {self[f'{palette}SelectedColor']};
}}

QTreeView::branch {{
    background-color: {self[f'{palette}Color']};
}}
QTreeView::branch:hover {{
    background-color: {self[f'{palette}HoverColor']};
}}
QTreeView::branch::selected {{
    border-top-left-radius: 6px;
    border-bottom-left-radius: 6px;
    background-color: {self[f'{palette}SelectedColor']};
}}

QTreeView::branch:closed:has-children {{
        image: url({self.get_image('buttons/right_arrow')});
}}
QTreeView::branch:open:has-children {{
        image: url({self.get_image('buttons/down_arrow')});
}}

QTreeWidget QScrollBar:vertical {{
    background: {self[f'{palette}Color']};
    border-top-right-radius: 4px;
    border-bottom-right-radius: 4px;
    width: 12px;
    margin: 0px;
}}
QTreeWidget QScrollBar:horizontal {{
    background: {self[f'{palette}Color']};
    border-bottom-left-radius: 4px;
    border-bottom-right-radius: 4px;
    height: 12px;
    margin: 0px;
}}
QTreeWidget QScrollBar::handle::vertical {{
    background-color: {self['BorderColor']};
    margin: 2px 2px 2px 6px;
    border-radius: 2px;
    min-height: 20px;
}}
QTreeWidget QScrollBar::handle::vertical:hover {{
    margin: 2px;
    border-radius: 4px;
}}
QTreeWidget QScrollBar::handle::horizontal {{
    background-color: {self['BorderColor']};
    margin: 6px 2px 2px 2px;
    border-radius: 2px;
    min-width: 20px;
}}
QTreeWidget QScrollBar::handle::horizontal:hover {{
    margin: 2px;
    border-radius: 4px;
}}
QTreeWidget QScrollBar::sub-page, QScrollBar::add-page {{
    background: none;
}}
QTreeWidget QScrollBar::sub-line, QScrollBar::add-line {{
    background: none;
    height: 0px;
    subcontrol-position: left;
    subcontrol-origin: margin;
}}
"""

    def base_css(self, palette='Bg', border=True, border_radius=True):
        return f"color: {self['TextColor']};\n" \
               f"background-color: {self[f'{palette}Color']};\n" \
               f"border: {'1' if border else '0'}px solid {self['BorderColor']};\n" \
               f"border-radius: {'4' if border_radius else '0'}px;"

    def line_edit_css(self, palette='Bg', border=True, border_radius=True):
        return f"""
QLineEdit {{
    {self.base_css(palette, border, border_radius)}
}}
QLineEdit:focus {{
    background-color: {self[f'{palette}HoverColor']};
}}
"""

    def scroll_area_css(self, palette, border=True):
        return f"""
QScrollArea {{
    {self.base_css(palette, border)}
}}
QScrollArea QScrollBar:vertical {{
    background: {self[f'{palette}Color']};
    border-top-right-radius: 4px;
    border-bottom-right-radius: 4px;
    width: 12px;
    margin: 0px;
}}
QScrollArea QScrollBar:horizontal {{
    background: {self[f'{palette}Color']};
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

    def text_edit_css(self, palette):
        return f"""
QTextEdit {{
    {self.base_css(palette)}
}}
QTextEdit QScrollBar:vertical {{
    background: {self[f'{palette}Color']};
    border-top-right-radius: 5px;
    border-bottom-right-radius: 5px;
    width: 12px;
    margin: 0px;
}}
QTextEdit QScrollBar:horizontal {{
    background: {self[f'{palette}Color']};
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
{self.menu_css(palette)}
"""

    def combobox_css(self, palette='Bg'):
        return f"""
QComboBox {{
    {self.base_css(palette)}
}}
QComboBox::hover {{
    background-color: {self[f'{palette}HoverColor']};
}}
QComboBox::drop-down:button {{
    border-radius: 5px;
}}
QComboBox::down-arrow {{
    image: url({self.get_image('buttons/down_arrow')});
}}
QComboBox QAbstractItemView {{
    color: {self['TextColor']};
    background-color: {self[f'{palette}Color']};
    border: 1px solid {self['BorderColor']};
    selection-color: {self['TextColor']};
    selection-background-color: {self[f'{palette}HoverColor']};
    border-radius: 4px;
}}
QComboBox QScrollBar:vertical {{
    background-color: {self[f'{palette}Color']};
    border-top-right-radius: 5px;
    border-bottom-right-radius: 5px;
    width: 12px;
    margin: 0px;
}}
QComboBox QScrollBar::handle::vertical {{
    background-color: {self['BorderColor']};
    margin: 2px 2px 2px 6px;
    border-radius: 2px;
    min-height: 20px;
}}
QComboBox QScrollBar::handle::vertical:hover {{
    margin: 2px;
    border-radius: 4px;
}}
QComboBox QScrollBar::sub-page, QScrollBar::add-page {{
    background: none;
}}
QComboBox QScrollBar::sub-line, QScrollBar::add-line {{
    background: none;
    height: 0px;
    subcontrol-position: left;
    subcontrol-origin: margin;
}}
"""

    def progress_bar_css(self, palette='Bg'):
        return f"""
QProgressBar {{
color: {self['TextColor']};
background-color: {self[f'{self.shift(palette)}Color']};
border: 1px solid {self['BorderColor']};
border-radius: 4px;
text-align: center;
}}
QProgressBar::chunk {{
background-color: {self[f'{palette}Color']};
}}
"""

    def spinbox_css(self, palette='Bg'):
        return f"""
QSpinBox {{
    {self.base_css(palette)}
}}
QSpinBox::up-button {{
    color: {self['TextColor']};
    background-color: {self[f'{palette}Color']};
    border-left: 1px solid {self['BorderColor']};
    border-bottom: 1px solid {self['BorderColor']};
    border-top-right-radius: 3px;
}}
QSpinBox::up-button::disabled {{
    border: 0px solid {self['BorderColor']};
}}
QSpinBox::up-button::hover {{
    background-color: {self[f'{palette}HoverColor']};
}}
QSpinBox::up-arrow {{
    image: url({self.get_image('buttons/up_arrow')});
}}
QSpinBox::down-button {{
    color: {self['TextColor']};
    background-color: {self[f'{palette}Color']};
    border-left: 1px solid {self['BorderColor']};
    border-top: 1px solid {self['BorderColor']};
    border-bottom-right-radius: 3px;
}}
QSpinBox::down-button::disabled {{
    border: 0px solid {self['BorderColor']};
}}
QSpinBox::down-button::hover {{
    background-color: {self[f'{palette}HoverColor']};
}}
QSpinBox::down-arrow {{
    image: url({self.get_image('buttons/down_arrow')});
}}
QSpinBox::disabled {{
    color: {self['BgColor']};
    border-color: {self[f'{palette}Color']};
}}
"""

    def double_spinbox_css(self, palette='Bg'):
        return self.spinbox_css(palette=palette).replace('QSpinBox', 'QDoubleSpinBox')

    def button_css(self, palette='Bg', border=True, border_radius=True, padding=False):
        return f"""
QPushButton {{
    color: {self['TextColor']};
    background-color: {self[f'{palette}Color']};
    border: {'1' if border else '0'}px solid {self['BorderColor']};
    border-radius: {'5' if border_radius else '0'}px;
    {'padding: 3px 8px 3px 8px;' if padding else 'padding: 0px;'}
}}
QPushButton::hover {{
    background-color: {self[f'{palette}HoverColor']};
}}
QPushButton::disabled {{
    color: {self['BgColor']};
    border-color: {self['MainColor']};
}}
QPushButton::checked {{
    background-color: {self[f'{palette}SelectedColor']};
}}
QPushButton::menu-indicator {{
    image: url({self.get_image('buttons/down_arrow')});
    subcontrol-origin: padding;
    padding-right: 5px;
    subcontrol-position: right;
}}
"""

    def tab_bar_css(self, palette='Main'):
        return f"""
QTabBar::tab {{
    color: {self['TextColor']};
    background-color: {self[f'{palette}Color']};
    border-bottom-color: {self['TextColor']};
    border-top-left-radius: 5px;
    border-top-right-radius: 5px;
    border: 1px solid {self['BorderColor']};
    width: 125px;
    padding: 4px;
}}
QTabBar::tab:hover {{
    background-color: {self[f'{palette}HoverColor']};
}}
QTabBar::tab:selected {{
    background-color: {self[f'{palette}SelectedColor']};
}}
QTabBar QToolButton {{
    background-color: {self[f'{palette}Color']};
    border: 1px solid {self['BorderColor']};
}}
QTabBar QToolButton::hover {{
    background-color: {self[f'{palette}HoverColor']};
}}
QTabBar QToolButton::right-arrow {{
    image: url({self.get_image('buttons/right_arrow')});
}}
QTabBar QToolButton::left-arrow {{
    image: url({self.get_image('buttons/left_arrow')});
}}
"""

    def tab_widget_css(self, palette='Main'):
        return f"""
QTabWidget::pane {{
    color: {self[f'{self.shift(palette)}Color']};
}}
{self.tab_bar_css(palette)}
"""

    def checkbox_css(self, palette='Main'):
        return f"""
QCheckBox::indicator {{
    width: 13px;
    height: 13px;
}}
QCheckBox::indicator:unchecked {{
    image: url({self.get_image('buttons/checkbox_unchecked')});
}}
QCheckBox::indicator:unchecked:hover {{
    image: url({self.get_image('buttons/checkbox_unchecked')});
}}
QCheckBox::indicator:unchecked:pressed {{
    image: url({self.get_image('buttons/checkbox_unchecked')});
}}
QCheckBox::indicator:checked {{
    image: url({self.get_image('buttons/checkbox')});
}}
QCheckBox::indicator:checked:hover {{
    image: url({self.get_image('buttons/checkbox')});
}}
QCheckBox::indicator:checked:pressed {{
    image: url({self.get_image('buttons/checkbox')});
}}"""

    def menu_css(self, palette='Bg', padding='4px 16px'):
        return f"""
QMenu {{
    color: {self['TextColor']};
    background-color: {self[f'{palette}Color']};
    border: 1px solid {self['BorderColor']};
    border-radius: 6px;
    spacing: 4px;
    padding: 3px;
}}

QMenu::item {{
    border: 0px solid {self['BorderColor']};
    background-color: transparent;
    border-radius: 8px;
    padding: {padding};
}}

QMenu::icon {{
    padding-left: 6px;
}}

QMenu::item:selected {{
    background-color: {self[f'{palette}HoverColor']};
}}
QMenu::separator {{
    height: 1px;
    background: {self['BorderColor']};
    margin: 4px 10px;
}}"""

    def get_image(self, name: str, default=None, color=None, mini=False):
        name = name.replace('❤', "❤️").replace('⚡', '⚡️').replace('✍', '✍️').replace('☃', '☃️').replace(
            '♂', '♂️').replace('♀', '♀️')
        if name not in resources:
            if default is not None:
                name = default
            else:
                raise KeyError(f"Image not found: {repr(name)}")

        if resources[name][0] == 'mono':
            return self._convert_mono_png(name, color)

        if resources[name][0] == 'emoji':
            return self._convert_emoji(name, mini)

        path = f"{self.sm.app_data_dir}/images/{name.replace('/', '_')}.png"
        if not os.path.isfile(path):
            image = Image.open(BytesIO(resources[name][1]))
            image.save(path)

        return path

    def _convert_emoji(self, name, mini=False):
        if name in self.__emojis:
            emoji_id = self.__emojis[name]
        else:
            emoji_id = uuid4()
            self.__emojis[name] = emoji_id
        path = f"{self.sm.app_data_dir}/images/{emoji_id}{'_m' if mini else ''}.png"
        if not os.path.isfile(path):
            image = Image.open(BytesIO(resources[name][1]))

            if mini:
                image = image.resize((20, 20))

            image.save(path)
        return path

    def _convert_mono_png(self, name, color=None):
        if color is None:
            color = self['ImageColor']
        elif isinstance(color, str):
            color = QColor(color)
            color = color.red(), color.green(), color.blue()
        elif isinstance(color, QColor):
            color = color.red(), color.green(), color.blue()

        path = f"{self.sm.app_data_dir}/images/{name.replace('/', '_')}_{QColor(*color).name()}.png"
        if not os.path.isfile(path):
            os.makedirs(f"{self.sm.app_data_dir}/images", exist_ok=True)
            image = Image.open(BytesIO(resources[name][1]))

            image = image.convert("RGBA")
            datas = image.getdata()
            new_data = []
            for item in datas:
                if item[0] == 255 and item[1] == 255 and item[2] == 255:
                    new_data.append((255, 255, 255, 0))
                elif item[0] == 0 and item[1] == 0 and item[2] == 0 and item[3] == 255:
                    new_data.append(color)
                else:
                    new_data.append(item)
            image.putdata(new_data)

            image.save(path)

        return path

    def clear_images(self):
        if os.path.isdir(path := f"{self.sm.app_data_dir}/images"):
            shutil.rmtree(path)

    def add_custom_theme(self, theme_name, theme_data):
        self.themes[theme_name] = Theme(theme_data)
