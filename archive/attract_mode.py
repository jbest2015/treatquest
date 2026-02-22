#!/usr/bin/env python3
"""
Treat Quest: Attract Mode - Harley & Shanti Edition
Auto-running arcade demo featuring John's dogs
"""

import pygame
import random
import sys
import math
import os

# Force software rendering to avoid driver issues
os.environ['SDL_VIDEODRIVER'] = 'x11'
os.environ['SDL_AUDIODRIVER'] = 'dummy'

pygame.init()

# Get actual screen size
info = pygame.display.Info()
SCREEN_WIDTH = info.current_w if info.current_w > 0 else 1920
SCREEN_HEIGHT = info.current_h if info.current_h > 0 else 1080
FPS = 60

print(f"Screen: {SCREEN_WIDTH}x{SCREEN_HEIGHT}", flush=True)

# Colors
SKY_TOP = (100, 180, 255)
SKY_BOTTOM = (180, 220, 255)
GRASS_LIGHT = (100, 200, 80)
GRASS_DARK = (60, 160, 40)

class Dog:
    """Harley (small cream) or Shanti (big brown)"""
    
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.grounded = False
        self.facing_right = True
        self.anim_frame = 0
        self.anim_timer = 0
        self.state = 'run'
        self.state_timer = 0
        
        if name == 'harley':
            # Small, cream-colored, floppy ears
            self.width, self.height = 38, 30
            self.color = (255, 250, 230)  # Cream
            self.ear_color = (220, 190, 150)  # Tan
            self.secondary = (240, 230, 210)
            self.speed = 3.5
            self.ear_type = 'floppy'
        else:  # shanti
            # Larger, brown
            self.width, self.height = 54, 42
            self.color = (145, 100, 55)  # Brown
            self.ear_color = (110, 75, 40)  # Darker brown
            self.secondary = (165, 115, 65)
            self.speed = 2.8
            self.ear_type = 'perky'
    
    def ai_update(self, treats):
        self.state_timer -= 1
        
        if self.state_timer <= 0:
            actions = ['run', 'run', 'run', 'sniff', 'jump', 'idle', 'run']
            self.state = random.choice(actions)
            self.state_timer = random.randint(60, 200)
            
            if self.state == 'run':
                self.facing_right = random.choice([True, False])
                self.vx = self.speed if self.facing_right else -self.speed
            elif self.state == 'jump' and self.grounded:
                self.vy = -13
            elif self.state == 'sniff':
                self.vx = 0
        
        # Attract to treats
        nearest = None
        nearest_dist = 9999
        for t in treats:
            if not t.collected:
                dx, dy = t.x - self.x, t.y - self.y
                dist = math.sqrt(dx*dx + dy*dy)
                if dist < nearest_dist and dist < 350:
                    nearest_dist, nearest = dist, t
        
        if nearest and self.state == 'run':
            self.facing_right = nearest.x > self.x
            self.vx = self.speed if self.facing_right else -self.speed
            if nearest.y < self.y - 50 and self.grounded and random.random() < 0.1:
                self.vy = -13
        
        # Screen bounds
        if self.x < 80:
            self.facing_right = True
            self.vx = self.speed
        if self.x > SCREEN_WIDTH - 80:
            self.facing_right = False
            self.vx = -self.speed
    
    def update(self, treats):
        self.ai_update(treats)
        
        self.vy += 0.6
        self.x += self.vx
        self.y += self.vy
        
        if self.y > SCREEN_HEIGHT - 100:
            self.y = SCREEN_HEIGHT - 100
            self.vy = 0
            self.grounded = True
        
        self.anim_timer += 1
        if self.anim_timer > 6:
            self.anim_timer = 0
            self.anim_frame = (self.anim_frame + 1) % 4
        
        for t in treats:
            if not t.collected:
                dx, dy = self.x - t.x, self.y - t.y
                if math.sqrt(dx*dx + dy*dy) < 45:
                    t.collected = True
                    t.respawn_timer = 240
    
    def draw(self, screen):
        running = abs(self.vx) > 0.5
        bounce = abs(math.sin(self.anim_frame * math.pi / 2)) * 4 if running else 0
        
        sx, sy = int(self.x), int(self.y)
        
        # Shadow
        pygame.draw.ellipse(screen, (30, 30, 30),
                           (sx - self.width//2 + 3, sy + self.height//2 - 3,
                            self.width - 6, 5))
        
        # Body
        body_y = sy - self.height//2 + bounce - 2
        pygame.draw.ellipse(screen, self.color,
                           (sx - self.width//2, body_y, self.width, self.height))
        pygame.draw.ellipse(screen, self.secondary,
                           (sx - self.width//2, body_y, self.width, self.height), 2)
        
        # Head
        head_size = self.width // 2 + 8
        head_x = sx + (12 if self.facing_right else -12)
        head_y = body_y + self.height//3 if self.state == 'sniff' else body_y - 6
        
        pygame.draw.ellipse(screen, self.color,
                           (head_x - head_size//2, head_y, head_size, head_size))
        
        # Ears
        if self.ear_type == 'floppy':  # Harley
            ear_y = head_y + 6
            ear_w = head_size // 2
            if self.facing_right:
                pygame.draw.ellipse(screen, self.ear_color,
                                   (head_x, ear_y, ear_w, ear_w + 6))
            else:
                pygame.draw.ellipse(screen, self.ear_color,
                                   (head_x - ear_w, ear_y, ear_w, ear_w + 6))
        else:  # Shanti - perky triangle ears
            ear_y = head_y - 6
            base_y = ear_y + 16
            if self.facing_right:
                pygame.draw.polygon(screen, self.ear_color,
                                  [(head_x + 2, base_y), (head_x + 10, ear_y), (head_x + 14, base_y - 2)])
                pygame.draw.polygon(screen, self.ear_color,
                                  [(head_x - 6, base_y), (head_x + 2, ear_y), (head_x + 6, base_y - 2)])
            else:
                pygame.draw.polygon(screen, self.ear_color,
                                  [(head_x - 2, base_y), (head_x - 10, ear_y), (head_x - 14, base_y - 2)])
                pygame.draw.polygon(screen, self.ear_color,
                                  [(head_x + 6, base_y), (head_x - 2, ear_y), (head_x - 6, base_y - 2)])
        
        # Eyes (happy curve)
        eye_x = head_x + (head_size//3 if self.facing_right else -head_size//3)
        eye_y = head_y + head_size//3
        pygame.draw.circle(screen, (0, 0, 0), (eye_x, eye_y), 5)
        pygame.draw.circle(screen, (255, 255, 255), (eye_x + 1, eye_y - 1), 2)
        
        # Nose
        pygame.draw.ellipse(screen, (50, 35, 20),
                           (head_x - 5, head_y + head_size * 2//3, 10, 6))
        
        # Mouth (smile)
        smile_y = head_y + head_size * 3//4
        if self.facing_right:
            pygame.draw.arc(screen, (40, 30, 20),
                          (head_x - 3, smile_y - 2, 10, 6), 3.14, 6.28, 2)
        else:
            pygame.draw.arc(screen, (40, 30, 20),
                          (head_x - 7, smile_y - 2, 10, 6), 3.14, 6.28, 2)
        
        # Legs
        leg_w = 7
        leg_h = self.height // 2 + 4
        if running:
            offset = math.sin(self.anim_frame * math.pi / 2) * 7
            pygame.draw.rect(screen, self.secondary,
                           (sx - self.width//3, sy - 2, leg_w, leg_h))
            pygame.draw.rect(screen, self.secondary,
                           (sx + self.width//3 - leg_w, sy - 2 + offset, leg_w, leg_h))
        else:
            pygame.draw.rect(screen, self.secondary,
                           (sx - self.width//3, sy - 2, leg_w, leg_h))
            pygame.draw.rect(screen, self.secondary,
                           (sx + self.width//3 - leg_w, sy - 2, leg_w, leg_h))
        
        # Tail (animated)
        tail_base_x = sx - (18 if self.facing_right else -18)
        tail_base_y = body_y + 8 + bounce
        wag = math.sin(pygame.time.get_ticks() * 0.008 + (0 if self.name == 'harley' else 3)) * 12
        tip_x = tail_base_x + (15 if self.facing_right else -15) + wag
        tip_y = tail_base_y - 10 + abs(wag//3)
        
        pygame.draw.line(screen, self.ear_color, (tail_base_x, tail_base_y),
                        (tip_x, tip_y), 5)
        pygame.draw.circle(screen, self.color, (int(tip_x), int(tip_y)), 4)


class Treat:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.collected = False
        self.respawn_timer = 0
        self.bob = random.random() * 6.28
    
    def update(self):
        if self.collected:
            self.respawn_timer -= 1
            if self.respawn_timer <= 0:
                self.collected = False
                self.x = random.randint(150, SCREEN_WIDTH - 150)
        self.bob += 0.08
    
    def draw(self, screen):
        if self.collected:
            return
        
        y_off = math.sin(self.bob) * 6
        sx, sy = int(self.x), int(self.y + y_off)
        
        # Golden bone
        c = (255, 200, 50)
        pygame.draw.ellipse(screen, c, (sx - 14, sy - 5, 28, 10))
        pygame.draw.circle(screen, c, (sx - 12, sy - 4), 6)
        pygame.draw.circle(screen, c, (sx + 12, sy - 4), 6)
        pygame.draw.circle(screen, c, (sx - 12, sy + 4), 6)
        pygame.draw.circle(screen, c, (sx + 12, sy + 4), 6)
        
        # Sparkle
        if (pygame.time.get_ticks() // 500) % 2 == 0:
            pygame.draw.circle(screen, (255, 255, 255), (sx, sy - 14), 3)
            pygame.draw.circle(screen, (255, 255, 200), (sx - 5, sy - 10), 2)


class Game:
    def __init__(self):
        print("Initializing display...", flush=True)
        
        # Try multiple display modes
        modes = [
            (pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE, "Fullscreen HW"),
            (pygame.FULLSCREEN | pygame.DOUBLEBUF, "Fullscreen DB"),
            (pygame.FULLSCREEN, "Fullscreen"),
            (0, "Windowed")
        ]
        
        self.screen = None
        for flags, name in modes:
            try:
                self.screen = pygame.display.set_mode((0, 0), flags)
                print(f"Display mode: {name}", flush=True)
                break
            except Exception as e:
                print(f"{name} failed: {e}", flush=True)
        
        if self.screen is None:
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            print("Fallback to fixed size", flush=True)
        
        pygame.display.set_caption("Treat Quest - Harley & Shanti")
        self.clock = pygame.time.Clock()
        
        # Fonts
        try:
            self.font = pygame.font.Font(None, 80)
            self.font_med = pygame.font.Font(None, 56)
            self.font_small = pygame.font.Font(None, 40)
        except:
            self.font = pygame.font.SysFont('arial', 60)
            self.font_med = pygame.font.SysFont('arial', 40)
            self.font_small = pygame.font.SysFont('arial', 30)
        
        # Harley (small) and Shanti (big)
        self.dogs = [
            Dog('harley', SCREEN_WIDTH // 3, SCREEN_HEIGHT - 150),
            Dog('shanti', 2 * SCREEN_WIDTH // 3, SCREEN_HEIGHT - 150)
        ]
        
        # Treats
        self.treats = [Treat(random.randint(200, SCREEN_WIDTH - 200),
                            SCREEN_HEIGHT - random.randint(140, 220))
                      for _ in range(10)]
        
        # Clouds
        self.clouds = []
        for _ in range(8):
            self.clouds.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(40, 200),
                'speed': random.uniform(0.3, 0.8),
                'size': random.randint(60, 100)
            })
        
        print("Game initialized!", flush=True)
    
    def draw_bg(self):
        # Sky gradient
        for y in range(SCREEN_HEIGHT):
            p = y / SCREEN_HEIGHT
            r = int(SKY_TOP[0] * (1-p) + SKY_BOTTOM[0] * p)
            g = int(SKY_TOP[1] * (1-p) + SKY_BOTTOM[1] * p)
            b = int(SKY_TOP[2] * (1-p) + SKY_BOTTOM[2] * p)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        
        # Sun with rays
        sun_x, sun_y = 140, 130
        pygame.draw.circle(self.screen, (255, 250, 200), (sun_x, sun_y), 75)
        pygame.draw.circle(self.screen, (255, 240, 150), (sun_x, sun_y), 60)
        for angle in range(0, 360, 30):
            rad = math.radians(angle)
            x1 = sun_x + math.cos(rad) * 80
            y1 = sun_y + math.sin(rad) * 80
            x2 = sun_x + math.cos(rad) * 95
            y2 = sun_y + math.sin(rad) * 95
            pygame.draw.line(self.screen, (255, 255, 200), (x1, y1), (x2, y2), 3)
    
    def draw_clouds(self):
        for c in self.clouds:
            c['x'] = (c['x'] + c['speed']) % (SCREEN_WIDTH + 150) - 75
            x, y, s = int(c['x']), c['y'], c['size']
            pygame.draw.ellipse(self.screen, (255, 255, 255),
                              (x - s//2, y, s, s//2))
            pygame.draw.ellipse(self.screen, (255, 255, 255),
                              (x - s//3, y - s//4, s//2, s//2))
            pygame.draw.ellipse(self.screen, (255, 255, 255),
                              (x - s//6, y - s//5, s//3, s//3))
    
    def draw_ground(self):
        pygame.draw.rect(self.screen, GRASS_LIGHT,
                        (0, SCREEN_HEIGHT - 90, SCREEN_WIDTH, 40))
        pygame.draw.rect(self.screen, GRASS_DARK,
                        (0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50))
        
        for x in range(0, SCREEN_WIDTH, 60):
            pygame.draw.line(self.screen, (45, 130, 35),
                           (x, SCREEN_HEIGHT - 90),
                           (x + 4, SCREEN_HEIGHT - 102), 2)
    
    def draw(self):
        self.draw_bg()
        self.draw_clouds()
        self.draw_ground()
        
        for t in self.treats:
            t.draw(self.screen)
        
        for dog in self.dogs:
            dog.draw(self.screen)
        
        # Title
        title = self.font.render("TREAT QUEST", True, (255, 215, 0))
        subtitle = self.font_med.render("Harley & Shanti", True, (255, 255, 255))
        
        # Blinking insert coin
        blink = (pygame.time.get_ticks() // 800) % 2 == 0
        if blink:
            prompt = self.font_small.render("INSERT BONE TO PLAY", True, (255, 255, 255))
            self.screen.blit(prompt, (SCREEN_WIDTH//2 - prompt.get_width()//2, SCREEN_HEIGHT - 50))
        
        self.screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 30))
        self.screen.blit(subtitle, (SCREEN_WIDTH//2 - subtitle.get_width()//2, 100))
        
        # Dog name tags
        for dog in self.dogs:
            name_surf = self.font_small.render(dog.name.upper(), True, (255, 255, 255))
            tag_w = name_surf.get_width() + 20
            pygame.draw.rect(self.screen, (0, 0, 0, 180),
                           (int(dog.x) - tag_w//2, int(dog.y) - 70, tag_w, 28))
            self.screen.blit(name_surf, (int(dog.x) - name_surf.get_width()//2, int(dog.y) - 65))
        
        pygame.display.flip()
    
    def update(self):
        for t in self.treats:
            t.update()
        
        for dog in self.dogs:
            dog.update(self.treats)
    
    def run(self):
        running = True
        print("Starting game loop...", flush=True)
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
            
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    print("Treat Quest: Harley & Shanti Edition", flush=True)
    Game().run()
