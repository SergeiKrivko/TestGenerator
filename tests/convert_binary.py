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
    def __init__(self, literal: str, size: int, value_type, name=''):
        self.literal = literal
        self.value_type = value_type
        self.size = size
        self.name = ''


FORMATS = {
    'x': StructFormat('x', 1, None, 'pad byte'),
    's': StructFormat('s', 1, str, 'char'),
    'b': StructFormat('b', 1, int, 'byte'),
    'B': StructFormat('B', 1, int, 'unsigned byte'),
    'h': StructFormat('h', 2, int, 'short'),
    'H': StructFormat('H', 2, int, 'unsigned short'),
    'i': StructFormat('i', 4, int, 'int'),
    'I': StructFormat('I', 4, int, 'unsigned int'),
    'q': StructFormat('q', 8, int, 'long'),
    'Q': StructFormat('Q', 8, int, 'unsigned long'),
    'f': StructFormat('f', 4, float, 'float'),
    'd': StructFormat('d', 4, float, 'double')
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
