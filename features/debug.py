import slimgui.imgui as slimgui

from sdk.ui.manager import register_feature

from sdk.memory import GameBase, AudioEngine, Beatmap, Player, GamePlay
from sdk.constants import OsuMode

class DebugFeature:
    def __init__(self):
        self.show_window = False

    def get_menu(self):
        return "Debug"

    def draw_menu(self):
        self.show_window = not self.show_window

    def draw_windows(self):
        if self.show_window:
            visible, open_state = slimgui.begin("Debug Window", True)
            if visible:
                slimgui.text(f"GameBase:")
                slimgui.text(f"State: {GameBase.mode.name}")
                slimgui.text(f"Time: {GameBase.time}")
                slimgui.new_line()
                slimgui.text(f"AudioEngine:")
                slimgui.text(f"Time: {AudioEngine.time}")
                slimgui.new_line()
                slimgui.text(f"Player:")
                slimgui.text(f"Gamemode: {Player.mode.name}")
                slimgui.text(f"Loaded: {Player.loaded}")
                slimgui.text(f"Failed: {Player.failed}")
                slimgui.text(f"Retrying: {Player.retrying}")
                slimgui.new_line()
                slimgui.text(f"Beatmap:")
                slimgui.text(f"Name: {Beatmap.artist} - {Beatmap.title} [{Beatmap.difficulty}]")
                slimgui.text(f"Creator: {Beatmap.creator}")
                slimgui.text(f"Map ID: {Beatmap.map_id}")
                slimgui.text(f"Set ID: {Beatmap.set_id}")
                slimgui.text(f"AR: {Beatmap.ar} | CS: {Beatmap.cs}")
                slimgui.text(f"HP: {Beatmap.hp} | OD: {Beatmap.od}")
                slimgui.new_line()
                if GameBase.mode == OsuMode.PLAY:
                    slimgui.text(f"Gameplay:")
                    slimgui.text(f"Gamemode: {GamePlay.mode.name}")
                    slimgui.text(f"Player Name: {GamePlay.player_name}")
                    slimgui.text(f"Mods: {GamePlay.mods.name}")
                    slimgui.text(f"Score: {GamePlay.score}")
                    slimgui.text(f"HP: {GamePlay.hp}")
                    slimgui.text(f"Accuracy: {GamePlay.accuracy}")
                    slimgui.text(f"Hit100: {GamePlay.hit100}")
                    slimgui.text(f"Hit300: {GamePlay.hit300}")
                    slimgui.text(f"Hit50: {GamePlay.hit50}")
                    slimgui.text(f"HitGeki: {GamePlay.hitGeki}")
                    slimgui.text(f"HitKatu: {GamePlay.hitKatu}")
                    slimgui.text(f"HitMiss: {GamePlay.hitMiss}")
                    slimgui.text(f"Combo: {GamePlay.combo}")
                    slimgui.text(f"Max Combo: {GamePlay.max_combo}")
            slimgui.end()
            self.show_window = open_state


# Register the feature
register_feature(DebugFeature())