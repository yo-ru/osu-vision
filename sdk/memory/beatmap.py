import os
import psutil

from sdk.constants.gamemodes import GameMode
from sdk.constants.mods import Mods
from . import Base

class Beatmap(Base):
    def __init__(self):
        super().__init__()

    @property
    def checksum(self) -> str:
        try:
            # [[Base - 0xC] + 0] + 0x6C
            beatmap_ptr = self.memory.resolve_pointer_chain("Base", [-0xC, 0])
            if not beatmap_ptr:
                return ""
            # [[Beatmap + 0x6C]
            return self.memory.read_csharp_string32(self.memory.read_int(beatmap_ptr + 0x6C))
        except:
            return ""

    @property
    def ranked_status(self) -> int:
        try:
            # [[Base - 0xC] + 0] + 0x12C
            beatmap_ptr = self.memory.resolve_pointer_chain("Base", [-0xC, 0])
            if not beatmap_ptr:
                return 0
            # [[Beatmap + 0x12C]
            return self.memory.read_int(beatmap_ptr + 0x12C)
        except:
            return 0

    @property
    def filename(self) -> str:
        try:
            # [[Base - 0xC] + 0] + 0x90
            beatmap_ptr = self.memory.resolve_pointer_chain("Base", [-0xC, 0])
            if not beatmap_ptr:
                return ""
            # [[Beatmap + 0x90]
            return self.memory.read_csharp_string32(self.memory.read_int(beatmap_ptr + 0x90))
        except:
            return ""

    @property
    def folder(self) -> str:
        try:
            # [[Base - 0xC] + 0] + 0x78
            beatmap_ptr = self.memory.resolve_pointer_chain("Base", [-0xC, 0])
            if not beatmap_ptr:
                return ""
            # [[Beatmap + 0x78]
            return self.memory.read_csharp_string32(self.memory.read_int(beatmap_ptr + 0x78))
        except:
            return ""

    @property
    def path(self) -> str:
        return os.path.join(os.path.dirname(psutil.Process(self.memory.pm.process_id).exe()), "Songs", self.folder, self.filename)
    
    @property
    def artist(self) -> str:
        try:
            # [[Base - 0xC] + 0] + 0x18
            beatmap_ptr = self.memory.resolve_pointer_chain("Base", [-0xC, 0])
            if not beatmap_ptr:
                return ""
            # [[Beatmap + 0x18]
            return self.memory.read_csharp_string32(self.memory.read_int(beatmap_ptr + 0x18))
        except:
            return ""

    @property
    def artist_original(self) -> str:
        try:
            # [[Base - 0xC] + 0] + 0x1C
            beatmap_ptr = self.memory.resolve_pointer_chain("Base", [-0xC, 0])
            if not beatmap_ptr:
                return ""
            # [[Beatmap + 0x1C]
            return self.memory.read_csharp_string32(self.memory.read_int(beatmap_ptr + 0x1C))
        except:
            return ""

    @property
    def title(self) -> str:
        try:
            # [[Base - 0xC] + 0] + 0x24
            beatmap_ptr = self.memory.resolve_pointer_chain("Base", [-0xC, 0])
            if not beatmap_ptr:
                return ""
            # [[Beatmap + 0x24]
            return self.memory.read_csharp_string32(self.memory.read_int(beatmap_ptr + 0x24))
        except:
            return ""
    
    @property
    def title_original(self) -> str:
        try:
            # [[Base - 0xC] + 0] + 0x28
            beatmap_ptr = self.memory.resolve_pointer_chain("Base", [-0xC, 0])
            if not beatmap_ptr:
                return ""
            # [[Beatmap + 0x28]
            return self.memory.read_csharp_string32(self.memory.read_int(beatmap_ptr + 0x28))
        except:
            return ""

    @property
    def ar(self) -> float:
        try:
            # [[Base - 0xC] + 0] + 0x2C
            beatmap_ptr = self.memory.resolve_pointer_chain("Base", [-0xC, 0])
            if not beatmap_ptr:
                return 0.0
            # [[Beatmap + 0x2C]
            return round(self.memory.read_float(beatmap_ptr + 0x2C), 1)
        except:
            return 0.0
    
    @property
    def cs(self) -> float:
        try:
            # [[Base - 0xC] + 0] + 0x30
            beatmap_ptr = self.memory.resolve_pointer_chain("Base", [-0xC, 0])
            if not beatmap_ptr:
                return 0.0
            # [[Beatmap + 0x30]
            return round(self.memory.read_float(beatmap_ptr + 0x30), 1)
        except:
            return 0.0
    
    @property
    def hp(self) -> float:
        try:
            # [[Base - 0xC] + 0] + 0x34
            beatmap_ptr = self.memory.resolve_pointer_chain("Base", [-0xC, 0])
            if not beatmap_ptr:
                return 0.0
            # [[Beatmap + 0x34]
            return round(self.memory.read_float(beatmap_ptr + 0x34), 1)
        except:
            return 0.0
    
    @property
    def od(self) -> float:
        try:
            # [[Base - 0xC] + 0] + 0x38
            beatmap_ptr = self.memory.resolve_pointer_chain("Base", [-0xC, 0])
            if not beatmap_ptr:
                return 0.0
            # [[Beatmap + 0x38]
            return round(self.memory.read_float(beatmap_ptr + 0x38), 2)
        except:
            return 0.0

    @property
    def od_offset(self) -> float:
        from sdk.memory import GamePlay

        if GamePlay.mode == GameMode.TAIKO:
            mod_od = self.od

            if GamePlay.mods & Mods.EASY:
                mod_od /= 2
            elif GamePlay.mods & Mods.HARDROCK:
                mod_od = min(self.od * 1.4, 10)

            return mod_od

        return self.od
    
    @property
    def audio_filename(self) -> str:
        try:
            # [[Base - 0xC] + 0] + 0x64
            beatmap_ptr = self.memory.resolve_pointer_chain("Base", [-0xC, 0])
            if not beatmap_ptr:
                return ""
            # [[Beatmap + 0x64]
            return self.memory.read_csharp_string32(self.memory.read_int(beatmap_ptr + 0x64))
        except:
            return ""

    @property
    def bg_filename(self) -> str:
        try:
            # [[Base - 0xC] + 0] + 0x68
            beatmap_ptr = self.memory.resolve_pointer_chain("Base", [-0xC, 0])
            if not beatmap_ptr:
                return ""
            # [[Beatmap + 0x68]
            return self.memory.read_csharp_string32(self.memory.read_int(beatmap_ptr + 0x68))
        except:
            return ""

    @property
    def creator(self) -> str:
        try:
            # [[Base - 0xC] + 0] + 0x7C
            beatmap_ptr = self.memory.resolve_pointer_chain("Base", [-0xC, 0])
            if not beatmap_ptr:
                return ""
            # [[Beatmap + 0x7C]
            return self.memory.read_csharp_string32(self.memory.read_int(beatmap_ptr + 0x7C))
        except:
            return ""

    @property
    def difficulty(self) -> str:
        try:
            # [[Base - 0xC] + 0] + 0xAC
            beatmap_ptr = self.memory.resolve_pointer_chain("Base", [-0xC, 0])
            if not beatmap_ptr:
                return ""
            # [[Beatmap + 0xAC]
            return self.memory.read_csharp_string32(self.memory.read_int(beatmap_ptr + 0xAC))
        except:
            return ""
    
    @property
    def map_id(self) -> int:
        try:
            # [[Base - 0xC] + 0] + 0xC8
            beatmap_ptr = self.memory.resolve_pointer_chain("Base", [-0xC, 0])
            if not beatmap_ptr:
                return 0
            # [[Beatmap + 0xC8]
            return self.memory.read_int(beatmap_ptr + 0xC8)
        except:
            return 0

    @property
    def set_id(self) -> int:
        try:
            # [[Base - 0xC] + 0] + 0xCC
            beatmap_ptr = self.memory.resolve_pointer_chain("Base", [-0xC, 0])
            if not beatmap_ptr:
                return 0
            # [[Beatmap + 0xCC]
            return self.memory.read_int(beatmap_ptr + 0xCC)
        except:
            return 0

    @property
    def object_count(self) -> int:
        try:
            # [[Base - 0xC] + 0] + 0xF8
            beatmap_ptr = self.memory.resolve_pointer_chain("Base", [-0xC, 0])
            if not beatmap_ptr:
                return 0
            # [[Beatmap + 0xF8]
            return self.memory.read_int(beatmap_ptr + 0xF8)
        except:
            return 0

