import os.path
import struct
import sys
from sys import argv


class BinaryConverterError(Exception):
    INVALID_MASK = 0
    TOO_BIG_VALUE = 1
    TOO_SMALL_VALUE = 2
    INVALID_VALUES_COUNT = 3
    INVALID_TYPE = 4

    def __init__(self, error_type: int, line=0, text='', start=0, end=0, **kwargs):
        super(BinaryConverterError, self).__init__()
        self.error_type = error_type
        self.line = line
        self.text = text
        self.start = start
        self.end = end
        self.kwargs = kwargs

    def __str__(self):
        errors = {self.INVALID_MASK: "Некорректная форматная строка",
                  self.TOO_BIG_VALUE: "Слишком большое значение",
                  self.TOO_SMALL_VALUE: "Слишком маленькое значение",
                  self.INVALID_VALUES_COUNT: "Неправильное количество значений",
                  self.INVALID_TYPE: "Некорректный тип значения"}
        if self.error_type == self.INVALID_MASK:
            message = ""
        elif self.error_type == self.TOO_BIG_VALUE and 'max' in self.kwargs:
            if 'literal' in self.kwargs:
                message = f"Спецификатор {self.kwargs['literal']} требует значение, " \
                          f"не превышающее {self.kwargs['max']}\n"
            else:
                message = f"Ожидалось значение, не превышающее {self.kwargs['max']}\n"
        elif self.error_type == self.TOO_SMALL_VALUE and 'min' in self.kwargs:
            if 'literal' in self.kwargs:
                message = f"Спецификатор {self.kwargs['literal']} требует значение " \
                          f"не ниже {self.kwargs['max']}\n"
            else:
                message = f"Ожидалось значение не ниже {self.kwargs['min']}\n"
        elif self.error_type == self.INVALID_VALUES_COUNT and 'expected' in self.kwargs and 'found' in self.kwargs:
            message = f"Ожидалось {self.kwargs['expected']} значений, но получено {self.kwargs['found']}\n"
        elif self.error_type == self.INVALID_TYPE and 'expected' in self.kwargs:
            types = {int: "целое число", float: "вещественное число"}
            message = f"Ожидалось {types[self.kwargs['expected']]}\n"
        else:
            message = ""
        return f"Строка {self.line + 1}: {errors[self.error_type]}\n{self.text}\n{message}"


class StructFormat:
    def __init__(self, literal: str, size: int, value_type, name='',
                 minimum: int | float = 0, maximum: int | float = 0):
        self.literal = literal
        self.value_type = value_type
        self.size = size
        self.name = ''
        self.min = minimum
        self.max = maximum


FORMATS = {
    'x': StructFormat('x', 1, None, 'pad byte'),
    's': StructFormat('s', 1, str, 'char'),
    'b': StructFormat('b', 1, int, 'byte', -(2 ** 7), 2 ** 7 - 1),
    'B': StructFormat('B', 1, int, 'unsigned byte', 0, 2 ** 8 - 1),
    'h': StructFormat('h', 2, int, 'short', -(2 ** 15), 2 ** 15 - 1),
    'H': StructFormat('H', 2, int, 'unsigned short', 0, 2 ** 16 - 1),
    'i': StructFormat('i', 4, int, 'int', -(2 ** 31), 2 ** 31 - 1),
    'I': StructFormat('I', 4, int, 'unsigned int', 0, 2 ** 32 - 1),
    'q': StructFormat('q', 8, int, 'long', -(2 ** 63), 2 ** 63 - 1),
    'Q': StructFormat('Q', 8, int, 'unsigned long', 0, 2 ** 64 - 1),
    'f': StructFormat('f', 4, float, 'float', -3.402823466e38, 3.402823466e38),
    'd': StructFormat('d', 4, float, 'double', -1.7976931348623157e308, 1.7976931348623157e308)
}


