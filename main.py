import glfw
from OpenGL import GL
import slimgui.imgui as slimgui
import slimgui.integrations.glfw as imgui_glfw

from sdk.ui.core import UI
from sdk.memory import Memory


def main():
    if not glfw.init():
        raise RuntimeError("Failed to initialize GLFW")

    # create window
    glfw.window_hint(glfw.DECORATED, False)
    glfw.window_hint(glfw.RESIZABLE, False)
    window = glfw.create_window(1280, 720, "osu!vision", None, None)
    glfw.make_context_current(window)
    glfw.swap_interval(0)

    # create imgui context
    ctx = slimgui.create_context()

    # create imgui renderer
    renderer = imgui_glfw.GlfwRenderer(window)

    # Pass both renderer + context into UI
    ui = UI(renderer, ctx, window)

    # Init memory
    try:
        memory = Memory()  # This will initialize the singleton
        print("Memory initialized successfully")
    except Exception as e:
        print(f"Failed to initialize memory: {e}")
        print("Make sure osu! is running and signatures.json exists")
        exit(1)

    # import features (auto-register on import)
    import features.taikomania.taikomania
    import features.mania.mania
    import features.debug

    # main loop
    while not glfw.window_should_close(window):
        glfw.poll_events()

        ui.new_frame()
        ui.render()

        GL.glClearColor(0.1, 0.1, 0.1, 1.0)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)

        fb_width, fb_height = glfw.get_framebuffer_size(window)
        slimgui.get_io().display_size = (fb_width, fb_height)

        renderer.render(slimgui.get_draw_data())
        glfw.swap_buffers(window)

    renderer.shutdown()
    slimgui.destroy_context(ctx)
    glfw.terminate()


if __name__ == "__main__":
    main()
