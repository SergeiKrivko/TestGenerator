import os.path

from PyQt6.QtCore import QObject, pyqtSignal

from src.backend.backend_types.project import Project
from src.backend.backend_types.util import Util
from src.backend.commands import *
from src.backend.managers._builds import BuildsManager
from src.backend.managers._func_tests import FuncTestsManager
from src.backend.managers._processes import CustomThread
from src.backend.managers._processes import ProcessManager
from src.backend.managers._programs import ProgramsManager
from src.backend.managers._project import ProjectManager
from src.backend.managers._unit_test import UnitTestsManager
from src.backend.managers._utils import UtilsManager
from src.backend.settings_manager import SettingsManager


class BackendManager(QObject):
    showMainTab = pyqtSignal(str)
    showSideTab = pyqtSignal(str)
    mainTabCommand = pyqtSignal(str, tuple, dict)
    sideTabCommand = pyqtSignal(str, tuple, dict)
    showNotification = pyqtSignal(str, str)

    def __init__(self):
        super().__init__()
        self._sm = SettingsManager()

        self.func_tests = FuncTestsManager(self._sm, self)
        self.builds = BuildsManager(self._sm, self)
        self.processes = ProcessManager(self._sm, self)
        self.programs = ProgramsManager(self._sm, self)
        self.projects = ProjectManager(self)
        self.utils = UtilsManager(self)
        self.unit_tests = UnitTestsManager(self)

        self.changing_project = False

    @property
    def sm(self):
        return self._sm

    # --------------------- tabs ----------------------------

    def main_tab_command(self, tab: str, *args, **kwargs):
        self.mainTabCommand.emit(tab, args, kwargs)

    def side_tab_command(self, tab: str, *args, **kwargs):
        self.sideTabCommand.emit(tab, args, kwargs)

    def main_tab_show(self, tab: str):
        self.showMainTab.emit(tab)

    def side_tab_show(self, tab: str):
        self.showSideTab.emit(tab)

    # ------------------- cmd args --------------------------

    async def _open_file_in_project(self, project: Project, file: str):
        lst = project.get('opened_files', [])
        if file in lst:
            lst.remove(file)
        lst.append(file)
        project.set('opened_files', lst)
        await self.projects.open(project)

    async def _open_file(self, file: str):
        path = os.path.dirname(file)
        recent = [proj.path() for proj in self.projects.recent]
        while path != os.path.dirname(path):
            if path in recent:
                project = self.projects.get(path)
                break
            path = os.path.dirname(path)
        else:
            project = self.projects.light_edit_project
        await self._open_file_in_project(project, file)

    async def parse_cmd_args(self, args):
        if args.filename or args.file:
            path = os.path.abspath(args.filename or args.file)
            await self._open_file(path)
        elif args.directory:
            path = os.path.abspath(args.directory)
            if path in [proj.path() for proj in self.projects.recent]:
                await self.projects.open(path)
            else:
                await self.projects.new(path, language=detect_project_lang(path))
        elif self._sm.get_general('light_edit_opened', False):
            await self.projects.open(self.projects.light_edit_project)
        else:
            await self.projects.open(self._sm.get_general('project'))

        if not args.build and not args.testing:
            return

        util = None
        if args.util:
            try:
                util_id = int(args.util)
            except ValueError:
                for key, item in self.utils.all.items():
                    if item['name'] == args.util:
                        util_id = key
                        break
                else:
                    raise KeyError("Util not found")
            util = self.utils.get(util_id)

        if args.build:
            try:
                build_id = int(args.build)
            except ValueError:
                for key, item in self.builds.all.items():
                    if item['name'] == args.build:
                        build_id = key
                        break
                else:
                    raise KeyError("Build not found")
            build = self.builds.get(build_id)
            command = build.command(args)
            if isinstance(util, Util):
                command = util['command'].format(app=command, args='')
            cwd = build.get('cwd', '.') if os.path.isabs(build.get('cwd', '.')) else \
                os.path.join(self._sm.project.path(), build.get('cwd', '.'))
            subprocess.run(command, cwd=cwd)

        if args.testing:
            await self.func_tests.testing_async(verbose=True)

        await self.close_program()

    def notification(self, title, message):
        self.showNotification.emit(title, message)

    async def close_program(self):
        for project in list(self.projects.all.values()):
            try:
                if project.get('temp', False):
                    await self.projects.delete(project)
            except KeyError:
                pass
