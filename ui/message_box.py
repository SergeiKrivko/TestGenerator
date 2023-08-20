from PyQt5.QtWidgets import QMessageBox


class MessageBox(QMessageBox):
    def __init__(self, message_type, title, message, tm):
        super(MessageBox, self).__init__(None)

        self.setIcon(message_type)
        self.setText(message)
        self.setWindowTitle(title)
        self.setFont(tm.font_small)

        self.setStyleSheet(tm.bg_style_sheet)
        self.addButton(QMessageBox.Ok)
        button = self.button(QMessageBox.Ok)
        tm.auto_css(button)
        button.setFixedSize(70, 24)
        self.exec()

