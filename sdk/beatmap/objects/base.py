from abc import ABC, abstractmethod
from enum import IntFlag
from typing import Optional, Dict, Any


class HitSound(IntFlag):
    """Hit sound flags as defined in osu!."""
    NONE = 0
    NORMAL = 1
    WHISTLE = 2
    FINISH = 4
    CLAP = 8


class HitObject(ABC):
    """
    Base class for all hit objects.
    """
    
    def __init__(self, start_time: int, x: int = 0, y: int = 0, 
                 hit_sound: HitSound = HitSound.NORMAL, 
                 extras: Optional[Dict[str, Any]] = None):
        """
        Initialize base hit object.
        
        Args:
            start_time: Start time in milliseconds
            x: X position (0-512)
            y: Y position (0-384) 
            hit_sound: Hit sound flags
            extras: Additional properties
        """
        self.start_time = start_time
        self.x = x
        self.y = y
        self.hit_sound = hit_sound
        self.extras = extras or {}
        
        # Game mode specific properties
        self._taiko_hits_required: Optional[int] = None
        self._taiko_ticks: Optional[list] = None
        self._mania_column: Optional[int] = None
    
    @property
    def end_time(self) -> int:
        """End time of the hit object. Override in derived classes."""
        return self.start_time
    
    @property
    def duration(self) -> int:
        """Duration of the hit object in milliseconds."""
        return self.end_time - self.start_time
    
    # Taiko-specific properties
    @property
    def taiko_hits_required(self) -> Optional[int]:
        """Number of hits required for taiko spinners."""
        return self._taiko_hits_required
    
    @taiko_hits_required.setter
    def taiko_hits_required(self, value: int):
        self._taiko_hits_required = value
    
    @property
    def taiko_ticks(self) -> Optional[list]:
        """Tick times for taiko drumrolls."""
        return self._taiko_ticks
    
    @taiko_ticks.setter  
    def taiko_ticks(self, value: list):
        self._taiko_ticks = value
    
    # Mania-specific properties
    @property
    def mania_column(self) -> Optional[int]:
        """Column index for mania notes."""
        return self._mania_column
    
    @mania_column.setter
    def mania_column(self, value: int):
        self._mania_column = value
    
    @abstractmethod
    def clone(self) -> 'HitObject':
        """Create a copy of this hit object."""
        pass
    
    def __str__(self) -> str:
        return f"{self.__class__.__name__}(start_time={self.start_time}, x={self.x}, y={self.y})"
    
    def __repr__(self) -> str:
        return self.__str__()
