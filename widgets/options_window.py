from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox, QDoubleSpinBox, \
    QLineEdit, QCheckBox, QComboBox, QFileDialog, QPushButton, QApplication
from PyQt5.QtCore import Qt, pyqtSignal


class OptionsWindow(QMainWindow):
    NAME_TOP = 0
    NAME_LEFT = 1
    NAME_RIGHT = 2
    NAME_SKIP = 3
    INITIAL_WIDGET_WIDTH = 150
    INITIAL_WIDGET_HEIGHT = 25
    clicked = pyqtSignal(str)
    returnPressed = pyqtSignal(dict)
    cancelPressed = pyqtSignal(dict)

    def __init__(self, dct):
        super(OptionsWindow, self).__init__()
        self.dct = dct

        central_widget = QWidget(self)

        self.main_widget = OptionsWidget(dct, self)
        self.main_widget.clicked.connect(self.clicked.emit)
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.main_widget)

        self.button_widget = QWidget()
        self.button_widget.setFixedHeight(50)
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignRight)

        self.enter_button = QPushButton("OK")
        self.enter_button.setFixedSize(100, 30)
        self.enter_button.clicked.connect(lambda arg: (self.close(), self.returnPressed.emit(self.main_widget.values)))
        layout.addWidget(self.enter_button)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setFixedSize(100, 30)
        layout.addWidget(self.cancel_button)
        self.cancel_button.clicked.connect(lambda arg: (self.close(), self.cancelPressed.emit(self.main_widget.values)))

        self.button_widget.setLayout(layout)
        main_layout.addWidget(self.button_widget)

        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def set_widgets_width(self, width):
        self.main_widget.set_widgets_width(width)

    def set_widgets_height(self, height):
        self.main_widget.set_widgets_height(height)

    def set_widgets_size(self, width, height):
        self.main_widget.set_widgets_size(width, height)

    def __getitem__(self, item):
        return self.main_widget.values[item]

    def fix_size(self):
        self.setFixedSize(self.size())