class BinaryConverter:
    def __init__(self, text: str):
        self.text = text
        self.encoding = 'utf-8'

    def preprocessor(self):
        defines = []
        lst = self.text.split('\n')
        for i, line in enumerate(lst):
            if '//' in line:
                line = line[:line.index('//')]

            if not line:
                continue

            words = line.split()
            for j, el in enumerate(words):
                for define in defines:
                    if el == define[0]:
                        words[j] = define[1]
                        break
            line = ' '.join(words)

            if line.startswith('#define '):
                words = line.split()
                if len(words) >= 3:
                    defines.append((words[1], words[2]))
            elif line.startswith('#encoding '):
                self.encoding = line.split()[1]
            elif line.startswith('#'):
                pass
            else:
                yield line

    def get_defines(self):
        defines = dict()
        lst = self.text.split('\n')
        for i, line in enumerate(lst):
            if line.startswith("#define ") and len(words := line.split()) == 3:
                defines[words[1]] = words[2]
        return defines

    def convert(self):
        lst = []
        for i, line in enumerate(self.preprocessor()):
            if not line.strip():
                continue

            try:
                n = len(self.get_expected_values(line.split()[0]))
            except BinaryConverterError as ex:
                raise BinaryConverterError(ex.error_type, i, line, **ex.kwargs)

            if n != (found := len(self.split_line(line)) - 1):
                raise BinaryConverterError(BinaryConverterError.INVALID_VALUES_COUNT, i, line, expected=n, found=found)

            try:
                lst.append(self.convert_line(line))
            except BinaryConverterError as ex:
                raise BinaryConverterError(ex.error_type, i, line, **ex.kwargs)
        return b''.join(lst)

    def convert_line(self, line: str):
        lst = BinaryConverter.split_line(line)
        numbers = []
        i = 1
        for count, literal in self.parse_mask(lst[0]):
            if literal == 'x':
                continue
            if i == len(lst):
                raise BinaryConverterError(BinaryConverterError.INVALID_VALUES_COUNT)
            if literal == 's':
                byte_str = lst[i].encode(self.encoding)
                if len(byte_str) >= count:
                    byte_str = byte_str[:count - 1]
                byte_str += b'\0' * (count - len(byte_str))
                numbers.append(byte_str)
                i += 1
            else:
                for j in range(count):
                    try:
                        numbers.append(FORMATS[literal].value_type(lst[i]))
                    except ValueError:
                        raise BinaryConverterError(BinaryConverterError.INVALID_TYPE, expected=FORMATS[literal].value_type)
                    if numbers[-1] > FORMATS[literal].max:
                        raise BinaryConverterError(BinaryConverterError.TOO_BIG_VALUE, max=FORMATS[literal].max)
                    if numbers[-1] < FORMATS[literal].min:
                        raise BinaryConverterError(BinaryConverterError.TOO_SMALL_VALUE, min=FORMATS[literal].min)
                    i += 1
        if i != len(lst):
            raise BinaryConverterError(BinaryConverterError.INVALID_VALUES_COUNT)
        return struct.pack(lst[0], *numbers)

    @staticmethod
    def replace_line(line):
        line = line.replace('\\\\', '{\\\\}')
        if line.startswith('"'):
            line = line[1:]
        if line.endswith('"') and not line.endswith('\\"'):
            line = line[:-1]
        line = line.replace('\\t', '\t').replace('\\r', '\r').replace('\\n', '\n').replace('\\0', '\0').replace(
            '\\"', '\"').replace('\\b', '\b').replace('{\\\\}', '\\')
        return line

    @staticmethod
    def split_line(line: str, replace=True):
        res = []
        elem = []
        for el in line.split(' '):
            if elem:
                elem.append(el)
                if el.endswith('"') and (len(el) <= 1 or (el[-2] != '\\' or len(el) >= 2 and (el[-3] == '\\'))):
                    res.append(' '.join(elem).strip('\r\n'))
                    elem = []
            elif el.strip():
                if el.startswith('"'):
                    if len(el) > 1 and el.endswith('"'):
                        res.append(el)
                    else:
                        elem.append(el)
                else:
                    res.append(el)
        if elem:
            res.append(' '.join(elem))
        if replace:
            for i in range(len(res)):
                res[i] = BinaryConverter.replace_line(res[i])
        return res

    @staticmethod
    def parse_mask(mask: str):
        while mask:
            num, literal, mask = BinaryConverter._get_number(mask)
            yield num, literal

    @staticmethod
    def get_expected_values(mask: str):
        res = []
        while mask:
            num, literal, mask = BinaryConverter._get_number(mask)
            if literal == 's':
                res.append((str, 0, num - 1))
            elif literal != 'x':
                if literal not in FORMATS:
                    raise BinaryConverterError(BinaryConverterError.INVALID_MASK)
                for _ in range(num):
                    res.append((FORMATS[literal].value_type, FORMATS[literal].min, FORMATS[literal].max))
        return res

    @staticmethod
    def _get_number(mask: str):
        i = 0
        try:
            while mask[i].isdigit():
                i += 1
            if i == 0:
                return 1, mask[0], mask[1:]
            return int(mask[:i]), mask[i], mask[i + 1:]
        except IndexError:
            raise BinaryConverterError(BinaryConverterError.INVALID_MASK)


def convert_bytes(text):
    encoder = BinaryConverter(text)
    return encoder.convert()


def convert_file(text='', path='', in_path='', exceptions=True):
    try:
        if in_path:
            with open(in_path, encoding='utf-8') as f:
                path, name = os.path.split(in_path)
                if '.' in name and (ind := name.rindex('.')) != 0:
                    path = os.path.join(path, name[:ind] + '.bin')
                encoder = BinaryConverter(f.read())
                res = encoder.convert()
        else:
            encoder = BinaryConverter(text)
            res = encoder.convert()
        with open(path, 'bw') as f:
            f.write(res)
    except Exception as ex:
        if exceptions:
            raise ex
        return f"{ex.__class__.__name__}: {ex}"
    if not exceptions:
        return ''


if __name__ == '__main__':
    code = 0
    if len(argv) > 1:
        if len(argv) != 3:
            print('Error: invalid args')
            code = 1
        else:
            try:
                with open(argv[1], encoding='utf-8') as f:
                    convert_file(f.read(), argv[2])
            except BinaryConverterError as ex:
                print(ex)
                code = 2
            except FileNotFoundError as ex:
                print(f"Error: {ex}")
                code = 3
            except PermissionError as ex:
                print(f"Permission error: {ex}")
    else:
        file1 = input("Enter input file: ")
        file2 = input("Enter output file: ")
        try:
            with open(file1, encoding='utf-8') as f:
                convert_file(f.read(), file2)
        except BinaryConverterError as ex:
            print(ex)
            code = 2
        except FileNotFoundError as ex:
            print(f"Error: {ex}")
            code = 3
        except PermissionError as ex:
            print(f"Permission error: {ex}")
    sys.exit(code)
