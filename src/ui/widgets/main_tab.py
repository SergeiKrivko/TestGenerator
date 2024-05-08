from PyQtUIkit.widgets import KitVBoxLayout


class MainTab(KitVBoxLayout):
    def __init__(self):
        super().__init__()
        self.need_project = False

    def command(self, *args, **kwargs):
        pass
