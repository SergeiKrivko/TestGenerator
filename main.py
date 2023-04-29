from PyQt5.QtWidgets import QApplication
from widgets.main_window import MainWindow


def main():
    app = QApplication([])
    app.setOrganizationName("SergeiKrivko")
    app.setOrganizationDomain("https://github.com/SergeiKrivko/TestGenerator")
    app.setApplicationName("TestGenerator")
    window = MainWindow()
    window.show()
    window.set_theme()
    app.exec_()


if __name__ == '__main__':
    main()
