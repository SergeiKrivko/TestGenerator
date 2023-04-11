import os

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QListWidgetItem, QHBoxLayout, QPushButton, QDialog, \
    QDialogButtonBox, QLabel, QComboBox, QLineEdit

from widgets.options_window import OptionsWidget, OptionsWindow


class TODOWidget(QWidget):
    jumpToCode = pyqtSignal(str, int)

    def __init__(self, settings, cm):
        super(TODOWidget, self).__init__()
        self.settings = settings
        self.cm = cm

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.options_widget = OptionsWidget({
            'h_line': {
                'Номер лабы:': {'type': int, 'min': 1, 'initial': self.settings.get('lab', 1),
                                'name': OptionsWidget.NAME_LEFT, 'width': 60}
            }
        })
        self.options_widget.clicked.connect(self.option_changed)
        layout.addWidget(self.options_widget)

        buttons_layout = QHBoxLayout()
        buttons_layout.setAlignment(Qt.AlignLeft)
        layout.addLayout(buttons_layout)

        self.button_add = QPushButton("Добавить")
        self.button_add.setFixedHeight(25)
        self.button_add.clicked.connect(lambda: self.list_widget.addItem(TODOItem(0, '')))
        buttons_layout.addWidget(self.button_add)

        self.button_addc = QPushButton("Добавить в код")
        self.button_addc.setFixedHeight(25)
        self.button_addc.clicked.connect(self.add_todo_to_code)
        buttons_layout.addWidget(self.button_addc)

        self.button_delete = QPushButton("Удалить")
        self.button_delete.setFixedHeight(25)
        self.button_delete.clicked.connect(self.delete_todo)
        buttons_layout.addWidget(self.button_delete)

        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)
        self.list_widget.doubleClicked.connect(self.open_todo)

    def option_changed(self, key):
        if key in ('Номер лабы:', 'Номер задания:'):
            self.settings['lab'] = self.options_widget["Номер лабы:"]
            self.open_lab()

    def open_todo(self):
        item = self.list_widget.currentItem()
        if isinstance(item, TODOItem):
            self.window = OptionsWindow({
                'Задание:': {'type': 'combo', 'values': ['Общее'] + self.cm.list_of_tasks(), 'initial': item.task},
                'Описание:': {'type': str, 'width': 500, 'initial': item.description},
            })
            self.window.show()
            self.window.returnPressed.connect(self.update_todo_item)
        elif isinstance(item, CodeTODOItem):
            self.jump_to_code()

    def add_todo_to_code(self):
        dlg = AddTODODialogWindow(self.settings['path'], self.settings['lab'])
        if dlg.exec():
            file = open(f"{self.settings['path']}/{dlg.task_combo_box.currentText()}/"
                        f"{dlg.file_combo_box.currentText()}", 'a', encoding='utf-8')
            file.write(f"// TODO: {dlg.line_edit.text()}\n")
            file.close()
        self.create_todo_file()
        self.open_lab()

    def delete_todo(self):
        item = self.list_widget.currentItem()
        if isinstance(item, CodeTODOItem):
            file = open(f"{self.settings['path']}/{item.path}", encoding='utf-8')
            text = file.read()
            file.close()

            text = text.replace(f"// TODO: {item.description.strip()}", "")
            file = open(f"{self.settings['path']}/{item.path}", 'w', encoding='utf-8')
            file.write(text)
            file.close()
        self.list_widget.takeItem(self.list_widget.currentRow())

    def update_todo_item(self, dct):
        item = self.list_widget.currentItem()
        if isinstance(item, TODOItem):
            item.set_task(dct.get('Задание:', 0))
            item.set_description(dct.get('Описание:', ''))

    def create_todo_file(self):
        for i in range(self.list_widget.count()):
            if isinstance(self.list_widget.item(i), TODOItem):

                self.list_widget.sortItems()

                os.makedirs(f"{self.settings['path']}/TODO", exist_ok=True)
                file = open(f"{self.settings['path']}/TODO/lab_{self.settings['lab']:0>2}.md", 'w', encoding='utf-8')
                file.write(f"# Лабораторная работа №{self.settings['lab']}: список задач\n\n")

                task = -1
                for i in range(self.list_widget.count()):
                    item = self.list_widget.item(i)
                    if isinstance(item, TODOItem):
                        if item.task != task:
                            file.write(f"\n## {'Задание ' + str(item.task) if item.task else 'Общее'}\n")
                            task = item.task
                        file.write(f"- {item.description}\n")
                file.close()
                break
        else:
            if os.path.isfile(f"{self.settings['path']}/TODO/lab_{self.settings['lab']:0>2}.md"):
                os.remove(f"{self.settings['path']}/TODO/lab_{self.settings['lab']:0>2}.md")

    def open_lab(self):
        self.list_widget.clear()

        for task, description in self.cm.parce_todo_md():
            self.list_widget.addItem(TODOItem(task, description))

        for path, line, description in self.cm.parse_todo_in_code():
            self.list_widget.addItem(CodeTODOItem(path, line, description))

        self.list_widget.sortItems()

    def jump_to_code(self):
        item = self.list_widget.currentItem()
        try:
            if isinstance(item, CodeTODOItem):
                self.settings['task'] = int(item.path[7:9])
                self.settings['var'] = int(item.path[10:12])
                self.jumpToCode.emit(item.path.split('/')[1], item.line)
        except Exception:
            pass

    def show(self) -> None:
        self.open_lab()
        super(TODOWidget, self).show()
        
    def hide(self, save_data=True) -> None:
        if not self.isHidden() and save_data:
            self.create_todo_file()
        super(TODOWidget, self).hide()


