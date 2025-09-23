import glfw
import slimgui.imgui as slimgui

from . import manager
from .native_drag import sysmove


class UI:
    def __init__(self, impl=None, ctx=None, window=None):
        self.impl = impl
        self.ctx = ctx
        self.window = window

    def new_frame(self):
        if self.impl:
            self.impl.new_frame()
        slimgui.new_frame()

    def render(self):
        features = manager.get_features()

        # --- Global Menu Bar ---
        if slimgui.begin_main_menu_bar():
            # App menu
            if slimgui.begin_menu("osu!vision"):
                if slimgui.menu_item("Exit")[0]:
                    glfw.set_window_should_close(self.window, True)
                slimgui.end_menu()

            slimgui.separator()

            # Feature menus
            for feature in features:
                menu_info = feature.get_menu()
                if isinstance(menu_info, tuple):
                    menu_name, menu_func = menu_info
                    if slimgui.begin_menu(menu_name):
                        menu_func()
                        slimgui.end_menu()
                else:
                    menu_name = menu_info
                    if slimgui.menu_item(menu_name)[0]:
                        feature.draw_menu()

            # --- Drag Zone ---
            bar_pos = slimgui.get_window_pos()
            bar_w, bar_h = slimgui.get_window_size()
            cur_x = slimgui.get_cursor_pos_x()

            btn_size = (30, bar_h - 2)
            control_w = 3 * btn_size[0]

            empty_w = (bar_w - control_w) - cur_x
            if empty_w > 0:
                x0 = bar_pos[0] + cur_x
                y0 = bar_pos[1]
                x1 = bar_pos[0] + cur_x + empty_w
                y1 = bar_pos[1] + bar_h

                mx, my = slimgui.get_mouse_pos()
                if (
                    slimgui.is_window_hovered()
                    and not slimgui.is_any_item_hovered()
                    and x0 <= mx <= x1 and y0 <= my <= y1
                    and slimgui.is_mouse_clicked(0)
                    and self.window is not None
                ):
                    hwnd = glfw.get_win32_window(self.window)
                    sysmove(hwnd)

            # --- Right-align the window controls ---
            slimgui.same_line(bar_w - control_w - 12)

            # Flat style overrides
            slimgui.push_style_var(slimgui.StyleVar.FRAME_ROUNDING, 0.0)
            slimgui.push_style_var(slimgui.StyleVar.FRAME_PADDING, (4, 2))
            slimgui.push_style_var(slimgui.StyleVar.ITEM_SPACING, (0, 0))

            slimgui.push_style_color(slimgui.Col.BUTTON, (0.1, 0.1, 0.1, 1.0))
            slimgui.push_style_color(slimgui.Col.BUTTON_HOVERED, (0.2, 0.2, 0.2, 1.0))
            slimgui.push_style_color(slimgui.Col.BUTTON_ACTIVE, (0.3, 0.3, 0.3, 1.0))

            # Minimize
            if slimgui.button("_", btn_size):
                glfw.iconify_window(self.window)

            slimgui.same_line()

            # Maximize / Restore
            label = "[ ]" if glfw.get_window_attrib(self.window, glfw.MAXIMIZED) else "[]"
            if slimgui.button(label, btn_size):
                if glfw.get_window_attrib(self.window, glfw.MAXIMIZED):
                    glfw.restore_window(self.window)
                else:
                    glfw.maximize_window(self.window)

            slimgui.same_line()

            # Close (with red hover/active)
            slimgui.push_style_color(slimgui.Col.BUTTON_HOVERED, (0.8, 0.2, 0.2, 1.0))
            slimgui.push_style_color(slimgui.Col.BUTTON_ACTIVE, (0.9, 0.1, 0.1, 1.0))
            if slimgui.button("X", btn_size):
                glfw.set_window_should_close(self.window, True)
            slimgui.pop_style_color(2)

            # Restore styles
            slimgui.pop_style_color(3)
            slimgui.pop_style_var(3)

            slimgui.end_main_menu_bar()

        # --- Feature Windows ---
        for feature in features:
            if hasattr(feature, "draw_windows"):
                feature.draw_windows()

        # --- Feature Overlays ---
        for feature in features:
            if hasattr(feature, "draw_overlay"):
                feature.draw_overlay()

        slimgui.render()
