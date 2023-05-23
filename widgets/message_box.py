from PyQt5.QtWidgets import QMessageBox


class MessageBox(QMessageBox):
    def __init__(self, message_type, title, message, tm):
        super(MessageBox, self).__init__(None)

        self.setIcon(message_type)
        self.setText(message)
        self.setWindowTitle(title)

        self.setStyleSheet(tm.bg_style_sheet)
        self.addButton(QMessageBox.Ok)
        button = self.button(QMessageBox.Ok)
        button.setStyleSheet(tm.buttons_style_sheet)
        button.setFixedSize(70, 24)
        self.exec()

