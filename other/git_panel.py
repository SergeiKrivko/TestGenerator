import os.path

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QVBoxLayout, QScrollArea, QWidget, QHBoxLayout, QCheckBox, QLabel, QLineEdit

from tests.commands import CommandManager
from ui.button import Button
from ui.message_box import MessageBox
from ui.side_panel_widget import SidePanelWidget


class GitPanel(SidePanelWidget):
    def __init__(self, sm, cm, tm):
        super().__init__(sm, tm, 'Git', ['pull', 'commit', 'push'])
        self.cm = cm
        self.setFixedWidth(300)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        self.commit_edit = QLineEdit()
        self.commit_edit.setPlaceholderText("Commit message")
        layout.addWidget(self.commit_edit)

        self.buttons['commit'].clicked.connect(self.commit)

        self.scroll_area = QScrollArea()
        self.scroll_layout = QVBoxLayout()
        scroll_widget = QWidget()
        self.scroll_area.setWidget(scroll_widget)
        self.scroll_area.setWidgetResizable(True)
        scroll_widget.setLayout(self.scroll_layout)
        layout.addWidget(self.scroll_area)

        self.tree = TreeWidget(self.sm, self.tm, dict())

        self.setLayout(layout)

        self.sm.project_changed.connect(self.update_tree)

    def update_tree(self):
        self.commit_edit.setText('')
        for i in reversed(range(self.scroll_layout.count())):
            self.scroll_layout.itemAt(i).widget().setParent(None)
        self.tree = TreeWidget(self.sm, self.tm, self.parse_git_status())
        self.scroll_layout.addWidget(self.tree)
        self.set_theme()

    def parse_git_status(self):
        git_status = self.cm.cmd_command(['git', 'status', '--porcelain', '-uall'], cwd=self.sm.path)
        if git_status.returncode:
            return dict()
        git_status = git_status.stdout.strip()
        res = dict()
        for el in git_status.split('\n'):
            status = el[:2]
            lst = el[3:].replace('\\', '/').split('/')
            dct = res
            for i in range(len(lst) - 1):
                if lst[i] not in dct:
                    dct[lst[i]] = dict()
                dct = dct[lst[i]]
            dct[el[3:]] = status
        return res

    def commit(self):
        res = self.cm.cmd_command(['git', 'commit', '-m', self.commit_edit.text()])
        if res.returncode:
            MessageBox(MessageBox.Warning, 'Ошибка', res.stderr, self.tm)
        else:
            self.update_tree()

    def set_theme(self):
        super().set_theme()
        self.tm.auto_css(self.commit_edit)
        self.tm.auto_css(self.scroll_area)
        self.tree.set_theme()


class TreeElement(QWidget):
    def __init__(self, sm, tm, path, status):
        super().__init__()
        self.sm = sm
        self.tm = tm
        self.path = path
        self.status = status

        top_layout = QHBoxLayout()
        top_layout.setSpacing(5)
        top_layout.setAlignment(Qt.AlignLeft)
        top_layout.setContentsMargins(22, 0, 0, 0)
        self.setLayout(top_layout)

        self.checkbox = QCheckBox()
        self.checkbox.stateChanged.connect(lambda flag: self.git_add() if flag else self.git_reset())
        top_layout.addWidget(self.checkbox)

        self.label = QLabel(os.path.basename(path))
        top_layout.addWidget(self.label)

        self.color = ''
        self.check_status()
        self.set_theme()

    def set_checked(self, flag):
        if self.checkbox == flag:
            return
        self.checkbox.setChecked(flag)

    def git_add(self):
        CommandManager.cmd_command(['git', 'add', self.path], cwd=self.sm.path)

    def git_reset(self):
        CommandManager.cmd_command(['git', 'reset', self.path], cwd=self.sm.path)

    def check_status(self):
        if self.status == '??':
            self.color = self.tm['CFile']
        elif self.status == ' M':
            self.color = self.tm['HFile']
        elif self.status == 'M ':
            self.color = self.tm['HFile']
            self.set_checked(True)
        elif self.color == 'AM':
            self.color = self.tm['TxtFile']
        elif self.color == 'A ':
            self.color = self.tm['TxtFile']
            self.set_checked(True)
        else:
            self.color = self.tm['TextColor']
        if isinstance(self.color, QColor):
            self.color = self.color.name()

    def set_theme(self):
        for el in [self.checkbox]:
            self.tm.auto_css(el)
        self.label.setFont(self.tm.font_small)
        self.label.setStyleSheet(f"color: {self.color};")


class TreeBranch(QWidget):
    def __init__(self, sm, tm, name, struct: dict):
        super().__init__()
        self.sm = sm
        self.tm = tm
        self.name = name

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)

        top_layout = QHBoxLayout()
        top_layout.setSpacing(5)
        top_layout.setAlignment(Qt.AlignLeft)
        top_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addLayout(top_layout)

        self.button_maximize = Button(self.tm, 'button_maximize')
        self.button_maximize.setFixedSize(17, 17)
        self.button_maximize.clicked.connect(self.maximize)
        top_layout.addWidget(self.button_maximize)

        self.button_minimize = Button(self.tm, 'button_minimize')
        self.button_minimize.setFixedSize(17, 17)
        self.button_minimize.clicked.connect(self.minimize)
        self.button_minimize.hide()
        top_layout.addWidget(self.button_minimize)

        self.checkbox = QCheckBox()
        self.checkbox.stateChanged.connect(self.set_checked)
        top_layout.addWidget(self.checkbox)

        self.label = QLabel(name)
        top_layout.addWidget(self.label)

        layout = QVBoxLayout()
        layout.setContentsMargins(15, 0, 0, 0)
        main_layout.addLayout(layout)

        self.child_widgets = dict()

        for key, item in struct.items():
            if isinstance(item, dict):
                widget = TreeBranch(self.sm, self.tm, key, item)
            else:
                widget = TreeElement(self.sm, self.tm, key, item)
            widget.hide()
            self.child_widgets[key] = widget
            layout.addWidget(widget)

    def maximize(self):
        for el in self.child_widgets.values():
            el.show()
        self.button_maximize.hide()
        self.button_minimize.show()

    def minimize(self):
        for el in self.child_widgets.values():
            el.hide()
        self.button_minimize.hide()
        self.button_maximize.show()

    def set_checked(self, flag):
        if self.checkbox == flag:
            return
        self.checkbox.setChecked(flag)
        for el in self.child_widgets.values():
            el.set_checked(flag)

    def set_theme(self):
        for el in [self.button_minimize, self.button_maximize, self.label, self.checkbox]:
            self.tm.auto_css(el)
        for el in self.child_widgets.values():
            el.set_theme()


class TreeWidget(QWidget):
    def __init__(self, sm, tm, struct):
        super().__init__()
        self.sm = sm
        self.tm = tm

        layout = QVBoxLayout()
        layout.setSpacing(5)
        layout.setAlignment(Qt.AlignTop)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self.child_widgets = dict()

        for key, item in struct.items():
            if isinstance(item, dict):
                widget = TreeBranch(self.sm, self.tm, key, item)
            else:
                widget = TreeElement(self.sm, self.tm, key, item)
            self.child_widgets[key] = widget
            layout.addWidget(widget)

    def set_theme(self):
        for el in self.child_widgets.values():
            el.set_theme()
