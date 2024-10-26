# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 16:30:11 2024

@author: Noble
"""

import pygame

import math

from loguru import logger

class Planet:
    def __init__(self, mass, radius, x, y, vx, dt):
        self.mass = mass
        self.radius = radius
        self.x = x
        self.y = y
        self.vx = vx
        self.dt = dt
    
    # move the planet by the x velocity of the scene
    def moveplanet(self, x, vx):
        self.x += vx * self.dt