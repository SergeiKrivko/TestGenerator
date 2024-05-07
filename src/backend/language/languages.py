import src.other.report.markdown_parser
import src.backend.builds
from src.backend.language.language import Language
from src.other.binary_redactor.convert_binary import convert_file as convert_binary
from src.other.binary_redactor.lexer import LexerBin

# from src.side_tabs.files.zip_manager import ZipManager


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
        fast_run=[('Запустить', 'icons/run', src.backend.builds.python.python_fast_run)]
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
    ),
    'batch': Language(
        'batch',
        icon='custom-shell',
        extensions=['.cmd', '.bat', '.ps1'],
    ),
    'markdown': Language(
        'markdown',
        extensions=['.md'],
        icon='custom-markdown',
        preview=Language.PreviewType.SIMPLE,
        fast_run=[
            ('Конвертировать в Docx', 'icon-docx', lambda path, pr, bm: (src.other.report.markdown_parser.convert(
                path, pr, bm, pdf=False), '')),
            ('Конвертировать в Pdf', 'icon-pdf', lambda path, pr, bm: (src.other.report.markdown_parser.convert(
                path, pr, bm, pdf=True), ''))
        ]
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
        extensions=['.js'],
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
        preview=Language.PreviewType.ONLY
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
            LexerBin.InvalidValue: 'String',
            LexerBin.InvalidMask: 'String',
            LexerBin.Comment: 'Comment'
        }),
        fast_run=[('Конвертировать', 'icon-bin', lambda path, project, bm: ('', convert_binary(
            in_path=path, exceptions=False)))]
    ),
    # 'ZIP': {'files': ['.zip'], 'open_files': False,
    #         'fast_run': [('Распаковать', 'icon-zip', lambda path, *args: ('', ZipManager.extract(path)))]}
}

PROJECT_LANGUAGES = ['C', 'C++', 'Python']


def detect_language(path, default=None):
    for lang in LANGUAGES.values():
        for ext in lang.extensions:
            if path.endswith(ext):
                return lang.name
    return default
