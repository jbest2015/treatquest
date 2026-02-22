#!/usr/bin/env python3
"""
Treat Quest: Dog Park Edition v2
Harley & Shanti's enhanced playground
Features: hills, fire hydrant, snoopy doghouse, changing weather
"""

import pygame
import random
import sys
import math
import os

os.environ['SDL_VIDEODRIVER'] = 'x11'
os.environ['SDL_AUDIODRIVER'] = 'dummy'

pygame.init()

info = pygame.display.Info()
SCREEN_WIDTH = info.current_w if info.current_w > 0 else 1920
SCREEN_HEIGHT = info.current_h if info.current_h > 0 else 1080
FPS = 60

print(f"Screen: {SCREEN_WIDTH}x{SCREEN_HEIGHT}", flush=True)

# Colors
SKY_TOP = (135, 206, 235)  # Sky blue
SKY_BOTTOM = (255, 248, 220)  # Cream horizon
SUNNY = {
    'sky_top': (135, 206, 235),
    'sky_bottom': (255, 248, 220),
    'grass': (100, 200, 80),
    'cloud': (255, 255, 255)
}
CLOUDY = {
    'sky_top': (160, 180, 200),
    'sky_bottom': (200, 200, 190),
    'grass': (90, 180, 70),
    'cloud': (220, 220, 220)
}
RAINY = {
    'sky_top': (80, 90, 110),
    'sky_bottom': (120, 130, 140),
    'grass': (70, 150, 60),
    'cloud': (100, 110, 120)
}

current_weather = 'sunny'
weather_timer = 0
WEATHER_CHANGE_TIME = 3000  # Change every ~50 seconds

