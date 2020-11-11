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
    
    fonts.pushHeadingFont()
    imgui.text("Add Metric")
    fonts.popFont()
    imgui.separator()

    wasChanged1, newName = imgui.input_text("Name", newName, 30)
    wasChanged2, newNum = imgui.input_double("Numerator", newNum)
    wasChanged3, newDenom = imgui.input_double("Denominator", newDenom)
    wasChanged4, newMin = imgui.input_double("Min", newMin)
    wasChanged5, newMax = imgui.input_double("Max", newMax)

    if(newNum<0.0):
        newNum = 0.0
    if(newDenom<0.00000001):
        newDenom = 1.0
    if(newMin<0.0):
        newMin = 0.0
    if(newMax<0.00000001):
        newMax = 0.00000001

    if(imgui.button("Add")):
        with open("userdata/metrics.json","r+") as metricsJSON:
            doc = json.load(metricsJSON)
            newMetric = {"Name": newName,
            "Numerator": newNum,
            "Denominator": newDenom, 
            "Min": newMin,
            "Max": newMax
            }
            doc["metrics"].append(newMetric)

            #rewrite JSON
            metricsJSON.seek(0)
            metricsJSON.truncate()
            json.dump(doc, metricsJSON, indent = 4, sort_keys=True)


    imgui.separator()
    fonts.pushHeadingFont()
    imgui.text("My Metrics")
    fonts.popFont()
    imgui.separator()

    with open("userdata/metrics.json","r+") as metricsJSON:
        doc = json.load(metricsJSON)
        metrics = doc["metrics"]
        # print(metrics)
        for metric in metrics:
            name = metric["Name"]
            imgui.text(name)
            imgui.indent()
            num = metric["Numerator"]
            den = metric["Denominator"]
            min = metric["Min"]
            max = metric["Max"]
            frac = num/den

            imgui.slider_float(str(num) + "/" + str(den), frac, min, max, format="")
            imgui.unindent()

            if(imgui.button("-")):
                metric["Numerator"] = num - 1

                #rewrite JSON
                metricsJSON.seek(0)
                metricsJSON.truncate()
                json.dump(doc, metricsJSON, indent = 4, sort_keys=True)
            imgui.same_line()
            if(imgui.button("+")):
                metric["Numerator"] = num + 1

                #rewrite JSON
                metricsJSON.seek(0)
                metricsJSON.truncate()
                json.dump(doc, metricsJSON, indent = 4, sort_keys=True)
                
    
    imgui.end()

    fonts.popFont()

#######################################
### MAIN ##############################

def main():
    window = pyglet.window.Window(width=360, height=480, resizable=True)
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