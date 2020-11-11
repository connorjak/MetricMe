# -*- coding: utf-8 -*-

# MetricMe

# Assumptions/Disclaimers:
# - 

# TODO:
# - 

# TODO BREAKING:
# - (none)

#######################################
### SETUP / PREREQUISITES #############

#######################################
### IMPORTS ###########################


# from __future__ import absolute_import
import pyglet
from pyglet import gl
import imgui
from imgui.integrations.pyglet import PygletRenderer
import os
from sys import platform
import subprocess
import signal
import psutil
from shutil import copyfile

import ImguiExtensions as imgui_ex

# Things you probably need to pip3 install:
# imgui[pyglet] psutil

# # initilize imgui context (see documentation)
# imgui.create_context()
# imgui.get_io().display_size = 100, 100
# imgui.get_io().fonts.get_tex_data_as_rgba32()

#######################################
### GLOBALS ###########################


#######################################
### Actions ###########################


#######################################
### UI PORTIONS #######################

    # os.chdir(oldpath)

#######################################
### UI UPDATE #########################

def ui_update(width, height, fonts):
    global currentMode

    imgui.new_frame()

    # Set font
    fonts.pushBodyFont()

    if imgui.begin_main_menu_bar():
        if imgui.begin_menu("File", True):

            clicked_quit, selected_quit = imgui.menu_item(
                "Quit", 'Cmd+Q', False, True
            )

            if clicked_quit:
                exit(0)

            imgui.end_menu()
        imgui.end_main_menu_bar()

    # imgui.show_test_window()
    imgui.set_next_window_size(width, height - imgui.get_text_line_height_with_spacing())
    imgui.set_next_window_position(0,imgui.get_text_line_height_with_spacing())
    imgui.begin("Test", True)
    
    # clicked, currentMode = imgui.combo(
    #     "Server Mode", currentMode, ["Clientless", "ShortCircuitOneClient", "Launcher", "ServerHandlerAPI"]
    # )



    imgui.text("MetricMe")

    
    imgui.end()

    fonts.popFont()

#######################################
### MAIN ##############################

def main():
    window = pyglet.window.Window(width=1280, height=720, resizable=True)
    gl.glClearColor(0.3, 0.3, 0.3, 1)
    imgui.create_context()
    impl = PygletRenderer(window)
    
    # Load font
    fonts = imgui_ex.ImguiFontSet()
    impl.refresh_font_texture()

    def update(dt, width, height):
        ui_update(width, height, fonts)
    @window.event
    def on_draw():
        width, height = window.get_size()
        update(1/2.0, width, height) #TODO support higher refresh? was 1/60.0 originally
        window.clear()
        imgui.render()
        impl.render(imgui.get_draw_data())
    
    pyglet.app.run()
    impl.shutdown()
if __name__ == "__main__":
    main()