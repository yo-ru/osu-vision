import slimgui.imgui as slimgui

from sdk.ui.manager import register_feature

from sdk.memory import GameBase, GamePlay
from sdk.constants import OsuMode

class Feature:
    def __init__(self):
        self.show_window = False

        self.show_combo = False
        self.combo_y = slimgui.get_io().display_size[1] * 0.5

        self.show_judge = False
        self.judge_y = (slimgui.get_io().display_size[1] + 120) * 0.5
        self.last_judge = None
        
        # Judgement tracking
        self.last_hit_counts = {
            'hit300': 0,
            'hit100': 0, 
            'hit50': 0,
            'hitGeki': 0,
            'hitKatu': 0,
            'hitMiss': 0
        }
        self.judge_text = ""
        self.judge_timer = 0.0
        
        # Cache frequently accessed values
        self._cached_combo = 0
        self._cached_mode = None
        self._cached_game_mode = None
        
        # Cache judgement strings to avoid repeated string creation
        self.judgement_strings = {
            'hit300': "PERFECT",
            'hit100': "GOOD", 
            'hit50': "BAD",
            'hitGeki': "MARVELOUS",
            'hitKatu': "GREAT",
            'hitMiss': "MISS"
        }

    def get_cached_combo(self):
        """Get combo value with caching - only reads memory when mode changes"""
        current_mode = GameBase.mode
        if current_mode != self._cached_mode:
            self._cached_mode = current_mode
            self._cached_combo = GamePlay.combo if current_mode == OsuMode.PLAY else 0
        elif current_mode == OsuMode.PLAY:
            # Only update combo if we're in play mode
            new_combo = GamePlay.combo
            if new_combo != self._cached_combo:
                self._cached_combo = new_combo
        return self._cached_combo

    def get_cached_hit_counts(self):
        """Get hit counts with change detection - only reads when needed"""
        if GameBase.mode != OsuMode.PLAY:
            return self.last_hit_counts
            
        # Only read memory if we're in play mode
        return {
            'hit300': GamePlay.hit300,
            'hit100': GamePlay.hit100,
            'hit50': GamePlay.hit50,
            'hitGeki': GamePlay.hitGeki,
            'hitKatu': GamePlay.hitKatu,
            'hitMiss': GamePlay.hitMiss
        }

    def update_judgement_tracking(self):
        """Check for changes in hit counts and update judgement display"""
        if GameBase.mode != OsuMode.PLAY:
            return
            
        # Get current hit counts using cached method
        current_counts = self.get_cached_hit_counts()
        
        # Check for changes and determine the judgement type
        for hit_type, current_count in current_counts.items():
            if current_count > self.last_hit_counts[hit_type]:
                # Hit count increased, show judgement using cached string
                self.judge_text = self.judgement_strings[hit_type]
                self.judge_timer = 0.15 # duration
                break
        
        # Update last counts
        self.last_hit_counts = current_counts
        
        # Decrease timer
        if self.judge_timer > 0:
            self.judge_timer -= slimgui.get_io().delta_time

    def get_menu(self):
        return "Gameplay"

    def draw_menu(self):
        self.show_window = not self.show_window

    def draw_windows(self):
        # Only update judgement tracking if judgements are enabled
        if self.show_judge:
            self.update_judgement_tracking()
        
        if self.show_window:
            # Gameplay Settings
            slimgui.set_next_window_size((0,0))
            visible, open_state = slimgui.begin("Gameplay Settings", True, flags=slimgui.WindowFlags.NO_RESIZE)
            if visible:
                dY = slimgui.get_io().display_size[1] - 120


                # Combo
                _, self.show_combo = slimgui.checkbox("Show Combo", self.show_combo)
                _, self.combo_y = slimgui.slider_float("Combo Y", self.combo_y, 125, dY,  format="%.1f", flags=slimgui.SliderFlags.ALWAYS_CLAMP)

                slimgui.separator()

                # Judgements
                _, self.show_judge = slimgui.checkbox("Show Judgements", self.show_judge)
                _, self.judge_y = slimgui.slider_float("Judgement Y", self.judge_y, 125, dY,  format="%.1f", flags=slimgui.SliderFlags.ALWAYS_CLAMP)


            slimgui.end()
            self.show_window = open_state

        # Combo
        if self.show_combo:
                flags = (
                    slimgui.WindowFlags.NO_TITLE_BAR               |
                    slimgui.WindowFlags.NO_RESIZE                  |
                    slimgui.WindowFlags.NO_BACKGROUND              |
                    slimgui.WindowFlags.NO_COLLAPSE                |
                    slimgui.WindowFlags.NO_FOCUS_ON_APPEARING      |
                    slimgui.WindowFlags.NO_MOVE                    |
                    slimgui.WindowFlags.NO_INPUTS                  |
                    slimgui.WindowFlags.NO_NAV_INPUTS
                )

                slimgui.set_next_window_size((0, 0))
                slimgui.set_next_window_pos((slimgui.get_io().display_size[0] * 0.5, self.combo_y), pivot=(0.5, 0.5))
                visible, open_state = slimgui.begin("Combo", False, flags)
                if visible:
                    slimgui.push_font(None, 50)
                    slimgui.text(f"{self.get_cached_combo()}")
                    slimgui.pop_font()
                slimgui.end()

        # Judgements
        if self.show_judge:
                flags = (
                    slimgui.WindowFlags.NO_TITLE_BAR               |
                    slimgui.WindowFlags.NO_RESIZE                  |
                    slimgui.WindowFlags.NO_BACKGROUND              |
                    slimgui.WindowFlags.NO_COLLAPSE                |
                    slimgui.WindowFlags.NO_FOCUS_ON_APPEARING      |
                    slimgui.WindowFlags.NO_MOVE                    |
                    slimgui.WindowFlags.NO_INPUTS                  |
                    slimgui.WindowFlags.NO_NAV_INPUTS
                )

                slimgui.set_next_window_size((0, 0))
                slimgui.set_next_window_pos((slimgui.get_io().display_size[0] * 0.5, self.judge_y), pivot=(0.5, 0.5))
                visible, open_state = slimgui.begin("Judgement", False, flags)
                if visible:
                    if self.judge_timer > 0 and GameBase.mode == OsuMode.PLAY:
                        text = self.judge_text
                    else:
                        text = "" if GameBase.mode == OsuMode.PLAY else "JUDGE"
                    slimgui.push_font(None, 30)
                    slimgui.text(text)
                    slimgui.pop_font()
                slimgui.end()

# Register the feature
register_feature(Feature())