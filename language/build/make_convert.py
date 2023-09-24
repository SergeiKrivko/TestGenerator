class MakeConverter:
    def __init__(self, sm, tm):
        self.tm = tm
        self.sm = sm
        self.src_path = f"{sm.data_lab_path()}/scenarios/make"
        self.dst_path = sm.lab_path()

        self.commands = dict()

    def add_scenario(self, scenario: dict):
        if scenario['type'] == 0:

