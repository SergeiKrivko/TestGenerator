import json
import webbrowser

from PyQt6.QtCore import Qt, QUrl, QObject, pyqtSlot
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QTextEdit, QLabel, QWidget, QHBoxLayout

import config


class PreviewWidget(QWidget):
    def __init__(self, sm, tm, path=None):
        super().__init__()
        self.sm = sm
        self.tm = tm

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        self.text_edit = QTextEdit()
        self.text_edit.setViewportMargins(30, 10, 30, 10)
        self.text_edit.setReadOnly(True)
        layout.addWidget(self.text_edit)

        self.label = QLabel()
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)

        if config.USE_WEB_ENGINE:
            from PyQt6.QtWebEngineCore import QWebEngineSettings
            from PyQt6.QtWebEngineWidgets import QWebEngineView

            self.web_engine = QWebEngineView()
            self.web_engine.settings().setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, True)
            self.web_engine.settings().setAttribute(QWebEngineSettings.WebAttribute.PdfViewerEnabled, True)
            layout.addWidget(self.web_engine)
        else:
            self.web_engine = QWidget()

        # channel = QWebChannel()
        # handler = CallHandler(self.web_engine)  # Создание экземпляра объекта внешней обработки QWebChannel
        # channel.registerObject('PyHandler',
        #                        handler)  # Зарегистрируйте объект обработки внешнего интерфейса как объект PyHandler на странице внешнего интерфейса. Имя этого объекта - PyHandler при доступе к интерфейсу.
        # self.web_engine.page().setWebChannel(channel)  # Смонтировать объект внешней обработки

        self.setLayout(layout)
        self.theme_apply = False
        self.file = ''

        if path is not None:
            self.open(path)

    def open(self, file: str):
        self.text_edit.hide()
        self.web_engine.hide()
        self.label.hide()
        self.file = file

        try:
            if file.endswith('.md'):
                with open(file, encoding='utf-8') as f:
                    self.text_edit.setMarkdown(f.read())
                self.text_edit.show()
            if file.endswith('.html') or file.endswith('.pdf') or file.endswith('.svg'):
                file = file.replace('\\', '/')
                if config.USE_WEB_ENGINE:
                    self.web_engine.setUrl(QUrl(f"file:///{file}"))
                    self.web_engine.show()
                else:
                    webbrowser.open(f"file:///{file}")
            if file.endswith('.png') or file.endswith('.jpg') or file.endswith('.bmp'):
                self.label.setPixmap(QPixmap(file))
                self.label.show()
        except Exception as ex:
            print(f"{ex.__class__.__name__}: {ex}")

    def set_theme(self):
        if self.isHidden():
            return
        self.theme_apply = True
        for widget in [self.text_edit]:
            self.tm.auto_css(widget)
        self.label.setStyleSheet(self.tm.style_sheet)

    def show(self) -> None:
        super().show()
        self.set_theme()
        if not self.file.endswith('.pdf'):
            self.open(self.file)


class CallHandler(QObject):

    def __init__(self, view):
        super(CallHandler, self).__init__()
        self.view = view

    @pyqtSlot(str, result=str)  # Первый параметр - это тип параметра, передаваемый в обратном вызове
    def init_home(self, str_args):
        print('resolving......init home..')
        print(str_args)  # Просмотр параметров

        # #####
        # Напишите соответствующую логику обработки, такую ​​как:
        # msg = 'Получить сообщение от python'
        msg = self.getInfo()
        # view.page().runJavaScript("alert('%s')" % msg)
        self.view.page().runJavaScript("window.say_hello('%s')" % msg)
        return 'hello, Python'

    def getInfo(self):
        import socket, platform
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        list_info = platform.uname()
        sys_name = list_info[0] + list_info[2]
        cpu_name = list_info[5]
        dic_info = {"hostname": hostname, "ip": ip, "sys_name": sys_name, \
                    "cpu_name": cpu_name}
        # # Вызвать js функцию, реализовать обратный вызов
        # self.mainFrame.evaluateJavaScript('%s(%s)' % ('onGetInfo', json.dumps(dic_info)))
        return json.dumps(dic_info)


# class WebEngine(QWebEngineView):
#     def __init__(self):
#         super(WebEngine, self).__init__()
#         self.setContextMenuPolicy(
#             Qt.NoContextMenu)  # Установить правило контекстного меню как настраиваемое контекстное меню
#         # self.customContextMenuRequested.connect (self.showRightMenu) # Здесь, чтобы загрузить и отобразить настраиваемое контекстное меню, здесь мы не фокусируемся, пропустите подробную ленту
#
#         self.setWindowTitle('QWebChannel взаимодействует с интерфейсом пользователя')
#
#         self.resize(1100, 650)
#         cp = QDesktopWidget().availableGeometry().center()
#         self.move(QPoint(cp.x() - self.width() / 2, cp.y() - self.height() / 2))

