from PyQt6.QtCore import QThread

from backend.backend_manager import BackendManager
from side_tabs.chat import gpt


class GPTTestGenerator(QThread):
    def __init__(self, bm: BackendManager):
        super().__init__()
        self.bm = bm
        self.sm = bm.sm
        self.project = self.sm.project

    def run(self):
        print('RUN\n')
        resp = gpt.simple_response([
            {'role': 'system', 'content': f"Ты пишешь программу на {self.project.get('language')}, которая должна\n"
                                          f"```\n{self.project.get_data('description')}\n```"},
            {'role': 'user',
             'content': "Составь классы эквивалентности позитивных функциональных тестов этой программы.\n"
                        "Выдай ответ в виде списка классов эквивалентности без пояснений"
             }], temperature=0)
        print(resp)
        classes = []
        for line in resp.split('\n'):
            if line.lstrip(' 1234567890').startswith('.') and not line.startswith('.'):
                classes.append(line.lstrip(' 1234567890').lstrip('.').strip())

        for test_class in classes:
            print(test_class)
            resp = gpt.simple_response([
                {'role': 'system', 'content': f"Ты пишешь программу на {self.project.get('language')}, которая должна\n"
                                              f"```\n{self.project.get_data('description')}\n```"},
                {'role': 'user',
                 'content': f"Придумай входные и выходные данные для теста \"{test_class}\". В ответ напиши только "
                            f"входные и выходные данные на разных строках, без пояснений"
                 }], temperature=0)
            self.create_test(test_class, resp)
            print(resp)

    def create_test(self, desc, text: str):
        test = None
        status = 0
        for line in text.split('\n'):
            if line.strip('* ') == 'Входные данные:':
                test = self.bm.new_func_test('pos')
                test['desc'] = desc
                test['in'] = ''
                test['out'] = ''
                status = 1
            elif line.strip('* ') == 'Выходные данные:' and test:
                status = 2
            elif status == 1 and line.strip() != '```':
                test['in'] += line + '\n'
            elif status == 2 and line.strip() != '```':
                test['out'] += line + '\n'
