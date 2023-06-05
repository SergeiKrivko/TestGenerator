from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QListWidget, QListWidgetItem, QLabel, \
    QComboBox

BUTTONS_MAX_WIDTH = 30


class TestTableWidget(QWidget):
    def __init__(self, tm, sm):
        super(TestTableWidget, self).__init__()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        self.tm = tm
        self.sm = sm
        self.labels = []

        # Positive tests

        pos_layout = QVBoxLayout()
        layout.addLayout(pos_layout)

        pos_buttons_layout = QHBoxLayout()
        pos_layout.addLayout(pos_buttons_layout)
        pos_buttons_layout.addWidget(label := QLabel("Позитивные тесты"))
        self.labels.append(label)

        self.pos_add_button = QPushButton()
        self.pos_add_button.setText("+")
        self.pos_add_button.setMaximumWidth(BUTTONS_MAX_WIDTH)
        pos_buttons_layout.addWidget(self.pos_add_button)

        self.pos_delete_button = QPushButton()
        self.pos_delete_button.setText("✕")
        self.pos_delete_button.setMaximumWidth(BUTTONS_MAX_WIDTH)
        pos_buttons_layout.addWidget(self.pos_delete_button)

        self.pos_button_up = QPushButton()
        self.pos_button_up.setText("▲")
        self.pos_button_up.setMaximumWidth(BUTTONS_MAX_WIDTH)
        pos_buttons_layout.addWidget(self.pos_button_up)

        self.pos_button_down = QPushButton()
        self.pos_button_down.setText("▼")
        self.pos_button_down.setMaximumWidth(BUTTONS_MAX_WIDTH)
        pos_buttons_layout.addWidget(self.pos_button_down)

        self.pos_button_copy = QPushButton()
        self.pos_button_copy.setText("📑")
        self.pos_button_copy.setMaximumWidth(BUTTONS_MAX_WIDTH)
        pos_buttons_layout.addWidget(self.pos_button_copy)

        self.pos_button_generate = QPushButton()
        self.pos_button_generate.setText("⚙")
        self.pos_button_generate.setMaximumWidth(BUTTONS_MAX_WIDTH)
        pos_buttons_layout.addWidget(self.pos_button_generate)

        self.pos_test_list = QListWidget()
        pos_layout.addWidget(self.pos_test_list)

        pos_comparator_layout = QHBoxLayout()
        pos_comparator_layout.addWidget(label := QLabel('Компаратор:'))
        self.labels.append(label)
        self.pos_comparator_widget = QComboBox()
        self.pos_comparator_widget.addItems(['По умолчанию', 'Числа', 'Числа как текст', 'Текст после подстроки',
                                             'Слова после подстроки', 'Текст', 'Слова'])
        self.pos_comparator_widget.setMaximumWidth(200)
        self.pos_comparator_widget.currentIndexChanged.connect(self.save_pos_comparator)
        pos_comparator_layout.addWidget(self.pos_comparator_widget)
        pos_layout.addLayout(pos_comparator_layout)

        # Negative tests

        neg_layout = QVBoxLayout()
        layout.addLayout(neg_layout)

        neg_buttons_layout = QHBoxLayout()
        neg_layout.addLayout(neg_buttons_layout)
        neg_buttons_layout.addWidget(label := QLabel("Негативные тесты"))
        self.labels.append(label)

        self.neg_add_button = QPushButton()
        self.neg_add_button.setText("+")
        self.neg_add_button.setMaximumWidth(BUTTONS_MAX_WIDTH)
        neg_buttons_layout.addWidget(self.neg_add_button)

        self.neg_delete_button = QPushButton()
        self.neg_delete_button.setText("✕")
        self.neg_delete_button.setMaximumWidth(BUTTONS_MAX_WIDTH)
        neg_buttons_layout.addWidget(self.neg_delete_button)

        self.neg_button_up = QPushButton()
        self.neg_button_up.setText("▲")
        self.neg_button_up.setMaximumWidth(BUTTONS_MAX_WIDTH)
        neg_buttons_layout.addWidget(self.neg_button_up)

        self.neg_button_down = QPushButton()
        self.neg_button_down.setText("▼")
        self.neg_button_down.setMaximumWidth(BUTTONS_MAX_WIDTH)
        neg_buttons_layout.addWidget(self.neg_button_down)

        self.neg_button_copy = QPushButton()
        self.neg_button_copy.setText("📑")
        self.neg_button_copy.setMaximumWidth(BUTTONS_MAX_WIDTH)
        neg_buttons_layout.addWidget(self.neg_button_copy)

        self.neg_button_generate = QPushButton()
        self.neg_button_generate.setText("⚙")
        self.neg_button_generate.setMaximumWidth(BUTTONS_MAX_WIDTH)
        neg_buttons_layout.addWidget(self.neg_button_generate)

        self.neg_test_list = QListWidget()
        neg_layout.addWidget(self.neg_test_list)

        neg_comparator_layout = QHBoxLayout()
        neg_comparator_layout.addWidget(label := QLabel('Компаратор:'))
        self.labels.append(label)
        self.neg_comparator_widget = QComboBox()
        self.neg_comparator_widget.addItems(
            ['По умолчанию', 'Нет', 'Числа', 'Числа как текст', 'Текст после подстроки',
             'Слова после подстроки', 'Текст', 'Слова'])
        self.neg_comparator_widget.setMaximumWidth(200)
        self.neg_comparator_widget.currentIndexChanged.connect(self.save_neg_comparator)
        neg_comparator_layout.addWidget(self.neg_comparator_widget)
        neg_layout.addLayout(neg_comparator_layout)

    def save_pos_comparator(self):
        dct = self.sm.get('pos_comparators')
        if not isinstance(dct, dict):
            dct = dict()
            self.sm.set('pos_comparators', dct)
        dct[f"{self.sm.get('lab')}_{self.sm.get('task')}_{self.sm.get('var')}"] = \
            self.pos_comparator_widget.currentIndex() - 1

    def save_neg_comparator(self):
        dct = self.sm.get('neg_comparators')
        if not isinstance(dct, dict):
            dct = dict()
            self.sm.set('neg_comparators', dct)
        dct[f"{self.sm.get('lab')}_{self.sm.get('task')}_{self.sm.get('var')}"] = \
            self.neg_comparator_widget.currentIndex() - 1

    def set_theme(self):
        self.tm.set_theme_to_list_widget(self.pos_test_list)
        self.tm.set_theme_to_list_widget(self.neg_test_list)
        for el in [self.pos_add_button, self.pos_delete_button, self.pos_button_up, self.pos_button_down,
                   self.pos_button_copy, self.pos_button_generate, self.neg_add_button, self.neg_delete_button,
                   self.neg_button_up, self.neg_button_down, self.neg_button_copy, self.neg_button_generate,
                   self.pos_comparator_widget, self.neg_comparator_widget]:
            self.tm.auto_css(el)
        for label in self.labels:
            label.setFont(self.tm.font_small)
