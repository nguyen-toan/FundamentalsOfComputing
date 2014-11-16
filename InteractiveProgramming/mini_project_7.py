#!/bin/env python
# -*- coding: utf-8 -*-

# implementation of Spaceship
import simplegui
import math
import random

# globals for user interface
width = 800
height = 600
score = 0
lives = 3
time = 0
started = False
explosion_group = set([])
unloaded = 0

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://dipanjans.github.io/games/asteroids/img/debris3_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://dipanjans.github.io/games/asteroids/img/nebula_blue.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://dipanjans.github.io/games/asteroids/img/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://dipanjans.github.io/games/asteroids/img/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5, 5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://dipanjans.github.io/games/asteroids/img/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://dipanjans.github.io/games/asteroids/img/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://dipanjans.github.io/games/asteroids/img/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
# .ogg versions of sounds are also available, just replace .mp3 by .ogg
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0]-q[0])**2 + (p[1]-q[1])**2)


# Ship class
class Ship:
    
    def __init__(self, pos, vel, angle, image, info):
        self.pos = pos
        self.vel = vel
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        forward = []
        
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    
    def draw(self,canvas):
        if self.thrust:
            canvas.draw_image(self.image, [self.image_center[0]+90,self.image_center[1]], self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)

    def update(self):
        global forward
        
        self.pos[0] = (self.pos[0] + self.vel[0]) % width
        self.pos[1] = (self.pos[1] + self.vel[1]) % height
            
        self.angle += self.angle_vel
        self.vel[0] *= 0.95
        self.vel[1] *= 0.95
        forward = angle_to_vector(self.angle)
        
        if self.thrust:
            self.vel[0] += 0.7 * forward[0]
            self.vel[1] += 0.7 * forward[1]
        
    def dec_angle_vel(self):
        self.angle_vel -= 0.1
        
    def inc_angle_vel(self):
        self.angle_vel += 0.1
    
    def update_thrust(self,thrust):
        self.thrust = thrust
        if self.thrust:
            ship_thrust_sound.rewind()
            ship_thrust_sound.play()   
        else:
            ship_thrust_sound.pause()
        
    def shoot(self):
        global missile_group, forward
        
        missile_pos = [self.pos[0] + self.radius * forward[0], self.pos[1] + self.radius * forward[1]]
        missile_vel = [self.vel[0] + 5 * forward[0], self.vel[1] + 5 * forward[1]]
        a_missile = Sprite(missile_pos, missile_vel, self.angle, 0, missile_image, missile_info, missile_sound)
        missile_group.add(a_missile)


# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = pos
        self.vel = vel
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def get_position(self):
        return self.pos
    
    def get_velocity(self):
        return self.velocity
    
    def get_radius(self):
        return self.radius
    
    def draw(self, canvas):
        if self.animatedTrue:
            index = (self.age % self.lifespan) // 1
            center = [64 + index * 128, 64]
            canvas.draw_image(self.image, center, self.image_size,
                          self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size,
                          self.pos, self.image_size, self.angle)

    def update(self):
        # update angle
        self.angle += self.angle_vel
        
        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % width
        self.pos[1] = (self.pos[1] + self.vel[1]) % height
        
        #update age
        self.age += 1
        
        if self.age < self.lifespan:
            return True
        else:
            return False

    def collide(self, other_object):
        position_from = self.pos
        position_to = other_object.get_position()
        radius_of_from = self.radius
        radius_of_to = other_object.get_radius()
        
        current_distance_between = dist(position_from,position_to)
        non_collision_distance = radius_of_from + radius_of_to
        
        if current_distance_between <= non_collision_distance:
            return True
        else:
            return False
        

# key handlers to control ship   
def keydown(key):
    if key == simplegui.KEY_MAP["space"]:
        my_ship.shoot()
    if key == simplegui.KEY_MAP["up"]:
        my_ship.update_thrust(True)
    if key == simplegui.KEY_MAP["left"]:
        my_ship.dec_angle_vel()  
    if key == simplegui.KEY_MAP["right"]:
        my_ship.inc_angle_vel()

def keyup(key):
    if key == simplegui.KEY_MAP["left"]:
        my_ship.inc_angle_vel()  
    if key == simplegui.KEY_MAP["right"]:
        my_ship.dec_angle_vel()
    if key == simplegui.KEY_MAP["up"]:
        my_ship.update_thrust(False)

# helper functions for sprites
def process_sprite_group(sprite_group, canvas):
    for sprite in sprite_group:
        val = sprite.update()
        if val:
            sprite.draw(canvas)
        else:
            sprite_group.discard(sprite)
        
def group_collide(sprite_group, other_object):
    global explosion_group
    count = 0
    for sprite in sprite_group:
        if sprite.collide(other_object):
            explosion = Sprite(sprite.get_position(), [0, 0], 0, 0, explosion_image, explosion_info, explosion_sound)
            explosion_group.add(explosion)
            sprite_group.discard(sprite)
            count = count + 1
    return count

def group_group_collide(sprite_group1, sprite_group2):
    hits = 0
    for sprite in sprite_group1:
        if group_collide(sprite_group2, sprite) > 0:
            sprite_group1.discard(sprite)
            hits += 1
    return hits

# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started, unloaded, score, lives, rock_group, missile_group, explosion_group, soundtrack
    center = [width / 2, height / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        if unloaded == 0:
            started = True
            score = 0
            lives = 3
            rock_group = set([])
            missile_group = set([])
            explosion_group = set([])
            soundtrack.rewind()

def draw(canvas):
    global time, started, lives, score, rock_group, missile_group, explosion_group, unloaded
    
    # animiate background
    time += 1
    unloaded = 0
    
    if nebula_image.get_width() == 0 or nebula_image.get_height() == 0:
        unloaded += 1
    if debris_image.get_width() == 0 or debris_image.get_height() == 0:
        unloaded += 1
    if ship_image.get_width() == 0 or ship_image.get_height() == 0:
        unloaded += 1
    if splash_image.get_width() == 0 or splash_image.get_height() == 0:
        unloaded += 1 
    if missile_image.get_width() == 0 or missile_image.get_height() == 0:
        unloaded += 1
    if asteroid_image.get_width() == 0 or asteroid_image.get_height() == 0:
        unloaded += 1
    if explosion_image.get_width() == 0 or explosion_image.get_height() == 0:
        unloaded += 1
    
    if unloaded > 0:
        canvas.draw_text("Please wait, "+str(unloaded)+" images left to be loaded", (70, 100), 30, "White")
            
    else:
        center = debris_info.get_center()
        size = debris_info.get_size()
        wtime = (time / 8) % center[0]
        canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [width/2, height/2], [width, height])
        canvas.draw_image(debris_image, [center[0]-wtime, center[1]], [size[0] - 2*wtime, size[1]], 
                                    [width/2 + 1.25*wtime, height/2], [width - 2.5*wtime, height])
        canvas.draw_image(debris_image, [size[0]-wtime, center[1]], [2*wtime, size[1]], 
                                    [1.25*wtime, height/2], [2.5*wtime, height])

        # draw UI
        canvas.draw_text("Lives: "+str(lives), (10, 30), 20, "White")
        canvas.draw_text("Score: "+str(score), (620, 30), 20, "White")
        
        if score < 200:
            canvas.draw_text("Level: Nice and Easy", (300, 30), 20, "White")
        if (score > 200) and (score < 500):
            canvas.draw_text("Level: Watch out!", (300, 30), 20, "Maroon")
        if score > 500:
            canvas.draw_text("Level: Doom surely awaits you!", (230, 30), 20, "Red")
    
        # draw ship and sprites
        my_ship.draw(canvas)
    
        if started:
            process_sprite_group(missile_group, canvas)
            process_sprite_group(rock_group, canvas)
            process_sprite_group(explosion_group,canvas)
            soundtrack.play()
            # update ship and sprites
            my_ship.update()

        if group_collide(rock_group,my_ship) > 0:
            lives = lives - 1
            if lives == 0:
                started = False
                
        score += (group_group_collide(missile_group, rock_group) * 10)
        
        # draw splash screen if not started
        if not started:
            canvas.draw_image(splash_image, splash_info.get_center(), 
                              splash_info.get_size(), [width/2, height/2], 
                              splash_info.get_size())

# timer handler that spawns a rock    
def rock_spawner():
    global rock_group, my_ship, score
    vel = [1, 1]
    ship_pos = my_ship.get_position()
    lpos0 = int(ship_pos[0] - 80)
    rpos0 = int(ship_pos[0] + 80)
    lpos1 = int(ship_pos[1] - 80)
    rpos1 = int(ship_pos[1] + 80)
    
    if lpos0 < 0:
        lpos0 += 80
    if rpos0 > width:
        rpos0 -= 80
    if lpos1 < 0:
        lpos1 += 80
    if rpos1 > height:
        rpos1 -= 80
        
    pos = [random.choice([random.randrange(0, lpos0), random.randrange(rpos0, width)]), random.choice([random.randrange(0, lpos1), random.randrange(rpos1, height)])]
    if score < 200:
        vel = [random.choice([random.randrange(1, 2), -random.randrange(1,2)]), random.choice([random.randrange(1, 2), -random.randrange(1, 2)])]
    if score > 200 and score < 500:
        vel = [random.choice([random.randrange(1, 3), -random.randrange(1,3)]), random.choice([random.randrange(1, 3), -random.randrange(1, 3)])]
    if score > 500:
        vel = [random.choice([random.randrange(3, 6), -random.randrange(3,6)]), random.choice([random.randrange(3, 6), -random.randrange(3, 6)])]
    
    ang_vel = random.choice([(-random.random()) * (0.1-0.05) - 0.05, (random.random()) * (0.1-0.05) + 0.05])
    a_rock = Sprite(pos, vel, 0, ang_vel, asteroid_image, asteroid_info)
    if len(rock_group) < 12:
        rock_group.add(a_rock)

# initialize stuff
frame = simplegui.create_frame("Asteroids", width, height)

# initialize ship and two sprites
my_ship = Ship([width / 2, height / 2], [0, 0], 0, ship_image, ship_info)
rock_group = set([])
missile_group = set([])

# register handlers
frame.set_keyup_handler(keyup)
frame.set_keydown_handler(keydown)
frame.set_mouseclick_handler(click)
frame.set_draw_handler(draw)
frame.add_label("SHIP CONTOLS")
frame.add_label("1. UP - moves ship forward")
frame.add_label("2. LEFT - turns ship left")
frame.add_label("3. RIGHT - turns ship right")
frame.add_label("4. SPACE - fires missile")

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
