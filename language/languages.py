from PyQt5.Qsci import QsciLexerCPP, QsciLexerPython, QsciLexerBash, QsciLexerBatch, QsciLexerCSharp, QsciLexerJava, \
    QsciLexerJavaScript, QsciLexerMarkdown, QsciLexerHTML, QsciLexerJSON
from language.autocomplition.abstract import CodeAutocompletionManager as AcMAbstract
from language.autocomplition.c import CodeAutocompletionManager as AcMC
from language.autocomplition.python import CodeAutocompletionManager as AcMPython
import language.testing.c
import language.testing.python
import language.testing.shell

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
        },
        'compile': language.testing.c.c_compile,
        'run': language.testing.c.c_run,
        'coverage': language.testing.c.c_collect_coverage,
        'clear_coverage': language.testing.c.c_clear_coverage_files
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
        'compile': language.testing.python.python_compile,
        'run': language.testing.python.python_run,
        'coverage': language.testing.python.python_collect_coverage,
        'clear_coverage': language.testing.python.python_clear_coverage_files,
        'fast_run': True,
    },
    'C++': {'lexer': QsciLexerCPP, 'files': ['.cpp', '.h'], 'autocompletion': AcMAbstract, 'colors': {
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
    }},
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
            QsciLexerBash.Error: 'Preprocessor'
        },
        'run': language.testing.shell.bash_run,
        'fast_run': True,
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
        'run': language.testing.shell.batch_run,
        'fast_run': True, },
    'Markdown': {'lexer': QsciLexerMarkdown, 'files': ['.md'], 'autocompletion': AcMAbstract, 'colors': {
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
        QsciLexerMarkdown.Link: 'String',
        QsciLexerMarkdown.Default: 'Identifier'
    }},
    'html': {'lexer': QsciLexerHTML, 'files': ['.html'], 'autocompletion': AcMAbstract},
    'json': {'lexer': QsciLexerJSON, 'files': ['.json'], 'autocompletion': AcMAbstract},
    'c#': {'lexer': QsciLexerCSharp},
    'java': {'lexer': QsciLexerJava},
    'javascript': {'lexer': QsciLexerJavaScript, 'files': ['.js'], 'autocompletion': AcMAbstract},
}
