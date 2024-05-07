from src.backend.backend_types import Build

ITEMS = {
    Build.Type.C_EXE: "Сборка C",
    Build.Type.C_LIB: "Библиотека C",
    Build.Type.CPP_EXE: "Сборка C++",
    Build.Type.PYTHON: "Python",
    Build.Type.BASH: "Скрипт Bash",
    Build.Type.COMMAND: "Команда",
}
IMAGES = {
    Build.Type.C_EXE: 'custom-c',
    Build.Type.C_LIB: 'custom-c',
    Build.Type.CPP_EXE: 'custom-cpp',
    Build.Type.PYTHON: 'solid-logo-python',
    Build.Type.BASH: 'custom-shell',
    Build.Type.COMMAND: 'custom-shell',
}
