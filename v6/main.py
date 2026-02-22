#!/usr/bin/env python3
"""
Treat Quest v6.0 — WWI Flying Aces
Harley & Shanti as WWI pilots chasing balloon-borne treats
Time Pilot 84 style side-scrolling aerial combat
"""

import pygame
import sys
from config import *

# TODO: Import modules as they're implemented
# from core.camera import TrackingCamera
# from core.physics import BiplanePhysics
# from entities.aircraft import HarleyPlane, ShantiPlane
# from world.level import Level
# from game.game_state import GameState

def main():
    pygame.init()
    
    # Initialize display
    if FULLSCREEN:
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    clock = pygame.time.Clock()
    running = True
    
    print(f"Treat Quest v{VERSION} — {VERSION_NAME}")
    print(f"Screen: {screen.get_size()}")
    
    # Game loop
    while running:
        dt = clock.tick(FPS) / 1000.0
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        # TODO: Update game state
        # TODO: Render frame
        
        # Placeholder clear
        screen.fill((135, 206, 235))  # Sky blue
        
        # Placeholder text
        font = pygame.font.Font(None, 48)
        text = font.render(f"Treat Quest v{VERSION} — {VERSION_NAME}", True, (0, 0, 0))
        text_rect = text.get_rect(center=(screen.get_width()//2, screen.get_height()//2))
        screen.blit(text, text_rect)
        
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
