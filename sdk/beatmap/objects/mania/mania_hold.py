from typing import Optional, Dict, Any
from ..base import HitObject, HitSound


class ManiaHold(HitObject):
    """
    Represents a mania hold object (long note).
    """
    
    def __init__(self, start_time: int, end_time: int, column: int, key_count: int = 7,
                 hit_sound: HitSound = HitSound.NORMAL,
                 extras: Optional[Dict[str, Any]] = None):
        """
        Initialize mania hold.
        
        Args:
            start_time: Start time in milliseconds
            end_time: End time in milliseconds
            column: Column index (0-based)
            key_count: Total number of keys/columns
            hit_sound: Hit sound flags
            extras: Additional properties
        """
        # Calculate x position based on column
        x = int((column + 0.5) * (512 / key_count))
        super().__init__(start_time, x, 192, hit_sound, extras)
        self._end_time = end_time
        self.column = column
        self.key_count = key_count
    
    @property
    def end_time(self) -> int:
        """End time of the hold note."""
        return self._end_time
    
    @end_time.setter
    def end_time(self, value: int):
        self._end_time = value
    
    def clone(self) -> 'ManiaHold':
        """Create a copy of this mania hold."""
        return ManiaHold(
            start_time=self.start_time,
            end_time=self.end_time,
            column=self.column,
            key_count=self.key_count,
            hit_sound=self.hit_sound,
            extras=self.extras.copy() if self.extras else None
        )
    
    def __str__(self) -> str:
        return f"ManiaHold(start_time={self.start_time}, end_time={self.end_time}, column={self.column}/{self.key_count}, duration={self.duration}ms)"
