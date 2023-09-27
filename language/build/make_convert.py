from language.build.make_command import MakeCommand
from language.languages import languages


class MakeConverter:
    def __init__(self, sm):
        self.sm = sm
        self.src_path = f"{sm.data_lab_path()}/scenarios/make"
        self.dst_path = sm.lab_path()

        self.commands = dict()

    def add_scenario(self, scenario: dict):
        if scenario['type'] == 0:
            if 'to_make' in languages[scenario['language']]:
                for el in languages[scenario['language']]['to_make'](self.sm, scenario):
                    if el.name not in self.commands:
                        self.commands[el.name] = el
        elif scenario['type'] == 1:
            self.commands[scenario['name']] = MakeCommand(scenario['name'],
                                                          [el['data']['name'] for el in scenario['dependencies']],
                                                          [el['data'] for el in scenario['commands']])

    def add_scenarios(self, *args: dict):
        for el in args:
            self.add_scenario(el)

    def _convert(self):
        with open(f"{self.dst_path}/makefile2.txt", 'w', encoding='utf-8') as f:
            for command in self.commands.values():
                f.write(f"{command.name}: {' '.join(command.dependencies)}\n\t")
                f.write('\n\t'.join(command.commands))
                f.write('\n\n')

    def run(self):
        self._convert()

