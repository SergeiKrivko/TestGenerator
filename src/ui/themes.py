from PyQt6.QtGui import QColor
from PyQtUIkit.core import KitFont
from PyQtUIkit.themes import KitTheme, builtin_themes, KitPalette

LIGHT = KitTheme(
    {
        'CodeBg': KitPalette('#FFFFFF', '#DFE1E5', '#CFDEFC', '#222222'),
    }, fonts={
        'default': KitFont('Roboto', 8, 10, 14, 20),
        'italic': KitFont('Roboto', 8, 10, 14, 20, italic=True),
        'bold': KitFont('Roboto', 8, 10, 14, 20, bold=True),
        'strike': KitFont('Roboto', 8, 10, 14, 20, strike=True),
        'mono': KitFont('Roboto Mono', 8, 10, 14, 20),
    },
    inherit=builtin_themes['Light']
)

DARK = KitTheme(
    {
        'CodeBg': KitPalette('#1E1F22', '#3E4145', '#2E436E', '#F0F0F0'),
    }, fonts={
        'default': KitFont('Roboto', 8, 10, 14, 20),
        'italic': KitFont('Roboto', 8, 10, 14, 20, italic=True),
        'bold': KitFont('Roboto', 8, 10, 14, 20, bold=True),
        'strike': KitFont('Roboto', 8, 10, 14, 20, strike=True),
        'mono': KitFont('Roboto Mono', 8, 10, 14, 20),
    },
    inherit=builtin_themes['Dark']
)

themes = {
    'light-classic': KitTheme(inherit=LIGHT),
    'light-neon': KitTheme(inherit=LIGHT),
    'light-twilight': KitTheme(inherit=LIGHT),

    'dark-classic': KitTheme(inherit=DARK),
    'dark-neon': KitTheme(code_colors={
        'Identifier': QColor('#EFEFEF'),
        'Preprocessor': QColor('#148270'),
        'Comment': QColor('#1D822A'),
        'Keyword': QColor('#5164BD'),
        'Number': QColor('#CC7119'),
        'String': QColor('#D9417D'),
        'Function': QColor('#9E3CD4'),
        'Danger': QColor('#DF1C1C'),
    }, inherit=DARK),
    'dark-twilight': KitTheme(palettes={
        'CodeBg': KitPalette('#141414', '#302C2A', '#302C2A', '#D4CB81'),
    }, code_colors={
        'Identifier': QColor('#D4CB81'),
        'Preprocessor': QColor('#3E5FD4'),
        'Comment': QColor('#498C9C'),
        'Keyword': QColor('#D44710'),
        'Number': QColor('#52D440'),
        'String': QColor('#D48D5A'),
        'Function': QColor('#B465D4'),
        'Danger': QColor('#DF1C1C'),
    }, inherit=DARK)
}
