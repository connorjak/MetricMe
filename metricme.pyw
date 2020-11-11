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
import os
import sys

abspath = os.path.abspath(sys.argv[0])
dname = os.path.dirname(abspath)
os.chdir(dname)

#######################################
### IMPORTS ###########################


# from __future__ import absolute_import
import pyglet
from pyglet import gl
import imgui
from imgui.integrations.pyglet import PygletRenderer
# import os
# from sys import platform
# import subprocess
# import signal
# import psutil
from shutil import copyfile
import json
import time
from datetime import *

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
double_val = 3.0

#######################################
### Actions ###########################
def save():
    filename1 = datetime.now().strftime("%Y%m%d-%H%M%S")
    copyfile("userdata/metrics.json","userdata/metrics_"+str(filename1)+".json")

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
    global double_val

    imgui.new_frame()

    # Set font
    fonts.pushBodyFont()

    if imgui.begin_main_menu_bar():
        if imgui.begin_menu("File", True):

            clicked_save, selected_quit = imgui.menu_item(
                "Save", 'Cmd+S', False, True
            )

            clicked_quit, selected_quit = imgui.menu_item(
                "Quit", 'Cmd+Q', False, True
            )

            if clicked_save:
                save()

            if clicked_quit:
                exit(0)

            imgui.end_menu()
        if(imgui.button("Save")):
            save()
        imgui.end_main_menu_bar()

    # imgui.show_test_window()

    with open("userdata/metrics.json","r") as metricsJSON:
        doc = json.load(metricsJSON)
        year = doc["meta"]["StartYear"]
        month = doc["meta"]["StartMonth"]
        day = doc["meta"]["StartDay"]
        hour = doc["meta"]["StartHour"]
        startDate = datetime(year,month,day,hour)
        dateDelta = datetime.now() - startDate
        weekDecimal = dateDelta.seconds / (7.0*24*60*60)
        weekPercent = weekDecimal*100

    imgui.set_next_window_size(width, height - imgui.get_text_line_height_with_spacing())
    imgui.set_next_window_position(0,imgui.get_text_line_height_with_spacing())
    imgui.begin("MetricMe - Week Percentage: " + "{:.1f}".format(weekPercent) + "%", True)
    
    fonts.pushHeadingFont()
    imgui.text("Add Metric")
    fonts.popFont()
    imgui.separator()

    wasChanged1, newName = imgui.input_text("Name", newName, 30)
    wasChanged2, newNum = imgui.input_float("Numerator", newNum, step=1.0, format="%.3f")
    wasChanged3, newDenom = imgui.input_float("Denominator", newDenom, step=1.0, format="%.3f")
    wasChanged4, newMin = imgui.input_float("Min", newMin, step=1.0, format="%.3f")
    wasChanged5, newMax = imgui.input_float("Max", newMax, step=1.0, format="%.3f")

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

        imgui.slider_float("Week %", weekPercent, 0, 100, format="%.1f %%")
        imgui.text(doc["meta"]["Desc"])
        imgui.separator()

        metrics = doc["metrics"]
        # print(metrics)

        index = 0
        for metric in metrics:
            imgui.push_id(str(index))
            name = metric["Name"]
            imgui.text(name)
            # imgui.indent()
            num = metric["Numerator"]
            den = metric["Denominator"]
            min = metric["Min"]
            max = metric["Max"]
            frac = num/den

            #percentage of the way from min to max
            percent = 100 *  (frac-min)/(max-min) 

            if(percent < weekPercent):
                col = imgui_ex.rgba_color(0.3,0.1, 0.03)
                imgui.push_style_color(imgui.COLOR_FRAME_BACKGROUND, col.r,col.g,col.b)

            imgui.slider_float(str(num) + "/" + str(den), percent, 0, 100, format="%2.1f %%")
            
            if(percent < weekPercent):
                imgui.pop_style_color()

            wasChanged_, num = imgui.input_float("", num, step=1.0, format="%.3f")

            if(wasChanged_):
                doc["metrics"][index]["Numerator"] = num

                #rewrite JSON
                metricsJSON.seek(0)
                metricsJSON.truncate()
                json.dump(doc, metricsJSON, indent = 4, sort_keys=True)
            imgui.same_line()
            # if(imgui.button(" - ")):
            #     doc["metrics"][index]["Numerator"] = num - 1

            #     #rewrite JSON
            #     metricsJSON.seek(0)
            #     metricsJSON.truncate()
            #     json.dump(doc, metricsJSON, indent = 4, sort_keys=True)
            # imgui.same_line()
            # if(imgui.button(" + ")):
            #     doc["metrics"][index]["Numerator"] = num + 1

            #     #rewrite JSON
            #     metricsJSON.seek(0)
            #     metricsJSON.truncate()
            #     json.dump(doc, metricsJSON, indent = 4, sort_keys=True)
            # imgui.same_line(spacing=50)
            if(imgui.button("Delete")):
                doc["metrics"].pop(index)

                #rewrite JSON
                metricsJSON.seek(0)
                metricsJSON.truncate()
                json.dump(doc, metricsJSON, indent = 4, sort_keys=True)

            # imgui.unindent()
            # imgui.spacing()
            imgui.pop_id()
            imgui.separator()
            index += 1
                
    
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