import sys

from PyQt6.QtWidgets import QApplication

import config
from ui.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    app.setOrganizationName(config.ORGANISATION_NAME)
    app.setOrganizationDomain(config.ORGANISATION_URL)
    app.setApplicationName(config.APP_NAME)
    app.setApplicationVersion(config.APP_VERSION)

    window = MainWindow(app)
    window.show()
    window.set_theme()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
