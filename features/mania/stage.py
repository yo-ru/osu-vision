from typing import List, Tuple, Optional

class Stage:
    """Represents a single stage/column in the mania playfield"""

    def __init__(self):
        self.notes: List[int] = []  # list of regular note timestamps (ms)
        self.holds: List[Tuple[int, int]] = []  # list of (start_time, end_time) tuples for LNs

    def add_note(self, timestamp: int):
        """Add a regular note to this stage"""
        self.notes.append(timestamp)
        self.notes.sort()

    def add_hold(self, start_time: int, end_time: int):
        """Add a long note (hold) to this stage"""
        self.holds.append((start_time, end_time))
        self.holds.sort(key=lambda x: x[0])

    def get_notes(self) -> List[int]:
        return self.notes.copy()

    def get_holds(self) -> List[Tuple[int, int]]:
        return self.holds.copy()

    def clear_objects(self):
        self.notes.clear()
        self.holds.clear()

    def get_object_count(self) -> int:
        return len(self.notes) + len(self.holds)