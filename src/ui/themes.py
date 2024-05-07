from PyQtUIkit.core import KitFont
from PyQtUIkit.themes import KitTheme, builtin_themes, KitPalette

themes = {
    'light': KitTheme(
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
    ),
    'dark': KitTheme(
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
}
