from functools import cached_property
import math
from . import Base
from ..constants import Mods, GameMode

class GamePlay(Base):
    def __init__(self):
        super().__init__()

    @property
    def retries(self) -> int:
        try:
            # [[Base - 0x33] + 0] + 0x8
            retries_ptr = self.memory.resolve_pointer_chain("Base", [-0x33, 0])
            if not retries_ptr:
                return 0
            # [[Retries + 0x8]
            return self.memory.read_int(retries_ptr + 0x8)
        except:
            return 0

    @property
    def mods(self) -> Mods:
        try:
            # [[Rulesets - 0xb] + 0x4] + 0x68] + 0x38] + 0x1C] + 0xC
            score_ptr = self.memory.resolve_pointer_chain("Rulesets", [-0xb, 0x4, 0x68, 0x38])
            if not score_ptr:
                return Mods(0)
            # [[Score + 0x1C] + 0xC]
            mods1 = self.memory.read_int(self.memory.read_int(score_ptr + 0x1C) + 0xC)
            # [[Score + 0x1C] + 0x8]
            mods2 = self.memory.read_int(self.memory.read_int(score_ptr + 0x1C) + 0x8)
            return Mods(mods1 ^ mods2)
        except:
            return Mods(0)

    @property
    def mode(self) -> GameMode:
        try:
            # [[Rulesets - 0xb] + 0x4] + 0x68] + 0x38] + 0x64
            score_ptr = self.memory.resolve_pointer_chain("Rulesets", [-0xb, 0x4, 0x68, 0x38])
            if not score_ptr:
                return GameMode(0)
            # [[Score + 0x64]
            return GameMode(self.memory.read_int(score_ptr + 0x64))
        except:
            return GameMode(0)

    @property
    def score(self) -> int:
        try:
            # [[Rulesets - 0xb] + 0x4] + 0x100
            rulesets_ptr = self.memory.resolve_pointer_chain("Rulesets", [-0xb, 0x4])
            if not rulesets_ptr:
                return 0
            # [[Ruleset + 0x100]
            return self.memory.read_int(rulesets_ptr + 0x100)
        except:
            return 0

    @property
    def hp_smooth(self) -> float:
        try:
            # [[Rulesets - 0xb] + 0x4] + 0x68] + 0x40] + 0x14
            hp_bar_ptr = self.memory.resolve_pointer_chain("Rulesets", [-0xb, 0x4, 0x68, 0x40])
            if not hp_bar_ptr:
                return 0.0
            # [[HpBar + 0x14]
            return round(self.memory.read_double(hp_bar_ptr + 0x14), 2) or 0.0
        except:
            return 0.0

    @property
    def hp(self) -> float:
        try:
            # [[Rulesets - 0xb] + 0x4] + 0x68] + 0x40] + 0x1C
            hp_bar_ptr = self.memory.resolve_pointer_chain("Rulesets", [-0xb, 0x4, 0x68, 0x40])
            if not hp_bar_ptr:
                return 0.0
            # [[HpBar + 0x1C]
            return round(self.memory.read_double(hp_bar_ptr + 0x1C), 2)
        except:
            return 0.0

    @property
    def accuracy(self) -> float:
        try:
            # [[Rulesets - 0xb] + 0x4] + 0x68] + 0x48] + 0xC
            gameplay_ptr = self.memory.resolve_pointer_chain("Rulesets", [-0xb, 0x4, 0x68])
            if not gameplay_ptr:
                return 0.0
            # [[Gameplay + 0x48] + 0xC]
            return round(self.memory.read_double(self.memory.read_int(gameplay_ptr + 0x48) + 0xC), 2)
        except:
            return 0.0
    
    @property
    def hit100(self) -> int:
        try:
            # TODO: Add playtime check like tosu: if global.playTime >= beatmapPP.timings.firstObj - 100
            # [[Rulesets - 0xb] + 0x4] + 0x68] + 0x38] + 0x88
            score_ptr = self.memory.resolve_pointer_chain("Rulesets", [-0xb, 0x4, 0x68, 0x38])
            if not score_ptr:
                return 0
            # [[Score + 0x88]
            return self.memory.read_short(score_ptr + 0x88)
        except:
            return 0
    
    @property
    def hit300(self) -> int:
        try:
            # [[Rulesets - 0xb] + 0x4] + 0x68] + 0x38] + 0x8A
            score_ptr = self.memory.resolve_pointer_chain("Rulesets", [-0xb, 0x4, 0x68, 0x38])
            if not score_ptr:
                return 0
            # [[Score + 0x8A]
            return self.memory.read_short(score_ptr + 0x8A)
        except:
            return 0
    
    @property
    def hit50(self) -> int:
        try:
            # [[Rulesets - 0xb] + 0x4] + 0x68] + 0x38] + 0x8C
            score_ptr = self.memory.resolve_pointer_chain("Rulesets", [-0xb, 0x4, 0x68, 0x38])
            if not score_ptr:
                return 0
            # [[Score + 0x8C]
            return self.memory.read_short(score_ptr + 0x8C)
        except:
            return 0
    
    @property
    def hitGeki(self) -> int:
        try:
            # [[Rulesets - 0xb] + 0x4] + 0x68] + 0x38] + 0x8E
            score_ptr = self.memory.resolve_pointer_chain("Rulesets", [-0xb, 0x4, 0x68, 0x38])
            if not score_ptr:
                return 0
            # [[Score + 0x8E]
            return self.memory.read_short(score_ptr + 0x8E)
        except:
            return 0

    @property
    def hitKatu(self) -> int:
        try:
            # [[Rulesets - 0xb] + 0x4] + 0x68] + 0x38] + 0x90
            score_ptr = self.memory.resolve_pointer_chain("Rulesets", [-0xb, 0x4, 0x68, 0x38])
            if not score_ptr:
                return 0
            # [[Score + 0x90]
            return self.memory.read_short(score_ptr + 0x90)
        except:
            return 0
    
    @property
    def hitMiss(self) -> int:
        try:
            # [[Rulesets - 0xb] + 0x4] + 0x68] + 0x38] + 0x92
            score_ptr = self.memory.resolve_pointer_chain("Rulesets", [-0xb, 0x4, 0x68, 0x38])
            if not score_ptr:
                return 0
            # [[Score + 0x92]
            return self.memory.read_short(score_ptr + 0x92)
        except:
            return 0
    
    @property
    def combo(self) -> int:
        try:
            # [[Rulesets - 0xb] + 0x4] + 0x68] + 0x38] + 0x94
            score_ptr = self.memory.resolve_pointer_chain("Rulesets", [-0xb, 0x4, 0x68, 0x38])
            if not score_ptr:
                return 0
            # [[Score + 0x94]
            return self.memory.read_short(score_ptr + 0x94)
        except:
            return 0

    @property
    def max_combo(self) -> int:
        try:
            # [[Rulesets - 0xb] + 0x4] + 0x68] + 0x38] + 0x68
            score_ptr = self.memory.resolve_pointer_chain("Rulesets", [-0xb, 0x4, 0x68, 0x38])
            if not score_ptr:
                return 0
            # [[Score + 0x68]
            return self.memory.read_short(score_ptr + 0x68)
        except:
            return 0
    
    @property
    def player_name(self) -> str:
        try:
            # [[[Rulesets - 0xb] + 0x4] + 0x68] + 0x38] + 0x28]
            score_ptr = self.memory.resolve_pointer_chain("Rulesets", [-0xb, 0x4, 0x68, 0x38])
            if not score_ptr:
                return ""
            # [[Score + 0x28]
            return self.memory.read_csharp_string32(self.memory.read_int(score_ptr + 0x28))
        except:
            return ""

    @property
    def hit_errors(self) -> list:
        try:
            rulesets_ptr = self.memory.resolve_pointer_chain("Rulesets", [-0xb, 0x4])
            gameplay_ptr = self.memory.resolve_pointer_chain("Rulesets", [-0xb, 0x4, 0x68])
            score_ptr = self.memory.resolve_pointer_chain("Rulesets", [-0xb, 0x4, 0x68, 0x38])
            if not rulesets_ptr or not gameplay_ptr or not score_ptr:
                return []

            leader_start = 0x8

            base = self.memory.read_int(score_ptr + 0x38)
            items = self.memory.read_int(base + 0x4)
            size = self.memory.read_int(base + 0xc)

            errors = []
            for i in range(size):
                current = items + leader_start + 0x4 * i
                error = self.memory.read_int(current)

                errors.append(error)

            return errors

        except:
            return []
    
    @property
    def unstable_rate(self) -> float:
        base_ur = self._calculate_ur()

        if self.mods & Mods.DOUBLETIME or self.mods & Mods.NIGHTCORE:
            return base_ur / 1.5
        elif self.mods & Mods.HALFTIME:
            return base_ur * 1.33
        return base_ur

    def _calculate_ur(self) -> float:
        if len(self.hit_errors) < 1:
            return 0.

        total_all = 0.
        
        for hit in self.hit_errors: # TODO: we shouldn't do this every time
            total_all += hit
        
        average = total_all / len(self.hit_errors)
        variance = 0.

        for hit in self.hit_errors:
            variance += math.pow(hit - average, 2)
        variance /= len(self.hit_errors)

        return math.sqrt(variance) * 10

    
    @cached_property
    def od_offset(self) -> float:
        from sdk.memory import Beatmap

        match self.mode:
            case GameMode.TAIKO:
                mod_od = Beatmap.od

                if self.mods & Mods.EASY:
                    mod_od /= 2
                elif self.mods & Mods.HARDROCK:
                    mod_od = min(Beatmap.od * 1.4, 10)

                return (50 - 3 * mod_od) / 8
            
            case GameMode.MANIA:
                return 2 # 16 / 8 == 1 ???

        return ((159 - 12 * Beatmap.od) / 2) / 8