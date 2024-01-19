import sys

import config
from backend.arg_parser import args


def main():
    if args.build is None and not args.testing and not args.unit:
        run_ui()
    else:
        run_console()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


def run_console():
    from backend.managers import BackendManager
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    app.setOrganizationName(config.ORGANISATION_NAME)
    app.setOrganizationDomain(config.ORGANISATION_URL)
    app.setApplicationName(config.APP_NAME)
    app.setApplicationVersion(config.APP_VERSION)

    bm = BackendManager()
    bm.parse_cmd_args(args)


def run_ui():
    from PyQt6.QtWidgets import QApplication
    from ui.main_window import MainWindow

    app = QApplication(sys.argv)
    app.setOrganizationName(config.ORGANISATION_NAME)
    app.setOrganizationDomain(config.ORGANISATION_URL)
    app.setApplicationName(config.APP_NAME)
    app.setApplicationVersion(config.APP_VERSION)

    window = MainWindow(app, args)

    window.show()
    window.set_theme()
    sys.excepthook = except_hook
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
