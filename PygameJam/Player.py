# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 16:27:02 2024

@author: Noble
"""

import pygame

import math

from loguru import logger

class Player:
    def __init__(self, mass, x, y, vx, vy, G):
        # define variables
        self.mass = mass
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.G = G

class Planet:
    def __init__(self, mass, radius, x, y, vx):
        self.mass = mass
        self.radius = radius
        self.x = x
        self.y = y
        self.vx = vx