#!/usr/bin/env python
# -*- coding: utf-8 -*-

import simplegui
import random
import math

secret_number = 0
maxrange = 100
maxguess = 0

# helper function to start and restart the game
def new_game():
    global secret_number
    secret_number = random.randrange(0, maxrange)
    global maxguess
    maxguess = int(math.ceil(math.log(maxrange+1, 2)))
    print
    print 'New game starts with secret number set to range: 0 - ' + str(maxrange)
    print 'Number of remaining guesses is ' + str(maxguess)

# define event handlers for control panel
def range100():
    # button that changes the range to [0,100) and starts a new game 
    global maxrange
    maxrange = 100
    new_game()

def range1000():
    # button that changes the range to [0,1000) and starts a new game     
    global maxrange
    maxrange = 1000
    new_game()
    
def input_guess(guess):
    
    # print guess number
    print
    guess = int(guess)
    print 'Guess was ' + str(guess)
    
    # print remaining guesses
    global maxguess
    maxguess = maxguess -1
    print 'Number of remaining guesses is ' + str(maxguess)
    
    # compare guess number with secret number
    if guess == secret_number:
        print 'Correct!'
        new_game()
    else:
        if maxguess == 0:
            print 'You ran out of guesses.  The number was ' + str(secret_number)
            new_game()
        if guess < secret_number:
            print 'Higher'
        else:
            print 'Lower'
    
# create frame
frame = simplegui.create_frame("Guess the number", 300, 300)
inp = frame.add_input("Input your guess", input_guess, 50)
rang100_button = frame.add_button("Range: 0 - 100", range100)
rang1000_button = frame.add_button("Range: 0 - 1000", range1000)

# register event handlers for control elements and start frame
frame.start()

# call new_game 
new_game()

