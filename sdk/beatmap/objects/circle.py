from typing import Optional, Dict, Any
from .base import HitObject, HitSound


class Circle(HitObject):
    """
    Represents a circle hit object (normal hit circle).
    Used in Standard, Taiko (converted to don/katsu), and Catch modes.
    """
    
    def __init__(self, start_time: int, x: int = 0, y: int = 0,
                 hit_sound: HitSound = HitSound.NORMAL,
                 extras: Optional[Dict[str, Any]] = None):
        """
        Initialize circle hit object.
        
        Args:
            start_time: Start time in milliseconds
            x: X position (0-512)
            y: Y position (0-384)
            hit_sound: Hit sound flags
            extras: Additional properties
        """
        super().__init__(start_time, x, y, hit_sound, extras)
    
    def clone(self) -> 'Circle':
        """Create a copy of this circle."""
        return Circle(
            start_time=self.start_time,
            x=self.x,
            y=self.y,
            hit_sound=self.hit_sound,
            extras=self.extras.copy() if self.extras else None
        )
    
    def __str__(self) -> str:
        return f"Circle(start_time={self.start_time}, x={self.x}, y={self.y}, hit_sound={self.hit_sound})"
