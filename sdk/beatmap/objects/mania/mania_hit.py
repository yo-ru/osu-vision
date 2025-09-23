from typing import Optional, Dict, Any
from ..base import HitObject, HitSound


class ManiaHit(HitObject):
    """
    Represents a mania hit object (single note).
    """
    
    def __init__(self, start_time: int, column: int, key_count: int = 7,
                 hit_sound: HitSound = HitSound.NORMAL,
                 extras: Optional[Dict[str, Any]] = None):
        """
        Initialize mania hit.
        
        Args:
            start_time: Start time in milliseconds
            column: Column index (0-based)
            key_count: Total number of keys/columns
            hit_sound: Hit sound flags
            extras: Additional properties
        """
        # Calculate x position based on column
        x = int((column + 0.5) * (512 / key_count))
        super().__init__(start_time, x, 192, hit_sound, extras)
        self.column = column
        self.key_count = key_count
    
    def clone(self) -> 'ManiaHit':
        """Create a copy of this mania hit."""
        return ManiaHit(
            start_time=self.start_time,
            column=self.column,
            key_count=self.key_count,
            hit_sound=self.hit_sound,
            extras=self.extras.copy() if self.extras else None
        )
    
    def __str__(self) -> str:
        return f"ManiaHit(start_time={self.start_time}, column={self.column}/{self.key_count})"
