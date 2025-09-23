from enum import IntEnum
from typing import List

class TaikoManiaObjectType(IntEnum):
    DON = 0
    KATSU = 1

class Stage:
    """Represents a single stage/line in the playfield"""

    def __init__(self, type: TaikoManiaObjectType):
        self.type: TaikoManiaObjectType = type
        self.objects: List[int] = [] # list of object timestamps (ms)

    def add_object(self, timestamp: int):
        self.objects.append(timestamp)
        self.objects.sort()

    def get_objects(self) -> List[int]:
        return self.objects.copy()

    def get_type(self) -> TaikoManiaObjectType:
        return self.type

    def set_type(self, value: TaikoManiaObjectType):
        self.type = value

    def clear_objects(self):
        self.objects.clear()

    def get_object_count(self) -> int:
        return len(self.objects)