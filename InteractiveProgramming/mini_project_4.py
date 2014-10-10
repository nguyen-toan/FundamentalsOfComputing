#!/bin/env python
# -*- coding: utf-8 -*-

import simplegui

# define global variables
time_in_seconds = 0
total_stops = 0
whole_stops = 0
interval = 100
running_state = False

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    """
    Returns a string of the form A:BC.D 
    where A, C and D are digits in the range 0-9 
    and B is in the range 0-5.
    """
    D = t % 10
    ABC = (t - D) / 10
    A = ABC / 60
    BC = ABC % 60
    B = BC / 10
    C = BC % 10
    return str(A) + ':' + str(B) + str(C) + '.' + str(D)
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    global running_state, timer
    running_state = True
    timer.start()

def stop():
    global running_state, timer, time_in_seconds
    global total_stops, whole_stops
    timer.stop()
    running_state = False
    total_stops += 1
    if time_in_seconds % 10 == 0:
        whole_stops += 1

def reset():
    global time_in_seconds, total_stops, whole_stops
    stop()
    time_in_seconds = total_stops = whole_stops = 0

# define event handler for timer with 0.1 sec interval
def tick():
    global time_in_seconds
    if not running_state:
        timer.stop()
    else:
        time_in_seconds += 1

# define draw handler
def draw(canvas):
    global time_in_seconds
    canvas.draw_text(format(time_in_seconds), [60, 130], 40, 'White')
    canvas.draw_text(str(whole_stops)+'/'+str(total_stops), [110, 40], 30, 'Red')
    
# create frame
frame = simplegui.create_frame("Timer", 200, 200)

# register event handlers
frame.set_draw_handler(draw)
start_button = frame.add_button("Start", start, 100)
stop_button = frame.add_button("Stop", stop, 100)
reset_button = frame.add_button("Reset", reset, 100)
timer = simplegui.create_timer(interval, tick)

# start frame
frame.start()
timer.start()
