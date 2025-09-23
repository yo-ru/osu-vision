from enum import IntEnum, IntFlag
from typing import Optional, List, Dict, Any, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from ..constants import GameMode


class HitObjectType(IntEnum):
    """Hit object types as defined in osu!."""
    NORMAL = 1
    SLIDER = 2
    NEW_COMBO = 4
    SPINNER = 8
    NORMALNEWCOMBO = 5  # NORMAL | NEW_COMBO
    SLIDERNEWCOMBO = 6  # SLIDER | NEW_COMBO


class HitSound(IntFlag):
    """Hit sound flags as defined in osu!."""
    NORMAL = 0
    WHISTLE = 2
    FINISH = 4
    CLAP = 8


class TimingPoint:
    """Represents a timing point in the beatmap."""
    
    def __init__(self, time: int, beat_length: float, meter: int = 4, 
                 sample_set: int = 1, sample_index: int = 1, 
                 volume: int = 100, uninherited: bool = True, 
                 effects: int = 0):
        self.time = time
        self.beat_length = beat_length
        self.meter = meter
        self.sample_set = sample_set
        self.sample_index = sample_index
        self.volume = volume
        self.uninherited = uninherited
        self.effects = effects
    
    @property
    def bpm(self) -> float:
        """Calculate BPM from beat length."""
        if self.beat_length > 0:
            return 60000 / self.beat_length
        return 0.0


class HitObject:
    """Represents a hit object in the beatmap."""
    
    def __init__(self, x: int, y: int, time: int, type: HitObjectType, 
                 hit_sound: int, object_params: Dict[str, Any] = None,
                 end_time: Optional[int] = None, slider_type: Optional[str] = None,
                 curve_points: Optional[List[Tuple[int, int]]] = None,
                 repeats: Optional[int] = None, pixel_length: Optional[float] = None,
                 rotation_requirement: Optional[float] = None, hits_required: Optional[int] = None,
                 slider_velocity: Optional[float] = None, drumroll_ticks: Optional[List[int]] = None):
        self.x = x
        self.y = y
        self.time = time
        self.type = type
        self.hit_sound = hit_sound
        self.object_params = object_params or {}
        self.end_time = end_time
        self.slider_type = slider_type
        self.curve_points = curve_points or []
        self.repeats = repeats or 1
        self.pixel_length = pixel_length
        self.rotation_requirement = rotation_requirement  # For standard osu! mode
        self.hits_required = hits_required  # For taiko spinner mode
        self.slider_velocity = slider_velocity  # Slider velocity multiplier
        self.drumroll_ticks = drumroll_ticks or []  # Pre-calculated tick times for taiko drumrolls


class Metadata:
    """Represents beatmap metadata."""
    
    def __init__(self, title: str = "", artist: str = "", version: str = "",
                 mode: "GameMode" = None, file_format_version: int = 14,
                 stack_leniency: float = 0.7):
        self.title = title
        self.artist = artist
        self.version = version
        self.mode = mode
        self.file_format_version = file_format_version
        self.stack_leniency = stack_leniency


class BeatmapDifficulty:
    """Represents beatmap difficulty settings."""
    
    def __init__(self, hp: float = 5.0, cs: float = 5.0, od: float = 5.0, 
                 ar: float = 5.0, slider_multiplier: float = 1.0, 
                 slider_tick_rate: float = 1.0):
        self.hp = hp
        self.cs = cs
        self.od = od
        self.ar = ar
        self.slider_multiplier = slider_multiplier
        self.slider_tick_rate = slider_tick_rate