class Dog:
    """Harley (small cream) or Shanti (big brown)"""
    
    def __init__(self, name, x, y):
        self.name = name
        self.x, self.y = x, y
        self.vx, self.vy = 0, 0
        self.grounded = False
        self.facing_right = True
        self.anim_frame = 0
        self.anim_timer = 0
        self.state = 'run'
        self.state_timer = 0
        
        if name == 'harley':
            self.width, self.height = 38, 30
            self.color = (255, 250, 230)
            self.ear_color = (220, 190, 150)
            self.secondary = (240, 230, 210)
            self.speed = 3.5
            self.ear_type = 'floppy'
        else:
            self.width, self.height = 54, 42
            self.color = (145, 100, 55)
            self.ear_color = (110, 75, 40)
            self.secondary = (165, 115, 65)
            self.speed = 2.8
            self.ear_type = 'perky'
        
        self.score = 0
    
    def ai_update(self, treats, other_dog):
        self.state_timer -= 1
        
        # Avoid crowding - if other dog is nearby, move away
        dx = other_dog.x - self.x
        dy = other_dog.y - self.y
        dist = math.sqrt(dx*dx + dy*dy)
        
        if dist < 100 and dist > 0:
            # Too close - move away
            self.facing_right = dx < 0
            self.vx = -self.speed if dx > 0 else self.speed
            return
        
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
                tdx, tdy = t.x - self.x, t.y - self.y
                dist = math.sqrt(tdx*tdx + tdy*tdy)
                if dist < nearest_dist and dist < 400:
                    nearest_dist, nearest = dist, t
        
        if nearest and self.state == 'run':
            self.facing_right = nearest.x > self.x
            self.vx = self.speed if self.facing_right else -self.speed
            if nearest.y < self.y - 50 and self.grounded and random.random() < 0.15:
                self.vy = -13
        
        # Screen bounds
        if self.x < 100:
            self.facing_right = True
            self.vx = self.speed
        if self.x > SCREEN_WIDTH - 100:
            self.facing_right = False
            self.vx = -self.speed
    
    def update(self, treats, other_dog):
        self.ai_update(treats, other_dog)
        
        self.vy += 0.6
        self.x += self.vx
        self.y += self.vy
        
        if self.y > SCREEN_HEIGHT - 120:
            self.y = SCREEN_HEIGHT - 120
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
                    t.respawn_timer = 300
                    t.collector = self.name
                    self.score += 1
    
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
        if self.ear_type == 'floppy':
            ear_y = head_y + 6
            ear_w = head_size // 2
            if self.facing_right:
                pygame.draw.ellipse(screen, self.ear_color,
                                   (head_x, ear_y, ear_w, ear_w + 6))
            else:
                pygame.draw.ellipse(screen, self.ear_color,
                                   (head_x - ear_w, ear_y, ear_w, ear_w + 6))
        else:
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
        
        # Eyes
        eye_x = head_x + (head_size//3 if self.facing_right else -head_size//3)
        eye_y = head_y + head_size//3
        pygame.draw.circle(screen, (0, 0, 0), (eye_x, eye_y), 5)
        pygame.draw.circle(screen, (255, 255, 255), (eye_x + 1, eye_y - 1), 2)
        
        # Happy mouth
        smile_y = head_y + head_size * 3//4
        if self.facing_right:
            pygame.draw.arc(screen, (40, 30, 20),
                          (head_x - 3, smile_y - 2, 10, 6), 3.14, 6.28, 2)
        else:
            pygame.draw.arc(screen, (40, 30, 20),
                          (head_x - 7, smile_y - 2, 10, 6), 3.14, 6.28, 2)
        
        # Collar
        col_y = body_y + self.height//3
        col_color = (200, 50, 50) if self.name == 'harley' else (50, 50, 200)
        pygame.draw.ellipse(screen, col_color,
                           (sx - self.width//2 + 2, col_y, self.width - 4, 8))
        
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
        
        # Tail
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
        self.collector = None
    
    def update(self):
        if self.collected:
            self.respawn_timer -= 1
            if self.respawn_timer <= 0:
                self.collected = False
                self.collector = None
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
        
        if pygame.time.get_ticks() % 1000 < 500:
            pygame.draw.circle(screen, (255, 255, 255), (sx, sy - 14), 3)


class RainDrop:
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(-100, 0)
        self.speed = random.randint(8, 15)
        self.length = random.randint(10, 20)
    
    def update(self):
        self.y += self.speed
        if self.y > SCREEN_HEIGHT:
            self.y = random.randint(-50, -10)
            self.x = random.randint(0, SCREEN_WIDTH)
    
    def draw(self, screen):
        pygame.draw.line(screen, (150, 160, 180),
                       (self.x, self.y), (self.x - 2, self.y + self.length), 1)


class Game:
    def __init__(self):
        print("Initializing display...", flush=True)
        
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
        
        pygame.display.set_caption("Treat Quest - Harley & Shanti v2")
        self.clock = pygame.time.Clock()
        
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
                            SCREEN_HEIGHT - random.randint(130, 220))
                      for _ in range(12)]
        
        # Clouds
        self.clouds = []
        for _ in range(10):
            self.clouds.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(30, 180),
                'speed': random.uniform(0.4, 1.0),
                'size': random.randint(70, 110)
            })
        
        # Rain
        self.rain = [RainDrop() for _ in range(100)]
        
        # Scene elements positions (fixed positions)
        self.hydrant_x = 180
        self.doghouse_x = SCREEN_WIDTH - 200
        
        # Hills
        self.hills = []
        for i in range(4):
            self.hills.append({
                'x': i * (SCREEN_WIDTH // 3),
                'height': random.randint(80, 150),
                'width': random.randint(300, 500),
                'color': (80 + i * 20, 140 + i * 15, 60 + i * 10)
            })
        
        print("Game initialized!", flush=True)
    
    def update_weather(self):
        global current_weather, weather_timer
        weather_timer += 1
        if weather_timer > WEATHER_CHANGE_TIME:
            weather_timer = 0
            choices = ['sunny', 'cloudy', 'raining']
            current_weather = random.choice(choices)
            print(f"Weather changed to: {current_weather}", flush=True)
    
    def draw_hills(self, weather_colors):
        # Back hills (darker)
        for i, hill in enumerate(self.hills):
            h_color = (hill['color'][0] - 20, hill['color'][1] - 20, hill['color'][2] - 10)
            pygame.draw.ellipse(self.screen, h_color,
                              (hill['x'] - hill['width']//2, 
                               SCREEN_HEIGHT - 200 - hill['height'],
                               hill['width'], hill['height'] * 2))
            
            # Front hill curve
            pygame.draw.ellipse(self.screen, hill['color'],
                              (hill['x'] - hill['width']//3,
                               SCREEN_HEIGHT - 180 - hill['height']//2,
                               hill['width'] * 2//3, hill['height']))
    
    def draw_hydrant(self):
        hx, hy = self.hydrant_x, SCREEN_HEIGHT - 145
        
        # Yellow fire hydrant
        pygame.draw.rect(self.screen, (220, 200, 50), (hx - 12, hy - 35, 24, 55))  # Main body
        pygame.draw.rect(self.screen, (200, 180, 40), (hx - 15, hy - 42, 30, 10))  # Top cap
        pygame.draw.rect(self.screen, (180, 160, 30), (hx - 18, hy - 45, 36, 5))  # Dome
        
        # Side nozzles
        pygame.draw.rect(self.screen, (200, 180, 40), (hx - 22, hy - 25, 8, 12))
        pygame.draw.rect(self.screen, (200, 180, 40), (hx + 14, hy - 25, 8, 12))
        
        # Chain
        pygame.draw.line(self.screen, (100, 100, 100), (hx + 18, hy - 20), (hx + 25, hy - 10), 2)
        
        # Base
        pygame.draw.rect(self.screen, (180, 160, 30), (hx - 14, hy + 15, 28, 8))
    
    def draw_doghouse(self):
        x, y = self.doghouse_x, SCREEN_HEIGHT - 145
        
        # Red Snoopy-style doghouse
        wall_h = 70
        roof_h = 40
        width = 100
        
        # Walls (red)
        pygame.draw.rect(self.screen, (200, 60, 60),
                       (x - width//2, y - wall_h, width, wall_h))
        
        # Roof (red, peaked)
        roof_points = [
            (x - width//2 - 10, y - wall_h),
            (x, y - wall_h - roof_h),
            (x + width//2 + 10, y - wall_h)
        ]
        pygame.draw.polygon(self.screen, (180, 40, 40), roof_points)
        
        # Door (dark opening)
        pygame.draw.ellipse(self.screen, (50, 40, 30),
                          (x - 18, y - wall_h + 20, 36, wall_h - 20))
        
        # White trim
        pygame.draw.polygon(self.screen, (255, 255, 255), roof_points, 4)
        pygame.draw.rect(self.screen, (255, 255, 255),
                        (x - width//2, y - wall_h, width, 3))
        
        # "HOME" text
        try:
            text = self.font_small.render("HOME", True, (255, 255, 255))
            self.screen.blit(text, (x - text.get_width()//2, y - wall_h - 25))
        except:
            pass
    
    def draw_bg(self):
        weather = {'sunny': SUNNY, 'cloudy': CLOUDY, 'raining': RAINY}[current_weather]
        
        # Sky gradient
        for y in range(SCREEN_HEIGHT):
            p = y / SCREEN_HEIGHT
            r = int(weather['sky_top'][0] * (1-p) + weather['sky_bottom'][0] * p)
            g = int(weather['sky_top'][1] * (1-p) + weather['sky_bottom'][1] * p)
            b = int(weather['sky_top'][2] * (1-p) + weather['sky_bottom'][2] * p)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        
        # Sun or hidden behind clouds
        if current_weather != 'raining':
            sun_x, sun_y = 120, 100
            pygame.draw.circle(self.screen, (255, 250, 200), (sun_x, sun_y), 70)
            pygame.draw.circle(self.screen, (255, 240, 150), (sun_x, sun_y), 55)
        
        # Hills
        self.draw_hills(weather)
    
    def draw_clouds(self):
        weather = {'sunny': SUNNY, 'cloudy': CLOUDY, 'raining': RAINY}[current_weather]
        
        for c in self.clouds:
            c['x'] = (c['x'] + c['speed']) % (SCREEN_WIDTH + 200) - 100
            x, y, s = int(c['x']), c['y'], c['size']
            
            cloud_color = weather['cloud']
            pygame.draw.ellipse(self.screen, cloud_color,
                              (x - s//2, y, s, s//2))
            pygame.draw.ellipse(self.screen, cloud_color,
                              (x - s//3, y - s//4, s//2, s//2))
            pygame.draw.ellipse(self.screen, cloud_color,
                              (x - s//6, y - s//5, s//3, s//3))
    
    def draw_ground(self):
        weather = {'sunny': SUNNY, 'cloudy': CLOUDY, 'raining': RAINY}[current_weather]
        
        # Grassy ground
        pygame.draw.rect(self.screen, weather['grass'],
                        (0, SCREEN_HEIGHT - 90, SCREEN_WIDTH, 45))
        pygame.draw.rect(self.screen, (60, 140, 50),
                        (0, SCREEN_HEIGHT - 45, SCREEN_WIDTH, 45))
        
        # Grass blades
        for x in range(0, SCREEN_WIDTH, 40):
            pygame.draw.line(self.screen, (40, 120, 35),
                           (x, SCREEN_HEIGHT - 90),
                           (x + 3, SCREEN_HEIGHT - 102), 2)
    
    def draw_rain(self):
        if current_weather == 'raining':
            for drop in self.rain:
                drop.update()
                drop.draw(self.screen)
    
    def draw_weather_indicator(self):
        # Weather icon top right
        if current_weather == 'sunny':
            icon = "☀️"
            text = "Sunny"
        elif current_weather == 'cloudy':
            icon = "☁️"
            text = "Cloudy"
        else:
            icon = "🌧️"
            text = "Rain"
        
        try:
            surf = self.font_small.render(f"{icon} {text}", True, (255, 255, 255))
            self.screen.blit(surf, (SCREEN_WIDTH - 200, 35))
        except:
            pass
    
    def draw(self):
        self.draw_bg()
        self.draw_clouds()
        self.draw_hills({})
        
        # Background elements
        self.draw_hydrant()
        self.draw_doghouse()
        
        self.draw_ground()
        self.draw_rain()
        
        for t in self.treats:
            t.draw(self.screen)
        
        for dog in self.dogs:
            dog.draw(self.screen)
        
        # Title
        title = self.font.render("TREAT QUEST", True, (255, 200, 50))
        subtitle = self.font_med.render("Harley & Shanti's Dog Park", True, (255, 255, 255))
        self.screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 30))
        self.screen.blit(subtitle, (SCREEN_WIDTH//2 - subtitle.get_width()//2, 105))
        
        # Scores
        harley_surf = self.font_small.render(f"HARLEY: {self.dogs[0].score}", True, (255, 100, 100))
        shanti_surf = self.font_small.render(f"SHANTI: {self.dogs[1].score}", True, (100, 100, 255))
        self.screen.blit(harley_surf, (30, 30))
        self.screen.blit(shanti_surf, (30, 70))
        
        # Dog tags
        for dog in self.dogs:
            name_surf = self.font_small.render(dog.name.upper(), True, (255, 255, 255))
            tag_w = name_surf.get_width() + 20
            pygame.draw.rect(self.screen, (0, 0, 0, 150),
                           (int(dog.x) - tag_w//2, int(dog.y) - 72, tag_w, 28))
            self.screen.blit(name_surf, (int(dog.x) - name_surf.get_width()//2, int(dog.y) - 67))
        
        # Weather
        self.draw_weather_indicator()
        
        pygame.display.flip()
    
    def update(self):
        self.update_weather()
        
        for t in self.treats:
            t.update()
        
        for i, dog in enumerate(self.dogs):
            other = self.dogs[1-i]
            dog.update(self.treats, other)
    
    def run(self):
        running = True
        print("Starting Treat Quest v2!", flush=True)
        
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
    print("Treat Quest v2: Dog Park Edition", flush=True)
    Game().run()
