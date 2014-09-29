#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Rock-paper-scissors-lizard-Spock template

# The key idea of this program is to equate the strings
# "rock", "paper", "scissors", "lizard", "Spock" to numbers
# as follows:
#
# 0 - rock
# 1 - Spock
# 2 - paper
# 3 - lizard
# 4 - scissors

import random

# helper functions

def name_to_number(name):
    num = -1
    if name == 'rock':
        num = 0
    elif name == 'Spock':
        num = 1
    elif name == 'paper':
        num = 2
    elif name == 'lizard':
        num = 3
    elif name == 'scissors':
        num = 4
    else:
        num = "Invalid name"
    return num


def number_to_name(number):
    name = ""
    if number == 0:
        name = 'rock'
    elif number == 1:
        name = 'Spock'
    elif number == 2:
        name = 'paper'
    elif number == 3:
        name = 'lizard'
    elif number == 4:
        name = 'scissors'
    else:
        name = "Invalid number"
    return name
    

def rpsls(player_choice):     
    print ''
    print 'Player chooses ' + player_choice
    player_number = name_to_number(player_choice)
    comp_number = random.randrange(5)
    comp_choice = number_to_name(comp_number)
    print 'Computer chooses ' + comp_choice
    diff_number = (comp_number - player_number) % 5
    if diff_number > 0:
        print 'Computer wins!'
    elif diff_number < 0:
        print 'Player wins!'
    else:
        print 'Player and computer tie!'
    
# test
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")