class TODOItem(QListWidgetItem):
    def __init__(self, task, description):
        super(TODOItem, self).__init__()
        self.task = task
        self.description = description
        self.setText(f"{'Задание ' + str(task) if task else 'Общее':35}\t{description}")
        self.setForeground(Qt.blue)

    def set_description(self, description):
        self.description = description
        self.setText(f"{'Задание ' + str(self.task) if self.task else 'Общее':35}\t{description}")

    def set_task(self, task):
        self.task = task
        self.setText(f"{'Задание ' + str(self.task) if self.task else 'Общее':35}\t{self.description}")


class CodeTODOItem(QListWidgetItem):
    def __init__(self, path, line, description):
        super(CodeTODOItem, self).__init__()
        self.path = path
        self.description = description
        self.line = line
        self.setText(f"{self.path + '  ' + str(line):30}\t{self.description}")
        self.setForeground(Qt.darkYellow)


class AddTODODialogWindow(QDialog):
    def __init__(self, path, lab):
        super().__init__()
        self.path = path

        self.setWindowTitle("Добавить TODO в код")

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        h_layout = QHBoxLayout()
        self.layout.addLayout(h_layout)
        h_layout.addWidget(QLabel("Задание"))

        self.task_combo_box = QComboBox()
        h_layout.addWidget(self.task_combo_box)
        self.task_combo_box.setFixedSize(125, 25)
        self.task_combo_box.addItems(sorted(filter(lambda p: p.startswith(f"lab_{lab:0>2}_"), os.listdir(path))))
        self.task_combo_box.currentTextChanged.connect(self.change_task)

        h_layout.addWidget(QLabel("Файл"))
        self.file_combo_box = QComboBox()
        h_layout.addWidget(self.file_combo_box)
        self.file_combo_box.setFixedSize(125, 25)
        self.file_combo_box.addItems(sorted(filter(lambda p: p.endswith(".c") or p.endswith(".h"), os.listdir(
            f"{self.path}/{self.task_combo_box.currentText()}"))))

        self.line_edit = QLineEdit()
        self.line_edit.setFixedSize(400, 25)
        self.layout.addWidget(self.line_edit)

        self.layout.addWidget(self.buttonBox)

    def change_task(self):
        self.file_combo_box.clear()
        self.file_combo_box.addItems(sorted(filter(lambda p: p.endswith(".c") or p.endswith(".h"), os.listdir(
            f"{self.path}/{self.task_combo_box.currentText()}"))))
