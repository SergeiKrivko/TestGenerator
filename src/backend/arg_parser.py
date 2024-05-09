import argparse

from src import config

_parser = argparse.ArgumentParser(prog=config.APP_NAME)

_parser.add_argument('files', nargs='*', action='store')
# _parser.add_argument('-f', '--file', help="Открывает указанный файл. Если он находится в одном из известных проектов,"
#                                           "будет открыт этот проект и ближайший к файлу подпроект. Иначе будет создан"
#                                           "временный или постоянный проект в директории, где находится файл.")
_parser.add_argument('-d', '--directory', help="Открывает папку как проект.")
_parser.add_argument('-b', '--build', help="Запускает одну из конфигураций запуска. В качестве аргумента необходимо "
                                           "указать её название или ID. Графический интерфейс не будет запущен.")
_parser.add_argument('--new-window', help="Открывает файл(ы) в новом окне, "
                                          "даже если уже есть запущенные копии программы.", action='store_true')
_parser.add_argument('--util', help="Указывает утилиту для конфигурации запуска.")
_parser.add_argument('-t', '--testing', '--func-testing', action='store_true',
                     help="Запускает функциональное тестирование проекта. Графический интерфейс не будет запущен.")
_parser.add_argument('-u', '--unit', '--unit-testing', action='store_true',
                     help="Запускает модульное тестирование проекта. Графический интерфейс не будет запущен.")
_parser.add_argument('-v', '--version', action='version', version=f"{config.APP_NAME} {config.APP_VERSION}")

args = _parser.parse_args()

