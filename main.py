import sys

from PyQt5.QtWidgets import QApplication
from widgets.main_window import MainWindow


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


def main():
    app = QApplication(sys.argv)
    app.setOrganizationName("SergeiKrivko")
    app.setOrganizationDomain("https://github.com/SergeiKrivko/TestGenerator")
    app.setApplicationName("TestGenerator")
    window = MainWindow()
    window.show()
    window.set_theme()
    sys.excepthook = except_hook
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
