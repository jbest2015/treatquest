#!/usr/bin/env python3
"""
Treat Quest: Dog Park Edition v3
Real Tampa weather + actual time of day
"""

import pygame
import random
import sys
import math
import os
import subprocess
import json
from datetime import datetime, time as dt_time

os.environ['SDL_VIDEODRIVER'] = 'x11'
os.environ['SDL_AUDIODRIVER'] = 'dummy'

pygame.init()

info = pygame.display.Info()
SCREEN_WIDTH = info.current_w if info.current_w > 0 else 1920
SCREEN_HEIGHT = info.current_h if info.current_h > 0 else 1080
FPS = 60

print(f"Screen: {SCREEN_WIDTH}x{SCREEN_HEIGHT}", flush=True)

# Weather cache
weather_cache = {'condition': 'sunny', 'temp': 72, 'last_update': 0}
WEATHER_UPDATE_INTERVAL = 600  # Update every 10 minutes

def get_tampa_weather():
    """Fetch real Tampa weather from Open-Meteo"""
    global weather_cache
    now = pygame.time.get_ticks()
    
    if now - weather_cache['last_update'] < WEATHER_UPDATE_INTERVAL * 1000:
        return weather_cache
    
    try:
        cmd = [
            'curl', '-s', '--connect-timeout', '5', '--max-time', '10',
            'https://api.open-meteo.com/v1/forecast?latitude=27.95&longitude=-82.46&current=weather_code,temperature_2m,is_day&temperature_unit=fahrenheit'
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        if result.returncode == 0 and result.stdout:
            data = json.loads(result.stdout)
            current = data.get('current', {})
            code = current.get('weather_code', 0)
            is_day = current.get('is_day', 1)
            weather_cache['temp'] = int(current.get('temperature_2m', 72))
            weather_cache['last_update'] = now
            
            # Map WMO codes to conditions
            # 0=clear, 1-3=cloudy, 45-48=fog, 51-67=rain, 71-77=snow, 80-82=showers, 95-99=thunderstorm
            if code in [95, 96, 99]:
                weather_cache['condition'] = 'storm'
            elif code in [71, 73, 75, 77, 85, 86]:
                weather_cache['condition'] = 'rain'  # Treat snow as rain for Tampa
            elif code in [51, 53, 55, 56, 57, 61, 63, 65, 80, 81, 82]:
                weather_cache['condition'] = 'rain'
            elif code in [45, 48, 3]:
                weather_cache['condition'] = 'cloudy'
            elif code in [1, 2]:
                weather_cache['condition'] = 'partly'
            else:
                weather_cache['condition'] = 'sunny'
            
            weather_cache['is_day'] = is_day
            print(f"Weather updated: {weather_cache['condition']}, {weather_cache['temp']}°F, is_day={is_day}", flush=True)
    except Exception as e:
        print(f"Weather fetch error: {e}", flush=True)
    
    return weather_cache

def get_sky_colors(condition, is_day, hour):
    """Return sky colors based on actual time and weather"""
    
    # Night time (after sunset ~7pm, before sunrise ~7am)
    if hour >= 20 or hour <= 5:
        if condition == 'rain':
            return ((30, 40, 60), (50, 60, 80), 'rain')  # Stormy night
        elif condition == 'cloudy':
            return ((25, 30, 45), (40, 45, 60), 'cloudy-night')
        else:
            return ((20, 25, 50), (40, 50, 90), 'night')  # Clear night with stars
    
    # Dawn (5-7am)
    if hour >= 5 and hour < 7:
        if condition == 'rain':
            return ((60, 70, 90), (100, 110, 120), 'rain')
        return ((255, 140, 100), (255, 200, 150), 'dawn')
    
    # Sunset/Dusk (6-8pm)
    if hour >= 18 and hour < 20:
        if condition == 'rain':
            return ((80, 70, 100), (120, 110, 130), 'rain')
        return ((255, 100, 80), (255, 180, 120), 'sunset')
    
    # Daytime
    if condition == 'rain' or condition == 'storm':
        return ((80, 90, 110), (120, 130, 140), 'rain')
    elif condition == 'cloudy':
        return ((140, 150, 170), (180, 185, 190), 'cloudy')
    elif condition == 'partly':
        return ((135, 190, 230), (220, 240, 250), 'partly')
    else:  # sunny
        return ((100, 180, 255), (255, 248, 220), 'sunny')

class Dog:
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
        
        dx = other_dog.x - self.x
        dy = other_dog.y - self.y
        dist = math.sqrt(dx*dx + dy*dy)
        
        if dist < 100 and dist > 0:
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
        
        nearest = None
        nearest_dist = 9999
        for t in treats:
            if not t.collected:
                tdx, tdy = t.x - self.x, t.y - self.y
                td = math.sqrt(tdx*tdx + tdy*tdy)
                if td < nearest_dist and td < 400:
                    nearest_dist, nearest = td, t
        
        if nearest and self.state == 'run':
            self.facing_right = nearest.x > self.x
            self.vx = self.speed if self.facing_right else -self.speed
            if nearest.y < self.y - 50 and self.grounded and random.random() < 0.15:
                self.vy = -13
        
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
        # Handle sleep state
        if self.state == 'sleep':
            sx, sy = int(self.x), int(self.y)
            # Curled up body (circle)
            pygame.draw.ellipse(screen, self.color,
                               (sx - self.width//2, sy - self.height//3, 
                                self.width, self.height//1.5))
            pygame.draw.ellipse(screen, self.secondary,
                               (sx - self.width//2, sy - self.height//3, 
                                self.width, self.height//1.5), 2)
            # Head tucked in
            head_x = sx - self.width//3 if self.facing_right else sx + self.width//3
            pygame.draw.circle(screen, self.color, (int(head_x), sy - self.height//4), self.width//3)
            # Closed eyes
            pygame.draw.line(screen, (0, 0, 0), (head_x - 8, sy - self.height//4 - 2), (head_x - 4, sy - self.height//4 - 2), 2)
            pygame.draw.line(screen, (0, 0, 0), (head_x + 4, sy - self.height//4 - 2), (head_x + 8, sy - self.height//4 - 2), 2)
            # Tail curled
            pygame.draw.ellipse(screen, self.ear_color,
                               (sx + self.width//3, sy - 5, 15, 20))
            # Zzz animation
            if pygame.time.get_ticks() % 2000 < 1500:
                z_offset = (pygame.time.get_ticks() % 500) // 50
                try:
                    font = pygame.font.Font(None, 40)
                    z_text = font.render("Z", True, (200, 200, 255))
                    screen.blit(z_text, (sx + 15 + z_offset, sy - 50 - z_offset * 2))
                    if pygame.time.get_ticks() % 2000 > 500:
                        z2_text = font.render("Z", True, (180, 180, 240))
                        screen.blit(z2_text, (sx + 25 + z_offset, sy - 65 - z_offset * 2))
                except:
                    pass
            return  # Skip normal drawing

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
        
        # Smile
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
        
        c = (255, 200, 50)
        pygame.draw.ellipse(screen, c, (sx - 14, sy - 5, 28, 10))
        pygame.draw.circle(screen, c, (sx - 12, sy - 4), 6)
        pygame.draw.circle(screen, c, (sx + 12, sy - 4), 6)
        pygame.draw.circle(screen, c, (sx - 12, sy + 4), 6)
        pygame.draw.circle(screen, c, (sx + 12, sy + 4), 6)
        


class GoldenTreat:
    """Giant golden treat worth 5 points - rare spawn"""
    def __init__(self):
        self.x = random.randint(200, SCREEN_WIDTH - 200)
        self.y = SCREEN_HEIGHT - random.randint(130, 220)
        self.collected = False
        self.active = False
        self.spawn_timer = random.randint(1800, 3600)  # 30-60 seconds
        self.bob = random.random() * 6.28
        self.pulse = 0
    
    def update(self):
        if not self.active:
            self.spawn_timer -= 1
            if self.spawn_timer <= 0:
                self.active = True
                self.collected = False
                self.x = random.randint(200, SCREEN_WIDTH - 200)
                self.y = SCREEN_HEIGHT - random.randint(130, 220)
            return
        
        if self.collected:
            self.active = False
            self.collected = False
            self.spawn_timer = random.randint(1800, 3600)
            return
        
        self.bob += 0.08
        self.pulse += 0.1
    
    def draw(self, screen):
        if not self.active or self.collected:
            return
        
        y_off = math.sin(self.bob) * 8
        sx, sy = int(self.x), int(self.y + y_off)
        
        # Pulsing glow
        glow_size = int(25 + 8 * math.sin(self.pulse))
        
        # Outer glow ring
        pygame.draw.circle(screen, (255, 220, 100), (sx, sy), glow_size, 3)
        pygame.draw.circle(screen, (255, 200, 50), (sx, sy), glow_size - 8, 2)
        
        # Giant golden bone body
        c = (255, 180, 30)  # Deeper gold
        pygame.draw.ellipse(screen, c, (sx - 22, sy - 8, 44, 16))
        pygame.draw.circle(screen, c, (sx - 18, sy - 6), 10)
        pygame.draw.circle(screen, c, (sx + 18, sy - 6), 10)
        pygame.draw.circle(screen, c, (sx - 18, sy + 6), 10)
        pygame.draw.circle(screen, c, (sx + 18, sy + 6), 10)
        
        # Shine effect
        shine = int(200 + 55 * math.sin(self.pulse * 2))
        pygame.draw.circle(screen, (shine, shine, 150), (sx - 10, sy - 4), 6)
        
        # Sparkle dots around it
        for angle in range(0, 360, 45):
            rad = math.radians(angle + self.pulse * 50)
            sparkle_x = sx + math.cos(rad) * 35
            sparkle_y = sy + math.sin(rad) * 20
            if int(self.pulse * 10) % 10 > 5:
                pygame.draw.circle(screen, (255, 255, 200), (int(sparkle_x), int(sparkle_y)), 3)

        if pygame.time.get_ticks() % 1000 < 500:
            pygame.draw.circle(screen, (255, 255, 255), (sx, sy - 14), 3)




class Puddle:
    """Puddle obstacle that slows dogs down when they walk through it"""
    def __init__(self):
        self.x = random.randint(200, SCREEN_WIDTH - 200)
        self.y = SCREEN_HEIGHT - random.randint(100, 140)
        self.width = random.randint(60, 100)
        self.height = random.randint(30, 50)
        self.ripple_phase = random.random() * 6.28
    
    def update(self):
        self.ripple_phase += 0.05
    
    def draw(self, screen):
        # Main puddle shape (irregular ellipse)
        pygame.draw.ellipse(screen, (100, 130, 160), 
                           (self.x - self.width//2, self.y - self.height//2, 
                            self.width, self.height))
        pygame.draw.ellipse(screen, (80, 110, 140), 
                           (self.x - self.width//2 + 5, self.y - self.height//2 + 3, 
                            self.width - 10, self.height - 6))
        
        # Ripple effect
        ripple_size = int(3 + 2 * math.sin(self.ripple_phase))
        pygame.draw.ellipse(screen, (120, 150, 180), 
                           (self.x - self.width//4, self.y - 5, 
                            self.width//2, 10), ripple_size)
    
    def check_collision(self, dog):
        """Check if dog is in puddle - returns True if slowing should apply"""
        dx = abs(dog.x - self.x)
        dy = abs(dog.y - self.y)
        return dx < self.width//2 and dy < self.height//2

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


class Star:
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(0, SCREEN_HEIGHT // 2)
        self.brightness = random.randint(100, 255)
        self.twinkle = random.random() * 0.1
    
    def draw(self, screen):
        brightness = int(self.brightness * (0.7 + 0.3 * math.sin(pygame.time.get_ticks() * self.twinkle)))
        pygame.draw.circle(screen, (brightness, brightness, brightness), (self.x, self.y), 1)


class Firefly:
    """Glowing firefly that only appears at night"""
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(SCREEN_HEIGHT - 300, SCREEN_HEIGHT - 50)
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-0.5, 0.5)
        self.size = random.randint(2, 4)
        self.phase = random.random() * 6.28
        self.color = (200, 255, 100)  # Yellow-green glow
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.phase += 0.1
        
        # Gentle wandering
        if random.random() < 0.05:
            self.vx += random.uniform(-0.2, 0.2)
            self.vy += random.uniform(-0.2, 0.2)
        
        # Bounds
        if self.x < 0: self.x = SCREEN_WIDTH
        if self.x > SCREEN_WIDTH: self.x = 0
        if self.y < SCREEN_HEIGHT - 350: self.vy = abs(self.vy)
        if self.y > SCREEN_HEIGHT - 40: self.vy = -abs(self.vy)
        
        # Clamp velocity
        self.vx = max(-2, min(2, self.vx))
        self.vy = max(-1, min(1, self.vy))
    
    def draw(self, screen):
        # Pulsing glow
        glow = int(150 + 105 * math.sin(self.phase))
        color = (min(255, 200 + glow//4), 255, min(255, 100 + glow//2))
        
        # Outer glow
        pygame.draw.circle(screen, (color[0]//3, color[1]//3, color[2]//3), 
                          (int(self.x), int(self.y)), self.size + 2)
        # Core
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.size)
        # Bright center
        pygame.draw.circle(screen, (255, 255, 220), (int(self.x), int(self.y)), self.size - 1)


class Butterfly:
    """Colorful butterfly that flutters during the day"""
    def __init__(self):
        self.x = random.randint(100, SCREEN_WIDTH - 100)
        self.y = random.randint(100, SCREEN_HEIGHT - 200)
        self.base_y = self.y
        self.vx = random.uniform(1.5, 3) * random.choice([-1, 1])
        self.phase = random.random() * 6.28
        self.color = random.choice([
            (255, 100, 150),  # Pink
            (100, 150, 255),  # Blue
            (255, 200, 50),   # Yellow
            (150, 50, 200),   # Purple
        ])
        self.size = random.randint(6, 10)
        self.flap_speed = random.uniform(0.2, 0.4)
    
    def update(self):
        self.x += self.vx
        self.phase += self.flap_speed
        
        # Sine wave floating
        self.y = self.base_y + math.sin(self.phase * 0.5) * 30
        
        # Occasionally change direction and height
        if random.random() < 0.02:
            self.vx *= -1
            self.base_y += random.randint(-50, 50)
            self.base_y = max(80, min(SCREEN_HEIGHT - 250, self.base_y))
        
        # Wrap
        if self.x < -50: self.x = SCREEN_WIDTH + 50
        if self.x > SCREEN_WIDTH + 50: self.x = -50
    
    def draw(self, screen):
        sx, sy = int(self.x), int(self.y)
        flap = abs(math.sin(self.phase))
        
        # Wing span changes with flap
        wing_w = int(self.size * (0.5 + 0.5 * flap))
        wing_h = int(self.size * (1.2 - 0.4 * flap))
        
        # Wings (two ellipses)
        pygame.draw.ellipse(screen, self.color, 
                           (sx - wing_w - 2, sy - wing_h//2, wing_w, wing_h))
        pygame.draw.ellipse(screen, self.color, 
                           (sx + 2, sy - wing_h//2, wing_w, wing_h))
        
        # Body
        pygame.draw.ellipse(screen, (60, 40, 20), (sx - 2, sy - self.size//2, 4, self.size))
        
        # Antennae
        pygame.draw.line(screen, (60, 40, 20), (sx, sy - self.size//2), 
                        (sx - 4, sy - self.size - 4), 1)
        pygame.draw.line(screen, (60, 40, 20), (sx, sy - self.size//2), 
                        (sx + 4, sy - self.size - 4), 1)


class Squirrel:
    """Squirrel that runs across screen with acorn - drops bonus treat if caught"""
    def __init__(self):
        self.reset()
    
    def reset(self):
        """Reset squirrel for new spawn"""
        self.active = False
        self.spawn_timer = random.randint(1800, 3600)  # 30-60 seconds at 60fps
        self.x = -50
        self.y = random.randint(SCREEN_HEIGHT - 200, SCREEN_HEIGHT - 120)
        self.vx = random.uniform(5, 7)  # Fast!
        self.direction = 1  # 1 = right, -1 = left
        self.has_acorn = True
        self.anim_frame = 0
        self.anim_timer = 0
        self.bob = 0
    
    def spawn(self):
        """Spawn the squirrel"""
        self.active = True
        self.direction = random.choice([-1, 1])
        if self.direction == 1:
            self.x = -50
            self.vx = random.uniform(5, 7)
        else:
            self.x = SCREEN_WIDTH + 50
            self.vx = -random.uniform(5, 7)
        self.y = random.randint(SCREEN_HEIGHT - 200, SCREEN_HEIGHT - 120)
        self.has_acorn = True
    
    def update(self, dogs):
        """Update squirrel position and check for dog collisions"""
        if not self.active:
            self.spawn_timer -= 1
            if self.spawn_timer <= 0:
                self.spawn()
            return None
        
        # Move
        self.x += self.vx
        self.anim_timer += 1
        if self.anim_timer > 4:
            self.anim_timer = 0
            self.anim_frame = (self.anim_frame + 1) % 4
            self.bob = abs(math.sin(self.anim_frame * math.pi / 2)) * 3
        
        # Check if off screen
        if (self.direction == 1 and self.x > SCREEN_WIDTH + 100) or \
           (self.direction == -1 and self.x < -100):
            self.reset()
            return None
        
        # Check collision with dogs
        if self.has_acorn:
            for dog in dogs:
                dx = self.x - dog.x
                dy = self.y - dog.y
                dist = math.sqrt(dx*dx + dy*dy)
                if dist < 40:  # Caught!
                    self.has_acorn = False
                    # Drop acorn at current position
                    return {'x': self.x, 'y': self.y, 'active': True}
        
        return None
    
    def draw(self, screen):
        """Draw the squirrel"""
        if not self.active:
            return
        
        sx, sy = int(self.x), int(self.y + self.bob)
        facing_right = self.direction == 1
        
        # Body (oval)
        body_color = (180, 120, 60)  # Brown
        pygame.draw.ellipse(screen, body_color, 
                           (sx - 15, sy - 10, 30, 22))
        
        # Head (circle)
        head_x = sx + (12 if facing_right else -12)
        pygame.draw.circle(screen, body_color, (head_x, sy - 12), 10)
        
        # Ears (pointy)
        ear_color = (160, 100, 50)
        if facing_right:
            pygame.draw.polygon(screen, ear_color, 
                              [(head_x - 3, sy - 18), (head_x + 2, sy - 26), (head_x + 7, sy - 18)])
        else:
            pygame.draw.polygon(screen, ear_color, 
                              [(head_x - 7, sy - 18), (head_x - 2, sy - 26), (head_x + 3, sy - 18)])
        
        # Eye
        eye_x = head_x + (4 if facing_right else -4)
        pygame.draw.circle(screen, (0, 0, 0), (eye_x, sy - 14), 3)
        pygame.draw.circle(screen, (255, 255, 255), (eye_x + 1, sy - 16), 1)
        
        # Tail (big fluffy)
        tail_x = sx + (-18 if facing_right else 18)
        tail_y = sy - 15
        tail_bob = math.sin(pygame.time.get_ticks() * 0.01 + self.x * 0.01) * 5
        pygame.draw.ellipse(screen, (200, 140, 80), 
                           (tail_x - 12, tail_y + tail_bob - 20, 24, 35))
        
        # Legs (animated)
        leg_offset = math.sin(self.anim_frame * math.pi / 2) * 4
        pygame.draw.rect(screen, body_color, (sx - 8, sy + 8, 6, 10 + leg_offset))
        pygame.draw.rect(screen, body_color, (sx + 2, sy + 8, 6, 10 - leg_offset))
        
        # Acorn (if still has it)
        if self.has_acorn:
            acorn_x = sx + (14 if facing_right else -14)
            # Nut part
            pygame.draw.ellipse(screen, (160, 120, 80), (acorn_x - 5, sy - 5, 10, 12))
            # Cap
            pygame.draw.arc(screen, (100, 80, 60), (acorn_x - 6, sy - 8, 12, 8), 0, 3.14, 3)
            # Little stem
            pygame.draw.line(screen, (80, 60, 40), (acorn_x, sy - 8), (acorn_x, sy - 11), 2)


class AcornBonus:
    """Bonus acorn dropped when squirrel is caught"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.active = True
        self.bob = 0
        self.lifetime = 300  # 5 seconds
    
    def update(self):
        self.bob += 0.1
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.active = False
    
    def draw(self, screen):
        if not self.active:
            return
        
        y_off = math.sin(self.bob) * 5
        sx, sy = int(self.x), int(self.y + y_off)
        
        # Glow effect
        glow = int(128 + 127 * math.sin(self.bob * 2))
        pygame.draw.circle(screen, (glow, glow, 50), (sx, sy), 18)
        
        # Acorn
        pygame.draw.ellipse(screen, (180, 140, 100), (sx - 7, sy - 3, 14, 16))
        pygame.draw.arc(screen, (120, 90, 60), (sx - 8, sy - 6, 16, 10), 0, 3.14, 4)
        pygame.draw.line(screen, (100, 70, 50), (sx, sy - 6), (sx, sy - 10), 2)
        
        # "5 POINTS" sparkle
        if pygame.time.get_ticks() % 500 < 250:
            pygame.draw.circle(screen, (255, 255, 150), (sx, sy - 20), 4)



class Bird:
    """Bird that flies across the sky in flocks - day only"""
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.direction = random.choice([-1, 1])
        if self.direction == 1:
            self.x = random.randint(-200, -50)
        else:
            self.x = random.randint(SCREEN_WIDTH + 50, SCREEN_WIDTH + 200)
        self.y = random.randint(60, 250)
        self.speed = random.uniform(2.5, 4.5)
        self.wing_span = random.randint(10, 16)
        self.flap_speed = random.uniform(0.15, 0.25)
        self.phase = random.random() * 6.28
        self.active = True
    
    def update(self):
        if not self.active:
            return
        self.x += self.speed * self.direction
        self.phase += self.flap_speed
        if self.direction == 1 and self.x > SCREEN_WIDTH + 100:
            self.active = False
        elif self.direction == -1 and self.x < -100:
            self.active = False
    
    def draw(self, screen):
        if not self.active:
            return
        sx = int(self.x)
        sy = int(self.y)
        flap = abs(math.sin(self.phase))
        wing_len = int(self.wing_span * (0.6 + 0.4 * flap))
        bird_color = (60, 60, 70) if pygame.time.get_ticks() % 2000 < 1000 else (80, 80, 90)
        pygame.draw.ellipse(screen, bird_color, (sx - 4, sy - 2, 8, 5))
        wing_y = sy - int(flap * 6)
        if pygame.time.get_ticks() % 150 < 75:
            pygame.draw.line(screen, bird_color, (sx, sy), (sx - wing_len//2, wing_y), 2)
            pygame.draw.line(screen, bird_color, (sx, sy), (sx + wing_len//2, wing_y), 2)
        else:
            pygame.draw.line(screen, bird_color, (sx, sy - 4), (sx - wing_len, sy + 2), 2)
            pygame.draw.line(screen, bird_color, (sx, sy - 4), (sx + wing_len, sy + 2), 2)


class BirdFlock:
    """Manager for a flock of birds"""
    def __init__(self):
        self.birds = []
        self.spawn_timer = random.randint(600, 1800)
        self.next_flock_size = random.randint(3, 6)
    
    def update(self, hour):
        is_day = 6 <= hour < 19
        if is_day:
            self.spawn_timer -= 1
            if self.spawn_timer <= 0:
                self.spawn_flock()
                self.spawn_timer = random.randint(600, 2400)
        else:
            for bird in self.birds:
                bird.active = False
        for bird in self.birds:
            bird.update()
        self.birds = [b for b in self.birds if b.active]
    
    def spawn_flock(self):
        direction = random.choice([-1, 1])
        start_x = -100 if direction == 1 else SCREEN_WIDTH + 100
        start_y = random.randint(100, 300)
        flock_size = self.next_flock_size
        lead = Bird()
        lead.direction = direction
        lead.x = start_x
        lead.y = start_y
        lead.speed = random.uniform(3, 4.5)
        lead.active = True
        self.birds.append(lead)
        for i in range(1, flock_size):
            bird = Bird()
            bird.direction = direction
            bird.x = start_x - (i * 25 * direction)
            bird.y = start_y + ((i % 2) * 2 - 1) * (15 + i * 8)
            bird.speed = lead.speed * random.uniform(0.95, 1.05)
            bird.active = True
            self.birds.append(bird)
        self.next_flock_size = random.randint(3, 6)
    
    def draw(self, screen):
        for bird in self.birds:
            bird.draw(screen)


class BouncingBall:
    """A colorful beach ball that bounces around the park for dogs to chase!"""
    
    def __init__(self, screen_width, screen_height):
        self.radius = 20
        self.x = random.randint(self.radius, screen_width - self.radius)
        self.y = screen_height - self.radius - 80
        self.vx = random.choice([-4, -3, 3, 4])
        self.vy = -6
        self.gravity = 0.2
        self.bounce_dampening = 0.8
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.rotation = 0
        self.colors = [
            (255, 100, 100),  # Red
            (100, 200, 255),  # Blue
            (255, 255, 100),  # Yellow
            (100, 255, 150),  # Green
        ]
        
    def update(self):
        # Apply gravity
        self.vy += self.gravity
        
        # Update position
        self.x += self.vx
        self.y += self.vy
        
        # Rotate
        self.rotation = (self.rotation + 3) % 360
        
        # Bounce off ground
        ground_y = self.screen_height - 50
        if self.y + self.radius > ground_y:
            self.y = ground_y - self.radius
            self.vy *= -self.bounce_dampening
            # Re-bounce if energy low
            if abs(self.vy) < 2:
                self.vy = -random.uniform(5, 9)
                self.vx = random.choice([-4, -3, 3, 4])
                
        # Bounce off walls
        if self.x - self.radius < 0:
            self.x = self.radius
            self.vx *= -1
        elif self.x + self.radius > self.screen_width:
            self.x = self.screen_width - self.radius
            self.vx *= -1
            
    def draw(self, screen):
        center = (int(self.x), int(self.y))
        
        # Draw beach ball sections
        for i, color in enumerate(self.colors):
            angle_start = math.radians(self.rotation + i * 90)
            angle_end = math.radians(self.rotation + (i + 1) * 90)
            
            points = [center]
            steps = 8
            for j in range(steps + 1):
                angle = angle_start + (angle_end - angle_start) * j / steps
                px = center[0] + math.cos(angle) * self.radius
                py = center[1] + math.sin(angle) * self.radius
                points.append((int(px), int(py)))
            pygame.draw.polygon(screen, color, points)
        
        # Center white circle
        pygame.draw.circle(screen, (255, 255, 255), center, self.radius // 3)
        # Outer rim
        pygame.draw.circle(screen, (220, 220, 220), center, self.radius, 2)


class Game:
    def __init__(self):
        print("Initializing Treat Quest v3...", flush=True)
        
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
        
        pygame.display.set_caption("Treat Quest - Harley & Shanti v3")
        self.clock = pygame.time.Clock()
        
        try:
            self.font = pygame.font.Font(None, 80)
            self.font_med = pygame.font.Font(None, 56)
            self.font_small = pygame.font.Font(None, 40)
        except:
            self.font = pygame.font.SysFont('arial', 60)
            self.font_med = pygame.font.SysFont('arial', 40)
            self.font_small = pygame.font.SysFont('arial', 30)
        
        # Dogs
        self.dogs = [
            Dog('harley', SCREEN_WIDTH // 3, SCREEN_HEIGHT - 150),
            Dog('shanti', 2 * SCREEN_WIDTH // 3, SCREEN_HEIGHT - 150)
        ]
        
        # Treats
        self.treats = [Treat(random.randint(200, SCREEN_WIDTH - 200),
                            SCREEN_HEIGHT - random.randint(130, 220))
                      for _ in range(12)]
        
        # Golden treat (rare 5-point bonus!)
        self.golden_treat = GoldenTreat()
        
        # Puddles (slow dogs down)
        self.puddles = [Puddle() for _ in range(3)]
        
        # Stars for night
        self.stars = [Star() for _ in range(100)]
        
        # Fireflies (appear at night)
        self.fireflies = [Firefly() for _ in range(15)]
        
        # Butterflies (appear during day)
        self.butterflies = [Butterfly() for _ in range(6)]
        
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
        self.rain = [RainDrop() for _ in range(150)]
        
        # Scene elements
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
        
        # Initial weather fetch
        get_tampa_weather()
        
        # Squirrel NPC (bonus 5-point acorn!)
        self.squirrel = Squirrel()
        
        # Bouncing beach ball
        self.ball = BouncingBall(SCREEN_WIDTH, SCREEN_HEIGHT)
        
        # Bird flocks (day only)
        self.bird_flock = BirdFlock()
        self.bonus_acorn = None
        
        print("Game initialized!", flush=True)
    
    def draw_hills(self):
        for i, hill in enumerate(self.hills):
            h_color = (hill['color'][0] - 20, hill['color'][1] - 20, hill['color'][2] - 10)
            pygame.draw.ellipse(self.screen, h_color,
                              (hill['x'] - hill['width']//2, 
                               SCREEN_HEIGHT - 200 - hill['height'],
                               hill['width'], hill['height'] * 2))
            pygame.draw.ellipse(self.screen, hill['color'],
                              (hill['x'] - hill['width']//3,
                               SCREEN_HEIGHT - 180 - hill['height']//2,
                               hill['width'] * 2//3, hill['height']))
    
    def draw_hydrant(self):
        hx, hy = self.hydrant_x, SCREEN_HEIGHT - 145
        
        pygame.draw.rect(self.screen, (220, 200, 50), (hx - 12, hy - 35, 24, 55))
        pygame.draw.rect(self.screen, (200, 180, 40), (hx - 15, hy - 42, 30, 10))
        pygame.draw.rect(self.screen, (180, 160, 30), (hx - 18, hy - 45, 36, 5))
        pygame.draw.rect(self.screen, (200, 180, 40), (hx - 22, hy - 25, 8, 12))
        pygame.draw.rect(self.screen, (200, 180, 40), (hx + 14, hy - 25, 8, 12))
        pygame.draw.line(self.screen, (100, 100, 100), (hx + 18, hy - 20), (hx + 25, hy - 10), 2)
        pygame.draw.rect(self.screen, (180, 160, 30), (hx - 14, hy + 15, 28, 8))
    
    def draw_doghouse(self):
        x, y = self.doghouse_x, SCREEN_HEIGHT - 145
        wall_h = 70
        roof_h = 40
        width = 100
        
        pygame.draw.rect(self.screen, (200, 60, 60), (x - width//2, y - wall_h, width, wall_h))
        
        roof_points = [
            (x - width//2 - 10, y - wall_h),
            (x, y - wall_h - roof_h),
            (x + width//2 + 10, y - wall_h)
        ]
        pygame.draw.polygon(self.screen, (180, 40, 40), roof_points)
        pygame.draw.ellipse(self.screen, (50, 40, 30), (x - 18, y - wall_h + 20, 36, wall_h - 20))
        pygame.draw.polygon(self.screen, (255, 255, 255), roof_points, 4)
        pygame.draw.rect(self.screen, (255, 255, 255), (x - width//2, y - wall_h, width, 3))
        
        try:
            text = self.font_small.render("HOME", True, (255, 255, 255))
            self.screen.blit(text, (x - text.get_width()//2, y - wall_h - 25))
        except:
            pass
    
    def draw_bg(self, sky_top, sky_bottom, time_type):
        # Sky gradient
        for y in range(SCREEN_HEIGHT):
            p = y / SCREEN_HEIGHT
            r = int(sky_top[0] * (1-p) + sky_bottom[0] * p)
            g = int(sky_top[1] * (1-p) + sky_bottom[1] * p)
            b = int(sky_top[2] * (1-p) + sky_bottom[2] * p)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        
        # Sun/moon
        if time_type in ['night', 'cloudy-night']:
            # Moon
            pygame.draw.circle(self.screen, (220, 220, 240), (100, 80), 40)
            pygame.draw.circle(self.screen, sky_top, (85, 70), 35)  # Crescent
        elif time_type == 'sunset':
            # Setting sun
            pygame.draw.circle(self.screen, (255, 100, 50), (SCREEN_WIDTH - 150, 200), 60)
        elif time_type == 'dawn':
            # Rising sun
            pygame.draw.circle(self.screen, (255, 200, 100), (100, 150), 50)
        else:
            # Day sun
            pygame.draw.circle(self.screen, (255, 250, 200), (120, 100), 70)
            pygame.draw.circle(self.screen, (255, 240, 150), (120, 100), 55)
            # Sun rays
            for angle in range(0, 360, 30):
                rad = math.radians(angle)
                x1 = 120 + math.cos(rad) * 80
                y1 = 100 + math.sin(rad) * 80
                x2 = 120 + math.cos(rad) * 95
                y2 = 100 + math.sin(rad) * 95
                pygame.draw.line(self.screen, (255, 255, 180), (x1, y1), (x2, y2), 2)
        
        self.draw_hills()
    
    def draw_clouds(self, time_type):
        is_night = 'night' in time_type
        cloud_color = (180, 180, 190) if is_night else (255, 255, 255)
        
        for c in self.clouds:
            c['x'] = (c['x'] + c['speed']) % (SCREEN_WIDTH + 200) - 100
            x, y, s = int(c['x']), c['y'], c['size']
            pygame.draw.ellipse(self.screen, cloud_color, (x - s//2, y, s, s//2))
            pygame.draw.ellipse(self.screen, cloud_color, (x - s//3, y - s//4, s//2, s//2))
            pygame.draw.ellipse(self.screen, cloud_color, (x - s//6, y - s//5, s//3, s//3))
    
    def draw_stars(self):
        for star in self.stars:
            star.draw(self.screen)
    
    def draw_rain(self):
        for drop in self.rain:
            drop.update()
            drop.draw(self.screen)
    
    def draw_fireflies(self, hour):
        """Draw fireflies at night"""
        if hour >= 20 or hour <= 5:
            for firefly in self.fireflies:
                firefly.update()
                firefly.draw(self.screen)
    
    def draw_butterflies(self, hour):
        """Draw butterflies during day"""
        if 6 <= hour < 19:
            for butterfly in self.butterflies:
                butterfly.update()
                butterfly.draw(self.screen)
    
    def draw_ground(self, time_type):
        # Grass colors based on time
        if 'night' in time_type:
            grass_top = (50, 100, 40)
            grass_bottom = (40, 80, 35)
        elif time_type == 'sunset':
            grass_top = (80, 160, 60)
            grass_bottom = (60, 120, 45)
        else:
            grass_top = (100, 200, 80)
            grass_bottom = (60, 160, 50)
        
        pygame.draw.rect(self.screen, grass_top, (0, SCREEN_HEIGHT - 90, SCREEN_WIDTH, 45))
        pygame.draw.rect(self.screen, grass_bottom, (0, SCREEN_HEIGHT - 45, SCREEN_WIDTH, 45))
        
        for x in range(0, SCREEN_WIDTH, 40):
            pygame.draw.line(self.screen, (40, 120, 35),
                           (x, SCREEN_HEIGHT - 90), (x + 3, SCREEN_HEIGHT - 102), 2)
    
    def draw(self):
        # Get real time

        now = datetime.now()
        hour = now.hour
        
        # Get weather
        wx = get_tampa_weather()
        condition = wx['condition']
        temp = wx['temp']
        
        # Get sky colors
        sky_top, sky_bottom, time_type = get_sky_colors(condition, wx.get('is_day', 1), hour)
        
        self.draw_bg(sky_top, sky_bottom, time_type)
        
        if 'night' in time_type:
            self.draw_stars()
        
        self.draw_clouds(time_type)
        
        # Draw birds (day only)
        self.bird_flock.draw(self.screen)
        
        # Background elements
        self.draw_hydrant()
        self.draw_doghouse()
        
        self.draw_ground(time_type)
        
        # Draw puddles (on ground, behind dogs)
        for puddle in self.puddles:
            puddle.draw(self.screen)
        
        # Fireflies at night
        self.draw_fireflies(hour)
        
        # Butterflies during day  
        self.draw_butterflies(hour)
        
        if condition in ['rain', 'storm']:
            self.draw_rain()
        
        # Night creatures
        if 'night' in time_type:
            for firefly in self.fireflies:
                firefly.update()
                firefly.draw(self.screen)
        
        # Day creatures
        if time_type in ['sunny', 'partly', 'cloudy', 'dawn', 'sunset']:
            for butterfly in self.butterflies:
                butterfly.update()
                butterfly.draw(self.screen)
        
        # Update golden treat
        self.golden_treat.update()
        
        # Update puddles
        for puddle in self.puddles:
            puddle.update()
        
        # Check golden treat collection
        if self.golden_treat.active and not self.golden_treat.collected:
            for dog in self.dogs:
                dx = self.golden_treat.x - dog.x
                dy = self.golden_treat.y - dog.y
                if math.sqrt(dx*dx + dy*dy) < 50:
                    self.golden_treat.collected = True
                    dog.score += 5
                    break
        
        for t in self.treats:
            t.draw(self.screen)
        
        for dog in self.dogs:
            dog.draw(self.screen)
        
        # Draw squirrel (in front of dogs)
        self.squirrel.draw(self.screen)
        
        # Draw bonus acorn if active
        if self.bonus_acorn and self.bonus_acorn.active:
            self.bonus_acorn.draw(self.screen)
        
        # Title
        title = self.font.render("TREAT QUEST", True, (255, 200, 50))
        subtitle = self.font_med.render("Harley & Shanti's Dog Park", True, (255, 255, 255))
        self.screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 30))
        self.screen.blit(subtitle, (SCREEN_WIDTH//2 - subtitle.get_width()//2, 105))
        
        # Time and weather display
        time_str = now.strftime("%I:%M %p")
        time_surf = self.font_small.render(time_str, True, (255, 255, 255))
        self.screen.blit(time_surf, (SCREEN_WIDTH - 180, 30))
        
        wx_surf = self.font_small.render(f"Tampa: {condition.title()}, {temp}°F", True, (255, 255, 255))
        self.screen.blit(wx_surf, (SCREEN_WIDTH - 320, 70))
        
        # Scores
        harley_surf = self.font_small.render(f"HARLEY: {self.dogs[0].score}", True, (255, 100, 100))
        shanti_surf = self.font_small.render(f"SHANTI: {self.dogs[1].score}", True, (100, 100, 255))
        self.screen.blit(harley_surf, (30, 30))
        self.screen.blit(shanti_surf, (30, 70))
        
        # Draw bouncing ball
        self.ball.draw(self.screen)
        
        # Dog tags
        for dog in self.dogs:
            name_surf = self.font_small.render(dog.name.upper(), True, (255, 255, 255))
            tag_w = name_surf.get_width() + 20
            pygame.draw.rect(self.screen, (0, 0, 0, 150),
                           (int(dog.x) - tag_w//2, int(dog.y) - 72, tag_w, 28))
            self.screen.blit(name_surf, (int(dog.x) - name_surf.get_width()//2, int(dog.y) - 67))
        
        pygame.display.flip()
    
    def update(self):
        # Update golden treat
        self.golden_treat.update()
        
        # Update puddles
        for puddle in self.puddles:
            puddle.update()
        
        # Check golden treat collection
        if self.golden_treat.active and not self.golden_treat.collected:
            for dog in self.dogs:
                dx = self.golden_treat.x - dog.x
                dy = self.golden_treat.y - dog.y
                if math.sqrt(dx*dx + dy*dy) < 50:
                    self.golden_treat.collected = True
                    dog.score += 5
                    break
        
        for t in self.treats:
            t.update()
        
        for i, dog in enumerate(self.dogs):
            other = self.dogs[1-i]
            dog.update(self.treats, other)
            
            # Check puddle collisions and apply slowdown
            for puddle in self.puddles:
                if puddle.check_collision(dog):
                    dog.vx *= 0.7  # Slow down in puddle
        
        # Update squirrel and check for acorn drop
        dropped_acorn = self.squirrel.update(self.dogs)
        
        # Update bouncing ball
        self.ball.update()
        


        now = datetime.now()
        hour = now.hour
        # Update birds (day only)
        self.bird_flock.update(hour)
        if dropped_acorn and self.bonus_acorn is None:
            self.bonus_acorn = AcornBonus(dropped_acorn['x'], dropped_acorn['y'])
        
        # Update bonus acorn if active
        if self.bonus_acorn:
            self.bonus_acorn.update()
            if not self.bonus_acorn.active:
                self.bonus_acorn = None
            else:
                # Check if a dog collects the acorn
                for dog in self.dogs:
                    dx = self.bonus_acorn.x - dog.x
                    dy = self.bonus_acorn.y - dog.y
                    if math.sqrt(dx*dx + dy*dy) < 45:
                        dog.score += 5  # 5 point bonus!
                        self.bonus_acorn = None
                        break
    
    def run(self):
        running = True
        print("Starting Treat Quest v3!", flush=True)
        print("Real Tampa weather + actual time of day", flush=True)
        
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
    print("Treat Quest v3: Real Weather Edition", flush=True)
    Game().run()
