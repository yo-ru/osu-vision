from typing import Optional, Dict, Any, List, Tuple
from .base import HitObject, HitSound


class SliderPath:
    """Represents a slider's path with curve points."""
    
    def __init__(self, curve_type: str = "L", curve_points: Optional[List[Tuple[int, int]]] = None):
        self.curve_type = curve_type  # L=Linear, P=Perfect, B=Bezier, C=Catmull
        self.curve_points = curve_points or []
    
    def __str__(self) -> str:
        return f"SliderPath(type={self.curve_type}, points={len(self.curve_points)})"


class Slider(HitObject):
    """
    Represents a slider hit object.
    Behavior varies by game mode:
    - Standard: Follow slider path
    - Taiko: Drumroll (continuous hitting)
    - Catch: Juice stream
    - Mania: Hold note
    """
    
    def __init__(self, start_time: int, x: int = 0, y: int = 0,
                 hit_sound: HitSound = HitSound.NORMAL,
                 slider_path: Optional[SliderPath] = None,
                 repeats: int = 1, pixel_length: float = 0.0,
                 extras: Optional[Dict[str, Any]] = None):
        """
        Initialize slider hit object.
        
        Args:
            start_time: Start time in milliseconds
            x: X position (0-512)
            y: Y position (0-384)
            hit_sound: Hit sound flags
            slider_path: Path information
            repeats: Number of repeats (1 = no repeat)
            pixel_length: Length in pixels
            extras: Additional properties
        """
        super().__init__(start_time, x, y, hit_sound, extras)
        self.slider_path = slider_path or SliderPath()
        self.repeats = repeats
        self.pixel_length = pixel_length
        self._end_time: Optional[int] = None
        self.slider_velocity = 1.0
    
    @property
    def end_time(self) -> int:
        """End time of the slider."""
        return self._end_time or self.start_time
    
    @end_time.setter
    def end_time(self, value: int):
        self._end_time = value
    
    def clone(self) -> 'Slider':
        """Create a copy of this slider."""
        slider = Slider(
            start_time=self.start_time,
            x=self.x,
            y=self.y,
            hit_sound=self.hit_sound,
            slider_path=SliderPath(self.slider_path.curve_type, self.slider_path.curve_points.copy()),
            repeats=self.repeats,
            pixel_length=self.pixel_length,
            extras=self.extras.copy() if self.extras else None
        )
        slider.end_time = self.end_time
        slider.slider_velocity = self.slider_velocity
        slider.taiko_ticks = self.taiko_ticks.copy() if self.taiko_ticks else None
        return slider
    
    def __str__(self) -> str:
        return f"Slider(start_time={self.start_time}, end_time={self.end_time}, repeats={self.repeats}, length={self.pixel_length})"
