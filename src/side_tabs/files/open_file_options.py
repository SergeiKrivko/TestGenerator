import platform

match platform.system():
    case 'Windows':
        import winreg


def get_open_file_options(file):
    match platform.system():
        case 'Windows':
            return get_options_windows(file)
        case _:
            return []


def get_options_windows(file: str):
    extension = file[file.rindex('.'):]
    key = None
    try:
        prog_name, prog_icon, prog_command = windows_program_by_key(file, winreg.QueryValue(
            winreg.HKEY_CLASSES_ROOT, extension))
        if prog_name:
            yield prog_name, prog_icon, prog_command

        key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, f'{extension}\\OpenWithProgids')
        for prog in sub_values(key):
            prog_name, prog_icon, prog_command = windows_program_by_key(file, prog[0])
            if prog_name:
                yield prog_name, prog_icon, prog_command
    except FileNotFoundError:
        pass
    if key:
        winreg.CloseKey(key)


def windows_program_by_key(file, key):
    try:
        prog_key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, key)
    except FileNotFoundError:
        return None, None, None

    try:
        app_key = winreg.OpenKey(prog_key, 'Application')
        prog_name = winreg.QueryValueEx(app_key, 'ApplicationName')[0]
        winreg.CloseKey(app_key)
        prog_command = winreg.QueryValue(prog_key, 'Shell\\edit\\command').replace('%1', file)
        prog_icon = winreg.QueryValue(prog_key, 'DefaultIcon')
        winreg.CloseKey(prog_key)
        return prog_name, prog_icon, prog_command
    except FileNotFoundError:
        pass
    except OSError:
        pass

    try:
        prog_name = winreg.QueryValue(prog_key, '')
        prog_command = winreg.QueryValue(prog_key, 'shell\\open\\command').replace('%1', file)
        prog_icon = winreg.QueryValue(prog_key, 'DefaultIcon')
        winreg.CloseKey(prog_key)
        return prog_name, prog_icon, prog_command
    except FileNotFoundError:
        pass
    except OSError:
        pass

    winreg.CloseKey(prog_key)
    return None, None, None


def sub_values(key):
    i = 0
    while True:
        try:
            subkey = winreg.EnumValue(key, i)
            yield subkey
            i += 1
        except WindowsError as e:
            break
