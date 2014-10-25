#!/bin/env python
# -*- coding: utf-8 -*-

# implementation of card game - Memory

import simplegui
import random

# helper function to initialize globals
def new_game():
    global cards, exposed, state, turns
    state = 0
    turns = 0
    exposed = [False for _ in range(16)]
    cards = range(8) + range(8)
    random.shuffle(cards)
    print cards

     
# define event handlers
def mouseclick(pos):
    global state, first_index, second_index, turns
    
    for i, card in enumerate(cards):
        if 50*i < pos[0] < 50*(i+1) and 0 < pos[1] < 100:
            if not exposed[i]:
                exposed[i] = True
                if state == 0:
                    first_index = i
                elif state == 1:
                    second_index = i
                    turns += 1
                    label.set_text("Turns = " + str(turns))
                elif state == 2:
                    if cards[second_index] == cards[first_index]:
                        pass
                    else:
                        exposed[second_index], exposed[first_index] = False, False
                    first_index = i
                    state = 0
                state += 1
            else:
                pass

# cards are logically 50x100 pixels in size
def draw(canvas):
    global cards
    for i, card in enumerate(cards):
        if exposed[i]:
            canvas.draw_text(str(card+1), [i*50+20, 60], 26, "White")
        else:
            canvas.draw_polygon([(i*50, 0), ((i+1)*50, 0),
                                 ((i+1)*50, (i+1)*100), (i*50, 100)],
                                4, "White", "Green")


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game, 100)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()
