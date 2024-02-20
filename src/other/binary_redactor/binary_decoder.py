import struct
from src.other.binary_redactor.convert_binary import BinaryConverter


def decode(text: str, byte_str):
    res = []
    encoder = BinaryConverter(text)
    for line in encoder.preprocessor():
        try:
            mask = line.split()[0]
            res.append(mask + ' ' + ' '.join(map(
                lambda s: s.split(b'\0')[0].decode(encoder.encoding) if isinstance(s, bytes) else str(s),
                struct.unpack(mask, byte_str[:struct.calcsize(mask)]))))
            byte_str = byte_str[struct.calcsize(mask):]
        except UnicodeDecodeError:
            break
        except IndexError:
            break
        except struct.error:
            break
    else:
        return '\n'.join(res), 0
    return '\n'.join(res) + '\n' + str(byte_str).lstrip("b'").rstrip("'"), 1


def comparator(prog_out: bytes, out: str, out_bytes: bytes):
    try:
        encoder = BinaryConverter(out)
        prog_res, code = decode(out, prog_out)
        if code == 1:
            return prog_out == out_bytes
        prog_res = prog_res.split('\n')
        out = tuple(encoder.preprocessor())
        i, j = 0, 0
        while i < len(prog_res) and j < len(out):
            while not prog_res[i].strip():
                i += 1
            while not out[j].strip():
                j += 1
            if prog_res[i] != out[j]:
                return False
            i += 1
            j += 1
        return i == len(prog_res) and j == len(out)
    except Exception:
        return False
