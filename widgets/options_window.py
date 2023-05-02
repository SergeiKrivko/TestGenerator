from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox, QDoubleSpinBox, \
    QLineEdit, QCheckBox, QComboBox, QFileDialog, QPushButton, QApplication, QDialog, QDialogButtonBox
from PyQt5.QtCore import Qt, pyqtSignal


class OptionsWindow(QDialog):
    NAME_TOP = 0
    NAME_LEFT = 1
    NAME_RIGHT = 2
    NAME_SKIP = 3
    INITIAL_WIDGET_WIDTH = 150
    INITIAL_WIDGET_HEIGHT = 24
    clicked = pyqtSignal(str)

    def __init__(self, dct, parent=None, name=""):
        super(OptionsWindow, self).__init__(parent)
        self.dct = dct
        self.setWindowTitle(name)

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.main_widget = OptionsWidget(dct, self)
        self.main_widget.clicked.connect(self.clicked.emit)
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.main_widget)

        main_layout.addWidget(self.buttonBox)

        self.setLayout(main_layout)
        self.values = self.main_widget.values

    def set_widgets_width(self, width):
        self.main_widget.set_widgets_width(width)

    def set_widgets_height(self, height):
        self.main_widget.set_widgets_height(height)

    def set_widgets_size(self, width, height):
        self.main_widget.set_widgets_size(width, height)

    def set_widget_style_sheet(self, key, style_sheet):
        self.main_widget.set_widget_style_sheet(key, style_sheet)

    def __getitem__(self, item):
        return self.main_widget[item]

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

    def __init__(self, dct, parent=None, margins=None):
        super(OptionsWidget, self).__init__(parent)
        self.dct = dct
        self.values = dict()
        self.widgets = dict()

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        if margins:
            main_layout.setContentsMargins(*margins)
        main_layout.setAlignment(Qt.AlignTop)
        for key, item in dct.items():
            if 'h_line' in key:
                horizontal_layout = QHBoxLayout()
                horizontal_layout.setAlignment(Qt.AlignLeft)
                for key2, item2 in item.items():
                    label = QLabel(str(key2))
                    widget, value = self.get_widget(key2, item2)
                    if item2.get('name') == OptionsWindow.NAME_LEFT:
                        h_layout = QHBoxLayout()
                        h_layout.addWidget(label)
                        h_layout.addWidget(widget)
                        horizontal_layout.addLayout(h_layout)
                        h_layout.setAlignment(Qt.AlignLeft)
                    elif item2.get('name') == OptionsWindow.NAME_RIGHT:
                        h_layout = QHBoxLayout()
                        h_layout.addWidget(widget)
                        h_layout.addWidget(label)
                        horizontal_layout.addLayout(h_layout)
                        h_layout.setAlignment(Qt.AlignLeft)
                    elif item2.get('name') != OptionsWindow.NAME_SKIP:
                        v_layout = QVBoxLayout()
                        v_layout.setAlignment(Qt.AlignLeft)
                        v_layout.addWidget(label)
                        v_layout.addWidget(widget)
                        horizontal_layout.addLayout(v_layout)
                    else:
                        label.hide()
                        horizontal_layout.addWidget(widget)
                    self.widgets[key2] = widget
                    self.values[key2] = value
                main_layout.addLayout(horizontal_layout)
                continue

            label = QLabel(str(key), self)
            widget, value = self.get_widget(key, item)
            if item.get('name') == OptionsWindow.NAME_LEFT:
                h_layout = QHBoxLayout()
                h_layout.setAlignment(Qt.AlignLeft)
                h_layout.addWidget(label)
                h_layout.addWidget(widget)
                main_layout.addLayout(h_layout)
            elif item.get('name') == OptionsWindow.NAME_RIGHT:
                h_layout = QHBoxLayout()
                h_layout.setAlignment(Qt.AlignLeft)
                h_layout.addWidget(widget)
                h_layout.addWidget(label)
                main_layout.addLayout(h_layout)
            elif item.get('name') != OptionsWindow.NAME_SKIP:
                v_layout = QVBoxLayout()
                v_layout.setAlignment(Qt.AlignTop)
                v_layout.addWidget(label)
                v_layout.addWidget(widget)
                main_layout.addLayout(v_layout)
            else:
                label.hide()
                main_layout.addWidget(widget)
            self.widgets[key] = widget
            self.values[key] = value

        self.setLayout(main_layout)

    def __getitem__(self, item):
        if isinstance(item, tuple):
            return self.values[item[0]][1][item[1]]
        return self.values[item]

    def set_dict_value(self, item, value):
        if item not in self.values or value != self.values[item] or isinstance(self.widgets[item], QPushButton):
            self.values[item] = value
            self.clicked.emit(item)

    def set_widget_style_sheet(self, key, style_sheet):
        self.widgets[key].setStyleSheet(style_sheet)

    def set_value(self, item, value):
        self.values[item] = value
        if isinstance(self.widgets[item], (QSpinBox, QDoubleSpinBox)):
            self.widgets[item].setValue(value)
        elif isinstance(self.widgets[item], QLineEdit):
            self.widgets[item].setText(value)
        elif isinstance(self.widgets[item], QCheckBox):
            self.widgets[item].setChecked(value)
        elif isinstance(self.widgets[item], QComboBox):
            self.widgets[item].setCurrentIndex(value)

    def get_widget(self, key, item):
        if item['type'] == int or item['type'] == 'int':
            return self.spin_box(key, item)
        elif item['type'] == float or item['type'] == 'float':
            return self.double_spin_box(key, item)
        elif item['type'] == str or item['type'] == 'str':
            return self.line_edit(key, item)
        elif item['type'] == bool or item['type'] == 'bool':
            return self.check_box(key, item)
        elif item['type'] == 'combo':
            return self.combo_box(key, item)
        elif item['type'] == 'file':
            return self.file_widget(key, item)
        elif item['type'] == 'button':
            return self.button(key, item)
        elif item['type'] == 'size':
            return self.size_widget(key, item)
        else:
            raise TypeError(f"unknown value type {item['type']}")

    def spin_box(self, key, item):
        widget = QSpinBox()
        widget.setFixedSize(item.get('width', OptionsWindow.INITIAL_WIDGET_WIDTH),
                            item.get('height', OptionsWindow.INITIAL_WIDGET_HEIGHT))
        value = item.get('initial', 0)
        widget.setValue(value)
        widget.setMinimum(item.get('min', -100000000))
        widget.setMaximum(item.get('max', 100000000))
        widget.valueChanged.connect(lambda value: self.set_dict_value(key, value))
        return widget, value

    def double_spin_box(self, key, item):
        widget = QDoubleSpinBox()
        widget.setFixedSize(item.get('width', OptionsWindow.INITIAL_WIDGET_WIDTH),
                            item.get('height', OptionsWindow.INITIAL_WIDGET_HEIGHT))
        value = item.get('initial', 0)
        widget.setValue(value)
        widget.setMinimum(item.get('min', -100000000))
        widget.setMaximum(item.get('max', 100000000))
        widget.valueChanged.connect(lambda value: self.set_dict_value(key, value))
        return widget, value

    def line_edit(self, key, item):
        widget = QLineEdit()
        widget.setFixedSize(item.get('width', OptionsWindow.INITIAL_WIDGET_WIDTH),
                            item.get('height', OptionsWindow.INITIAL_WIDGET_HEIGHT))
        value = str(item.get('initial', ''))
        if 'echo_mode' in item:
            widget.setEchoMode(item.get('echo_mode'))
        widget.setText(value)
        widget.textChanged.connect(lambda value: self.set_dict_value(key, value))
        return widget, value

    def check_box(self, key, item):
        widget = QCheckBox()
        widget.setFixedHeight(item.get('height', OptionsWindow.INITIAL_WIDGET_HEIGHT))
        value = item.get('initial', False)
        widget.setChecked(bool(value))
        widget.clicked.connect(lambda: self.set_dict_value(key, int(widget.isChecked())))
        return widget, value

    def combo_box(self, key, item):
        if isinstance(item.get('values'), dict):
            widget = SuperComboBox(item)
            widget.currentIndexChanged.connect(lambda value: self.set_dict_value(key, (
                value, dict() if widget.widgets[value] is None else widget.widgets[value].values)))
            value = item.get('initial', 0)
            widget.setCurrentIndex(value)
            if widget.widgets[value]:
                value = value, widget.widgets[value].values
            else:
                value = value, None
        else:
            widget = QComboBox()
            for el in item.get('values', []):
                widget.addItem(str(el))
            widget.setFixedSize(item.get('width', OptionsWindow.INITIAL_WIDGET_WIDTH),
            item.get('height', OptionsWindow.INITIAL_WIDGET_HEIGHT))
            widget.currentIndexChanged.connect(lambda value: self.set_dict_value(key, value))
            value = item.get('initial', 0)
            widget.setCurrentIndex(value)
        if 'max_visible' in item:
            widget.setMaxVisibleItems(item.get('max_visible', 6))
        return widget, value

    def file_widget(self, key, item):
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
        self.connect_file_dialog(key, widget, widget1, widget2, self.dct[key].get('mode', 'save'),
                                 self.dct[key].get('caption', ''), self.dct[key].get('directory', ''),
                                 self.dct[key].get('filter', ''))
        return widget, value

    def button(self, key, item):
        widget = QPushButton()
        widget.setFixedSize(item.get('width', OptionsWindow.INITIAL_WIDGET_WIDTH),
                            item.get('height', OptionsWindow.INITIAL_WIDGET_HEIGHT))
        widget.setText(item.get('text', ''))
        value = item.get('initial', False) if item.get('checkable', False) else False
        widget.setCheckable(item.get('checkable', False))
        widget.clicked.connect(lambda value: self.set_dict_value(key, value))
        return widget, value

    def size_widget(self, key, item):
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
        widget1.valueChanged.connect(lambda value: self.set_dict_value(key, (value, widget2.value())))
        widget2.valueChanged.connect(lambda value: self.set_dict_value(key, (widget1.value(), value)))
        return widget, value

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

    def connect_file_dialog(self, key, widget, widget1, widget2, type, caption, directory, filter):
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
        widget1.textChanged.connect(lambda value: self.set_dict_value(key, value))
        widget2.clicked.connect(triggerd)


