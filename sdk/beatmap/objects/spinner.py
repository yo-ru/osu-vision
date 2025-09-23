from typing import Optional, Dict, Any
from .base import HitObject, HitSound


class Spinner(HitObject):
    """
    Represents a spinner hit object.
    Behavior varies by game mode:
    - Standard: Cursor spinning around center
    - Taiko: Alternating don/katsu hits (denden)
    - Catch: Spinner catching
    - Mania: Not used
    """
    
    def __init__(self, start_time: int, end_time: int, x: int = 256, y: int = 192,
                 hit_sound: HitSound = HitSound.NORMAL,
                 extras: Optional[Dict[str, Any]] = None):
        """
        Initialize spinner hit object.
        
        Args:
            start_time: Start time in milliseconds
            end_time: End time in milliseconds
            x: X position (usually center: 256)
            y: Y position (usually center: 192)
            hit_sound: Hit sound flags
            extras: Additional properties
        """
        super().__init__(start_time, x, y, hit_sound, extras)
        self._end_time = end_time
    
    @property
    def end_time(self) -> int:
        """End time of the spinner."""
        return self._end_time
    
    @end_time.setter
    def end_time(self, value: int):
        self._end_time = value
    
    def clone(self) -> 'Spinner':
        """Create a copy of this spinner."""
        spinner = Spinner(
            start_time=self.start_time,
            end_time=self.end_time,
            x=self.x,
            y=self.y,
            hit_sound=self.hit_sound,
            extras=self.extras.copy() if self.extras else None
        )
        spinner.taiko_hits_required = self.taiko_hits_required
        return spinner
    
    def __str__(self) -> str:
        return f"Spinner(start_time={self.start_time}, end_time={self.end_time}, duration={self.duration}ms)"
