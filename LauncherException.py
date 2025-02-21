class LauncherException(Exception):
    def __init__(self, *args: object, info:str) -> None:
        super().__init__(*args)
        self.info=info