class OptionsWidget(QWidget):
    NAME_TOP = 0
    NAME_LEFT = 1
    NAME_RIGHT = 2
    NAME_SKIP = 3
    INITIAL_WIDGET_WIDTH = 150
    INITIAL_WIDGET_HEIGHT = 25
    clicked = pyqtSignal(str)

    def __init__(self, dct, parent=None):
        super(OptionsWidget, self).__init__(parent)
        self.dct = dct
        self.values = dict()
        self.widgets = dict()

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        for key, item in dct.items():
            label = QLabel(str(key), self)
            widget, value = self.get_widget(item)
            if item.get('name') == OptionsWindow.NAME_LEFT:
                h_layout = QHBoxLayout()
                h_layout.setAlignment(Qt.AlignLeft)
                h_layout.addWidget(label)
                h_layout.addWidget(widget)
                layout.addLayout(h_layout)
            elif item.get('name') == OptionsWindow.NAME_RIGHT:
                h_layout = QHBoxLayout()
                h_layout.setAlignment(Qt.AlignLeft)
                h_layout.addWidget(widget)
                h_layout.addWidget(label)
                layout.addLayout(h_layout)
            elif item.get('name') != OptionsWindow.NAME_SKIP:
                layout.addWidget(label)
                layout.addWidget(widget)
            else:
                label.hide()
                layout.addWidget(widget)
            self.widgets[key] = widget
            self.values[key] = value
            self.connect_widget(key)

        self.setLayout(layout)

    def __getitem__(self, item):
        return self.values[item]

    def set_dict_value(self, item, value):
        if value != self.values[item] or self.dct[item]['type'] == 'button':
            self.values[item] = value
            self.clicked.emit(item)

    def set_value(self, item, value):
        self.values[item] = value
        if self.dct[item]['type'] in [int, 'int', float, 'float']:
            self.widgets[item].setValue(value)
        elif self.dct[item]['type'] in [str, 'str']:
            self.widgets[item].setText(value)
        elif self.dct[item]['type'] in [bool, 'bool']:
            self.widgets[item].setChecked(value)
        elif self.dct[item]['type'] == 'combo':
            self.widgets[item].setCurrentIndex(value)

    @staticmethod
    def get_widget(item):
        if item['type'] == int or item['type'] == 'int':
            widget = QSpinBox()
            widget.setFixedSize(item.get('width', OptionsWindow.INITIAL_WIDGET_WIDTH),
                                item.get('height', OptionsWindow.INITIAL_WIDGET_HEIGHT))
            value = item.get('initial', 0)
            widget.setValue(value)
            widget.setMinimum(item.get('min', -100000000))
            widget.setMaximum(item.get('max', 100000000))
        elif item['type'] == float or item['type'] == 'float':
            widget = QDoubleSpinBox()
            widget.setFixedSize(item.get('width', OptionsWindow.INITIAL_WIDGET_WIDTH),
                                item.get('height', OptionsWindow.INITIAL_WIDGET_HEIGHT))
            value = item.get('initial', 0)
            widget.setValue(value)
            widget.setMinimum(item.get('min', -100000000))
            widget.setMaximum(item.get('max', 100000000))
        elif item['type'] == str or item['type'] == 'str':
            widget = QLineEdit()
            widget.setFixedSize(item.get('width', OptionsWindow.INITIAL_WIDGET_WIDTH),
                                item.get('height', OptionsWindow.INITIAL_WIDGET_HEIGHT))
            value = str(item.get('initial', ''))
            widget.setText(value)
        elif item['type'] == bool or item['type'] == 'bool':
            widget = QCheckBox()
            widget.setFixedHeight(item.get('height', OptionsWindow.INITIAL_WIDGET_HEIGHT))
            value = item.get('initial', False)
            widget.setChecked(value)
        elif item['type'] == 'combo':
            widget = QComboBox()
            widget.setFixedSize(item.get('width', OptionsWindow.INITIAL_WIDGET_WIDTH),
                                item.get('height', OptionsWindow.INITIAL_WIDGET_HEIGHT))
            for el in item.get('values', []):
                widget.addItem(str(el))
            value = item.get('initial', 0)
            widget.setCurrentIndex(value)
            widget.setMaxVisibleItems(item.get('max_visible', 6))
        elif item['type'] == 'file':
            widget = QWidget()
            widget.setFixedSize(item.get('width', OptionsWindow.INITIAL_WIDGET_WIDTH),
                                item.get('height', OptionsWindow.INITIAL_WIDGET_HEIGHT))
            layout = QHBoxLayout()
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(0)
            widget1 = QLineEdit()
            value = item.get('initial', 'select file')
            widget1.setText(value)
            widget2 = QPushButton()
            widget2.setText('Files')
            widget2.setFixedSize(40, item.get('height', OptionsWindow.INITIAL_WIDGET_HEIGHT))
            layout.addWidget(widget1)
            layout.addWidget(widget2)
            widget.setLayout(layout)
            widget.widget_1 = widget1
            widget.widget_2 = widget2
        elif item['type'] == 'button':
            widget = QPushButton()
            widget.setFixedSize(item.get('width', OptionsWindow.INITIAL_WIDGET_WIDTH),
                                item.get('height', OptionsWindow.INITIAL_WIDGET_HEIGHT))
            widget.setText(item.get('text', ''))
            value = item.get('initial', False) if item.get('checkable', False) else False
            widget.setCheckable(item.get('checkable', False))
        elif item['type'] == 'size':
            widget = QWidget()
            widget.setFixedSize(item.get('width', OptionsWindow.INITIAL_WIDGET_WIDTH),
                                item.get('height', OptionsWindow.INITIAL_WIDGET_HEIGHT))
            layout = QHBoxLayout()
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(0)
            value = item.get('initial', (0, 0))
            widget1 = QSpinBox()
            widget1.setValue(value[0])
            widget1.setMinimum(item.get('min', (0, 0))[0])
            widget1.setMaximum(item.get('max', (10000000, 10000000))[0])
            widget2 = QSpinBox()
            widget2.setValue(value[1])
            widget2.setMinimum(item.get('min', (0, 0))[1])
            widget2.setMaximum(item.get('max', (10000000, 10000000))[1])
            layout.addWidget(widget1)
            label = QLabel()
            label.setText('x')
            layout.addWidget(label)
            label.setFixedWidth(10)
            layout.addWidget(widget2)
            widget.setLayout(layout)
            widget.widget_1 = widget1
            widget.widget_2 = widget2
        else:
            raise TypeError(f"unknown value type {item['type']}")
        return widget, value

    def connect_widget(self, key):
        widget = self.widgets[key]
        if self.dct[key]['type'] in (int, 'int', float, 'float'):
            widget.valueChanged.connect(lambda value: self.set_dict_value(key, value))
        elif self.dct[key]['type'] in (str, 'str'):
            widget.textChanged.connect(lambda value: self.set_dict_value(key, value))
        elif self.dct[key]['type'] in (bool, 'bool'):
            widget.clicked.connect(lambda value: self.set_dict_value(key, value))
        elif self.dct[key]['type'] == 'combo':
            widget.currentIndexChanged.connect(lambda value: self.set_dict_value(key, value))
        elif self.dct[key]['type'] == 'file':
            self.connect_file_dialog(key, widget, self.dct[key].get('mode', 'save'), self.dct[key].get('caption', ''),
                                     self.dct[key].get('directory', ''), self.dct[key].get('filter', ''))
        elif self.dct[key]['type'] == 'button':
            widget.clicked.connect(lambda value: self.set_dict_value(key, value))
        if self.dct[key]['type'] == 'size':
            widget.widget_1.valueChanged.connect(lambda value: self.set_dict_value(key, (value, widget.widget_2.value())))
            widget.widget_2.valueChanged.connect(lambda value: self.set_dict_value(key, (widget.widget_1.value(), value)))

    def set_widgets_width(self, width):
        for key, item in self.dct.items():
            if not isinstance(item['widget'], QCheckBox):
                item['widget'].setFixedWidth(item.get('width', width))

    def set_widgets_height(self, height):
        for key, item in self.dct.items():
            item['widget'].setFixedHeight(item.get('height', height))

    def set_widgets_size(self, width, height):
        self.set_widgets_width(width)
        self.set_widgets_height(height)

    def connect_file_dialog(self, key, widget, type, caption, directory, filter):
        def triggerd(*args):
            if type == 'save':
                file = QFileDialog.getSaveFileName(None, caption, directory, filter)[0]
            elif type == 'open':
                file = QFileDialog.getOpenFileName(None, caption, directory, filter)[0]
            elif type == 'dir':
                file = QFileDialog.getExistingDirectory(None, caption, directory)
            else:
                raise TypeError('Unknown mode')
            if file:
                widget.widget_1.setText(file)
                self.set_dict_value(key, file)
        widget.widget_1.textChanged.connect(lambda value: self.set_dict_value(key, value))
        widget.widget_2.clicked.connect(triggerd)


def main():
    app = QApplication([])
    window = OptionsWindow(
        {
            'value1': {'type': int, 'min': -100},
            'value2': {'type': float, 'initial': 10},
            'value3': {'type': str, 'initial': 'initial_text'},
            'value4': {'type': bool, 'initial': True, 'name': OptionsWindow.NAME_RIGHT},
            'value5': {'type': 'combo', 'initial': 3, 'values': ['var1', 'var2', 'var3', 'var4', 'var5', 'var6'],
                       'name': OptionsWindow.NAME_SKIP},
            'value6': {'type': 'file', 'width': 250},
            'button': {'type': 'button', 'text': 'PRESS ME', 'name': OptionsWindow.NAME_SKIP},
            'size': {'type': 'size'}
        }
    )
    window.show()
    window.returnPressed.connect(print)
    window.cancelPressed.connect(lambda: print('Canceled'))
    app.exec_()


if __name__ == '__main__':
    main()
