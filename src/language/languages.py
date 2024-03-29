from PyQt6.Qsci import QsciLexerCPP, QsciLexerPython, QsciLexerBash, QsciLexerBatch, QsciLexerCSharp, QsciLexerJava, \
    QsciLexerJavaScript, QsciLexerMarkdown, QsciLexerHTML, QsciLexerJSON, QsciLexerXML

from src import config
from src.language.autocomplition.abstract import CodeAutocompletionManager as AcMAbstract
from src.language.autocomplition.c import CodeAutocompletionManager as AcMC
from src.language.autocomplition.python import CodeAutocompletionManager as AcMPython
import src.language.testing.shell
from src.other.binary_redactor.lexer import LexerBin
from src.other.binary_redactor.convert_binary import convert as convert_binary
import src.other.report.markdown_parser
from src.side_tabs.files.zip_manager import ZipManager

languages = {
    'txt': {'lexer': None, 'files': ['.txt'], 'autocompletion': AcMAbstract},
    'C': {
        'lexer': QsciLexerCPP,
        'files': ['.c', '.h'],
        'autocompletion': AcMC,
        'colors': {
            QsciLexerCPP.Identifier: 'Identifier',
            QsciLexerCPP.PreProcessor: 'Preprocessor',
            QsciLexerCPP.Comment: 'Comment',
            QsciLexerCPP.CommentLine: 'Comment',
            QsciLexerCPP.CommentDoc: 'Comment',
            QsciLexerCPP.Keyword: 'Keyword',
            QsciLexerCPP.Number: 'Number',
            QsciLexerCPP.Operator: 'Identifier',
            QsciLexerCPP.DoubleQuotedString: 'String',
            QsciLexerCPP.SingleQuotedString: 'String',
            QsciLexerCPP.UnclosedString: 'String'
        },
        'compile': src.language.testing.c.c_compile,
        'run': src.language.testing.c.c_run,
        'coverage': src.language.testing.c.c_collect_coverage,
        # 'fast_run': True,
        'compiler_mask': "{file}:{line}:",
    },
    'Python': {
        'lexer': QsciLexerPython,
        'files': ['.py'],
        'autocompletion': AcMPython,
        'colors': {
            QsciLexerPython.Identifier: 'Identifier',
            QsciLexerPython.Comment: 'Comment',
            QsciLexerPython.CommentBlock: 'Comment',
            QsciLexerPython.Keyword: 'Keyword',
            QsciLexerPython.Number: 'Number',
            QsciLexerPython.Operator: 'Identifier',
            QsciLexerPython.ClassName: 'Preprocessor',
            QsciLexerPython.Decorator: 'Preprocessor',
            QsciLexerPython.FunctionMethodName: 'Preprocessor',
            QsciLexerPython.DoubleQuotedString: 'String',
            QsciLexerPython.SingleQuotedString: 'String',
            QsciLexerPython.DoubleQuotedFString: 'String',
            QsciLexerPython.SingleQuotedFString: 'String',
            QsciLexerPython.TripleDoubleQuotedString: 'String',
            QsciLexerPython.TripleSingleQuotedString: 'String',
            QsciLexerPython.TripleDoubleQuotedFString: 'String',
            QsciLexerPython.TripleSingleQuotedFString: 'String',
        },
        'run': src.language.testing.python.python_run,
        'coverage': src.language.testing.python.python_collect_coverage,
        'fast_run': [('Запустить', 'icons/run', src.language.testing.python.python_fast_run)],
    },
    'C++': {
        'lexer': QsciLexerCPP,
        'files': ['.cpp', '.h'],
        'autocompletion': AcMC,
        'colors': {
            QsciLexerCPP.Identifier: 'Identifier',
            QsciLexerCPP.PreProcessor: 'Preprocessor',
            QsciLexerCPP.Comment: 'Comment',
            QsciLexerCPP.CommentLine: 'Comment',
            QsciLexerCPP.CommentDoc: 'Comment',
            QsciLexerCPP.Keyword: 'Keyword',
            QsciLexerCPP.Number: 'Number',
            QsciLexerCPP.Operator: 'Identifier',
            QsciLexerCPP.DoubleQuotedString: 'String',
            QsciLexerCPP.SingleQuotedString: 'String',
            QsciLexerCPP.UnclosedString: 'String'
        },
        'compile': src.language.testing.c.c_compile,
        'run': src.language.testing.c.c_run,
        'coverage': src.language.testing.c.c_collect_coverage,
        # 'fast_run': True,
        'compiler_mask': "{file}:{line}:",
    },
    'Bach': {
        'lexer': QsciLexerBash,
        'files': ['.sh'],
        'autocompletion': AcMAbstract,
        'colors': {
            QsciLexerBash.Identifier: 'Identifier',
            QsciLexerBash.Operator: 'Identifier',
            QsciLexerBash.Number: 'Number',
            QsciLexerBash.Comment: 'Comment',
            QsciLexerBash.Keyword: 'Keyword',
            QsciLexerBash.DoubleQuotedString: 'String',
            QsciLexerBash.SingleQuotedString: 'String',
            QsciLexerBash.ParameterExpansion: 'Preprocessor',
            QsciLexerBash.Backticks: 'Preprocessor',
            QsciLexerBash.Error: 'Preprocessor'
        },
        'run': src.language.testing.shell.bash_run,
        'fast_run': [('Запустить', 'icons/run', src.language.testing.python.python_fast_run)],
    },
    'Batch': {
        'lexer': QsciLexerBatch,
        'files': ['.bat', '.cmd'],
        'autocompletion': AcMAbstract,
        'colors': {
            QsciLexerBatch.Keyword: 'Keyword',
            QsciLexerBatch.Comment: 'Comment',
            QsciLexerBatch.ExternalCommand: 'Preprocessor',
            QsciLexerBatch.Operator: 'Identifier',
            QsciLexerBatch.HideCommandChar: 'String',
            QsciLexerBatch.Variable: 'Number',
            QsciLexerBatch.Default: 'Identifier'
        },
        'run': src.language.testing.shell.batch_run,
        'fast_run': [('Запустить', 'icons/run', src.language.testing.python.python_fast_run)],
    },
    'Markdown': {
        'lexer': QsciLexerMarkdown,
        'files': ['.md'],
        'autocompletion': AcMAbstract,
        'colors': {
            QsciLexerMarkdown.BlockQuote: 'Keyword',
            QsciLexerMarkdown.CodeBlock: 'Preprocessor',
            QsciLexerMarkdown.CodeBackticks: 'Preprocessor',
            QsciLexerMarkdown.CodeDoubleBackticks: 'Preprocessor',
            QsciLexerMarkdown.Header1: 'Keyword',
            QsciLexerMarkdown.Header2: 'Keyword',
            QsciLexerMarkdown.Header3: 'Keyword',
            QsciLexerMarkdown.Header4: 'Keyword',
            QsciLexerMarkdown.Header5: 'Keyword',
            QsciLexerMarkdown.Header6: 'Keyword',
            QsciLexerMarkdown.OrderedListItem: 'Keyword',
            QsciLexerMarkdown.UnorderedListItem: 'Keyword',
            QsciLexerMarkdown.Link: 'String',
            QsciLexerMarkdown.Default: 'Identifier'
        }, 'preview': True,
        'fast_run': [('Конвертировать в Docx', 'files/docx', lambda path, pr, bm: (src.other.report.markdown_parser.convert(
            path, pr, bm, pdf=False), '')),
                     ('Конвертировать в Pdf', 'files/pdf', lambda path, pr, bm: (src.other.report.markdown_parser.convert(
                         path, pr, bm, pdf=True), ''))],
    },
    'HTML': {
        'lexer': QsciLexerHTML,
        'files': ['.html'],
        'autocompletion': AcMAbstract,
        'preview': True,
        'colors': {
            QsciLexerHTML.Default: 'Identifier',
            QsciLexerHTML.Entity: 'Keyword',
            QsciLexerHTML.HTMLValue: 'Preprocessor',
            QsciLexerHTML.HTMLNumber: 'Number',
            QsciLexerHTML.HTMLComment: 'Comment',
            QsciLexerHTML.HTMLDoubleQuotedString: 'String',
            QsciLexerHTML.HTMLSingleQuotedString: 'String',
            QsciLexerHTML.Attribute: 'Preprocessor',
            QsciLexerHTML.Tag: 'Keyword',
            QsciLexerHTML.OtherInTag: 'Identifier',
            QsciLexerHTML.UnknownTag: 'Keyword',
            QsciLexerHTML.UnknownAttribute: 'Preprocessor',
        }},
    'SVG': {
        'files': ['.svg'],
        'autocompletion': AcMAbstract,
        'lexer': QsciLexerXML,
        'preview': True,
        'colors': {
            QsciLexerXML.Default: 'Identifier',
            QsciLexerXML.Entity: 'Keyword',
            QsciLexerXML.HTMLValue: 'Preprocessor',
            QsciLexerXML.HTMLNumber: 'Number',
            QsciLexerXML.HTMLComment: 'Comment',
            QsciLexerXML.HTMLDoubleQuotedString: 'String',
            QsciLexerXML.HTMLSingleQuotedString: 'String',
            QsciLexerXML.Attribute: 'Preprocessor',
            QsciLexerXML.Tag: 'Keyword',
            QsciLexerXML.OtherInTag: 'Identifier',
            QsciLexerXML.UnknownTag: 'Keyword',
            QsciLexerXML.UnknownAttribute: 'Preprocessor',
        },
        'show_preview': True
    },
    'json': {'lexer': QsciLexerJSON, 'files': ['.json', '.dg'], 'autocompletion': AcMAbstract, 'colors': {
        QsciLexerJSON.Default: 'Identifier',
        QsciLexerJSON.Number: 'Number',
        QsciLexerJSON.Keyword: 'Keyword',
        QsciLexerJSON.Operator: 'Identifier',
        QsciLexerJSON.CommentBlock: 'Comment',
        QsciLexerJSON.CommentLine: 'Comment',
        QsciLexerJSON.EscapeSequence: 'Identifier',
        QsciLexerJSON.String: 'String',
        QsciLexerJSON.Property: 'Preprocessor',
        QsciLexerJSON.UnclosedString: 'String',
    }},
    'c#': {'lexer': QsciLexerCSharp, 'files': ['.cs']},
    'java': {'lexer': QsciLexerJava, 'files': []},
    'javascript': {'lexer': QsciLexerJavaScript, 'files': ['.js'], 'autocompletion': AcMAbstract, 'colors': {
        QsciLexerJavaScript.Default: 'Identifier',
        QsciLexerJavaScript.Number: 'Number',
        QsciLexerJavaScript.Keyword: 'Keyword',
        QsciLexerJavaScript.KeywordSet2: 'Keyword',
        QsciLexerJavaScript.Comment: 'Comment',
        QsciLexerJavaScript.CommentLine: 'Comment',
        QsciLexerJavaScript.CommentDoc: 'Comment',
        QsciLexerJavaScript.CommentLineDoc: 'Comment',
        QsciLexerJavaScript.InactiveComment: 'Comment',
        QsciLexerJavaScript.SingleQuotedString: 'String',
        QsciLexerJavaScript.UnclosedString: 'String',
        QsciLexerJavaScript.DoubleQuotedString: 'String',
        QsciLexerJavaScript.RawString: 'String',
        QsciLexerJavaScript.HashQuotedString: 'String',
        QsciLexerJavaScript.VerbatimString: 'String',
        QsciLexerJavaScript.Identifier: 'Identifier',
        QsciLexerJavaScript.Operator: 'Identifier',
        QsciLexerJavaScript.PreProcessor: 'Preprocessor',
    }},
    'XML': {'lexer': QsciLexerXML, 'files': ['.xml'], 'autocompletion': AcMAbstract, 'colors': {
        QsciLexerXML.Default: 'Identifier',
        QsciLexerXML.Entity: 'Keyword',
        QsciLexerXML.HTMLValue: 'Preprocessor',
        QsciLexerXML.HTMLNumber: 'Number',
        QsciLexerXML.HTMLComment: 'Comment',
        QsciLexerXML.HTMLDoubleQuotedString: 'String',
        QsciLexerXML.HTMLSingleQuotedString: 'String',
        QsciLexerXML.Attribute: 'Preprocessor',
        QsciLexerXML.Tag: 'Keyword',
        QsciLexerXML.OtherInTag: 'Identifier',
        QsciLexerXML.UnknownTag: 'Keyword',
        QsciLexerXML.UnknownAttribute: 'Preprocessor',
    }},
    'image': {'files': ['.bmp', '.png', '.jpg', '.pdf'], 'preview': True, 'open_files': config.USE_WEB_ENGINE},
    'Text2Bin': {
        'lexer': LexerBin,
        'files': ['.t2b'],
        'autocompletion': AcMAbstract,
        'colors': {
            LexerBin.Value: 'Identifier',
            LexerBin.Mask: 'Keyword',
            LexerBin.Default: 'Identifier',
            LexerBin.PreProcessor: 'Preprocessor',
            LexerBin.InvalidValue: 'String',
            LexerBin.InvalidMask: 'String',
            LexerBin.Comment: 'Comment'
        },
        'run': lambda path, *args, **kwargs: convert_binary(in_path=path),
        'fast_run': [('Конвертировать', 'files/bin', lambda path, project, bm: ('', convert_binary(
            in_path=path, exceptions=False)))]
    },
    'ZIP': {'files': ['.zip'], 'open_files': False,
            'fast_run': [('Распаковать', 'files/zip', lambda path, *args: ('', ZipManager.extract(path)))]}
}

PROJECT_LANGUAGES = ['C', 'C++', 'Python']
