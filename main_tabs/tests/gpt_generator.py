from PyQt6.QtCore import QThread, pyqtSignal

from backend.backend_manager import BackendManager
from side_tabs.chat import gpt


class GPTTestGenerator(QThread):
    progressChanged = pyqtSignal(int, int)

    def __init__(self, bm: BackendManager):
        super().__init__()
        self.bm = bm
        self.sm = bm.sm
        self.project = self.sm.project

    def run(self):
        print('RUN\n')
        resp = gpt.try_response([
            {'role': 'system', 'content': f"Ты пишешь программу на {self.project.get('language')}, которая должна\n"
                                          f"```\n{self.project.get_data('description')}\n```"},
            {'role': 'user',
             'content': "Составь классы эквивалентности функциональных тестов этой программы.\n"
                        "Выдай ответ в виде списка классов эквивалентности без пояснений"
             }], temperature=0)
        print(resp)
        classes = []
        for line in resp.split('\n'):
            if line.lstrip(' 1234567890').startswith('.') and not line.startswith('.'):
                classes.append(line.lstrip(' 1234567890').lstrip('.').strip())

        classes_text = '\n'.join(f'{i + 1}. {test_class}' for i, test_class in enumerate(classes))
        resp = gpt.try_response([
            {'role': 'system', 'content': f"Ты пишешь программу на {self.project.get('language')}, которая должна\n"
                                          f"```\n{self.project.get_data('description')}\n```"},
            {'role': 'system', 'content': f"Необходимо провести функциональное тестирование программы. Были выделены"
                                          f"следующие классы эквивалентности:\n{classes_text}\n"},
            {'role': 'user',
             'content': "Чего не хватает? Выдай ответ в виде списка недостающих классов "
                        "эквивалентности без пояснений"
             }], temperature=0)
        print(resp)
        for line in resp.split('\n'):
            if line.lstrip(' 1234567890').startswith('.') and not line.startswith('.'):
                classes.append(line.lstrip(' 1234567890').lstrip('.').strip())
        self.progressChanged.emit(3, len(classes) + 3)

        for i, test_class in enumerate(classes):
            print(test_class)
            test_type = gpt.try_response([
                {'role': 'system', 'content': f"Ты пишешь программу на {self.project.get('language')}, которая должна\n"
                                              f"```\n{self.project.get_data('description')}\n```"},
                {'role': 'user',
                 'content': f"Тест \"{test_class}\" является позитивным или негативным?. В ответ напиши только "
                            f"одно слово - \"Позитивный\" или \"Негативный\""
                 }], handler=GPTTestGenerator._get_test_type, temperature=0)

            resp = gpt.try_response([
                {'role': 'system', 'content': f"Ты пишешь программу на {self.project.get('language')}, которая должна\n"
                                              f"```\n{self.project.get_data('description')}\n```"},
                {'role': 'user',
                 'content': f"Придумай входные и выходные данные для теста \"{test_class}\". В ответ напиши только "
                            f"входные и выходные данные на разных строках, без пояснений"
                 }], temperature=0)
            self.create_test(test_class, resp, test_type)
            print(resp)
            self.progressChanged.emit(4 + i, len(classes) + 3)

    def create_test(self, desc, text: str, test_type: str):
        test = None
        status = 0
        for line in text.split('\n'):
            if line.strip('* ') == 'Входные данные:':
                test = self.bm.new_func_test(test_type)
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

    @staticmethod
    def _get_test_type(text):
        if 'позитив' in text.strip().lower() and 'негатив' in text.strip().lower():
            raise RuntimeError
        if 'позитив' in text.strip().lower():
            return 'pos'
        elif 'негатив' in text.strip().lower():
            return 'neg'
        else:
            raise RuntimeError

