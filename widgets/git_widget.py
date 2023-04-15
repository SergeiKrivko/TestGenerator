from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QCheckBox, QPushButton, QLabel, QListWidget, \
    QListWidgetItem, QLineEdit
from widgets.options_window import OptionsWidget, OptionsWindow
import os


class GitWidget(QWidget):
    def __init__(self, settings):
        super(GitWidget, self).__init__()
        self.settings = settings
        self.widgets = []
        layout = QHBoxLayout()
        self.setLayout(layout)

        self.options_widget = OptionsWidget({
            'Номер лабы:': {'type': int, 'min': 1, 'initial': self.settings.get('lab', 1),
                            'name': OptionsWidget.NAME_LEFT},
            'add_code': {'type': 'button', 'text': 'Добавить весь код', 'name': OptionsWidget.NAME_SKIP},
            'add_tests': {'type': 'button', 'text': 'Добавить все тесты', 'name': OptionsWidget.NAME_SKIP},
            'git_reset': {'type': 'button', 'text': 'Сбросить', 'name': OptionsWidget.NAME_SKIP},
            'Описание коммита:': {'type': str, 'width': 300},
            'Commit': {'type': 'button', 'text': 'Commit', 'name': OptionsWidget.NAME_SKIP},
            'Push': {'type': 'button', 'text': 'Push', 'name': OptionsWidget.NAME_SKIP}
        })
        layout.addWidget(self.options_widget)
        self.options_widget.clicked.connect(self.options_changed)

        self.files_list_widget = QListWidget()
        self.files_list_widget.setFont(QFont("Courier", 10))
        self.files_list_widget.doubleClicked.connect(self.git_add)
        layout.addWidget(self.files_list_widget)

    def options_changed(self, key):
        if key == 'Номер лабы:':
            self.settings['lab'] = self.options_widget["Номер лабы:"]
            old_dir = os.getcwd()
            os.chdir(self.settings['path'])
            os.system(f"git reset > {self.settings['path']}/temp.txt")
            os.remove(f"{self.settings['path']}/temp.txt")
            os.chdir(old_dir)
            self.update_files_list()
        elif key == 'add_code':
            self.all_code_to_index()
        elif key == 'add_tests':
            self.all_tests_to_index()
        elif key == 'git_reset':
            self.git_reset()
        elif key == 'Commit':
            self.commit()
        elif key == 'Push':
            self.git_push()

    def parce_lab_number(self, s):
        if s[:7] != f"lab_{self.settings['lab']:0>2}_":
            return 0, 0
        if len(s) == 9:
            try:
                return int(s[7:]), -1
            except ValueError:
                return 0, 0
        try:
            return int(s[7:9]), int(s[10:])
        except ValueError:
            return 0, 0

    def git_add(self):
        old_dir = os.getcwd()
        os.chdir(self.settings['path'])
        path = self.files_list_widget.currentItem().text()
        if path[0] == ' ' or path[:2] == '??':
            os.system(f"git add {path[2:]}")
        else:
            os.system(f"git reset --{path[2:]} > {self.settings['path']}/temp.txt")
            os.remove(f"{self.settings['path']}/temp.txt")
        os.chdir(old_dir)
        self.update_files_list()

    def commit(self):
        old_dir = os.getcwd()
        os.chdir(self.settings['path'])
        os.system(f"git commit -m \"{self.options_widget['Описание коммита:']}\"")
        os.chdir(old_dir)
        self.update_files_list()

    def git_push(self):
        old_dir = os.getcwd()
        os.chdir(self.settings['path'])

        # file = open(f"{self.settings['path']}/temp.txt", 'w', encoding='utf-8')
        # file.write(self.settings.get('git_login', '-') + '\n')
        # file.write(self.settings.get('git_password', '-'))
        # file.close()
        #
        # os.system(f"git push origin lab_{self.settings['lab']:0>2} < {self.settings['path']}/temp.txt > "
        #           f"{self.settings['path']}/temp_errors.txt")
        # errors = read_file(f"{self.settings['path']}temp_errors.txt")
        errors = '-'

        if errors.strip():
            options_window = OptionsWindow({
                "Логин:": {'type': str, 'width': 250},
                "Пароль:": {'type': str, 'width': 250, 'echo_mode': QLineEdit.Password}
            })
            options_window.show()
            options_window.returnPressed.connect(self.git_push_from_window)
        if os.path.isfile(f"{self.settings['path']}/temp.txt"):
            os.remove(f"{self.settings['path']}/temp.txt")
        if os.path.isfile(f"{self.settings['path']}/temp_errors.txt"):
            os.remove(f"{self.settings['path']}/temp_errors.txt")
        os.chdir(old_dir)

    def git_push_from_window(self, settings):
        old_dir = os.getcwd()
        os.chdir(self.settings['path'])

        os.system("git config remote.origin.url > temp.txt")
        url = read_file('temp.txt').replace("https://", f"https://{settings['Логин:']}:{settings['Пароль:']}@")

        os.system(f"git push {url} lab_{self.settings['lab']:0>2} > {self.settings['path']}/temp_errors.txt")

        if os.path.isfile(f"{self.settings['path']}/temp.txt"):
            os.remove(f"{self.settings['path']}/temp.txt")
        os.chdir(old_dir)

    def update_files_list(self):
        old_dir = os.getcwd()
        os.chdir(self.settings['path'])
        os.system(f"git status --porcelain > {self.settings['path']}temp.txt")
        git_status = read_file(f"{self.settings['path']}temp.txt", readlines=True)

        self.files_list_widget.clear()
        for line in git_status:
            self.files_list_widget.addItem(QListWidgetItem(line.rstrip()))
        os.chdir(old_dir)

    def all_code_to_index(self):
        old_dir = os.getcwd()
        os.chdir(self.settings['path'])
        for dir in os.listdir(self.settings['path']):
            if dir.startswith(f"lab_{self.settings['lab']:0>2}"):
                for file in os.listdir(f"{self.settings['path']}/{dir}"):
                    if '.c' in file or '.h' in file:
                        os.system(f"git add {dir}/{file}")
        os.chdir(old_dir)
        self.update_files_list()

    def all_tests_to_index(self):
        old_dir = os.getcwd()
        os.chdir(self.settings['path'])
        for dir in os.listdir(self.settings['path']):
            if dir.startswith(f"lab_{self.settings['lab']:0>2}"):
                os.system(f"git add {dir}/func_tests/readme.md")
                os.system(f"git add {dir}/func_tests/data")
        os.chdir(old_dir)
        self.update_files_list()

    def git_reset(self):
        old_dir = os.getcwd()
        os.chdir(self.settings['path'])
        os.system("git reset")
        os.chdir(old_dir)
        self.update_files_list()

    def show(self) -> None:
        self.update_files_list()
        super(GitWidget, self).show()

    def hide(self) -> None:
        super(GitWidget, self).hide()


