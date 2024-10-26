# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 16:12:36 2024

@author: Noble
"""

# import modules
import pygame

import math

from loguru import logger

# import classes
from Player import Player

from Player import Planet

class Game:
    # name the game
    game_name: str = 'test name, please change'
    # set the screen size
    screen_size: tuple [int, int] = (1280, 720)
    # framerate cap
    fps: float = 60
    
    # create the game
    def __init__(self):
        logger.info("Initialising PyGame")
        pygame.init()

        # Create the screen
        self.screen: pygame.Surface = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption(self.game_name)

        # Run the main loop
        self.running: bool = True

        # time keeping for deltatime calculations
        self.clock: pygame.time.Clock = pygame.time.Clock()

        # time taken for last frame
        self.dt: float = 60
        
        # define other variables
        self.G = 1
        self.playerm = 1
        self.vx = 0
        self.vy = 0
        self.playerx = self.screen.get_width()*0.25
        self.playery = self.screen.get_height()*0.5
        self.players = []

        # define planet position variables
        self.planetx = self.screen.get_width()*0.75
        self.planety = self.screen.get_height()*0.75
        self.planets = []
        self.create_planet = True

    
    # Main update loop

    def update(self) -> None:
        # fill the screen with a color to wipe away anything from last frame
        self.screen.fill("black")
        
        # create the player
        player = Player(self.playerm, self.playerx, self.playery, self.vx, self.vy, self.G)
        self.players.append(player)
        if len(self.players) > 1:
            del(self.players[0])
        # draw the player
        pygame.draw.circle(self.screen, "red", (player.x, player.y), 5)
        
        if self.create_planet == True:
            # create planet
            NewPlanet = Planet(10, 60, self.planetx, self.planety, self.vx)
            # add planet to the array
            self.planets.append(NewPlanet)
            print(len(self.planets))
        
        # calculate gravitational effects on the player
        for i in range(len(self.planets)):
            # draw the planet
            pygame.draw.circle(self.screen, 'blue', [self.planets[i].x, self.planets[i].y], self.planets[i].radius)
            
            # find the distance and angle
            rx = player.x - self.planets[i].x
            ry = player.y - self.planets[i].y
            r = math.sqrt(rx**2 + ry**2)
            theta = math.atan2(ry, rx)
            
            # find gravitational force on the player
            F = self.G * player.mass * self.planets[i].mass / r
            Fx = F*math.cos(theta)
            Fy = F*math.sin(theta)
            
            # find acceleration and hence change velocity of player
            ax = Fx * player.mass * self.dt
            ay = Fy * player.mass * self.dt
            
            self.vx += ax * self.dt
            self.vy += ay * self.dt
            
        # move the player and the planets
        self.planetx += self.vx * self.dt
        self.playery += self.vy * self.dt
        
        self.create_planet = False
        
        # flip the screen
        pygame.display.flip()
        
        
    
    # Process a given event
    def process_event(self, event: pygame.event.Event) -> None:
        # logger.debug("Event: {}", event)
        if ((event.type == pygame.QUIT) or
                (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)):
            logger.warning("Game Exiting")
            self.running = False
        # More event code
    
    # Start the Game
    def run(self) -> None:
        logger.info("Starting Game")

        # Main Game loop
        while self.running:

            # Process events
            for event in pygame.event.get():
                self.process_event(event)

            # Run the update loop
            self.update()
            # Update the display
            pygame.display.flip()

            # Synchronise framerate to self.fps and update deltatime
            self.delta_time = self.clock.tick(self.fps) / 1000

        # Shutdown pygame
        logger.info("Pygame Shutdown")
        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()

    
    