import os.path

from PyQt5.QtWidgets import QVBoxLayout, QScrollArea, QWidget, QLineEdit

from tests.commands import CommandManager
from ui.message_box import MessageBox
from ui.side_panel_widget import SidePanelWidget
from ui.tree_widget import TreeWidgetItemCheckable, TreeWidget


class TreeElement(TreeWidgetItemCheckable):
    def __init__(self, sm, tm, path, status):
        super().__init__(tm, os.path.basename(path))
        self.sm = sm
        self.path = path
        self.status = status

        self.stateChanged.connect(lambda flag: self.git_add() if flag else self.git_reset())
        self.check_status()

    def set_checked(self, flag):
        if self._checkbox == flag:
            return
        self._checkbox.setChecked(flag)

    def git_add(self):
        CommandManager.cmd_command(['git', 'add', self.path], cwd=self.sm.path)

    def git_reset(self):
        CommandManager.cmd_command(['git', 'reset', self.path], cwd=self.sm.path)

    def check_status(self):
        if self.status == '??':
            self.set_color('CFile')
        elif self.status == ' M':
            self.set_color('HFile')
        elif self.status == 'M ':
            self.set_color('HFile')
            self.set_checked(True)
        elif self.status == 'D ':
            self.set_color('Directory')
            self.set_checked(True)
        elif self.status == ' D':
            self.set_color('Directory')
        elif self.status == 'AM':
            self.set_color('TxtFile')
        elif self.status == 'A ':
            self.set_color('TxtFile')
            self.set_checked(True)
        else:
            self.set_color('TextColor')

    def set_theme(self):
        super().set_theme()


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

        self.tree = TreeWidget(self.tm, TreeWidget.CHECKABLE)
        layout.addWidget(self.tree)

        self.setLayout(layout)

        self.sm.project_changed.connect(self.update_tree)

    def update_tree(self):
        self.commit_edit.setText('')
        self.tree.clear()
        self.parse_git_status()
        self.set_theme()

    def parse_git_status(self):
        git_status = self.cm.cmd_command(['git', 'status', '--porcelain', '-uall'], cwd=self.sm.path)
        if git_status.returncode:
            return
        git_status = git_status.stdout.rstrip()
        for el in git_status.split('\n'):
            status = el[:2]
            path = el[3:]
            lst = path.replace('\\', '/').split('/')[:-1]
            self.tree.add_item(TreeElement(self.sm, self.tm, path, status), key=lst)

    def commit(self):
        res = self.cm.cmd_command(['git', 'commit', '-m', self.commit_edit.text()])
        if res.returncode:
            MessageBox(MessageBox.Warning, 'Ошибка', res.stderr, self.tm)
        else:
            self.update_tree()

    def set_theme(self):
        super().set_theme()
        self.tm.auto_css(self.commit_edit)
        self.tree.set_theme()
