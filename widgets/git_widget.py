from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QCheckBox, QPushButton, QLabel, QListWidget, \
    QListWidgetItem, QLineEdit
from widgets.options_window import OptionsWidget, OptionsWindow
import os


class GitWidget(QWidget):
    def __init__(self, sm, cm, tm):
        super(GitWidget, self).__init__()
        self.sm = sm
        self.cm = cm
        self.tm = tm
        self.widgets = []
        layout = QHBoxLayout()
        self.setLayout(layout)

        self.options_widget = OptionsWidget({
            'Номер лабы:': {'type': int, 'min': 1, 'name': OptionsWidget.NAME_LEFT},
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

    def set_theme(self):
        self.tm.set_theme_to_list_widget(self.files_list_widget)
        self.options_widget.setFont(self.tm.font_small)
        self.options_widget.set_widget_style_sheet('Номер лабы:', self.tm.spin_box_style_sheet)
        self.options_widget.set_widget_style_sheet('add_code', self.tm.buttons_style_sheet)
        self.options_widget.set_widget_style_sheet('add_tests', self.tm.buttons_style_sheet)
        self.options_widget.set_widget_style_sheet('git_reset', self.tm.buttons_style_sheet)
        self.options_widget.set_widget_style_sheet('Описание коммита:', self.tm.style_sheet)
        self.options_widget.set_widget_style_sheet('Commit', self.tm.buttons_style_sheet)
        self.options_widget.set_widget_style_sheet('Push', self.tm.buttons_style_sheet)

    def options_changed(self, key):
        if key == 'Номер лабы:':
            self.sm['lab'] = self.options_widget["Номер лабы:"]
            old_dir = os.getcwd()
            os.chdir(self.sm.path)
            self.cm.cmd_command(['git', 'reset'])
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
        if s[:7] != f"lab_{self.sm['lab']:0>2}_":
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
        os.chdir(self.sm.path)
        path = self.files_list_widget.currentItem().text()
        if path[0] == ' ' or path[:2] == '??':
            self.cm.cmd_command(["git", 'add', path[2:]])
        else:
            self.cm.cmd_command(['git', 'reset', f'--{path[2:]}'])
        os.chdir(old_dir)
        self.update_files_list()

    def commit(self):
        old_dir = os.getcwd()
        os.chdir(self.sm.path)
        self.cm.cmd_command(['git', 'commit', '-m', f"\"{self.options_widget['Описание коммита:']}\""])
        os.chdir(old_dir)
        self.update_files_list()

    def git_push(self):
        old_dir = os.getcwd()
        os.chdir(self.sm.path)

        # file = open(f"{self.sm.path}/temp.txt", 'w', encoding='utf-8')
        # file.write(self.sm.get('git_login', '-') + '\n')
        # file.write(self.sm.get('git_password', '-'))
        # file.close()
        #
        # os.system(f"git push origin lab_{self.sm['lab']:0>2} < {self.sm.path}/temp.txt > "
        #           f"{self.sm.path}/temp_errors.txt")
        # errors = read_file(f"{self.sm.path}temp_errors.txt")
        errors = '-'

        if errors.strip():
            self.options_window = OptionsWindow({
                "Логин:": {'type': str, 'width': 250},
                "Пароль:": {'type': str, 'width': 250, 'echo_mode': QLineEdit.Password}
            })
            if self.options_window.exec():
                self.git_push_from_window()
        if os.path.isfile(f"{self.sm.path}/temp.txt"):
            os.remove(f"{self.sm.path}/temp.txt")
        if os.path.isfile(f"{self.sm.path}/temp_errors.txt"):
            os.remove(f"{self.sm.path}/temp_errors.txt")
        os.chdir(old_dir)

    def git_push_from_window(self):
        old_dir = os.getcwd()
        os.chdir(self.sm.path)

        res = self.cm.cmd_command(['git', 'config', 'remote.origin.url'])
        url = res.stdout.replace(
            "https://", f"https://{self.options_window.values['Логин:']}:{self.options_window.values['Пароль:']}@")

        self.cm.cmd_command(['git', 'push', 'url', f"lab_{self.sm['lab']:0>2}"])

        os.chdir(old_dir)

    def update_files_list(self):
        self.files_list_widget.clear()
        try:
            old_dir = os.getcwd()
            os.chdir(self.sm.path)
            res = self.cm.cmd_command(['git', 'status', '--porcelain'])

            git_status = res.stdout

            for line in git_status.split('\n'):
                item = QListWidgetItem(line.rstrip())
                item.setFont(self.tm.font_small)
                self.files_list_widget.addItem(item)
            os.chdir(old_dir)
        except Exception:
            pass

    def all_code_to_index(self):
        old_dir = os.getcwd()
        os.chdir(self.sm.path)
        for dir in os.listdir(self.sm.path):
            if dir.startswith(f"lab_{self.sm['lab']:0>2}"):
                for file in os.listdir(f"{self.sm.path}/{dir}"):
                    if '.c' in file or '.h' in file:
                        self.cm.cmd_command(['git', 'add', f"{dir}/{file}"])
        os.chdir(old_dir)
        self.update_files_list()

    def all_tests_to_index(self):
        old_dir = os.getcwd()
        os.chdir(self.sm.path)
        for dir in os.listdir(self.sm.path):
            if dir.startswith(f"lab_{self.sm['lab']:0>2}"):
                self.cm.cmd_command(['git', 'add', f"{dir}/func_tests/readme.md"])
                self.cm.cmd_command(['git', 'add', f"{dir}/func_tests/data/"])
        os.chdir(old_dir)
        self.update_files_list()

    def git_reset(self):
        old_dir = os.getcwd()
        os.chdir(self.sm.path)
        self.cm.cmd_command(['git', 'reset'])
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