class SuperComboBox(QWidget):
    currentIndexChanged = pyqtSignal(int)

    def __init__(self, item):
        super(SuperComboBox, self).__init__()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        self.main_combo_box = QComboBox()
        self.main_combo_box.setFixedSize(item.get('width', OptionsWindow.INITIAL_WIDGET_WIDTH),
                            item.get('height', OptionsWindow.INITIAL_WIDGET_HEIGHT))
        layout.addWidget(self.main_combo_box)
        value = item.get('initial', 0)

        struct = item.get('values', dict())
        self.widgets = [None] * len(struct)
        i = 0
        for key, item2 in struct.items():
            self.main_combo_box.addItem(str(key))
            if item2:
                widget = OptionsWidget(item2)
                layout.addWidget(widget)
                widget.hide()
                self.widgets[i] = widget
            i += 1

        self.main_combo_box.setCurrentIndex(value)
        self.main_combo_box.setMaxVisibleItems(item.get('max_visible', 6))
        self.main_combo_box.currentIndexChanged.connect(self.setCurrentIndex)

    def setCurrentIndex(self, index):
        for el in self.widgets:
            if el:
                el.hide()
        self.main_combo_box.setCurrentIndex(index)
        if isinstance(self.widgets[index], OptionsWidget):
            self.widgets[index].show()
        self.currentIndexChanged.emit(index)

    def setMaxVisibleItems(self, count):
        self.main_combo_box.setMaxVisibleItems(count)


def main():
    app = QApplication([])
    window = OptionsWindow(
        {
            'h_line1': {'value1': {'type': int, 'min': -100}, 'value1-1': {'type': int, 'min': -100}},
            'value2': {'type': float, 'initial': 10},
            'value3': {'type': str, 'initial': 'initial_text'},
            'value4': {'type': bool, 'initial': True, 'name': OptionsWindow.NAME_RIGHT},
            'value5': {'type': 'combo', 'initial': 3, 'values': ['var1', 'var2', 'var3', 'var4', 'var5', 'var6'],
                       'name': OptionsWindow.NAME_SKIP},
            'value6': {'type': 'file', 'width': 250},
            'button': {'type': 'button', 'text': 'PRESS ME', 'name': OptionsWindow.NAME_SKIP},
            'size': {'type': 'size'},
            'value7': {'type': 'combo', 'values': {
                'int': {'value': {'type': int, 'min': -100}},
                'float': {'value': {'type': float, 'initial': 10}},
                'str': {'value': {'type': str, 'initial': 'initial_text'}}
            }}
        }
    )
    window.show()
    window.returnPressed.connect(print)
    window.cancelPressed.connect(lambda: print('Canceled'))
    app.exec_()


if __name__ == '__main__':
    main()
