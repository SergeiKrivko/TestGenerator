import os
import platform


toast_notifier = None


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
        global toast_notifier
        if toast_notifier is None:
            import win11toast
            toast_notifier = True
        win11toast.toast(title, message, on_click=on_click)
