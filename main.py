#!/usr/bin/env python3
"""
Treat Quest: A Dog Adventure
16-bit style side-scroller featuring John's dogs
Fullscreen PyGame for Raspberry Pi
"""

import pygame
import random
import sys
import math
from enum import Enum

# Initialize PyGame
pygame.init()

# Constants
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
FPS = 60
TILE_SIZE = 64

# Colors - 16-bit style vibrant palette
SKY_TOP = (100, 180, 255)
SKY_BOTTOM = (180, 220, 255)
GRASS_LIGHT = (100, 200, 80)
GRASS_DARK = (60, 160, 40)
DIRT = (139, 90, 43)

class DogType(Enum):
    MILO = 1  # Smaller, white/cream
    BIG_DOG = 2  # Larger, brown

class Dog:
    def __init__(self, dog_type, x, y):
        self.type = dog_type
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.grounded = False
        self.facing_right = True
        self.anim_frame = 0
        self.anim_timer = 0
        self.sniffing = False
        self.sniff_timer = 0
        self.bark_timer = 0
        
        # Different sizes for distinguishable dogs
        if dog_type == DogType.MILO:
            self.width = 36
            self.height = 28
            self.color = (255, 248, 220)  # Cream white
            self.ear_color = (210, 180, 140)  # Light tan ears
            self.secondary_color = (255, 235, 200)
            self.run_speed = 5
            self.jump_power = -14
        else:  # BIG_DOG
            self.width = 52
            self.height = 40
            self.color = (139, 90, 43)  # Brown
            self.ear_color = (101, 67, 33)  # Darker brown
            self.secondary_color = (160, 110, 60)
            self.run_speed = 4
            self.jump_power = -12
    
    def draw(self, screen, camera_x):
        screen_x = self.x - camera_x
        screen_y = self.y
        
        # Animation frame
        self.anim_timer += 1
        if self.anim_timer > 8:
            self.anim_timer = 0
            self.anim_frame = (self.anim_frame + 1) % 4
        
        # Sniff animation override
        if self.sniffing:
            self.draw_sniffing(screen, screen_x, screen_y)
            return
        
        # Bounce when running
        bounce = 0
        if abs(self.vx) > 0.5 and self.grounded:
            bounce = abs(math.sin(self.anim_frame * math.pi / 2)) * 3
        
        # Shadow
        pygame.draw.ellipse(screen, (0, 0, 0, 30), 
                           (screen_x - self.width//2 + 2, screen_y + self.height - 4, 
                            self.width - 4, 6))
        
        # Body (oval shape)
        body_rect = pygame.Rect(screen_x - self.width//2, 
                                screen_y - self.height//2 + bounce,
                                self.width, self.height)
        pygame.draw.ellipse(screen, self.color, body_rect)
        pygame.draw.ellipse(screen, self.secondary_color, body_rect, 2)
        
        # Head
        head_size = self.width // 2 + 4
        head_y = screen_y - self.height//2 - head_size//2 + bounce
        head_x = screen_x + (8 if self.facing_right else -8)
        
        pygame.draw.ellipse(screen, self.color, 
                           (head_x - head_size//2, head_y, head_size, head_size))
        
        # Ears - distinctive shapes
        ear_w = head_size // 2
        ear_h = head_size // 2 + 4
        
        if self.type == DogType.MILO:
            # Floppy ears closer to head
            ear_y = head_y + 4
            if self.facing_right:
                pygame.draw.ellipse(screen, self.ear_color, 
                                   (head_x - 2, ear_y, ear_w, ear_h))
            else:
                pygame.draw.ellipse(screen, self.ear_color, 
                                   (head_x - ear_w + 2, ear_y, ear_w, ear_h))
        else:
            # Perky ears standing up
            ear_y = head_y - ear_h//2
            ear_points_left = [
                (head_x - head_size//3, ear_y + ear_h),
                (head_x - head_size//3 - 4, ear_y),
                (head_x - head_size//3 + 4, ear_y + 3)
            ]
            ear_points_right = [
                (head_x + head_size//3, ear_y + ear_h),
                (head_x + head_size//3 + 4, ear_y),
                (head_x + head_size//3 - 4, ear_y + 3)
            ]
            if self.facing_right:
                pygame.draw.polygon(screen, self.ear_color, ear_points_right)
                pygame.draw.polygon(screen, self.ear_color, ear_points_left)
            else:
                pygame.draw.polygon(screen, self.ear_color, ear_points_left)
                pygame.draw.polygon(screen, self.ear_color, ear_points_right)
        
        # Eyes
        eye_size = 4 if self.type == DogType.MILO else 5
        eye_y = head_y + head_size//3
        eye_offset = head_size//4
        
        if self.facing_right:
            pygame.draw.circle(screen, (0, 0, 0), (head_x + eye_offset, eye_y), eye_size)
            pygame.draw.circle(screen, (255, 255, 255), (head_x + eye_offset + 1, eye_y - 1), 1)
        else:
            pygame.draw.circle(screen, (0, 0, 0), (head_x - eye_offset, eye_y), eye_size)
            pygame.draw.circle(screen, (255, 255, 255), (head_x - eye_offset - 1, eye_y - 1), 1)
        
        # Nose
        nose_y = head_y + head_size * 2//3
        nose_color = (60, 40, 20)
        pygame.draw.ellipse(screen, nose_color, 
                           (head_x - 4, nose_y, 8, 5))
        
        # Legs - animated
        leg_w = 6
        leg_h = self.height // 2
        leg_color = self.secondary_color
        
        if abs(self.vx) > 0.5 and self.grounded:
            # Running animation
            leg_offset = math.sin(self.anim_frame * math.pi / 2) * 6
            
            # Front legs
            pygame.draw.rect(screen, leg_color, 
                           (screen_x - self.width//3, 
                            screen_y + self.height//2 + bounce, leg_w, leg_h))
            pygame.draw.rect(screen, leg_color, 
                           (screen_x + self.width//3 - leg_w, 
                            screen_y + self.height//2 + bounce + leg_offset, leg_w, leg_h))
            
            # Back legs
            pygame.draw.rect(screen, leg_color, 
                           (screen_x - self.width//3, 
                            screen_y + self.height//2 + bounce + leg_offset, leg_w, leg_h))
            pygame.draw.rect(screen, leg_color, 
                           (screen_x + self.width//3 - leg_w, 
                            screen_y + self.height//2 + bounce, leg_w, leg_h))
        else:
            # Standing
            pygame.draw.rect(screen, leg_color, 
                           (screen_x - self.width//3, 
                            screen_y + self.height//2 + bounce, leg_w, leg_h))
            pygame.draw.rect(screen, leg_color, 
                           (screen_x + self.width//3 - leg_w, 
                            screen_y + self.height//2 + bounce, leg_w, leg_h))
        
        # Tail
        tail_x = screen_x - (self.width//2 if self.facing_right else -self.width//2)
        tail_y = screen_y + 2 + bounce
        tail_angle = math.sin(self.anim_timer * 0.3) * 0.3
        
        tail_end_x = tail_x + (math.cos(tail_angle) * 12 * (-1 if self.facing_right else 1))
        tail_end_y = tail_y + math.sin(tail_angle) * 8
        
        pygame.draw.line(screen, self.ear_color, (tail_x, tail_y), 
                        (tail_end_x, tail_end_y), 4)
        pygame.draw.circle(screen, self.color, (int(tail_end_x), int(tail_end_y)), 3)
    
    def draw_sniffing(self, screen, screen_x, screen_y):
        # Lowered head sniffing pose
        body_rect = pygame.Rect(screen_x - self.width//2, 
                                screen_y - self.height//2 + 4,
                                self.width, self.height - 4)
        pygame.draw.ellipse(screen, self.color, body_rect)
        
        # Head down sniffing
        head_size = self.width // 2 + 4
        head_y = screen_y + 4
        head_x = screen_x + (12 if self.facing_right else -12)
        
        pygame.draw.ellipse(screen, self.color, 
                           (head_x - head_size//2, head_y, head_size, head_size))
        
        # Sniff particles
        for i in range(3):
            particle_x = head_x + random.randint(-15, 15)
            particle_y = head_y + head_size - random.randint(5, 15)
            pygame.draw.circle(screen, (200, 200, 255, 128), (particle_x, particle_y), 2)
    
    def update(self, platforms, treats):
        # Physics
        self.vy += 0.6  # Gravity
        
        self.x += self.vx
        self.y += self.vy
        
        self.grounded = False
        
        # Platform collision
        for plat in platforms:
            if (self.x + self.width//2 > plat.x and 
                self.x - self.width//2 < plat.x + plat.width and
                self.y + self.height//2 > plat.y and
                self.y - self.height//2 < plat.y + plat.height):
                
                # Landing on top
                if self.vy > 0 and self.y - self.height//2 < plat.y:
                    self.y = plat.y - self.height//2
                    self.vy = 0
                    self.grounded = True
                # Hitting bottom
                elif self.vy < 0 and self.y + self.height//2 > plat.y + plat.height:
                    self.y = plat.y + plat.height + self.height//2
                    self.vy = 0
        
        # Treat collection
        treats_collected = []
        for treat in treats:
            dx = self.x - treat.x
            dy = self.y - treat.y
            dist = math.sqrt(dx*dx + dy*dy)
            if dist < 40:
                treats_collected.append(treat)
        
        # Floor limit
        if self.y > SCREEN_HEIGHT - 100:
            self.y = SCREEN_HEIGHT - 100
            self.vy = 0
            self.grounded = True
        
        # Friction
        if self.grounded:
            self.vx *= 0.85
        else:
            self.vx *= 0.98
        
        return treats_collected

class Platform:
    def __init__(self, x, y, width, height, platform_type='grass'):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.type = platform_type
    
    def draw(self, screen, camera_x):
        screen_x = self.x - camera_x
        
        if self.type == 'grass':
            # Grass top
            pygame.draw.rect(screen, GRASS_LIGHT, 
                           (screen_x, self.y, self.width, 8))
            pygame.draw.rect(screen, GRASS_DARK, 
                           (screen_x, self.y + 8, self.width, self.height - 8))
            
            # Grass detail
            for i in range(0, self.width, 16):
                pygame.draw.line(screen, (50, 130, 30),
                               (screen_x + i, self.y),
                               (screen_x + i + 4, self.y - 4), 2)
        else:
            pygame.draw.rect(screen, (120, 120, 120), 
                           (screen_x, self.y, self.width, self.height))

class Treat:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.bob = 0
        self.collected = False
        self.fade = 1.0
    
    def draw(self, screen, camera_x):
        if self.collected:
            if self.fade > 0:
                self.fade -= 0.05
            return
        
        self.bob += 0.1
        screen_x = self.x - camera_x
        screen_y = self.y + math.sin(self.bob) * 5
        
        # Bone shape
        color = (255, 215, 0)  # Gold treat
        
        # Main bone
        pygame.draw.ellipse(screen, color, (screen_x - 12, screen_y - 6, 24, 12))
        # Knobs
        pygame.draw.circle(screen, color, (screen_x - 10, screen_y - 5), 6)
        pygame.draw.circle(screen, color, (screen_x + 10, screen_y - 5), 6)
        pygame.draw.circle(screen, color, (screen_x - 10, screen_y + 5), 6)
        pygame.draw.circle(screen, color, (screen_x + 10, screen_y + 5), 6)
        
        # Sparkle
        pygame.draw.circle(screen, (255, 255, 255), 
                          (int(screen_x), int(screen_y - 15)), 2)

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-5, -2)
        self.life = 30
        self.color = color
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.3
        self.life -= 1
    
    def draw(self, screen, camera_x):
        if self.life > 0:
            pygame.draw.circle(screen, self.color, 
                             (int(self.x - camera_x), int(self.y)), 
                             max(1, self.life // 6))

class Cloud:
    def __init__(self, x, layer):
        self.x = x
        self.y = random.randint(50, 300)
        self.layer = layer  # 0=far, 1=mid, 2=close
        self.speed = 0.2 + layer * 0.3
        self.width = 80 + random.randint(0, 100)
    
    def update(self):
        self.x += self.speed
        if self.x > 3000:
            self.x = -200
    
    def draw(self, screen, camera_x):
        parallax = 0.1 + self.layer * 0.2
        screen_x = self.x - camera_x * parallax
        y = self.y
        
        # Cloud puffs
        alpha = 180 - self.layer * 40
        color = (255, 255, 255)
        
        pygame.draw.ellipse(screen, color, (screen_x, y, self.width, 30))
        pygame.draw.ellipse(screen, color, (screen_x + self.width//3, y - 15, self.width//2, 40))
        pygame.draw.ellipse(screen, color, (screen_x - self.width//4, y - 10, self.width//2, 35))

class Game:
    def __init__(self):
        # Fullscreen mode
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Treat Quest: A Dog Adventure")
        
        self.font = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 36)
        
        # Game world
        self.world_width = 4000
        self.camera_x = 0
        
        # Create dogs
        self.dogs = [
            Dog(DogType.MILO, 200, SCREEN_HEIGHT - 150),
            Dog(DogType.BIG_DOG, 280, SCREEN_HEIGHT - 150)
        ]
        self.active_dog = 0
        
        # Platforms
        self.platforms = self.generate_platforms()
        
        # Treats
        self.treats = self.generate_treats()
        self.score = 0
        
        # Particles
        self.particles = []
        
        # Background
        self.clouds = [Cloud(random.randint(-200, 3000), i % 3) for i in range(12)]
        
        # Trees
        self.trees = [(random.randint(100, 3900), random.randint(0, 2)) for _ in range(20)]
    
    def generate_platforms(self):
        platforms = []
        # Ground
        for i in range(0, self.world_width, 200):
            platforms.append(Platform(i, SCREEN_HEIGHT - 80, 200, 80, 'grass'))
        
        # Floating platforms
        platform_layouts = [
            (400, SCREEN_HEIGHT - 250, 120),
            (650, SCREEN_HEIGHT - 200, 100),
            (900, SCREEN_HEIGHT - 300, 150),
            (1200, SCREEN_HEIGHT - 220, 100),
            (1500, SCREEN_HEIGHT - 350, 120),
            (1800, SCREEN_HEIGHT - 280, 100),
            (2100, SCREEN_HEIGHT - 200, 120),
            (2400, SCREEN_HEIGHT - 320, 140),
            (2800, SCREEN_HEIGHT - 250, 100),
            (3200, SCREEN_HEIGHT - 380, 160),
            (3500, SCREEN_HEIGHT - 220, 100),
            (3700, SCREEN_HEIGHT - 300, 120),
        ]
        
        for x, y, w in platform_layouts:
            platforms.append(Platform(x, y, w, 20, 'grass'))
        
        return platforms
    
    def generate_treats(self):
        treats = []
        treat_positions = [
            (450, SCREEN_HEIGHT - 300),
            (700, SCREEN_HEIGHT - 250),
            (950, SCREEN_HEIGHT - 350),
            (1250, SCREEN_HEIGHT - 270),
            (1550, SCREEN_HEIGHT - 400),
            (2120, SCREEN_HEIGHT - 250),
            (2430, SCREEN_HEIGHT - 370),
            (2830, SCREEN_HEIGHT - 300),
            (3230, SCREEN_HEIGHT - 430),
            (3530, SCREEN_HEIGHT - 270),
            (3730, SCREEN_HEIGHT - 350),
            (100, SCREEN_HEIGHT - 150),
            (500, SCREEN_HEIGHT - 150),
            (1000, SCREEN_HEIGHT - 150),
            (2000, SCREEN_HEIGHT - 150),
            (3000, SCREEN_HEIGHT - 150),
            (3800, SCREEN_HEIGHT - 150),
        ]
        
        for x, y in treat_positions:
            treats.append(Treat(x, y))
        
        return treats
    
    def draw_background(self):
        # Sky gradient
        for y in range(SCREEN_HEIGHT):
            ratio = y / SCREEN_HEIGHT
            r = int(SKY_TOP[0] * (1 - ratio) + SKY_BOTTOM[0] * ratio)
            g = int(SKY_TOP[1] * (1 - ratio) + SKY_BOTTOM[1] * ratio)
            b = int(SKY_TOP[2] * (1 - ratio) + SKY_BOTTOM[2] * ratio)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        
        # Sun
        pygame.draw.circle(self.screen, (255, 255, 200), (150, 150), 60)
        pygame.draw.circle(self.screen, (255, 255, 150), (150, 150), 50)
    
    def draw_trees(self, camera_x):
        for tx, ttype in self.trees:
            screen_x = tx - camera_x * 0.5
            if -100 < screen_x < SCREEN_WIDTH + 100:
                # Tree trunk
                trunk_color = (101, 67, 33)
                pygame.draw.rect(self.screen, trunk_color, 
                               (screen_x - 8, SCREEN_HEIGHT - 200, 16, 120))
                
                # Tree top
                leaf_color = (34, 139, 34) if ttype == 0 else (50, 150, 50)
                pygame.draw.polygon(self.screen, leaf_color, [
                    (screen_x - 40, SCREEN_HEIGHT - 180),
                    (screen_x, SCREEN_HEIGHT - 280),
                    (screen_x + 40, SCREEN_HEIGHT - 180)
                ])
                pygame.draw.polygon(self.screen, leaf_color, [
                    (screen_x - 35, SCREEN_HEIGHT - 220),
                    (screen_x, SCREEN_HEIGHT - 300),
                    (screen_x + 35, SCREEN_HEIGHT - 220)
                ])
    
    def update(self):
        dog = self.dogs[self.active_dog]
        
        # Treat collection
        for treat in self.treats:
            if not treat.collected:
                dx = dog.x - treat.x
                dy = dog.y - treat.y
                dist = math.sqrt(dx*dx + dy*dy)
                if dist < 40:
                    treat.collected = True
                    self.score += 10
                    # Particles
                    for _ in range(8):
                        self.particles.append(Particle(treat.x, treat.y, (255, 215, 0)))
        
        # Update dogs
        for d in self.dogs:
            collected = d.update(self.platforms, self.treats)
        
        # Camera follow
        target_x = dog.x - SCREEN_WIDTH // 2
        self.camera_x += (target_x - self.camera_x) * 0.1
        self.camera_x = max(0, min(self.camera_x, self.world_width - SCREEN_WIDTH))
        
        # Update particles
        for p in self.particles:
            p.update()
        self.particles = [p for p in self.particles if p.life > 0]
        
        # Update clouds
        for cloud in self.clouds:
            cloud.update()
    
    def draw_ui(self):
        # Score
        score_text = self.font.render(f"TREATS: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (20, 20))
        
        # Dog selector
        dog_text = self.font_small.render("Press 1 or 2 to switch dogs", True, (255, 255, 255))
        self.screen.blit(dog_text, (20, 70))
        
        # Mini dog icons
        for i, dog in enumerate(self.dogs):
            x = SCREEN_WIDTH - 150 + i * 70
            y = 30
            color = dog.color
            
            # Selection indicator
            if i == self.active_dog:
                pygame.draw.rect(self.screen, (255, 255, 0), (x - 5, y - 5, 50, 50), 3)
            
            # Mini dog icon
            pygame.draw.ellipse(self.screen, color, (x, y, 40, 35))
            pygame.draw.circle(self.screen, color, (x + 20, y - 8), 15)
        
        # Controls hint
        controls = self.font_small.render("← → Move  |  SPACE Jump/Sniff  |  ESC Quit", True, (200, 200, 200))
        self.screen.blit(controls, (SCREEN_WIDTH//2 - controls.get_width()//2, SCREEN_HEIGHT - 40))
    
    def draw(self):
        self.draw_background()
        
        # Clouds
        for cloud in self.clouds:
            cloud.draw(self.screen, self.camera_x)
        
        # Trees
        self.draw_trees(self.camera_x)
        
        # Platforms
        for plat in self.platforms:
            if plat.x - self.camera_x > -200 and plat.x - self.camera_x < SCREEN_WIDTH + 200:
                plat.draw(self.screen, self.camera_x)
        
        # Treats
        for treat in self.treats:
            treat.draw(self.screen, self.camera_x)
        
        # Dogs
        for dog in self.dogs:
            dog.draw(self.screen, self.camera_x)
        
        # Particles
        for p in self.particles:
            p.draw(self.screen, self.camera_x)
        
        # UI
        self.draw_ui()
        
        pygame.display.flip()
    
    def handle_input(self):
        keys = pygame.key.get_pressed()
        dog = self.dogs[self.active_dog]
        
        # Movement
        if keys[pygame.K_LEFT]:
            dog.vx = -dog.run_speed
            dog.facing_right = False
        elif keys[pygame.K_RIGHT]:
            dog.vx = dog.run_speed
            dog.facing_right = True
        
        # Jump / Sniff
        if keys[pygame.K_SPACE]:
            if dog.grounded and not dog.sniffing:
                dog.vy = dog.jump_power
                dog.grounded = False
            else:
                dog.sniffing = True
                dog.sniff_timer = 30
        
        # Dog switching
        if keys[pygame.K_1]:
            self.active_dog = 0
        if keys[pygame.K_2]:
            self.active_dog = 1
        
        # Update sniffing state
        if dog.sniffing:
            dog.sniff_timer -= 1
            if dog.sniff_timer <= 0 or keys[pygame.K_SPACE] == False:
                dog.sniffing = False
    
    def run(self):
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
            
            self.handle_input()
            self.update()
            self.draw()
            
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
