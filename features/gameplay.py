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

    def update_judgement_tracking(self):
        """Check for changes in hit counts and update judgement display"""
        if GameBase.mode != OsuMode.PLAY:
            return
            
        # Get current hit counts
        current_counts = {
            'hit300': GamePlay.hit300,
            'hit100': GamePlay.hit100,
            'hit50': GamePlay.hit50,
            'hitGeki': GamePlay.hitGeki,
            'hitKatu': GamePlay.hitKatu,
            'hitMiss': GamePlay.hitMiss
        }
        
        # Check for changes and determine the judgement type
        for hit_type, current_count in current_counts.items():
            if current_count > self.last_hit_counts[hit_type]:
                # Hit count increased, show judgement
                if hit_type == 'hit300':
                    self.judge_text = "MARVELOUS"
                elif hit_type == 'hit100':
                    self.judge_text = "GREAT"
                elif hit_type == 'hit50':
                    self.judge_text = "OK"
                elif hit_type == 'hitGeki':
                    self.judge_text = "GEKI"
                elif hit_type == 'hitKatu':
                    self.judge_text = "KATU"
                elif hit_type == 'hitMiss':
                    self.judge_text = "MISS"
                
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
        # Update judgement tracking
        self.update_judgement_tracking()
        
        if self.show_window:
            # Gameplay Settings
            slimgui.set_next_window_size((0,0))
            visible, open_state = slimgui.begin("Gameplay Settings", True, flags=slimgui.WindowFlags.NO_RESIZE)
            if visible:
                # slimgui.text(f"GameBase:")
                # slimgui.text(f"State: {GameBase.mode.name}")
                # slimgui.text(f"Time: {GameBase.time}")
                # slimgui.new_line()
                # slimgui.text(f"AudioEngine:")
                # slimgui.text(f"Time: {AudioEngine.time}")
                # slimgui.new_line()
                # slimgui.text(f"Player:")
                # slimgui.text(f"Gamemode: {Player.mode.name}")
                # slimgui.text(f"Loaded: {Player.loaded}")
                # slimgui.text(f"Failed: {Player.failed}")
                # slimgui.text(f"Retrying: {Player.retrying}")
                # slimgui.new_line()
                # slimgui.text(f"Beatmap:")
                # slimgui.text(f"Path: {Beatmap.path}")
                # slimgui.text(f"Name: {Beatmap.artist} - {Beatmap.title} [{Beatmap.difficulty}]")
                # slimgui.text(f"Creator: {Beatmap.creator}")
                # slimgui.text(f"Map ID: {Beatmap.map_id}")
                # slimgui.text(f"Set ID: {Beatmap.set_id}")
                # slimgui.text(f"AR: {Beatmap.ar} | CS: {Beatmap.cs}")
                # slimgui.text(f"HP: {Beatmap.hp} | OD: {Beatmap.od}")
                # slimgui.new_line()
                # if GameBase.mode == OsuMode.PLAY:
                #     slimgui.text(f"Gameplay:")
                #     slimgui.text(f"Gamemode: {GamePlay.mode.name}")
                #     slimgui.text(f"Player Name: {GamePlay.player_name}")
                #     slimgui.text(f"Mods: {GamePlay.mods.name}")
                #     slimgui.text(f"Score: {GamePlay.score}")
                #     slimgui.text(f"HP: {GamePlay.hp}")
                #     slimgui.text(f"Accuracy: {GamePlay.accuracy}")
                #     slimgui.text(f"Hit100: {GamePlay.hit100}")
                #     slimgui.text(f"Hit300: {GamePlay.hit300}")
                #     slimgui.text(f"Hit50: {GamePlay.hit50}")
                #     slimgui.text(f"HitGeki: {GamePlay.hitGeki}")
                #     slimgui.text(f"HitKatu: {GamePlay.hitKatu}")
                #     slimgui.text(f"HitMiss: {GamePlay.hitMiss}")
                #     slimgui.text(f"Combo: {GamePlay.combo}")
                #     slimgui.text(f"Max Combo: {GamePlay.max_combo}")
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
                    slimgui.WindowFlags.NO_MOVE
                )

                slimgui.set_next_window_size((0, 0))
                slimgui.set_next_window_pos((slimgui.get_io().display_size[0] * 0.5, self.combo_y), pivot=(0.5, 0.5))
                visible, open_state = slimgui.begin("Combo", False, flags)
                if visible:
                    slimgui.push_font(None, 50)
                    slimgui.text(f"{GamePlay.combo if GameBase.mode == OsuMode.PLAY else "0"}")
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
                    slimgui.WindowFlags.NO_MOVE
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