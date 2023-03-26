from PyQt5.QtWidgets import QApplication
from widgets.main_window import MainWindow


def main():
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