class GitItem(QWidget):
    def __init__(self, name, struct):
        super(GitItem, self).__init__()
        self.name = name
        self.struct = struct
        self.widgets = dict()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        layout1 = QHBoxLayout()
        layout1.setAlignment(Qt.AlignLeft)
        layout.addLayout(layout1)

        self.button = QPushButton()
        self.button.setText("▼")
        self.button.setFixedSize(20, 20)
        layout1.addWidget(self.button)
        layout1.setContentsMargins(0, 0, 0, 0)

        self.check_box = QCheckBox()
        layout1.addWidget(self.check_box)

        layout1.addWidget(QLabel(self.name))

        self.main_widget = QWidget()
        layout.addWidget(self.main_widget)

        layout2 = QVBoxLayout()
        layout2.setContentsMargins(35, 0, 0, 0)
        layout2.setAlignment(Qt.AlignTop)
        self.main_widget.setLayout(layout2)

        for key, item in self.struct.items():
            if isinstance(item, dict):
                widget = GitItem(key, item)
            else:
                widget = SimpleGitItem(key)
            self.widgets[key] = widget
            layout2.addWidget(widget)

        self.button.clicked.connect(self.maximize_minimize)

    def maximize_minimize(self, *args):
        if self.main_widget.isHidden():
            self.main_widget.show()
            self.button.setText("▼")
        else:
            self.main_widget.hide()
            self.button.setText("▶")


class SimpleGitItem(QWidget):
    def __init__(self, name):
        super(SimpleGitItem, self).__init__()
        self.name = name
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignLeft)
        self.setLayout(layout)

        self.check_box = QCheckBox()
        layout.addWidget(self.check_box)

        layout.addWidget(QLabel(self.name))


def read_file(path, readlines=False):
    file = open(path, encoding='utf-8')
    if readlines:
        res = file.readlines()
    else:
        res = file.read()
    file.close()
    return res
