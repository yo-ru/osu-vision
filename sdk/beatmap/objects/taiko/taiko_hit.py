from typing import Optional, Dict, Any
from ..base import HitObject, HitSound


class TaikoHit(HitObject):
    """
    Represents a taiko hit object (don or katsu).
    """
    
    def __init__(self, start_time: int, is_katsu: bool = False, is_large: bool = False,
                 hit_sound: HitSound = HitSound.NORMAL,
                 extras: Optional[Dict[str, Any]] = None):
        """
        Initialize taiko hit.
        
        Args:
            start_time: Start time in milliseconds
            is_katsu: True for katsu (blue), False for don (red)
            is_large: True for large hit (both hands)
            hit_sound: Hit sound flags
            extras: Additional properties
        """
        super().__init__(start_time, 256, 192, hit_sound, extras)
        self.is_katsu = is_katsu
        self.is_large = is_large
    
    @property
    def is_don(self) -> bool:
        """True if this is a don (red) hit."""
        return not self.is_katsu
    
    def clone(self) -> 'TaikoHit':
        """Create a copy of this taiko hit."""
        return TaikoHit(
            start_time=self.start_time,
            is_katsu=self.is_katsu,
            is_large=self.is_large,
            hit_sound=self.hit_sound,
            extras=self.extras.copy() if self.extras else None
        )
    
    def __str__(self) -> str:
        hit_type = "Katsu" if self.is_katsu else "Don"
        size = "Large" if self.is_large else "Normal"
        return f"TaikoHit(start_time={self.start_time}, type={hit_type}, size={size})"
