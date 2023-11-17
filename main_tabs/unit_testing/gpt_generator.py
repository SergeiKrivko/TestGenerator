from PyQt6.QtCore import QThread

from backend.backend_manager import BackendManager
from side_tabs.chat import gpt


class GPTUnitTestGenerator(QThread):
    def __init__(self, bm: BackendManager):
        super().__init__()
        self.bm = bm
        self.sm = bm.sm
        self.project = self.sm.project

    def run(self):
        print('RUN\n')
        resp = gpt.try_response([
            {'role': 'system', 'content': f"Ты пишешь модульные тесты для функций на языке "
                                          f"{self.project.get('language')}, используя Check."},
            {'role': 'system', 'content': f"Необходимо написать тесты для функции "
                                          f"{self.project.get('language')}, используя Check."},
            {'role': 'user',
             'content': "Составь классы эквивалентности функциональных тестов этой программы.\n"
                        "Выдай ответ в виде списка классов эквивалентности без пояснений"
             }], temperature=0)
        print(resp)

