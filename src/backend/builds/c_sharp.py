import os
from uuid import UUID

from src.backend.backend_types.build import Build
from src.backend.commands import check_files_mtime, cmd_command, remove_files


class BuildCSharp(Build):
    def compile(self):
        compiler = self.program('dotnet')
        path = self.get('project', '')
        if not os.path.isabs(path):
            path = os.path.join(self._project.path(), path)
        configuration = self.get('configuration', 'Debug')

        res = compiler(f"build --configuration {configuration}", cwd=path)

        return res.returncode == 0, res.stderr

    def command(self, args=''):
        configuration = self.get('configuration', 'Debug')
        compiler = self.program('dotnet')
        path = self.get('project', '')
        if not os.path.isabs(path):
            path = os.path.join(self._project.path(), path)
        return f"{compiler.command()} run {args} --project {path} --configuration {configuration}"
