import struct
from sys import argv


class PackError(Exception):
    def __init__(self, message=''):
        super(PackError, self).__init__()
        self.message = message

    def __str__(self):
        return self.message


def preprocessor(text: str):
    defines = []
    lst = text.split('\n')
    for i, line in enumerate(lst):
        if not line:
            continue

        words = line.split()
        for j, el in enumerate(words):
            for define in defines:
                if el == define[0]:
                    words[j] = define[1]
                    break
        line = ' '.join(words)

        if line.startswith("#define "):
            words = line.split()
            defines.append((words[1], words[2]))
        else:
            yield line


def get_defines(text: str):
    defines = dict()
    lst = text.split('\n')
    for i, line in enumerate(lst):
        if line.startswith("#define ") and len(words := line.split()) == 3:
            defines[words[1]] = words[2]
    return defines


def convert(text: str, path):
    file = open(path, 'bw')
    for i, line in enumerate(preprocessor(text)):
        try:
            file.write(convert_line(line))
        except PackError:
            raise PackError(f"Invalid mask on line {i + 1}")
        except ValueError as ex:
            raise PackError(f"Invalid value on line {i + 1}: \n{ex}")
        except IndexError as ex:
            raise PackError(f"Invalid values on line {i + 1}: \n{ex}")


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


def convert_line(line: str):
    lst = line.split()
    numbers = []
    i = 1
    for count, literal in parse_mask(lst[0]):
        if literal == 'x':
            continue
        if i == len(lst):
            raise IndexError(f"Expected more values then {i}")
        if literal == 's':
            byte_str = lst[i].encode('utf-8')
            if len(byte_str) >= count:
                byte_str = byte_str[:count - 1]
            byte_str += b'\0' * (count - len(byte_str))
            numbers.append(byte_str)
            i += 1
        else:
            for j in range(count):
                numbers.append(FORMATS[literal].value_type(lst[i]))
                i += 1
    if i != len(lst):
        raise IndexError(f"Expected {i - 1} values but {len(lst) - 1} found")
    return struct.pack(lst[0], *numbers)


def parse_mask(mask: str):
    while mask:
        num, literal, mask = get_number(mask)
        yield num, literal


def get_expected_values(mask: str):
    res = []
    while mask:
        num, literal, mask = get_number(mask)
        if literal == 's':
            res.append((str, 0, num - 1))
        elif literal != 'x':
            for _ in range(num):
                res.append((FORMATS[literal].value_type, FORMATS[literal].min, FORMATS[literal].max))
    return res


def get_number(mask: str):
    i = 0
    try:
        while mask[i].isdigit():
            i += 1
        if i == 0:
            return 1, mask[0], mask[1:]
        return int(mask[:i]), mask[i], mask[i + 1:]
    except IndexError:
        raise PackError("Invalid mask")


if __name__ == '__main__':
    if len(argv) > 1:
        if len(argv) != 3:
            print('Error: invalid args')
        else:
            with open(argv[1], encoding='utf-8') as f:
                convert(f.read(), argv[2])
    else:
        file1 = input("Enter input file: ")
        file2 = input("Enter output file: ")
        with open(file1, encoding='utf-8') as f:
            convert(f.read(), file2)
