import src.backend.builds
from src.backend.language.language import Language, FastRunFunction, FastRunCommand
from src.other.binary_redactor.convert_binary import convert_file as convert_binary
from src.other.binary_redactor.lexer import LexerBin


LANGUAGES = {
    'txt': Language('txt', ['.txt'], 'custom-text'),
    'c': Language(
        'c',
        extensions=['.c', '.h'],
        icon='custom-c',
    ),
    'python': Language(
        'python',
        extensions=['.py'],
        icon='solid-logo-python',
        fast_run=[FastRunCommand('Запустить', 'line-play', src.backend.builds.python.python_fast_run)]
    ),
    'c++': Language(
        'c++',
        icon='custom-cpp',
        extensions=['.cpp', '.h'],
    ),
    'bash': Language(
        'bash',
        icon='custom-shell',
        extensions=['.sh'],
        fast_run=[FastRunCommand('Запустить', 'line-play', src.backend.builds.shell.bash_fast_run)]
    ),
    'batch': Language(
        'batch',
        icon='custom-shell',
        extensions=['.cmd', '.bat', '.ps1'],
        fast_run=[FastRunCommand('Запустить', 'line-play', src.backend.builds.shell.batch_fast_run)]
    ),
    'markdown': Language(
        'markdown',
        extensions=['.md'],
        icon='custom-markdown',
        preview=Language.PreviewType.SIMPLE,
    ),
    'html': Language(
        'html',
        extensions=['.html'],
        icon='solid-logo-html5',
        preview=Language.PreviewType.SIMPLE,
    ),
    'svg': Language(
        'svg',
        extensions=['.svg'],
        icon='custom-image',
        preview=Language.PreviewType.ACTIVE,
    ),
    'json': Language(
        'json',
        icon='custom-json',
        extensions=['.json', '.dg'],
    ),
    'c#': Language(
        'c#',
        icon='custom-text',
        extensions=['.cs'],
    ),
    'java': Language(
        'java',
        icon='custom-text',
        extensions=['.java'],
    ),
    'javascript': Language(
        'javascript',
        icon='solid-logo-javascript',
        extensions=['.js'],
    ),
    'typescript': Language(
        'typescript',
        icon='solid-logo-javascript',
        extensions=['.ts'],
    ),
    'xml': Language(
        'xml',
        icon='custom-xml',
        extensions=['.xml'],
    ),
    'masm': Language(
        name='masm',
        icon='custom-asm',
        extensions=['.asm'],
    ),
    'css': Language(
        name='css',
        icon='solid-logo-css3',
        extensions=['css', 'scss'],
    ),
    '__image__': Language(
        '__image__',
        extensions=['.bmp', '.png', '.jpg', '.jpeg', '.webp'],
        icon='custom-image',
        preview=Language.PreviewType.ONLY
    ),
    'pdf': Language(
        'pdf',
        extensions=['.pdf'],
        icon='custom-pdf',
        preview=Language.PreviewType.SYSTEM
    ),
    'text-to-binary': Language(
        'text-to-binary',
        extensions=['.t2b'],
        icon='custom-t2b',
        kit_language=(LexerBin, {
            LexerBin.Value: 'Identifier',
            LexerBin.Mask: 'Keyword',
            LexerBin.Default: 'Identifier',
            LexerBin.PreProcessor: 'Preprocessor',
            LexerBin.InvalidValue: 'Danger',
            LexerBin.InvalidMask: 'Danger',
            LexerBin.Comment: 'Comment'
        }),
        fast_run=[
            FastRunFunction('Конвертировать', 'custom-bin',
                            lambda path, bm: ('', convert_binary(in_path=path, exceptions=False)))
        ]
    ),
    # 'ZIP': {'files': ['.zip'], 'open_files': False,
    #         'fast_run': [('Распаковать', 'icon-zip', lambda path, *args: ('', ZipManager.extract(path)))]}
}

PROJECT_LANGUAGES = ['c', 'c++', 'python', 'masm']


def detect_language(path, default=None):
    for lang in LANGUAGES.values():
        for ext in lang.extensions:
            if path.endswith(ext):
                return lang
    return default
