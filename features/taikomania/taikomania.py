from re import L
import slimgui.imgui as slimgui

from sdk.ui.manager import register_feature
from sdk.memory import AudioEngine, Beatmap, Player, GameBase, GamePlay
from sdk.beatmap.wrapper import load_beatmap
from sdk.beatmap.objects import TaikoHit, TaikoDrumroll, TaikoSwell
from sdk.constants import GameMode, OsuMode, Mods

from .stage import Stage, TaikoManiaObjectType

class Feature:
    def __init__(self):
        self.show_window = False
        self.show_playfield = False

        self.note_style = 0
        self.playstyle = 0
        self._2k_finisher = False
        self.alternate_bpm = 0
        self.scroll_speed = 2.0
        self.stage_spacing = 5
        self.offset = 0
        self.don_color = (255/255.0, 83/255.0, 72/255.0, 1.0)  # Normalized RGBA
        self.katsu_color = (133/255.0, 195/255.0, 236/255.0, 1.0)  # Normalized RGBA

        self.od_offset = False

        # primary katsu, secondary katsu, primary don, secondary don
        self.stages = [Stage(TaikoManiaObjectType.KATSU), Stage(TaikoManiaObjectType.KATSU), Stage(TaikoManiaObjectType.DON), Stage(TaikoManiaObjectType.DON)]

        self._current_beatmap_path = ""
        self._initialized = False

    # Top-level menu entry
    def get_menu(self):
        return ("TaikoMania", self.draw_menu)

    # Inside the "TaikoMania" menu
    def draw_menu(self):
        if slimgui.menu_item("Settings")[0]:
            self.show_window = not self.show_window

        if slimgui.menu_item("Toggle Playfield")[0]:
            self.show_playfield = not self.show_playfield

    def draw_windows(self):
        if self.show_window:
            slimgui.set_next_window_size((0,0))
            visible, open_state = slimgui.begin("TaikoMania Settings", True, flags=slimgui.WindowFlags.NO_RESIZE)
            if visible:
                _, self.note_style = slimgui.combo("Note Style", self.note_style, ["Circle", "Rectangle"])
                _, self.playstyle = slimgui.combo("Playstyle", self.playstyle, ["KDDK", "DKKD", "KKDD", "DDKK", "KDKD", "DKDK"])
                _, self._2k_finisher = slimgui.checkbox("2K Finisher", self._2k_finisher)
                if slimgui.is_item_hovered():
                    slimgui.set_tooltip("Splits finishers into two notes, using both keys instead of one.")
                _, self.alternate_bpm = slimgui.slider_int("Alternate BPM", self.alternate_bpm, 0, 500, flags=slimgui.SliderFlags.CLAMP_ON_INPUT)
                _, self.scroll_speed = slimgui.slider_float("Scroll Speed", self.scroll_speed, 0.1, 3.0, format="%.1f", flags=slimgui.SliderFlags.ALWAYS_CLAMP)
                _, self.stage_spacing = slimgui.slider_int("Stage Spacing", self.stage_spacing, 5, 30, flags=slimgui.SliderFlags.CLAMP_ON_INPUT)
                _, self.offset = slimgui.slider_int("Offset (ms)", self.offset, -100, 100, flags=slimgui.SliderFlags.CLAMP_ON_INPUT)
                _, self.don_color = slimgui.color_edit4("Don Color", self.don_color, flags=slimgui.ColorEditFlags.NO_INPUTS)
                _, self.katsu_color = slimgui.color_edit4("Katsu Color", self.katsu_color, flags=slimgui.ColorEditFlags.NO_INPUTS)
                
                slimgui.separator()

                # Experimental
                _, self.od_offset = slimgui.checkbox("OD Offset", self.od_offset)
                if slimgui.is_item_hovered():
                    slimgui.set_tooltip("Enable/Disable Exerimental OD Offset")
            slimgui.end()
            self.show_window = open_state

    def render_playfield(self):
       draw_list = slimgui.get_window_draw_list()

       draw_list.add_rect_filled(self.playfield_rect, (255, 255, 255, 255))

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

        visible, _ = slimgui.begin("TaikoMania Playfield", False, flags)
        if visible:
            if Player.mode == GameMode.TAIKO and GameBase.mode == OsuMode.PLAY:
                current_path = Beatmap.path
                if current_path != self._current_beatmap_path:
                    self._current_beatmap_path = current_path
                    self._initialized = False
                
                if not self._initialized:
                    self.initialize()
                    self._initialized = True
                
                self.render_objects(AudioEngine.time + self.offset + Beatmap.od_offset if self.od_offset else 0)
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
        is_rect = self.note_style == 1
        stage_spacing = self.stage_spacing
        scroll_speed = self.get_normalized_scroll_speed()
        katsu_color = slimgui.color_convert_float4_to_u32(self.katsu_color)
        don_color = slimgui.color_convert_float4_to_u32(self.don_color)

        draw_list = slimgui.get_window_draw_list()
        window_width = slimgui.get_window_size()[0]
        window_height = slimgui.get_window_size()[1]

        object_radius = (window_width / 4 - stage_spacing * 2) / 2
        object_size = (object_radius * 2, object_radius if is_rect else object_radius * 2)

        window_pos = slimgui.get_window_pos()
        scroll_distance = (
            (window_height - object_size[1] / 2 - stage_spacing - window_height / 30) -
            (window_pos[1] - object_size[1] / 2)
        )

        note_vis_ms = 750 / scroll_speed
        
        for i, stage in enumerate(self.stages):
            x_center = window_pos[0] + stage_spacing + i * (window_width / 4) + object_size[0] / 2
            
            for object_time in stage.objects:
                if time >= object_time or time < object_time - note_vis_ms:
                    continue

                t = (time - (object_time - note_vis_ms)) / note_vis_ms

                y_center = (window_pos[1] - object_size[1] / 2) + scroll_distance * t

                if is_rect:
                    draw_list.add_rect_filled(
                        (x_center - object_size[0] / 2, y_center - object_size[1] / 2),
                        (x_center + object_size[0] / 2, y_center + object_size[1] /2),
                        don_color if stage.type == TaikoManiaObjectType.DON else katsu_color,
                        5
                    )
                else:
                    draw_list.add_circle_filled(
                        (x_center, y_center),
                        object_radius,
                        don_color if stage.type == TaikoManiaObjectType.DON else katsu_color,
                        32
                    )
        
        for i, stage in enumerate(self.stages):
            if is_rect:
                draw_list.add_rect(
                    (window_pos[0] + (window_width / len(self.stages)) * i + stage_spacing,
                     window_pos[1] + window_height - object_size[1] - stage_spacing - window_height / 30),
                    (window_pos[0] + (window_width / len(self.stages)) * i + object_size[0] + stage_spacing,
                     window_pos[1] + window_height - stage_spacing - window_height / 30),
                    slimgui.color_convert_float4_to_u32((255/255.0, 255/255.0, 255/255.0, 255/255.0)),
                    5,
                    0,
                    3
                )
            else:
                draw_list.add_circle(
                    (window_pos[0] + (window_width / len(self.stages)) * i + object_radius + stage_spacing,
                     window_pos[1] + window_height - object_radius - stage_spacing - window_height / 30),
                    object_radius,
                    slimgui.color_convert_float4_to_u32((255/255.0, 255/255.0, 255/255.0, 255/255.0)),
                    32,
                    3
                )
    
    def initialize(self):
        """Initialize TaikoMania stages with beatmap data."""
        # Clear all stages
        for stage in self.stages: stage.clear_objects()

        # Update stage types based on playstyle
        # playstyle: 0=KDDK, 1=DKKD, 2=KKDD, 3=DDKK, 4=KDKD, 5=DKDK
        playstyle_stages = [
            [TaikoManiaObjectType.KATSU, TaikoManiaObjectType.DON, TaikoManiaObjectType.DON, TaikoManiaObjectType.KATSU],  # KDDK
            [TaikoManiaObjectType.DON, TaikoManiaObjectType.KATSU, TaikoManiaObjectType.KATSU, TaikoManiaObjectType.DON],  # DKKD
            [TaikoManiaObjectType.KATSU, TaikoManiaObjectType.KATSU, TaikoManiaObjectType.DON, TaikoManiaObjectType.DON],  # KKDD
            [TaikoManiaObjectType.DON, TaikoManiaObjectType.DON, TaikoManiaObjectType.KATSU, TaikoManiaObjectType.KATSU],  # DDKK
            [TaikoManiaObjectType.KATSU, TaikoManiaObjectType.DON, TaikoManiaObjectType.KATSU, TaikoManiaObjectType.DON],  # KDKD
            [TaikoManiaObjectType.DON, TaikoManiaObjectType.KATSU, TaikoManiaObjectType.DON, TaikoManiaObjectType.KATSU],  # DKDK
        ]
        
        # Set stage types based on current playstyle
        for i, stage_type in enumerate(playstyle_stages[self.playstyle]):
            self.stages[i].set_type(stage_type)
        

        INT_MIN = -2147483648
        last_don_time = INT_MIN
        last_katsu_time = INT_MIN
        is_last_don_stage_primary = False
        is_last_katsu_stage_primary = False
        is_don_stage_primary = True
        is_katsu_stage_primary = True

        beatmap = load_beatmap(Beatmap.path)
        if not beatmap:
            print(f"Failed to load beatmap! {Beatmap.path}")
            return

        for i, hit_object in enumerate(beatmap.hit_objects):
            if isinstance(hit_object, TaikoHit):
                object_type = TaikoManiaObjectType.KATSU if hit_object.is_katsu else TaikoManiaObjectType.DON
                is_large = hit_object.is_large and self._2k_finisher

                if ((is_large or object_type == TaikoManiaObjectType.DON) and 
                    last_don_time != INT_MIN and
                    60000 / max(min(hit_object.start_time - last_don_time, 60000), 1) / 4 >= self.alternate_bpm):
                    is_don_stage_primary = not is_last_don_stage_primary
                elif ((is_large or object_type == TaikoManiaObjectType.KATSU) and 
                      last_katsu_time != INT_MIN and
                      60000 / max(min(hit_object.start_time - last_katsu_time, 60000), 1) / 4 >= self.alternate_bpm):
                    is_katsu_stage_primary = not is_last_katsu_stage_primary

                # Add objects to stages
                if object_type == TaikoManiaObjectType.DON:
                    if is_large:
                        # Large don goes to both don stages
                        don_stages = [stage_idx for stage_idx in range(4) if self.stages[stage_idx].type == TaikoManiaObjectType.DON]
                        for stage_idx in don_stages:
                            self.stages[stage_idx].add_object(hit_object.start_time)
                    elif is_don_stage_primary:
                        # Find first don stage
                        for stage_idx in range(4):
                            if self.stages[stage_idx].type == TaikoManiaObjectType.DON:
                                self.stages[stage_idx].add_object(hit_object.start_time)
                                break
                    else:
                        # Find second don stage
                        don_count = 0
                        for stage_idx in range(4):
                            if self.stages[stage_idx].type == TaikoManiaObjectType.DON:
                                don_count += 1
                                if don_count == 2:
                                    self.stages[stage_idx].add_object(hit_object.start_time)
                                    break
                    
                    last_don_time = hit_object.start_time
                    is_last_don_stage_primary = is_don_stage_primary
                else:  # KATSU
                    if is_large:
                        # Large katsu goes to both katsu stages
                        katsu_stages = [stage_idx for stage_idx in range(4) if self.stages[stage_idx].type == TaikoManiaObjectType.KATSU]
                        for stage_idx in katsu_stages:
                            self.stages[stage_idx].add_object(hit_object.start_time)
                    elif is_katsu_stage_primary:
                        # Find first katsu stage
                        for stage_idx in range(4):
                            if self.stages[stage_idx].type == TaikoManiaObjectType.KATSU:
                                self.stages[stage_idx].add_object(hit_object.start_time)
                                break
                    else:
                        # Find second katsu stage
                        katsu_count = 0
                        for stage_idx in range(4):
                            if self.stages[stage_idx].type == TaikoManiaObjectType.KATSU:
                                katsu_count += 1
                                if katsu_count == 2:
                                    self.stages[stage_idx].add_object(hit_object.start_time)
                                    break
                    
                    last_katsu_time = hit_object.start_time
                    is_last_katsu_stage_primary = is_katsu_stage_primary

            elif isinstance(hit_object, TaikoDrumroll):
                # Taiko drumrolls (sliders) - always DON notes
                min_hit_delay = int(beatmap.calculate_taiko_drumroll_tick_delay(hit_object.start_time))
                end_point_hittable = True

                # Check if end point is hittable based on next object timing
                if i < len(beatmap.hit_objects) - 1:
                    next_hit_object = beatmap.hit_objects[i + 1]
                    hittable_start_time = next_hit_object.start_time - min_hit_delay

                    if hittable_start_time - (hit_object.end_time + min_hit_delay) < min_hit_delay:
                        end_point_hittable = False
                
                hittable_end_time = hit_object.end_time + (min_hit_delay if end_point_hittable else 0)

                count = 0
                for current_time in range(hit_object.start_time, hittable_end_time, min_hit_delay):
                    if count % 2:
                        # Primary DON stage (first don stage)
                        for stage_idx in range(4):
                            if self.stages[stage_idx].type == TaikoManiaObjectType.DON:
                                self.stages[stage_idx].add_object(current_time)
                                break
                    else:
                        # Secondary DON stage (second don stage)
                        don_count = 0
                        for stage_idx in range(4):
                            if self.stages[stage_idx].type == TaikoManiaObjectType.DON:
                                don_count += 1
                                if don_count == 2:
                                    self.stages[stage_idx].add_object(current_time)
                                    break
                    count += 1
                
                # Update last don time for stage alternation (use end time)
                last_don_time = hit_object.end_time
                is_last_don_stage_primary = is_don_stage_primary

            elif isinstance(hit_object, TaikoSwell):
                # Taiko swell (denden) - spinners
                duration = hit_object.duration
                if duration > 0:
                    hits_required = beatmap.calculate_taiko_spinner_hits_required(duration)
                    
                    # Distribute hits evenly across spinner duration
                    if hits_required <= 1:
                        hit_times = [hit_object.start_time + duration // 2]
                    else:
                        hit_interval = duration / (hits_required - 1)
                        hit_times = [hit_object.start_time + int(i * hit_interval) for i in range(hits_required)]

                    # Generate spinner hits with pattern based on playstyle
                    for count, hit_time in enumerate(hit_times):
                        spinner_patterns = [
                            [0, 1, 3, 2],  # KDDK: K(0), D(1), K(3), D(2)
                            [0, 1, 3, 2],  # DKKD: D(0), K(1), D(3), K(2)
                            [0, 2, 3, 1],  # KKDD: K(0), D(2), D(3), K(1)
                            [0, 2, 3, 1],  # DDKK: D(0), K(2), K(3), D(1)
                            [0, 1, 2, 3],  # KDKD: K(0), D(1), K(2), D(3)
                            [0, 1, 2, 3],  # DKDK: D(0), K(1), D(2), K(3)
                        ]
                        stage_pattern = spinner_patterns[self.playstyle]
                        stage_index = stage_pattern[count % 4]

                        self.stages[stage_index].add_object(hit_time)


# Register the feature
register_feature(Feature())