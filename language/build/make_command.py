class MakeCommand:
    def __init__(self, name: str, dependencies: list[str] | str, commands: list[str] | str):
        self.name = name
        self.dependencies = dependencies if isinstance(dependencies, list) else [dependencies]
        self.commands = commands if isinstance(commands, list) else [commands]

