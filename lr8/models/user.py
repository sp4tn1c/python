class User:
    def __init__(self, user_id: int, name: str):
        self.user_id = user_id
        self.name = name

    @property
    def id(self):
        return self.user_id

    @property
    def username(self):
        return self.name
