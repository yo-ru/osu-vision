from typing import Optional, Dict, Any
from ..base import HitObject, HitSound


class CatchBanana(HitObject):
    """
    Represents a catch banana (spinner fruit).
    """
    
    def __init__(self, start_time: int, x: int = 0,
                 hit_sound: HitSound = HitSound.NORMAL,
                 extras: Optional[Dict[str, Any]] = None):
        """
        Initialize catch banana.
        
        Args:
            start_time: Start time in milliseconds
            x: X position (0-512)
            hit_sound: Hit sound flags
            extras: Additional properties
        """
        super().__init__(start_time, x, 0, hit_sound, extras)
    
    def clone(self) -> 'CatchBanana':
        """Create a copy of this catch banana."""
        return CatchBanana(
            start_time=self.start_time,
            x=self.x,
            hit_sound=self.hit_sound,
            extras=self.extras.copy() if self.extras else None
        )
    
    def __str__(self) -> str:
        return f"CatchBanana(start_time={self.start_time}, x={self.x})"
