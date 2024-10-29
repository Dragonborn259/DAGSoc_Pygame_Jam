# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 16:47:10 2024

@author: Noble
"""

# import modules
import pygame

import math

import random

from loguru import logger

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

# initialise random number generator
random.seed()

# setup G
G = 6.67e-11

# player variables
player_pos = pygame.Vector2(screen.get_width() * 0.25, screen.get_height() * 0.5)
playerm = 1

# movement variables
ax = 0
ay = 0
vx = 0
vy = 11

# planet variables
planets = []
spawnplanet = True
spawnpoint = screen.get_width()/2

# monster variables
monster_x = 100
vmx = 100

def genplanet():
    size = random.uniform(0.5, 2)
    r = 30 * size
    m = 5.972e24 * size
    px = screen.get_width() + r/2
    py = screen.get_height() * random.uniform(0.25, 0.75)
    newplanet = [px, py, m, r]
    return newplanet

while running:
    for event in pygame.event.get():
        if ((event.type == pygame.QUIT) or
                (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)):
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")
    
    # set thrust
    Thrust = 40
    
    if len(planets) > 0:
        # delete any planets off the far edge of the screen
        if planets[0][0] <= -screen.get_width():
            del planets[0]
        # check if the last planet has passed the spawnpoint
        if planets[-1][0] <= spawnpoint:
            spawnplanet = True
            spawnpoint = screen.get_width() * random.uniform(0.45, 0.55)
                
    # draw the monster
    monster = pygame.Rect(0, 0, monster_x, screen.get_height())
    pygame.draw.rect(screen, 'red', monster)
    
    # generate planets
    if spawnplanet == True:
        planet = genplanet()
        planets.append(planet)
        spawnplanet = False
    
    # calculate gravitational forces
    if len(planets) > 0:
        for i in range(len(planets)):
            # find the distance and angle
            rx = planets[i][0] - player_pos.x
            ry = planets[i][1] - player_pos.y
            r = math.sqrt(rx**2 + ry**2)
            theta = math.atan2(ry, rx)
            
            # find gravitational force on the player
            F = G * playerm * planets[i][2] / (r*100000)**2
            Fx = F*math.cos(theta)
            Fy = F*math.sin(theta)
            
            # find acceleration and hence change velocity of player
            ax += Fx / playerm
            ay += Fy / playerm

    # take player input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        ay -= Thrust * dt
    if keys[pygame.K_s]:
        ay += Thrust * dt
    if keys[pygame.K_a]:
        ax -= Thrust * dt
    if keys[pygame.K_d]:
        ax += Thrust * dt

    vx += ax * dt
    vy += ay * dt
    
    if vx > 150:
        vx = 150
    if vy > 150:
        vy = 150
    
    # define the tracer
    tracer_pos = pygame.Vector2(player_pos.x, player_pos.y)
    vtx = vx
    vty = vy
    atx = ax
    aty = ay
    dtt = 0.1
    for i in range(1000):
        
        # calculate gravitational forces
        if len(planets) > 0:
            for i in range(len(planets)):
                
                # find the distance and angle
                rtx = planets[i][0] - tracer_pos.x
                rty = planets[i][1] - tracer_pos.y
                rt = math.sqrt(rtx**2 + rty**2)
                thetat = math.atan2(rty, rtx)
                
                # find gravitational force on the player
                Ft = G * playerm * planets[i][2] / (rt*100000)**2
                Ftx = Ft*math.cos(thetat)
                Fty = Ft*math.sin(thetat)
                
                # find acceleration and hence change velocity of player
                atx += Ftx / playerm
                aty += Fty / playerm
        
        if vtx > 150:
            vtx = 150
        if vty > 150:
            vty = 150
        
        # change the tracer's velocity by its acceleration
        vtx += atx * dt
        vty += aty * dt
        
        # change the tracer's position
        tracer_pos.x += vtx * dt
        tracer_pos.y += vty * dt
        
        # draw a dot at the tracer's position
        pygame.draw.circle(screen, 'white', tracer_pos, 1)
    
    # find the prograde, retrograde, radial in, and radial out directions
    alpha = math.atan2(vy,vx)
    
    # draw planets
    if len(planets) > 0:
        for i in range(len(planets)):
            planets[i][0] -= vx * dt
            planet_pos = pygame.Vector2(planets[i][0], planets[i][1])
            pygame.draw.circle(screen, 'blue', planet_pos, planets[i][3])
    
    # move player
    player_pos.y += vy * dt
    
    # move monster
    if monster_x <= 0.15:
        vmx = vx
    else:
        vmx = 90
        monster_x -= vx * dt
    monster_x += vmx * dt
    
    # draw player
    pygame.draw.circle(screen, 'red', player_pos, 5)
    
    pygame.display.flip()
    
    dt = (clock.tick(60) / 1000)
    
pygame.quit()