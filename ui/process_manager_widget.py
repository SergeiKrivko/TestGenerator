from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QMenu


class ProcessManagerWidget(QPushButton):
    def __init__(self, bm, tm):
        super().__init__()
        self.bm = bm
        self.tm = tm
        self.setText("Фоновые Процессы")

        self.menu = QMenu()
        self.setMenu(self.menu)
        self.menu_layout = QVBoxLayout()
        self.menu.setLayout(self.menu_layout)

        self._groups = dict()
        self.bm.processStatusChanged.connect(self._on_process_status_changed)
        self._update()

    def _on_process_status_changed(self, group, name):
        if group in self._groups:
            if self.bm.get_processes_of_group(group):
                self._groups[group].update_processes()
            else:
                self._groups.pop(group).setParent(None)
        else:
            item = _GroupWidget(self.bm, self.tm, group)
            self.menu_layout.addWidget(item)
            self._groups[group] = item
            item.set_theme()

    def _update(self):
        for el in self._groups.values():
            el.setParent(None)
        self._groups.clear()
        for el in self.bm.get_process_groups():
            item = _GroupWidget(self.bm, self.tm, el)
            self.menu_layout.addWidget(item)
            self._groups[el] = item
            item.set_theme()

    def set_theme(self):
        self.tm.auto_css(self, padding=True)
        self.tm.auto_css(self.menu)
        for el in self._groups.values():
            el.set_theme()


class _GroupWidget(QWidget):
    def __init__(self, bm, tm, group: str):
        super().__init__()
        self.bm = bm
        self.tm = tm
        self.group = group

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)

        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addLayout(top_layout)

        self.name_label = QLabel(group)
        top_layout.addWidget(self.name_label)

        self.children_layout = QVBoxLayout()
        self.children_layout.setContentsMargins(20, 0, 0, 0)
        main_layout.addLayout(self.children_layout)

        self._children = dict()
        self.update_processes()

    def update_processes(self):
        for el in self._children.values():
            el.setParent(None)
        for el in self.bm.get_processes_of_group(self.group):
            item = _ProcessWidget(self.tm, el)
            self.children_layout.addWidget(item)
            self._children[el] = item

    def set_theme(self):
        for el in [self.name_label]:
            self.tm.auto_css(el)
        for el in self._children.values():
            el.set_theme()


class _ProcessWidget(QWidget):
    def __init__(self, tm, name):
        super().__init__()
        self.tm = tm
        self.name = name

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)

        self.label = QLabel(self.name)
        main_layout.addWidget(self.label)

    def set_theme(self):
        for el in [self.label]:
            self.tm.auto_css(el)
