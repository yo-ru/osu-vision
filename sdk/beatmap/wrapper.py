import os
from typing import Optional, List, Dict, Any
from pathlib import Path

from slider.beatmap import Beatmap as SliderBeatmap


from .types import TimingPoint, Metadata, BeatmapDifficulty
from .objects import (
    HitObject, HitSound, Circle, Slider, Spinner,
    TaikoHit, TaikoDrumroll, TaikoSwell,
    CatchHit, CatchDroplet, CatchBanana,
    ManiaHit, ManiaHold
)
from .objects.slider import SliderPath
from ..constants.gamemodes import GameMode
from ..constants.mods import Mods


class Beatmap:
    """
    Wrapper around slider's Beatmap class
    """
    
    def __init__(self, slider_beatmap: SliderBeatmap):
        """Initialize with a slider Beatmap instance."""
        self._beatmap = slider_beatmap
        self._metadata = None
        self._difficulty = None
        self._hit_objects = None
        self._timing_points = None
    
    @classmethod
    def from_path(cls, path: str) -> 'Beatmap':
        """
        Load a beatmap from a file path.
        
        Args:
            path: Path to the .osu file
            
        Returns:
            Beatmap instance
        """
        if not os.path.exists(path):
            raise FileNotFoundError(f"Beatmap file not found: {path}")
        
        slider_beatmap = SliderBeatmap.from_path(path)
        return cls(slider_beatmap)
    
    @classmethod
    def from_string(cls, content: str) -> 'Beatmap':
        """
        Load a beatmap from a string content.
        
        Args:
            content: Beatmap file content as string
            
        Returns:
            Beatmap instance
        """
        slider_beatmap = SliderBeatmap.from_string(content)
        return cls(slider_beatmap)
    
    @property
    def metadata(self) -> Metadata:
        """Get beatmap metadata."""
        if self._metadata is None:
            # Slider library stores metadata directly on the beatmap object
            self._metadata = Metadata(
                title=self._beatmap.title,
                artist=self._beatmap.artist,
                version=self._beatmap.version,
                mode=GameMode(self._beatmap.mode) if self._beatmap.mode is not None else GameMode.STANDARD,
                file_format_version=self._beatmap.format_version,
                stack_leniency=self._beatmap.stack_leniency
            )
        return self._metadata
    
    @property
    def difficulty(self) -> BeatmapDifficulty:
        """Get beatmap difficulty settings."""
        if self._difficulty is None:
            # Slider library stores difficulty settings directly on the beatmap object
            self._difficulty = BeatmapDifficulty(
                hp=self._beatmap.hp_drain_rate,
                cs=self._beatmap.circle_size,
                od=self._beatmap.overall_difficulty,
                ar=self._beatmap.approach_rate,
                slider_multiplier=self._beatmap.slider_multiplier,
                slider_tick_rate=self._beatmap.slider_tick_rate
            )
        return self._difficulty
    
    @property
    def hit_objects(self) -> List[HitObject]:
        """Get list of hit objects with proper mode-specific types."""
        if self._hit_objects is None:
            self._hit_objects = []
            for slider_obj in self._beatmap.hit_objects():
                hit_obj = self._convert_hit_object(slider_obj)
                if hit_obj:
                    self._hit_objects.append(hit_obj)
        return self._hit_objects
    
    def _convert_hit_object(self, slider_obj) -> Optional[HitObject]:
        """Convert slider hit object to proper mode-specific hit object."""
        # Handle time conversion
        start_time = int(slider_obj.time.total_seconds() * 1000)
        
        # Handle position
        x = int(slider_obj.position.x) if hasattr(slider_obj, 'position') else 0
        y = int(slider_obj.position.y) if hasattr(slider_obj, 'position') else 0
        
        # Handle hit sound
        hit_sound = HitSound(slider_obj.hitsound) if hasattr(slider_obj, 'hitsound') else HitSound.NORMAL
        
        # Get end time if available
        end_time = None
        if hasattr(slider_obj, 'end_time') and slider_obj.end_time:
            end_time = int(slider_obj.end_time.total_seconds() * 1000)
        elif hasattr(slider_obj, 'endTime') and slider_obj.endTime:
            # Alternative attribute name
            end_time = int(slider_obj.endTime.total_seconds() * 1000)
        
        # Determine object type
        if not hasattr(slider_obj, 'type_code'):
            return None
            
        type_code = slider_obj.type_code
        
        # Convert based on game mode and object type
        if self.metadata.mode == GameMode.TAIKO:
            return self._convert_to_taiko(slider_obj, start_time, end_time, hit_sound, type_code)
        elif self.metadata.mode == GameMode.CATCH:
            return self._convert_to_catch(slider_obj, start_time, end_time, x, hit_sound, type_code)
        elif self.metadata.mode == GameMode.MANIA:
            return self._convert_to_mania(slider_obj, start_time, end_time, x, hit_sound, type_code)
        else:  # Standard mode
            return self._convert_to_standard(slider_obj, start_time, end_time, x, y, hit_sound, type_code)
    
    def _convert_to_taiko(self, slider_obj, start_time: int, end_time: Optional[int], 
                         hit_sound: HitSound, type_code: int) -> Optional[HitObject]:
        """Convert to taiko-specific objects."""
        if type_code & 8:  # Spinner -> TaikoSwell
            if not end_time:
                return None
            return TaikoSwell(start_time, end_time, hit_sound)
            
        elif type_code & 2:  # Slider -> TaikoDrumroll
            if not end_time:
                return None
            return TaikoDrumroll(start_time, end_time, hit_sound)
            
        else:  # Circle -> TaikoHit
            is_katsu = bool(hit_sound & (HitSound.WHISTLE | HitSound.CLAP))
            is_large = bool(hit_sound & HitSound.FINISH)
            return TaikoHit(start_time, is_katsu, is_large, hit_sound)
    
    def _convert_to_catch(self, slider_obj, start_time: int, end_time: Optional[int],
                         x: int, hit_sound: HitSound, type_code: int) -> Optional[HitObject]:
        """Convert to catch-specific objects."""
        if type_code & 8:  # Spinner -> CatchBanana
            return CatchBanana(start_time, x, hit_sound)
        elif type_code & 2:  # Slider -> CatchDroplet (simplified)
            return CatchDroplet(start_time, x, hit_sound)
        else:  # Circle -> CatchHit
            return CatchHit(start_time, x, hit_sound)
    
    def _convert_to_mania(self, slider_obj, start_time: int, end_time: Optional[int],
                         x: int, hit_sound: HitSound, type_code: int) -> Optional[HitObject]:
        """Convert to mania-specific objects."""
        # Calculate column from x position (assuming 7K for now)
        key_count = 7
        column = min(int(x / (512 / key_count)), key_count - 1)
        
        if type_code & 2 and end_time:  # Slider -> ManiaHold
            return ManiaHold(start_time, end_time, column, key_count, hit_sound)
        else:  # Circle -> ManiaHit (spinners don't exist in mania)
            return ManiaHit(start_time, column, key_count, hit_sound)
    
    def _convert_to_standard(self, slider_obj, start_time: int, end_time: Optional[int],
                            x: int, y: int, hit_sound: HitSound, type_code: int) -> Optional[HitObject]:
        """Convert to standard osu! objects."""
        if type_code & 8:  # Spinner
            if not end_time:
                return None
            return Spinner(start_time, end_time, x, y, hit_sound)
            
        elif type_code & 2:  # Slider
            if not end_time:
                return None
            # Create slider path
            curve_type = getattr(slider_obj, 'curve_type', 'L')
            curve_points = getattr(slider_obj, 'curve_points', [])
            slider_path = SliderPath(curve_type, curve_points)
            
            repeats = getattr(slider_obj, 'repeat', 1)
            pixel_length = getattr(slider_obj, 'length', 0.0)
            
            slider = Slider(start_time, x, y, hit_sound, slider_path, repeats, pixel_length)
            slider.end_time = end_time
            return slider
            
        else:  # Circle
            return Circle(start_time, x, y, hit_sound)
    
    @property
    def timing_points(self) -> List[TimingPoint]:
        """Get list of timing points."""
        if self._timing_points is None:
            self._timing_points = []
            for slider_tp in self._beatmap.timing_points:
                # Handle time conversion (slider uses timedelta offset, we need milliseconds)
                time_ms = int(slider_tp.offset.total_seconds() * 1000)
                
                timing_point = TimingPoint(
                    time=time_ms,
                    beat_length=getattr(slider_tp, 'ms_per_beat', 500.0),
                    meter=getattr(slider_tp, 'meter', 4),
                    sample_set=getattr(slider_tp, 'sample_set', 1),
                    sample_index=getattr(slider_tp, 'sample_type', 1),
                    volume=getattr(slider_tp, 'volume', 100),
                    uninherited=getattr(slider_tp, 'kiai_mode', False),  # This might be wrong, need to check
                    effects=0  # Default for now
                )
                self._timing_points.append(timing_point)
        return self._timing_points
    
    @property
    def bpm(self) -> float:
        """Get the base BPM of the beatmap."""
        # Find the first uninherited timing point for BPM
        for tp in self.timing_points:
            if tp.uninherited and tp.beat_length > 0:
                return tp.bpm
        return 0.0
    
    @property
    def beat_divisor(self) -> int:
        """Beat division for placing objects."""
        return getattr(self._beatmap, 'beat_divisor', 4)
    
    @property
    def audio_filename(self) -> str:
        """The location of the audio file."""
        return getattr(self._beatmap, 'audio_filename', '')
    
    @property
    def audio_lead_in(self) -> int:
        """Audio lead in time in milliseconds."""
        lead_in = getattr(self._beatmap, 'audio_lead_in', None)
        if lead_in and hasattr(lead_in, 'total_seconds'):
            return int(lead_in.total_seconds() * 1000)
        return 0
    
    @property
    def preview_time(self) -> int:
        """Preview time in milliseconds."""
        preview = getattr(self._beatmap, 'preview_time', None)
        if preview and hasattr(preview, 'total_seconds'):
            return int(preview.total_seconds() * 1000)
        return -1
    
    @property
    def countdown(self) -> bool:
        """Should countdown be displayed."""
        return getattr(self._beatmap, 'countdown', True)
    
    @property
    def sample_set(self) -> str:
        """Default sample set."""
        return getattr(self._beatmap, 'sample_set', 'Normal')
    
    @property
    def letterbox_in_breaks(self) -> bool:
        """Should letterbox appear during breaks."""
        return getattr(self._beatmap, 'letterbox_in_breaks', False)
    
    @property
    def widescreen_storyboard(self) -> bool:
        """Is storyboard widescreen."""
        return getattr(self._beatmap, 'widescreen_storyboard', False)
    
    @property
    def bookmarks(self) -> List[int]:
        """Bookmark times in milliseconds."""
        bookmarks = getattr(self._beatmap, 'bookmarks', [])
        return [int(b.total_seconds() * 1000) if hasattr(b, 'total_seconds') else b for b in bookmarks]
    
    @property
    def distance_spacing(self) -> float:
        """Distance snap multiplier."""
        return getattr(self._beatmap, 'distance_spacing', 1.0)
    
    @property
    def grid_size(self) -> int:
        """Grid snap size."""
        return getattr(self._beatmap, 'grid_size', 4)
    
    @property
    def timeline_zoom(self) -> float:
        """Editor timeline zoom."""
        return getattr(self._beatmap, 'timeline_zoom', 1.0)
    
    @property
    def title_unicode(self) -> str:
        """Unicode title."""
        return getattr(self._beatmap, 'title_unicode', self.metadata.title)
    
    @property
    def artist_unicode(self) -> str:
        """Unicode artist."""
        return getattr(self._beatmap, 'artist_unicode', self.metadata.artist)
    
    @property
    def creator(self) -> str:
        """Beatmap creator."""
        return getattr(self._beatmap, 'creator', '')
    
    @property
    def source(self) -> str:
        """Song source."""
        return getattr(self._beatmap, 'source', '')
    
    @property
    def tags(self) -> List[str]:
        """Beatmap tags."""
        tags = getattr(self._beatmap, 'tags', [])
        return tags if isinstance(tags, list) else tags.split() if tags else []
    
    @property
    def beatmap_id(self) -> Optional[int]:
        """Beatmap ID."""
        return getattr(self._beatmap, 'beatmap_id', None)
    
    @property
    def beatmap_set_id(self) -> Optional[int]:
        """Beatmap set ID."""
        return getattr(self._beatmap, 'beatmap_set_id', None)
    
    @property
    def display_name(self) -> str:
        """Display name as it appears in game."""
        return f"{self.metadata.artist} - {self.metadata.title} [{self.metadata.version}]"
    
    @property
    def bpm_min(self) -> float:
        """Minimum BPM in the beatmap."""
        min_bpm = float('inf')
        for tp in self.timing_points:
            if tp.uninherited and tp.beat_length > 0:
                min_bpm = min(min_bpm, tp.bpm)
        return min_bpm if min_bpm != float('inf') else 0.0
    
    @property
    def bpm_max(self) -> float:
        """Maximum BPM in the beatmap."""
        max_bpm = 0.0
        for tp in self.timing_points:
            if tp.uninherited and tp.beat_length > 0:
                max_bpm = max(max_bpm, tp.bpm)
        return max_bpm

    
    def beat_length_at(self, time: int, allow_multiplier: bool = True) -> float:
        """
        Calculate beat length at specific time
        
        Args:
            time: Time in milliseconds
            allow_multiplier: Whether to apply BPM multiplier from inherited timing points
            
        Returns:
            Beat length in milliseconds at the given time
        """
        if not self.timing_points:
            return 500.0  # Default fallback
        
        # Find the last timing change (red line) and inherited point (green line) before this time
        last_timing_change_idx = -1
        last_inherited_idx = -1
        
        for i, tp in enumerate(self.timing_points):
            if tp.time <= time:
                if tp.uninherited:  # Red line (timing change)
                    last_timing_change_idx = i
                else:  # Green line (inherited)
                    last_inherited_idx = i
        
        if last_timing_change_idx == -1:
            return 500.0  # No timing points found
        
        base_beat_length = self.timing_points[last_timing_change_idx].beat_length
        multiplier = 1.0
        
        # Apply multiplier from inherited timing point if applicable
        if (allow_multiplier and 
            last_inherited_idx > last_timing_change_idx and 
            last_inherited_idx < len(self.timing_points)):
            
            inherited_tp = self.timing_points[last_inherited_idx]
            if inherited_tp.beat_length < 0.0:
                # OsuMathHelper.Clamp((float)(-(float)this.BeatLength), 10f, 10000f) / 100f
                clamped_value = max(10.0, min(-inherited_tp.beat_length, 10000.0))
                multiplier = clamped_value / 100.0
        
        return base_beat_length * multiplier
    
    def calculate_taiko_drumroll_tick_delay(self, start_time: int) -> float:
        """
        Calculate taiko drumroll tick delay.
        
        Args:
            start_time: Start time of the drumroll in milliseconds
            
        Returns:
            Tick delay in milliseconds
        """

        slider_tick_rate = self.difficulty.slider_tick_rate if self.difficulty else 1.0
    
        if slider_tick_rate == 3.0:
            tick_delay = self.beat_length_at(start_time, False) / 3.0
        else:
            tick_delay = self.beat_length_at(start_time, False) / 4.0
        
        if tick_delay <= 0:
            return 80.0  # Safe fallback for invalid values
            
        iterations = 0
        while tick_delay < 60.0 and iterations < 10:
            tick_delay *= 2.0
            iterations += 1
            
        iterations = 0  
        while tick_delay > 120.0 and iterations < 10:
            tick_delay /= 2.0
            iterations += 1

        return max(60.0, min(tick_delay, 120.0))
    
    def calculate_taiko_spinner_hits_required(self, spinner_length_ms: float, mods: int = 0) -> int:
        """
        Calculate taiko spinner hits required.
        
        Args:
            spinner_length_ms: Duration of the spinner in milliseconds
            mods: Active mods bitmask (for DT/HT adjustments)
        
        Returns:
            Number of hits required for spinner completion (rotationRequirement + 1)
        """
        if spinner_length_ms <= 0:
            return 1
        
        od = self.difficulty.od if self.difficulty else 5.0
        spinner_length_seconds = spinner_length_ms / 1000.0
        
        # Calculate base rotation requirement (standard osu! formula)
        if od >= 5.0:
            rotations_per_second = 2.5 * 0.5 * od
        else:
            rotations_per_second = 3.0 + 0.4 * od
        
        base_rotation_requirement = spinner_length_seconds * rotations_per_second
        
        # this.rotationRequirement = (int)Math.Max(1f, (float)this.rotationRequirement * 1.65f);
        rotation_requirement = int(max(1.0, base_rotation_requirement * 1.65))
        
        # DT: this.rotationRequirement = Math.Max(1, (int)((float)this.rotationRequirement * 0.75f));
        if (mods & Mods.DOUBLETIME or mods & Mods.NIGHTCORE):
            rotation_requirement = max(1, int(rotation_requirement * 0.75))
        
        # HT: this.rotationRequirement = Math.Max(1, (int)((float)this.rotationRequirement * 1.5f));
        if (mods & Mods.HALFTIME):
            rotation_requirement = max(1, int(rotation_requirement * 1.5))

        # this.SpriteBonusCounter.set_Text((this.rotationRequirement + 1).ToString());
        displayed_hits = rotation_requirement + 1
        
        return displayed_hits
    
    def save(self, path: str) -> None:
        """Save the beatmap to a file."""
        self._beatmap.save(path)
    
    def to_string(self) -> str:
        """Convert beatmap to string representation."""
        return str(self._beatmap)


# Convenience functions
def load_beatmap(path: str) -> Optional[Beatmap]:
    """
    Load a beatmap from a file path.
    
    Args:
        path: Path to the .osu file
        
    Returns:
        Beatmap instance or None if loading fails
    """
    try:
        return Beatmap.from_path(path)
    except Exception:
        return None


def from_path(path: str) -> Beatmap:
    """
    Load a beatmap from a file path (alias for Beatmap.from_path).
    
    Args:
        path: Path to the .osu file
        
    Returns:
        Beatmap instance
    """
    return Beatmap.from_path(path)
