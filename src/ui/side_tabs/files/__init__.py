import os
import platform
import shutil
import subprocess
import sys
import typing

import send2trash
from PyQt6 import QtGui
from PyQt6.QtCore import Qt, QUrl, QMimeData
from PyQtUIkit.widgets import *

from src.backend.language.language import FastRunCommand, FastRunFunction, FastRunAsyncFunction
from src.backend.managers import BackendManager
from src.ui.side_tabs.files.context_menu import ContextMenu
from src.ui.side_tabs.files.fast_run_dialog import FastRunDialog
from src.ui.side_tabs.files.tree import TreeFile, TreeDirectory
from src.ui.side_tabs.files.zip_manager import ZipManager
from src.ui.widgets.side_panel_widget import SidePanelWidget, SidePanelButton


class FilesWidget(SidePanelWidget):
    ignore_files = []

    def __init__(self, bm: BackendManager):
        super(FilesWidget, self).__init__(bm, 'Файлы')

        main_layout = KitVBoxLayout()
        main_layout.setSpacing(3)
        self.setWidget(main_layout)

        self.button_add = SidePanelButton('line-add')
        self.button_add.on_click = self.create_file
        self.buttons_layout.addWidget(self.button_add)

        self.button_remove = SidePanelButton('line-trash')
        self.button_remove.on_click = self.delete_file
        self.buttons_layout.addWidget(self.button_remove)

        self.button_rename = SidePanelButton('custom-rename')
        self.button_rename.on_click = lambda: self.rename_file(False)
        self.buttons_layout.addWidget(self.button_rename)

        self.button_update = SidePanelButton('line-refresh')
        self.button_update.on_click = self.update_files_list
        self.buttons_layout.addWidget(self.button_update)

        self.tree = KitTreeWidget()
        self.tree.selection_type = KitTreeWidget.SelectionType.MULTI
        self.tree.contextMenuRequested.connect(self.run_context_menu)
        # self.tree.movable = True
        self.tree.moveRequested.connect(self.move_file)
        self.root_item = None
        main_layout.addWidget(self.tree)

        self.tree.doubleClicked.connect(self.open_file)

        self.dialog = None
        self.bm.projects.finishOpening.connect(self.open_task)

    def update_files_list(self, hard=False):
        path = self.bm.projects.current.path()
        if isinstance(self.root_item, TreeDirectory):
            if hard:
                self.root_item.deleteSelf()
                hard = True
            else:
                self.root_item.update_files_list()
        else:
            hard = True
        if hard:
            self.root_item = TreeDirectory(path)
            self.tree.addItem(self.root_item)
            self.root_item.expand()
        self.bm.main_tab_command('code', 'check_deleted')

    def move_file(self, items, item2):
        files = [item.path for item in items]
        dst = item2.path

        if not os.path.isdir(dst):
            dst = os.path.dirname(dst)
        for file in files:
            try:
                os.rename(file, os.path.join(dst, os.path.basename(file)))
            except Exception:
                pass
        self.update_files_list()

    def open_task(self):
        self.update_files_list(hard=True)

    def keyPressEvent(self, a0: typing.Optional[QtGui.QKeyEvent]) -> None:
        match a0.key():
            case Qt.Key.Key_C:
                if a0.modifiers() & Qt.KeyboardModifier.ControlModifier:
                    self.copy_file()
            case Qt.Key.Key_X:
                if a0.modifiers() & Qt.KeyboardModifier.ControlModifier:
                    self.copy_file()
            case Qt.Key.Key_V:
                if a0.modifiers() & Qt.KeyboardModifier.ControlModifier:
                    self.paste_files()
            case Qt.Key.Key_F2:
                self.rename_file()
            case Qt.Key.Key_Delete:
                self.delete_file(to_trash=not (bool(a0.modifiers() & Qt.KeyboardModifier.ShiftModifier)))
            case Qt.Key.Key_Backspace:
                if sys.platform == 'darwin':
                    self.delete_file(to_trash=not (bool(a0.modifiers() & Qt.KeyboardModifier.ShiftModifier)))

    def run_context_menu(self, point, item):
        item = self.tree.currentItem()
        if item is None:
            file = None
            path = self.bm.projects.current.path()
        elif isinstance(item, TreeDirectory):
            path = item.path
            file = item.path
        elif isinstance(item, TreeFile):
            file = item.path
            path = item.path
        else:
            raise TypeError("invalid item type")

        menu = ContextMenu(self, path, directory=isinstance(item, TreeDirectory))
        menu.move(self.tree.mapToGlobal(point))
        menu.exec()
        match menu.action:
            case ContextMenu.CREATE_DIR:
                self.create_file(directory=True, base_path=path)
            case ContextMenu.CREATE_FILE:
                self.create_file(base_path=path)
            case ContextMenu.CREATE_PY:
                self.create_file(base_path=path, extension='py')
            case ContextMenu.CREATE_C:
                self.create_file(base_path=path, extension='c')
            case ContextMenu.CREATE_H:
                self.create_file(base_path=path, extension='h')
            case ContextMenu.CREATE_MD:
                self.create_file(base_path=path, extension='md')
            case ContextMenu.CREATE_T2B:
                self.create_file(base_path=path, extension='t2b')
            case ContextMenu.DELETE_FILE:
                self.delete_file(to_trash=False)
            case ContextMenu.MOVE_TO_TRASH:
                self.delete_file(to_trash=True)
            case ContextMenu.RENAME_FILE:
                self.rename_file()
            case ContextMenu.COMPRESS_TO_ZIP:
                self.compress_files()
            case ContextMenu.OPEN_IN_CODE:
                self.open_file(item)
            case ContextMenu.OPEN_BY_SYSTEM:
                self.open_by_system(file)
            case ContextMenu.OPEN_IN_EXPLORER:
                self.open_by_system(file)
            case ContextMenu.OPEN_BY_SYSTEM_TERMINAL:
                self.open_in_system_terminal(file)
            case ContextMenu.OPEN_BY_POWER_SHELL:
                self.open_in_system_terminal(file, 'PowerShell')
            case ContextMenu.OPEN_BY_WSL_TERMINAL:
                self.open_in_system_terminal(file, 'WSL')
            case ContextMenu.OPEN_BY_COMMAND:
                subprocess.call(menu.action_data)
            case ContextMenu.COPY_FILES:
                self.copy_file()
            case ContextMenu.CUT_FILES:
                self.copy_file()
            case ContextMenu.COPY_PATH:
                self.copy_path()
            case ContextMenu.PASTE_FILES:
                self.paste_files()
            case ContextMenu.RUN_FILE:
                self.fast_run_file(menu.action_data)

    def rename_file(self, flag=True):
        if not isinstance(item := self.tree.currentItem(), (TreeFile, TreeDirectory)):
            return
        dialog = KitFormDialog(self,
                               KitForm.Label(f"Введите новое имя "
                                             f"{'папки' if isinstance(item, TreeDirectory) else 'файла'}:"),
                               KitForm.StrField(default=os.path.basename(item.path)))

        edit: KitLineEdit = dialog._form.fields[0]._line_edit
        name = os.path.basename(item.path)
        edit.setSelection(0, len(name) if '.' not in name else name.rindex('.'))

        if dialog.exec():
            new_path = os.path.join(os.path.dirname(item.path), dialog.res()[0])
            if os.path.exists(new_path):
                KitDialog.danger(self, "Ошибка", "Такой файл уже существует")
            else:
                os.rename(item.path, new_path)
                self.update_files_list()

    def fast_run_file(self, option: FastRunCommand | FastRunFunction | FastRunAsyncFunction):
        item = self.tree.currentItem()
        if isinstance(item, TreeFile) or isinstance(item, TreeDirectory):
            if isinstance(option, FastRunCommand):
                self.bm.side_tab_show('run')
                self.bm.side_tab_command('run', option(item.path, self.bm),
                                         cwd=self.bm.projects.current.path())
            elif isinstance(option, (FastRunFunction | FastRunAsyncFunction)):
                FastRunDialog(self, self.bm, item.path, option).exec()
                self.update_files_list()

    def copy_file(self):
        item = self.tree.currentItem()
        if isinstance(item, TreeFile) or isinstance(item, TreeDirectory):
            mime_data = QMimeData()
            mime_data.setUrls([QUrl.fromLocalFile(item.path)])
            KitApplication.clipboard().setMimeData(mime_data)

    def copy_path(self):
        item = self.tree.currentItem()
        if isinstance(item, TreeFile) or isinstance(item, TreeDirectory):
            KitApplication.clipboard().setText(item.path)

    def paste_files(self):
        item = self.tree.currentItem()
        if isinstance(item, TreeFile):
            path = os.path.abspath(os.path.dirname(item.path))
        elif isinstance(item, TreeDirectory):
            path = os.path.abspath(item.path)
        else:
            return

        if KitApplication.clipboard().mimeData().hasUrls():
            urls = [os.path.abspath(el.toLocalFile()) for el in
                    filter(lambda u: u.isLocalFile(), KitApplication.clipboard().mimeData().urls())]
            dst_list = []
            for url in urls.copy():
                dst = os.path.join(path, os.path.basename(url))
                if os.path.isfile(dst):
                    if url == dst:
                        if '.' in os.path.basename(dst):
                            name = dst[:dst.rindex('.')]
                            ext = dst[dst.rindex('.'):]
                        else:
                            name, ext = dst, ''
                        i = 1
                        while os.path.exists(dst := f'{name} ({i}){ext}'):
                            i += 1
                        dst_list.append(dst)
                    else:
                        if KitDialog.question(self, f"{dst} уже существует. Заменить?",
                                              answers=['Пропустить', 'Заменить'], default='Пропустить') == 'Заменить':
                            dst_list.append(dst)
                        else:
                            urls.remove(url)
                else:
                    dst_list.append(dst)

            for url, dst in zip(urls, dst_list):
                if os.path.exists(dst):
                    os.remove(dst)
                shutil.copy(str(url), str(dst))
            self.update_files_list()

    def compress_files(self):
        files = []
        for el in self.tree.selectedItems():
            if isinstance(el, (TreeDirectory, TreeFile)):
                files.append(el.path)
        if not files:
            return
        path = files[0][:files[0].rindex('.')] + '.zip'
        path = self.create_file(base_path=os.path.split(path)[0], base_name=os.path.basename(path), extension='zip')
        if path is None:
            return
        ZipManager.compress(path, files)
        self.update_files_list()

    @staticmethod
    def open_by_system(path):
        if platform.system() == 'Darwin':  # macOS
            subprocess.call(('open', path))
        elif platform.system() == 'Windows':  # Windows
            os.startfile(path)
        else:  # linux variants
            subprocess.call(('xdg-open', path))

    @staticmethod
    def open_in_explorer(path):
        match platform.system():
            case 'Windows':
                subprocess.call(['explorer', path])
            case 'Linux':
                subprocess.call(['nautilus', '--browser', path])
            case 'Darwin':
                subprocess.call(['open', path])

    @staticmethod
    def open_in_system_terminal(path, terminal=''):
        if not os.path.isdir(path):
            path = os.path.dirname(path)
        match platform.system():
            case 'Windows':
                match terminal:
                    case 'PowerShell':
                        os.system(f"start powershell.exe -noexit -command Set-Location -literalPath \"{path}\"")
                    case 'WSL':
                        os.system(f"start wsl.exe --cd \"{path}\"")
                    case _:
                        os.system(f"start cmd.exe /s /k pushd \"{path}\"")
            case 'Linux':
                os.system(f"gnome-terminal --working-directory \"{path}\"")
            case 'Darwin':
                os.system(f"open -a Terminal \"{path}\"")

    def create_directory(self):
        self.create_file(directory=True)

    def create_file(self, directory=False, base_path=None, base_name='', extension=''):
        if base_path is None:
            base_path = self.bm.projects.current.path()
        elif os.path.isfile(base_path):
            base_path = os.path.dirname(base_path)

        options = [(el[0](), el[1]) for el in self.bm.plugins.file_create_options(extension)]

        dialog = KitFormDialog(self,
                               KitForm.Label(f"Введите имя {'папки' if directory else 'файла'}:"),
                               KitForm.StrField(),
                               *[el[0] for el in options]
                               )
        if dialog.exec():
            if not dialog.res()[0]:
                KitDialog.danger(self, "Ошибка",
                                 f"Невозможно создать {'директорию' if directory else 'файл'}: имя не задано")
                return
            try:
                path = os.path.join(base_path, dialog.res()[0])
                if extension and not path.endswith('.' + extension):
                    path += '.' + extension
                if directory:
                    os.makedirs(path)
                else:
                    os.makedirs(self.bm.projects.current.path(), exist_ok=True)
                    open(path, 'x').close()

                    for form, func in options:
                        func(path, form.res())

            except FileExistsError:
                KitDialog.danger(self, "Ошибка",
                                 f"Невозможно создать {'директорию' if directory else 'файл'}: "
                                 f"{'директория' if directory else 'файл'} с таким именем уже существует")
            except PermissionError:
                KitDialog.danger(self, "Ошибка",
                                 f"Невозможно создать {'директорию' if directory else 'файл'}: недостаточно прав")
            except Exception as ex:
                KitDialog.danger(self, "Ошибка",
                                 f"Невозможно создать {'директорию' if directory else 'файл'}: {ex.__class__.__name__}: {ex}")
            else:
                self.update_files_list()
                return path

    def delete_file(self, to_trash=True):
        items = self.tree.selectedItems()
        files = [item.path for item in items]

        if to_trash:
            try:
                send2trash.send2trash(files)
            except FileExistsError:
                pass
            except Exception as ex:
                KitDialog.danger(self, "Ошибка", f"{ex.__class__.__name__}: {ex}")
        else:
            if len(files) // 10 == 1:
                string = 'файлов'
            elif len(files) % 10 == 1:
                string = 'файл'
            elif len(files) % 10 in [2, 3, 4]:
                string = 'файла'
            else:
                string = 'файлов'
            if KitDialog.question(
                    self, f"Вы уверены, что хотите безвозвратно удалить файл {self.tree.currentItem().name}?"
                    if len(files) == 1 else f"Вы уверены, что хотите безвозвратно удалить {len(files)} {string}?",
                    ('Нет', 'Да')) == 'Да':
                for file in files:
                    if os.path.isdir(file):
                        shutil.rmtree(file)
                    else:
                        os.remove(file)
        self.update_files_list()

    def open_file(self, item):
        if isinstance(item, (TreeFile, TreeDirectory)):
            if item.file_type != 'directory':
                self.bm.main_tab_show('code')
                self.bm.main_tab_command('code', 'open', file=item.path)
