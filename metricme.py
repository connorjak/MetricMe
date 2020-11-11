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
# import os
from sys import platform
# import subprocess
# import signal
# import psutil
# from shutil import copyfile
import json

import ImguiExtensions as imgui_ex

# Things you probably need to pip3 install:
# imgui[pyglet] psutil

# # initilize imgui context (see documentation)
# imgui.create_context()
# imgui.get_io().display_size = 100, 100
# imgui.get_io().fonts.get_tex_data_as_rgba32()

#######################################
### GLOBALS ###########################
newName = ""
newNum = 0.0
newDenom = 7.0
newMin = 0.0
newMax = 1.0

#######################################
### Actions ###########################


#######################################
### UI PORTIONS #######################


#######################################
### UI UPDATE #########################

def ui_update(width, height, fonts):
    global newName
    global newNum
    global newDenom
    global newMin
    global newMax

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
    imgui.begin("MetricMe", True)
    
    imgui.text("Add Metric")

    wasChanged1, newName = imgui.input_text("Name", newName, 30)
    wasChanged2, newNum = imgui.input_text("Numerator", newNum, 150)
    wasChanged3, newDenom = imgui.input_text("Denominator", newDenom, 150)
    wasChanged4, newMin = imgui.input_text("Min", newMin, 150)
    wasChanged4, newMax = imgui.input_text("Max", newMax, 150)


    if(imgui.button("Add")):
        with open("userdata/metrics.json","r+") as metricsJSON:
            doc = json.load(metricsJSON)
            newMetric = {newName: {"Numerator": 1.0,
            "Denominator": 1.0, 
            "Min": 0.0,
            "Max": 0.0
            }}
            doc["metrics"].update(newMetric)

            #rewrite JSON
            metricsJSON.seek(0)
            metricsJSON.truncate()
            json.dump(doc, metricsJSON, indent = 4, sort_keys=True)


    imgui.separator()
    imgui.text("My Metrics")

    with open("userdata/metrics.json") as metricsJSON:
        metrics = json.load(metricsJSON)["metrics"]
        # print(metrics)
        for metric in metrics:
            imgui.text(metric)
    
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