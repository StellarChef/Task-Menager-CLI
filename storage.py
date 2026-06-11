import json
import pydantic
from model import *


class Storage:
    def __init__(self, path: str):
        self.path = path

    def load(self):
        with open(self) as s:
            content = s.read(self.path)
            collection = TaskListCollection.model_validate_json(content)
        return collection

    def save(self, collection: TaskListCollection):
        with open(self.path, "w", encoding="utf-8") as s:
            s.write(collection.model_dump_json())
