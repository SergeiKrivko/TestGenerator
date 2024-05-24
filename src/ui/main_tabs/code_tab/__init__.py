import os
import platform
import subprocess
from enum import Enum

from PyQt6.QtCore import pyqtSignal, Qt
from PyQtUIkit.widgets import *

from src.backend.commands import check_text_file
from src.backend.language.languages import detect_language
from src.backend.language.icons import FILE_ICONS
from src.backend.language.language import Language
from src.backend.managers import BackendManager
from src.backend.language.languages import LANGUAGES
from src.ui.main_tabs.code_tab.preview_widgets import PreviewWidget
from src.ui.main_tabs.code_tab.search_panel import SearchPanel
from src.ui.main_tabs.code_tab.code_editor import CodeEditor, CodeFileEditor
from src.ui.widgets.main_tab import MainTab


class CodeWidget(MainTab):
    testing_signal = pyqtSignal()

    def __init__(self, bm: BackendManager):
        super(CodeWidget, self).__init__()
        self.bm = bm
        self.current_file = ''

        top_layout = KitHBoxLayout()
        top_layout.setFixedHeight(28)
        top_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        top_layout.setContentsMargins(0, 0, 5, 1)
        top_layout.setSpacing(5)
        self.addWidget(top_layout)

        self.tab_bar = KitTabBar()
        self.tab_bar.height = 28
        self.tab_bar.setFixedHeight(28)
        self.tab_bar.radius_top = 0
        self.tab_bar.tabs_palette = 'Bg'
        self.tab_bar.currentChanged.connect(self._on_current_file_changed)
        self.tab_bar.tabCloseRequested.connect(self._close_tab)
        self.tab_bar.tabMoved.connect(self._on_tab_moved)
        self.tab_bar.setTabsMovable(True)
        self.tab_bar.setTabsClosable(True)
        top_layout.addWidget(self.tab_bar, 1000)

        self.button_open = KitIconButton('line-add')
        self.button_open.size = 24
        self.button_open.border = 0
        top_layout.addWidget(self.button_open)

        self.button_search = KitIconButton('line-search')
        self.button_search.size = 24
        self.button_search.border = 0
        self.button_search.setCheckable(True)
        top_layout.addWidget(self.button_search)

        self.button_preview = KitIconButton('line-image')
        self.button_preview.size = 24
        self.button_preview.border = 0
        self.button_preview.setCheckable(True)
        self.button_preview.on_click = self._on_preview_clicked
        top_layout.addWidget(self.button_preview)
        
        self.addWidget(KitHSeparator())

        # self.search_panel = SearchPanel()
        # self.search_panel.hide()
        # self.top_panel.button_open.clicked.connect(self.open_non_project_file)
        # self.top_panel.button_search.clicked.connect(lambda flag:
        #                                              self.search_panel.show() if flag else self.search_panel.hide())
        # self.search_panel.selectText.connect(self.select_text)
        # self.search_panel.button_replace.clicked.connect(self.replace)
        # self.search_panel.button_replace_all.clicked.connect(self.replace_all)
        # self.addWidget(self.search_panel)

        self._layout = KitHBoxLayout()
        self.addWidget(self._layout)

        self.empty_widget = KitVBoxLayout()
        self._layout.addWidget(self.empty_widget)

        self._tabs = dict()
        self.bm.projects.finishOpening.connect(self.first_open)
        self.__widgets: dict[str: _FileEditor] = dict()

    def open_file(self, path: str, pos=None):
        lang = detect_language(path)
        if lang and lang.preview != Language.PreviewType.SYSTEM:
            self._open_file(path, lang)
        elif check_text_file(path):
            self._open_file(path, LANGUAGES.get('txt'))
        else:
            self.open_by_system(path)
        self.save_files_list()

    def _open_file(self, path: str, lang: Language):
        if path in self._tabs:
            self._show_file(path)
            return

        extension = '' if '.' not in path else path.split('.')[-1]

        widget = _FileEditor(path, lang)
        widget.fileDeleted.connect(lambda: self._close_file(path))
        self.__widgets[path] = widget
        self._layout.addWidget(widget)

        tab = KitTab(os.path.basename(path), value=path, icon=FILE_ICONS.get(extension, 'line-help'))
        self._tabs[path] = tab
        self.tab_bar.addTab(tab)

        self._show_file(path)

    def _show_file(self, path: str):
        self.tab_bar.setCurrentTab(self._tabs[path])

    def _on_current_file_changed(self):
        tab = self.tab_bar.currentTab()
        if not tab:
            self.empty_widget.show()
            for el in self.__widgets.values():
                el.hide()

            self.button_preview.hide()
            self.button_search.hide()
        else:
            try:
                self.empty_widget.hide()
                for el in self.__widgets.values():
                    el.hide()
                self.__widgets[tab.value].show()

                widget = self.__widgets[tab.value]
                self.button_preview.setHidden(not widget.has_code or not widget.has_preview)
                self.button_preview.setChecked(widget.state == _FileEditor.State.PREVIEW)
                self.button_search.setHidden(not widget.has_code)
            except KeyError:
                pass

    def command(self, action, **kwargs):
        match action:
            case 'open':
                self.open_file(kwargs['file'], kwargs.get('pos'))
            case 'check_deleted':
                self._check_deleted()

    def first_open(self):
        if not self.bm.projects.current:
            return

        for _ in range(len(self._tabs)):
            self._close_tab(0, save=False)

        for file in self.bm.sm.get('opened_files', []):
            if os.path.isfile(file):
                self.open_file(file)

    def save_files_list(self):
        self.bm.sm.set('opened_files', [self.tab_bar.tab(i).value for i in range(len(self._tabs))])

    def _close_tab(self, index, save=True):
        tab = self.tab_bar.tab(index)
        path = tab.value

        self._tabs.pop(path)
        self.tab_bar.removeTab(index)
        self._layout.removeWidget(self.__widgets[path])
        self.__widgets.pop(path)
        self.save_files_list()

    def _close_file(self, path):
        if path not in self._tabs:
            return
        lst = [self.tab_bar.tab(i) for i in range(self.tab_bar.tabsCount())]
        self._close_tab(lst.index(self._tabs[path]))

    def _check_deleted(self):
        lst = [self.tab_bar.tab(i) for i in range(self.tab_bar.tabsCount())]
        to_close = []
        for key in self._tabs:
            if not os.path.isfile(key):
                to_close.append(lst.index(self._tabs[key]))
        for i in sorted(to_close, reverse=True):
            self._close_tab(i)

    def _on_preview_clicked(self, flag):
        path = self.tab_bar.currentTab().value
        widget = self.__widgets[path]
        widget.set_state(_FileEditor.State.PREVIEW if flag else _FileEditor.State.CODE)

    def _on_tab_moved(self, ind1, ind2):
        self.save_files_list()

    def open_by_system(self, filepath):
        if platform.system() == 'Darwin':  # macOS
            subprocess.call(('open', filepath))
        elif platform.system() == 'Windows':  # Windows
            try:
                os.startfile(filepath)
            except OSError as ex:
                KitDialog.danger(self, "Ошибка", str(ex))
        else:  # linux variants
            subprocess.call(('xdg-open', filepath))


