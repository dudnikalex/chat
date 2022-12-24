import json
import re
import time


camel_case_re = re.compile(r"(?<!^)(?=[A-Z])")


class Message:
    def __init__(self):
        name = self.__class__.__name__.lower()
        self.type = camel_case_re.sub("_", name).lower()

    def as_string(self):
        data = self.__dict__
        data["timestamp"] = time.time()

        return json.dumps(data)

    def __str__(self):
        return self.as_string()


class NewConversation(Message):
    def __init__(self):
        super().__init__()


class ConnectedMessage(Message):
    def __init__(self):
        super().__init__()


connected = ConnectedMessage()


class Text(Message):
    def __init__(self, text=""):
        super().__init__()
        self.text = text


class Disconnect(Message):
    def __init__(self):
        super().__init__()


disconnect = Disconnect()