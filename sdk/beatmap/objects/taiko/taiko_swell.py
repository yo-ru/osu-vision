from typing import Optional, Dict, Any, List
from ..base import HitObject, HitSound


class TaikoSwell(HitObject):
    """
    Represents a taiko swell/denden (converted from spinner).
    """
    
    def __init__(self, start_time: int, end_time: int,
                 hit_sound: HitSound = HitSound.NORMAL,
                 extras: Optional[Dict[str, Any]] = None):
        """
        Initialize taiko swell.
        
        Args:
            start_time: Start time in milliseconds
            end_time: End time in milliseconds
            hit_sound: Hit sound flags
            extras: Additional properties
        """
        super().__init__(start_time, 256, 192, hit_sound, extras)
        self._end_time = end_time
    
    @property
    def end_time(self) -> int:
        """End time of the swell."""
        return self._end_time
    
    @end_time.setter
    def end_time(self, value: int):
        self._end_time = value
    
    def clone(self) -> 'TaikoSwell':
        """Create a copy of this taiko swell."""
        return TaikoSwell(
            start_time=self.start_time,
            end_time=self.end_time,
            hit_sound=self.hit_sound,
            extras=self.extras.copy() if self.extras else None
        )
    
    def __str__(self) -> str:
        return f"TaikoSwell(start_time={self.start_time}, end_time={self.end_time}, duration={self.duration}ms)"
