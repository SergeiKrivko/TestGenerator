import random
from copy import deepcopy


def random_value(data: dict):
    if data.get('type') == 'int':
        return random_int(data)
    if data.get('type') == 'float':
        return random_float(data)
    if data.get('type') == 'str':
        return random_str(data)
    if data.get('type') == 'array':
        return random_array(data)
    if data.get('type') == 'struct':
        return random_struct(data)


def get_negatives(data: dict):
    if data.get('type') == 'int':
        return int_negatives(data)
    if data.get('type') == 'float':
        return float_negatives(data)
    if data.get('type') == 'str':
        return str_negatives(data)
    if data.get('type') == 'array':
        return array_negatives(data)
    if data.get('type') == 'struct':
        return struct_negatives(data)


def convert(arg):
    if isinstance(arg, float):
        return "{arg:.{n}g}".format(arg=arg, n=random.randint(2, 8))
    return str(arg)


def array_to_str(lst: list, data: dict):
    text = ''
    if data.get('size_input', 0) == 1:
        text = str(len(lst)) + '\n'
    if data.get("one_line"):
        return text + ' '.join(map(convert, lst))
    return text + '\n'.join(map(convert, lst))


def random_int(data: dict):
    minimum = -10000 if data.get('min') is None else data.get('min')
    maximum = 10000 if data.get('max') is None else data.get('max')
    return random.randint(int(minimum), int(maximum))


def random_float(data: dict):
    minimum = -10000 if data.get('min') is None else data.get('min')
    maximum = 10000 if data.get('max') is None else data.get('max')
    return random.randint(int(minimum), int(maximum) - 1) + random.random()


def random_str(data: dict = None):
    st = "abcdefghijklmnopqrstuvwxyz"
    if data is None:
        return ''.join(random.choices(st, k=random.randint(1, 10)))
    if data.get('spaces', False):
        st += " " * 6
    minimum = data.get('min')
    if minimum is None or int(minimum) < 0:
        minimum = 0
    else:
        minimum = int(minimum)
        if data.get('open_brace') == '(':
            minimum += 1
    maximum = data.get('max')
    if maximum is None:
        maximum = 100 if data.get('spaces', False) else 10
    else:
        maximum = int(maximum)
        if data.get('close_brace') == ')':
            maximum -= 1
    return ''.join(random.choices(st, k=random.randint(minimum, maximum)))


def random_struct(data: dict):
    lst = []
    for item in data.get('items', []):
        lst.append(random_value(item))
    sep = ' ' if data.get('one_lie', True) else '\n'
    return sep.join(map(str, lst))


def random_array(data: dict, lst=False, not_empty=False):
    if data.get('size_input', 0) == 0:
        size = data.get('size', 0)
    else:
        minimum = 0 if data.get('min') is None else max(0, data.get('min'))
        maximum = 100 if data.get('max') is None else max(1, data.get('max'))
        size = random.randint(max(1 if not_empty else 0, int(minimum)), int(maximum))
    item_data = data.get('item', dict())
    if lst:
        return [random_value(item_data) for _ in range(size)]
    return array_to_str([random_value(item_data) for _ in range(size)], data)


def int_negatives(data: dict):
    if data.get('open_brace', '(') == '(' and data.get('min') is not None:
        yield f"{data.get('name')} равно {data.get('min')}", data.get('min')
    if data.get('close_brace', ')') == ')' and data.get('max') is not None:
        yield f"{data.get('name')} равно {data.get('max')}", data.get('max')
    if data.get('min') is not None:
        yield f"{data.get('name')} меньше {data.get('min')}", \
            random.randint(min(-10000, data.get('min') * 100), data.get('min'))
    if data.get('max') is not None:
        yield f"{data.get('name')} больше {data.get('max')}", \
            random.randint(data.get('max') + 1, max(10000, data.get('max') * 100) + 1)
    yield f"{data.get('name')} - вещественное число", random.random()
    yield f"{data.get('name')} - набор символов", random_str()


def float_negatives(data: dict):
    if data.get('open_brace', '(') == '(' and data.get('min') is not None:
        yield f"{data.get('name')} равно {data.get('min')}", data.get('min')
    if data.get('close_brace', ')') == ')' and data.get('max') is not None:
        yield f"{data.get('name')} равно {data.get('max')}", data.get('max')
    if data.get('min') is not None:
        yield f"{data.get('name')} меньше {data.get('min')}", \
            random.randint(min(-10000, data.get('min') * 100) - 1, data.get('min') - 1) + random.random()
    if data.get('max') is not None:
        yield f"{data.get('name')} больше {data.get('max')}", \
            random.randint(data.get('max'), max(10000, data.get('max') * 100)) + random.random()
    yield f"{data.get('name')} - набор символов", random_str()


def str_negatives(data: dict):
    if data.get('min') or data.get('min') == 0 and data.get('open_brace') == '(':
        yield f"{data.get('name')} - строка нулевой длины", ""
    if data.get('max'):
        st = "abcdefghijklmnopqrstuvwxyz"
        if data.get('spaces', False):
            st += " " * 6
        yield f"{data.get('name')} - слишком длинная строка", "".join(random.choices(
            st, k=random.randint(int(data.get('max') + 1), int(data.get('max') * 2))))
        if data.get('close_brace') == ')':
            yield f"{data.get('name')} - строка длиной {data.get('max')}", "".join(random.choices(
                st, k=int(data.get('max'))))


def array_negatives(data: dict):
    if data.get('size_input', 0) == 1:
        data_copy = deepcopy(data)
        data_copy['name'] = f"Размер массива {data.get('name', '')}"
        for el in int_negatives(data_copy):
            yield el
    elif data.get('size_input', 0) == 2:
        if data.get('close_brace', ')') == ']' and data.get('max') is not None:
            yield f"Длина массива {data.get('name')} равна {data.get('max')}", array_to_str(
                [random_value(data.get('item')) for _ in range(data.get('max'))], data)
        if data.get('max') is not None:
            yield f"Длина массива {data.get('name')} больше {data.get('max')}", array_to_str(
                [random_value(data.get('item')) for _ in range(random.randint(
                    data.get('max') * 2 + 1, max(50, data.get('max') * 2) + 1))], data)
    data_copy = deepcopy(data.get('item'))
    data_copy['name'] = f"Элемент массива {data.get('name')}"
    for desc, el in get_negatives(data_copy):
        lst = random_array(data, lst=True, not_empty=True)
        lst[random.randint(0, len(lst) - 1)] = el
        yield desc, array_to_str(lst, data)


def struct_negatives(data: dict):
    sep = ' ' if data.get('one_lie', True) else '\n'
    for item in data.get('items', []):
        for desc, el in get_negatives(item):
            lst = []
            for elem in data.get('items', []):
                if elem == item:
                    lst.append(el)
                else:
                    lst.append(random_value(elem))
            yield f"{data.get('name', '')}.{desc}", sep.join(map(str, lst))


def read_file(path, default=None):
    if default is not None:
        try:
            file = open(path, encoding='utf-8')
            res = file.read()
            file.close()
            return res
        except Exception:
            return default
    file = open(path, encoding='utf-8')
    res = file.read()
    file.close()
    return res


def clear_words(path):
    file = open(path, 'r', encoding='utf-8')
    result = []
    for line in file:
        lst = []
        for word in line.split():
            try:
                float(word)
                lst.append(word)
            except Exception:
                pass
        if len(lst):
            result.append(' '.join(lst))
    file.close()

    file = open(path, 'w', encoding='utf-8')
    file.write("\n".join(result))
    file.close()
