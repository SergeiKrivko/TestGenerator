import os
import platform

if platform.system() == 'Windows':
    import win11toast


def notification(title, message, on_click=None):
    plt = platform.system()
    if plt == "Darwin":
        command = f'''
        osascript -e 'display notification "{message}" with title "{title}"'
        '''
        os.system(command)
    elif plt == "Linux":
        command = f'''
        notify-send "{title}" "{message}"
        '''
        os.system(command)
    elif plt == "Windows":
        win11toast.toast(title, message, on_click=on_click, dialogue=title,
                         icon=r"file:///C:\Users\sergi\AppData\Local\SergeiKrivko\TestGenerator\icon.png")
