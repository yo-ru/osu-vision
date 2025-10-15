import slimgui.imgui as slimgui

from sdk.ui.manager import register_feature
from sdk.memory import AudioEngine, Beatmap, Player, GameBase, GamePlay
from sdk.beatmap.wrapper import load_beatmap
from sdk.beatmap.objects import ManiaHit, ManiaHold
from sdk.constants import GameMode, OsuMode, Mods

from .stage import Stage

class Feature:
    def __init__(self):
        self.show_window = False
        self.show_playfield = False

        self.note_style = 0
        self.scroll_speed = 2.2
        self.stage_spacing = 5
        self.offset = 0
        self.ln_tail = False
        self.note_color = (255/255.0, 255/255.0, 255/255.0, 1.0)  # Normalized RGBA
        self.ln_head_color = (255/255.0, 255/255.0, 255/255.0, 1.0)  # Normalized RGBA
        self.ln_body_color = (99/255.0, 99/255.0, 99/255.0, 1.0) # Normalized RGBA
        self.ln_tail_color = (255/255.0, 255/255.0, 255/255.0, 1.0)  # Normalized RGBA

        self.stages = []  # Will be dynamically created based on key count
        self.key_count = 4  # Default, will be updated from beatmap

        self._current_beatmap_path = ""
        self._initialized = False

    # Top-level menu entry
    def get_menu(self):
        return ("Mania", self.draw_menu)

    # Inside the "Mania" menu
    def draw_menu(self):
        if slimgui.menu_item("Settings")[0]:
            self.show_window = not self.show_window

        if slimgui.menu_item("Toggle Playfield")[0]:
            self.show_playfield = not self.show_playfield

    def draw_windows(self):
        if self.show_window:
            slimgui.set_next_window_size((0,0))
            visible, open_state = slimgui.begin("Mania Settings", True, flags=slimgui.WindowFlags.NO_RESIZE)
            if visible:
                _, self.note_style = slimgui.combo("Note Style", self.note_style, ["Circle", "Rectangle"])
                _, self.scroll_speed = slimgui.slider_float("Scroll Speed", self.scroll_speed, 0.1, 3.0, format="%.1f", flags=slimgui.SliderFlags.ALWAYS_CLAMP)
                _, self.stage_spacing = slimgui.slider_int("Stage Spacing", self.stage_spacing, 5, 30, flags=slimgui.SliderFlags.CLAMP_ON_INPUT)
                _, self.offset = slimgui.slider_int("Offset (ms)", self.offset, -100, 100, flags=slimgui.SliderFlags.CLAMP_ON_INPUT)
                _, self.note_color = slimgui.color_edit4("Note Color", self.note_color, flags=slimgui.ColorEditFlags.NO_INPUTS)
                _, self.ln_head_color = slimgui.color_edit4("LN Head Color", self.ln_head_color, flags=slimgui.ColorEditFlags.NO_INPUTS)
                _, self.ln_body_color = slimgui.color_edit4("LN Body Color", self.ln_body_color, flags=slimgui.ColorEditFlags.NO_INPUTS)
                _, self.ln_tail = slimgui.checkbox("##", self.ln_tail)
                if slimgui.is_item_hovered():
                    slimgui.set_tooltip("Enable/Disable LN Tail")
                slimgui.same_line()
                _, self.ln_tail_color = slimgui.color_edit4("LN Tail Color", self.ln_tail_color, flags=slimgui.ColorEditFlags.NO_INPUTS)
            slimgui.end()
            self.show_window = open_state

    def draw_overlay(self):
        if self.show_playfield:
            self.render_playfield()

    def render_playfield(self):
        viewport = slimgui.get_main_viewport()
        screen_width, screen_height = viewport.size
        
        playfield_width = screen_width // 3
        playfield_height = screen_height
        playfield_x = (screen_width - playfield_width) // 2
        playfield_y = (screen_height - playfield_height) // 2

        slimgui.set_next_window_pos((playfield_x, playfield_y))
        slimgui.set_next_window_size((playfield_width, playfield_height))

        flags = (
            slimgui.WindowFlags.NO_TITLE_BAR               |
            slimgui.WindowFlags.NO_RESIZE                  |
            slimgui.WindowFlags.NO_MOVE                    |
            slimgui.WindowFlags.NO_BRING_TO_FRONT_ON_FOCUS |
            slimgui.WindowFlags.NO_NAV_FOCUS               |
            slimgui.WindowFlags.NO_NAV_INPUTS
        )

        visible, _ = slimgui.begin("Mania Playfield", False, flags)
        if visible:
            if Player.mode == GameMode.MANIA and GameBase.mode == OsuMode.PLAY:
                current_path = Beatmap.path
                if current_path != self._current_beatmap_path:
                    self._current_beatmap_path = current_path
                    self._initialized = False
                
                if not self._initialized:
                    self.initialize()
                    self._initialized = True
                
                self.render_objects(AudioEngine.time + self.offset)
            else:
                self._initialized = False
        slimgui.end()

    def get_normalized_scroll_speed(self) -> float:
        """Get normalized scroll speed that compensates for speed mods"""
        try:
            mods = GamePlay.mods
            if mods & Mods.DOUBLETIME or mods & Mods.NIGHTCORE:
                return self.scroll_speed / 1.5
            elif mods & Mods.HALFTIME:
                return self.scroll_speed / 0.75
            else:
                return self.scroll_speed
        except:
            return self.scroll_speed

    def render_objects(self, time: int):
        if not self.stages or self.key_count == 0:
            return

        is_rect = self.note_style == 1
        stage_spacing = self.stage_spacing
        scroll_speed = self.get_normalized_scroll_speed()
        note_color = slimgui.color_convert_float4_to_u32(self.note_color)
        ln_head_color = slimgui.color_convert_float4_to_u32(self.ln_head_color)
        ln_body_color = slimgui.color_convert_float4_to_u32(self.ln_body_color)
        ln_tail_color = slimgui.color_convert_float4_to_u32(self.ln_tail_color)

        draw_list = slimgui.get_window_draw_list()
        window_width = slimgui.get_window_size()[0]
        window_height = slimgui.get_window_size()[1]
        window_pos = slimgui.get_window_pos()

        # Calculate object dimensions based on key count
        stage_width = window_width / self.key_count
        object_radius = (stage_width - stage_spacing * 2) / 2
        object_size = (object_radius * 2, object_radius if is_rect else object_radius * 2)

        # Calculate playfield height and scroll distance
        playfield_height = window_height
        scroll_distance = (
            (playfield_height - object_size[1] / 2 - stage_spacing - playfield_height / 30) -
            (window_pos[1] - object_size[1] / 2)
        )

        # Scroll parameters
        scroll_duration = 750  # ms - how long it takes for notes to reach the hit zone
        visible_range = scroll_duration * 1.2  # Show notes a bit before they start scrolling

        # First pass: Render hold bodies only (so they appear behind everything)
        for i, stage in enumerate(self.stages):
            x_center = window_pos[0] + stage_spacing + i * stage_width + object_size[0] / 2
            
            for start_time, end_time in stage.holds:
                # Check if the LN is in visible range
                if time >= end_time or time < start_time - visible_range / scroll_speed:
                    continue

                # Calculate Y positions for start and end of the hold
                hit_zone_y = window_pos[1] + window_height - object_size[1] / 2 - stage_spacing - window_height / 30
                
                # Start position
                if time < start_time:
                    t_start = (time - (start_time - (scroll_duration / scroll_speed))) / (scroll_duration / scroll_speed)
                    y_start = (window_pos[1] + object_size[1] / 2) + (hit_zone_y - (window_pos[1] + object_size[1] / 2)) * t_start
                else:
                    y_start = hit_zone_y
                
                # End position
                if time < end_time:
                    t_end = (time - (end_time - (scroll_duration / scroll_speed))) / (scroll_duration / scroll_speed)
                    y_end = (window_pos[1] + object_size[1] / 2) + (hit_zone_y - (window_pos[1] + object_size[1] / 2)) * t_end
                else:
                    y_end = hit_zone_y

                # Draw the hold body (connecting line/rect)
                hold_width = object_size[0] * 0.8
                if is_rect:
                    draw_list.add_rect_filled(
                        (x_center - hold_width / 2, min(y_start, y_end)),
                        (x_center + hold_width / 2, max(y_start, y_end)),
                        ln_body_color,
                        3
                    )
                else:
                    # For circles, draw as a rounded rectangle
                    draw_list.add_rect_filled(
                        (x_center - hold_width / 2, min(y_start, y_end)),
                        (x_center + hold_width / 2, max(y_start, y_end)),
                        ln_body_color,
                        object_radius * 0.5
                    )

        # Second pass: Render regular notes (so they appear above hold bodies)
        for i, stage in enumerate(self.stages):
            x_center = window_pos[0] + stage_spacing + i * stage_width + object_size[0] / 2
            
            for note_time in stage.notes:
                if time >= note_time or time < note_time - visible_range / scroll_speed:
                    continue

                t = (time - (note_time - (scroll_duration / scroll_speed))) / (scroll_duration / scroll_speed)
                
                # Calculate hit zone Y position (center of where receptors are drawn)
                hit_zone_y = window_pos[1] + window_height - object_size[1] / 2 - stage_spacing - window_height / 30
                # Calculate Y position from top of window to hit zone center
                y_center = (window_pos[1] + object_size[1] / 2) + (hit_zone_y - (window_pos[1] + object_size[1] / 2)) * t

                if is_rect:
                    draw_list.add_rect_filled(
                        (x_center - object_size[0] / 2, y_center - object_size[1] / 2),
                        (x_center + object_size[0] / 2, y_center + object_size[1] / 2),
                        note_color,
                        5
                    )
                else:
                    draw_list.add_circle_filled(
                        (x_center, y_center),
                        object_radius,
                        note_color,
                        32
                    )

        # Third pass: Render LN heads and tails (so they appear on top of everything)
        for i, stage in enumerate(self.stages):
            x_center = window_pos[0] + stage_spacing + i * stage_width + object_size[0] / 2
            
            for start_time, end_time in stage.holds:
                # Check if the LN is in visible range
                if time >= end_time or time < start_time - visible_range / scroll_speed:
                    continue

                # Calculate Y positions for start and end of the hold
                hit_zone_y = window_pos[1] + window_height - object_size[1] / 2 - stage_spacing - window_height / 30
                
                # Draw the head of the LN (at start position - the note you hit to begin the hold)
                if time < start_time:
                    t_start = (time - (start_time - (scroll_duration / scroll_speed))) / (scroll_duration / scroll_speed)
                    y_head = (window_pos[1] + object_size[1] / 2) + (hit_zone_y - (window_pos[1] + object_size[1] / 2)) * t_start
                    
                    if is_rect:
                        draw_list.add_rect_filled(
                            (x_center - object_size[0] / 2, y_head - object_size[1] / 2),
                            (x_center + object_size[0] / 2, y_head + object_size[1] / 2),
                            ln_head_color,
                            5
                        )
                    else:
                        draw_list.add_circle_filled(
                            (x_center, y_head),
                            object_radius,
                            ln_head_color,
                            32
                        )
                
                # Draw the tail of the LN (at end position - the note you release)
                if self.ln_tail and time < end_time:
                    t_end = (time - (end_time - (scroll_duration / scroll_speed))) / (scroll_duration / scroll_speed)
                    y_end = (window_pos[1] + object_size[1] / 2) + (hit_zone_y - (window_pos[1] + object_size[1] / 2)) * t_end
                    
                    if is_rect:
                        draw_list.add_rect_filled(
                            (x_center - object_size[0] / 2, y_end - object_size[1] / 2),
                            (x_center + object_size[0] / 2, y_end + object_size[1] / 2),
                            ln_tail_color,
                            5
                        )
                    else:
                        draw_list.add_circle_filled(
                            (x_center, y_end),
                            object_radius,
                            ln_tail_color,
                            32
                        )

        # Render receptors (hit zone indicators)
        for i in range(self.key_count):
            x_center = window_pos[0] + stage_spacing + i * stage_width + object_size[0] / 2
            hit_zone_y = window_pos[1] + window_height - object_size[1] / 2 - stage_spacing - window_height / 30
            
            if is_rect:
                draw_list.add_rect(
                    (x_center - object_size[0] / 2, hit_zone_y - object_size[1] / 2),
                    (x_center + object_size[0] / 2, hit_zone_y + object_size[1] / 2),
                    slimgui.color_convert_float4_to_u32((255/255.0, 255/255.0, 255/255.0, 255/255.0)),
                    5,
                    0,
                    3
                )
            else:
                draw_list.add_circle(
                    (x_center, hit_zone_y),
                    object_radius,
                    slimgui.color_convert_float4_to_u32((255/255.0, 255/255.0, 255/255.0, 255/255.0)),
                    32,
                    3
                )
    
    def initialize(self):
        """Initialize Mania stages with beatmap data."""
        beatmap = load_beatmap(Beatmap.path)
        if not beatmap:
            print(f"Failed to load beatmap! {Beatmap.path}")
            return

        # Determine key count from beatmap
        if not beatmap.hit_objects:
            return

        # Get key count from the first object (all objects should have the same key count)
        first_obj = beatmap.hit_objects[0]
        if isinstance(first_obj, (ManiaHit, ManiaHold)):
            self.key_count = first_obj.key_count
        else:
            return

        # Create stages for each column
        self.stages = [Stage() for _ in range(self.key_count)]

        # Load all hit objects into their respective stages
        for hit_object in beatmap.hit_objects:
            if isinstance(hit_object, ManiaHit):
                # Regular note
                if 0 <= hit_object.column < self.key_count:
                    self.stages[hit_object.column].add_note(hit_object.start_time)
                # Skip notes with invalid column indices

            elif isinstance(hit_object, ManiaHold):
                # Long note (hold)
                if 0 <= hit_object.column < self.key_count:
                    self.stages[hit_object.column].add_hold(hit_object.start_time, hit_object.end_time)
                # Skip holds with invalid column indices


# Register the feature
register_feature(Feature())
