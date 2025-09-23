"""
Beatmap parsing module wrapping the slider library.

This module provides a clean interface to the slider library for osu! beatmap parsing.
"""

from .wrapper import Beatmap, load_beatmap, from_path
from .types import HitObject, HitObjectType, HitSound, TimingPoint, Metadata, BeatmapDifficulty

__all__ = [
    'Beatmap',
    'HitObject', 
    'HitObjectType',
    'HitSound',
    'TimingPoint',
    'Metadata',
    'BeatmapDifficulty',
    'load_beatmap',
    'from_path',
]