class _FileEditor(KitHBoxLayout):
    class State(Enum):
        CODE = 1
        PREVIEW = 2

    fileDeleted = pyqtSignal()

    def __init__(self, path, lang: Language):
        super().__init__()
        self._path = path
        self._lang = lang

        self._state = self.State.CODE if (lang.preview == Language.PreviewType.NONE or
                                          lang.preview == Language.PreviewType.SIMPLE) else self.State.PREVIEW

        if lang.preview != Language.PreviewType.ONLY:
            self._code_editor = CodeFileEditor(self._path)
            self._code_editor.fileDeleted.connect(self.fileDeleted.emit)
            self.addWidget(self._code_editor)
            if lang.preview == Language.PreviewType.ACTIVE:
                self._code_editor.hide()

        if lang.preview != Language.PreviewType.NONE:
            self._preview_widget = PreviewWidget(self._path)
            self.addWidget(self._preview_widget)
            if lang.preview == Language.PreviewType.SIMPLE:
                self._preview_widget.hide()

    @property
    def path(self):
        return self._path

    @property
    def state(self):
        return self._state

    @property
    def has_code(self):
        return self._lang.preview != Language.PreviewType.ONLY

    @property
    def has_preview(self):
        return self._lang.preview != Language.PreviewType.NONE

    def set_state(self, state: State):
        self._state = state
        if state == self.State.PREVIEW:
            self._code_editor.hide()
            self._preview_widget.show()
        else:
            self._preview_widget.hide()
            self._code_editor.show()
