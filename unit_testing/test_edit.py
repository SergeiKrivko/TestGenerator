from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel


class UnitTestEdit(QWidget):
    def __init__(self, tm):
        super().__init__()
        self._tm = tm
        self._labels = []

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)

        name_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addLayout(name_layout)

        label = QLabel("Описание")
