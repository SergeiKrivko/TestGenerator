class CodeAutocompletionManager:
    def __init__(self, sm, directory):
        self._sm = sm
        self.dir = directory
        self.text = ''

    def update_libs(self):
        pass

    def full_update(self, text, current_pos):
        pass

    def get(self, text: str, current_pos):
        return [], 0
