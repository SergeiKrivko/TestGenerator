import os

from PyQtUIkit.widgets import KitTreeWidgetItem

from src.backend.language.icons import FILE_ICONS


class TreeFile(KitTreeWidgetItem):
    def __init__(self, path: str):
        self.path = path
        self.name = os.path.basename(self.path)
        if '.' not in self.name:
            self.file_type = None
        else:
            self.file_type = self.name[self.name.rindex('.') + 1:]

        super().__init__(self.name, FILE_ICONS.get(self.file_type, 'line-help'))


class TreeDirectory(KitTreeWidgetItem):
    def __init__(self, path):
        super().__init__()
        self.path = path
        self.name = os.path.basename(self.path)
        self.file_type = 'directory'
        self.always_expandable = True

        super().__init__(self.name, 'line-folder')

        self.update_files_list()

    def update_files_list(self):
        if not self.expanded():
            self.clear()
            return

        i = 0
        j = 0
        lst = list(filter(lambda p: os.path.isdir(os.path.join(self.path, p)), os.listdir(self.path))) + \
              list(filter(lambda p: os.path.isfile(os.path.join(self.path, p)), os.listdir(self.path)))
        lst = list(map(lambda p: os.path.join(self.path, p), lst))
        while i < self.childrenCount() and j < len(lst):
            if (path := self.child(i).path) != lst[j]:
                if path.startswith(self.path) and (os.path.isfile(path) or os.path.isdir(path)):
                    if os.path.isdir(lst[j]):
                        self.insertItem(i, TreeDirectory(lst[j]))
                    else:
                        self.insertItem(i, TreeFile(lst[j]))
                    i += 1
                    j += 1
                else:
                    self.deleteItem(i)
            elif isinstance(item := self.child(i), TreeDirectory):
                item.update_files_list()
                i += 1
                j += 1
            else:
                i += 1
                j += 1
        while i < self.childrenCount():
            self.deleteItem(i)
        while j < len(lst):
            if os.path.isdir(lst[j]):
                self.addItem(TreeDirectory(lst[j]))
            else:
                self.addItem(TreeFile(lst[j]))
            j += 1

    def expand(self):
        super().expand()
        self.update_files_list()

    def collapse(self):
        super().collapse()
        self.clear()
