#!/usr/bin/env python3
"""
Treat Quest: SPACE EDITION v5.0
Dogs in Space - Zero-G Dog Park
Harley & Shanti with jetpacks, floating in space!
"""

import pygame
import random
import sys
import math
import os
import subprocess
import json
from datetime import datetime

os.environ['SDL_VIDEODRIVER'] = 'x11'
os.environ['SDL_AUDIODRIVER'] = 'dummy'

pygame.init()

info = pygame.display.Info()
SCREEN_WIDTH = info.current_w if info.current_w > 0 else 1920
SCREEN_HEIGHT = info.current_h if info.current_h > 0 else 1080
FPS = 60

print(f"Space Screen: {SCREEN_WIDTH}x{SCREEN_HEIGHT}", flush=True)

# Space weather cache
space_weather_cache = {'condition': 'sunny', 'temp': 72, 'last_update': 0}
WEATHER_UPDATE_INTERVAL = 600

def get_tampa_weather():
    """Fetch weather (now from Space Station Tampa!)"""
    global space_weather_cache
    now = pygame.time.get_ticks()
    
    if now - space_weather_cache['last_update'] < WEATHER_UPDATE_INTERVAL * 1000:
        return space_weather_cache
    
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
            space_weather_cache['temp'] = int(current.get('temperature_2m', 72))
            space_weather_cache['last_update'] = now
            
            # Space weather conditions
            if code in [95, 96, 99]:
                space_weather_cache['condition'] = 'meteor_storm'
            elif code in [51, 53, 55, 56, 57, 61, 63, 65, 80, 81, 82]:
                space_weather_cache['condition'] = 'solar_rain'
            elif code in [45, 48, 3]:
                space_weather_cache['condition'] = 'nebula'
            else:
                space_weather_cache['condition'] = 'clear_space'
            
            print(f"Space weather: {space_weather_cache['condition']}, Earth: {space_weather_cache['temp']}°F", flush=True)
    except Exception as e:
        print(f"Space weather error: {e}", flush=True)
    
    return space_weather_cache


class SpaceDog:
    """Harley or Shanti in space with jetpack!"""
    def __init__(self, name, x, y):
        self.name = name
        self.x, self.y = x, y
        self.vx, self.vy = 0, 0
        self.angle = 0
        self.spin = 0
        self.score = 0
        self.anim_frame = 0
        self.anim_timer = 0
        self.has_acorn = False
        
        if name == 'harley':
            self.width, self.height = 38, 30
            self.color = (255, 250, 230)
            self.ear_color = (220, 190, 150)
            self.suit_color = (255, 100, 100)  # Red space suit
            self.secondary = (240, 230, 210)
            self.speed = 0.15
            self.ear_type = 'floppy'
        else:
            self.width, self.height = 54, 42
            self.color = (145, 100, 55)
            self.ear_color = (110, 75, 40)
            self.suit_color = (100, 100, 255)  # Blue space suit
            self.secondary = (165, 115, 65)
            self.speed = 0.12
            self.ear_type = 'perky'
        
        self.trail = []  # Jetpack trail
    
    def space_ai_update(self, treats, other_dog):
        """Zero-G AI - float and use jetpack to navigate"""
        # Find nearest treat
        nearest = None
        nearest_dist = 9999
        for t in treats:
            if not t.collected:
                tdx, tdy = t.x - self.x, t.y - self.y
                td = math.sqrt(tdx*tdx + tdy*tdy)
                if td < nearest_dist and td < 500:
                    nearest_dist, nearest = td, t
        
        if nearest:
            # Point toward treat
            dx = nearest.x - self.x
            dy = nearest.y - self.y
            target_angle = math.atan2(dy, dx)
            
            # Smooth rotation
            angle_diff = target_angle - self.angle
            while angle_diff > math.pi: angle_diff -= 2*math.pi
            while angle_diff < -math.pi: angle_diff += 2*math.pi
            self.angle += angle_diff * 0.05
            
            # Jetpack thrust toward target
            if nearest_dist > 100:
                self.vx += math.cos(self.angle) * self.speed
                self.vy += math.sin(self.angle) * self.speed
        
        # Random drifting behavior
        if random.random() < 0.02:
            self.spin = random.uniform(-0.05, 0.05)
            self.vx += random.uniform(-0.5, 0.5)
            self.vy += random.uniform(-0.5, 0.5)
        
        # Bounds - wrap around screen (space is infinite!)
        if self.x < -50: self.x = SCREEN_WIDTH + 50
        if self.x > SCREEN_WIDTH + 50: self.x = -50
        if self.y < -50: self.y = SCREEN_HEIGHT + 50
        if self.y > SCREEN_HEIGHT + 50: self.y = -50
    
    def update(self, treats, other_dog):
        self.space_ai_update(treats, other_dog)
        
        # Zero-G physics - no gravity!
        self.x += self.vx
        self.y += self.vy
        self.angle += self.spin
        
        # Dampen velocity (space friction)
        self.vx *= 0.98
        self.vy *= 0.98
        self.spin *= 0.95
        
        # Jetpack trail
        if abs(self.vx) > 0.5 or abs(self.vy) > 0.5:
            self.trail.append({
                'x': self.x, 
                'y': self.y, 
                'life': 30,
                'color': self.suit_color
            })
        
        # Update trail
        for t in self.trail:
            t['life'] -= 1
        self.trail = [t for t in self.trail if t['life'] > 0]
        
        self.anim_timer += 1
        if self.anim_timer > 8:
            self.anim_timer = 0
            self.anim_frame = (self.anim_frame + 1) % 4
        
        # Collect treats
        for t in treats:
            if not t.collected:
                dx, dy = self.x - t.x, self.y - t.y
                if math.sqrt(dx*dx + dy*dy) < 50:
                    t.collected = True
                    t.respawn_timer = 400
                    t.collector = self.name
                    self.score += t.value
                    # Spin celebration!
                    self.spin = random.uniform(-0.3, 0.3)
    
    def draw(self, screen):
        # Draw jetpack trail
        for t in self.trail:
            alpha = t['life'] / 30
            size = int(8 * alpha)
            color = (int(t['color'][0] * alpha), int(t['color'][1] * alpha), int(t['color'][2] * alpha))
            pygame.draw.circle(screen, color, (int(t['x']), int(t['y'])), size)
        
        # Space dog with rotation
        sx, sy = int(self.x), int(self.y)
        
        # Calculate rotated points for body
        cos_a = math.cos(self.angle)
        sin_a = math.sin(self.angle)
        
        # Space suit body (larger than regular dog)
        suit_points = []
        for dx, dy in [(-20, -15), (20, -15), (25, 0), (20, 15), (-20, 15), (-25, 0)]:
            rx = sx + dx * cos_a - dy * sin_a
            ry = sy + dx * sin_a + dy * cos_a
            suit_points.append((rx, ry))
        pygame.draw.polygon(screen, self.suit_color, suit_points)
        pygame.draw.polygon(screen, (200, 200, 200), suit_points, 3)  # Suit trim
        
        # Helmet (clear bubble)
        helmet_x = sx + 15 * cos_a
        helmet_y = sy + 15 * sin_a
        pygame.draw.circle(screen, (200, 230, 255), (int(helmet_x), int(helmet_y)), 22)
        pygame.draw.circle(screen, (150, 200, 255), (int(helmet_x), int(helmet_y)), 22, 2)
        
        # Dog face inside helmet
        face_x = int(helmet_x + 5 * cos_a - 3 * sin_a)
        face_y = int(helmet_y + 5 * sin_a + 3 * cos_a)
        pygame.draw.ellipse(screen, self.color, (face_x - 12, face_y - 10, 24, 20))
        
        # Eyes (space goggles)
        eye_x = int(helmet_x + 8 * cos_a)
        eye_y = int(helmet_y + 8 * sin_a)
        pygame.draw.circle(screen, (50, 50, 50), (eye_x, eye_y), 4)
        pygame.draw.circle(screen, (200, 255, 200), (eye_x + 1, eye_y - 1), 2)
        
        # Ears (poking out of helmet slightly)
        if self.ear_type == 'floppy':
            ear_base_x = int(helmet_x - 10 * cos_a)
            ear_base_y = int(helmet_y - 10 * sin_a)
            pygame.draw.ellipse(screen, self.ear_color, 
                               (ear_base_x - 8, ear_base_y - 15, 8, 18))
        else:
            # Perky ears on helmet
            ear_tip_x = int(helmet_x - 15 * cos_a - 20 * sin_a)
            ear_tip_y = int(helmet_y - 15 * sin_a + 20 * cos_a)
            pygame.draw.polygon(screen, self.ear_color, 
                              [(helmet_x - 15*cos_a, helmet_y - 15*sin_a),
                               (ear_tip_x, ear_tip_y),
                               (helmet_x - 10*cos_a - 5*sin_a, helmet_y - 10*sin_a + 5*cos_a)])
        
        # Jetpack flames
        flame_x = sx - 25 * cos_a
        flame_y = sy - 25 * sin_a
        flame_size = random.randint(8, 16)
        flame_color = random.choice([(255, 150, 50), (255, 200, 100), (255, 100, 50)])
        pygame.draw.ellipse(screen, flame_color, 
                           (int(flame_x - flame_size//2), int(flame_y - flame_size//2), 
                            flame_size, flame_size + 8))
        
        # Space suit details
        pygame.draw.rect(screen, (100, 100, 100), 
                        (int(sx - 8), int(sy - 8), 16, 16))  # Chest plate
        pygame.draw.circle(screen, (255, 200, 50), (int(sx), int(sy)), 5)  # Mission patch
        
        # Name tag above dog
        name_text = self.name.upper()
        try:
            name_font = pygame.font.SysFont('arial', 24, bold=True)
            name_surf = name_font.render(name_text, True, (255, 255, 255))
            name_bg = pygame.Surface((name_surf.get_width() + 10, name_surf.get_height() + 6))
            name_bg.fill((0, 0, 0))
            name_bg.set_alpha(180)
            # Position name tag above dog
            name_x = int(sx) - name_surf.get_width() // 2
            name_y = int(sy) - 55
            screen.blit(name_bg, (name_x - 5, name_y - 3))
            screen.blit(name_surf, (name_x, name_y))
        except:
            pass


class SpaceTreat:
    """Floating space treats!"""
    def __init__(self, x, y, treat_type='satellite'):
        self.x, self.y = x, y
        self.vx = random.uniform(-0.5, 0.5)
        self.vy = random.uniform(-0.3, 0.3)
        self.collected = False
        self.respawn_timer = 0
        self.type = treat_type
        self.value = 1
        self.rotation = 0
        self.rot_speed = random.uniform(-0.02, 0.02)
        
        if treat_type == 'satellite':
            self.value = 1
            self.color = (200, 200, 220)
        elif treat_type == 'cosmic_bone':
            self.value = 3
            self.color = (255, 220, 150)
        elif treat_type == 'alien_snack':
            self.value = 10
            self.color = (150, 255, 150)
        
        self.bob = random.random() * 6.28
    
    def update(self):
        if self.collected:
            self.respawn_timer -= 1
            if self.respawn_timer <= 0:
                self.collected = False
                self.x = random.randint(100, SCREEN_WIDTH - 100)
                self.y = random.randint(100, SCREEN_HEIGHT - 100)
                self.vx = random.uniform(-0.5, 0.5)
                self.vy = random.uniform(-0.3, 0.3)
            return
        
        # Float in space
        self.x += self.vx
        self.y += self.vy
        self.rotation += self.rot_speed
        self.bob += 0.05
        
        # Wrap around
        if self.x < 0: self.x = SCREEN_WIDTH
        if self.x > SCREEN_WIDTH: self.x = 0
        if self.y < 0: self.y = SCREEN_HEIGHT
        if self.y > SCREEN_HEIGHT: self.y = 0
    
    def draw(self, screen):
        if self.collected:
            return
        
        y_off = math.sin(self.bob) * 8
        sx, sy = int(self.x), int(self.y + y_off)
        
        if self.type == 'satellite':
            # Satellite dish
            pygame.draw.circle(screen, self.color, (sx, sy), 12)
            pygame.draw.circle(screen, (100, 100, 120), (sx, sy), 8)
            pygame.draw.line(screen, (150, 150, 170), (sx, sy), (sx, sy + 20), 3)
            # Solar panels
            pygame.draw.rect(screen, (80, 80, 150), (sx - 20, sy + 18, 40, 8))
        
        elif self.type == 'cosmic_bone':
            # Glowing bone
            pygame.draw.ellipse(screen, self.color, (sx - 12, sy - 4, 24, 10))
            pygame.draw.circle(screen, self.color, (sx - 10, sy - 3), 5)
            pygame.draw.circle(screen, self.color, (sx + 10, sy - 3), 5)
            pygame.draw.circle(screen, self.color, (sx - 10, sy + 3), 5)
            pygame.draw.circle(screen, self.color, (sx + 10, sy + 3), 5)
            # Glow
            pygame.draw.circle(screen, (255, 255, 200, 128), (sx, sy - 15), 6)
        
        else:  # alien_snack
            # Weird alien food
            pygame.draw.ellipse(screen, (255, 100, 200), (sx - 10, sy - 8, 20, 16))
            pygame.draw.circle(screen, (100, 255, 100), (sx, sy - 12), 4)
            pygame.draw.circle(screen, (100, 255, 100), (sx - 8, sy + 8), 3)
            pygame.draw.circle(screen, (100, 255, 100), (sx + 8, sy + 8), 3)


class Asteroid:
    """Floating space rocks"""
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(-100, SCREEN_HEIGHT // 2)
        self.size = random.randint(30, 80)
        self.vx = random.uniform(-0.3, 0.3)
        self.vy = random.uniform(0.1, 0.5)
        self.rotation = random.random() * 6.28
        self.rot_speed = random.uniform(-0.01, 0.01)
        self.color = (120, 110, 100)
        self.points = []
        # Generate irregular asteroid shape
        for i in range(8):
            angle = i * math.pi / 4
            r = self.size * random.uniform(0.7, 1.3)
            self.points.append((math.cos(angle) * r, math.sin(angle) * r))
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.rotation += self.rot_speed
        
        if self.y > SCREEN_HEIGHT + 100:
            self.y = -100
            self.x = random.randint(0, SCREEN_WIDTH)
    
    def draw(self, screen):
        # Rotate points
        cos_r = math.cos(self.rotation)
        sin_r = math.sin(self.rotation)
        rotated_points = []
        for px, py in self.points:
            rx = px * cos_r - py * sin_r + self.x
            ry = px * sin_r + py * cos_r + self.y
            rotated_points.append((rx, ry))
        
        pygame.draw.polygon(screen, self.color, rotated_points)
        pygame.draw.polygon(screen, (80, 70, 60), rotated_points, 2)
        # Craters
        pygame.draw.circle(screen, (90, 80, 70), (int(self.x - 5), int(self.y - 5)), 8)


class UFO:
    """Flying saucer - drops space snacks!"""
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.active = False
        self.spawn_timer = random.randint(1200, 2400)  # 20-40 seconds
        self.x = -100
        self.y = random.randint(50, 200)
        self.vx = random.uniform(2, 4)
        self.direction = 1
        self.beam_active = False
        self.snack_dropped = False
    
    def spawn(self):
        self.active = True
        self.direction = random.choice([-1, 1])
        self.x = -100 if self.direction == 1 else SCREEN_WIDTH + 100
        self.vx = self.direction * random.uniform(2, 4)
        self.y = random.randint(50, 200)
        self.snack_dropped = False
        self.beam_active = False
    
    def update(self):
        if not self.active:
            self.spawn_timer -= 1
            if self.spawn_timer <= 0:
                self.spawn()
            return None
        
        self.x += self.vx
        
        # Drop snack in middle of screen
        if not self.snack_dropped and 200 < self.x < SCREEN_WIDTH - 200:
            self.beam_active = True
            if random.random() < 0.05:  # 5% chance per frame to drop
                self.snack_dropped = True
                self.beam_active = False
                return {'x': self.x, 'y': self.y + 60, 'active': True}
        
        # Off screen check
        if (self.direction == 1 and self.x > SCREEN_WIDTH + 150) or \
           (self.direction == -1 and self.x < -150):
            self.reset()
        
        return None
    
    def draw(self, screen):
        if not self.active:
            return
        
        sx, sy = int(self.x), int(self.y)
        
        # UFO body (saucer)
        pygame.draw.ellipse(screen, (200, 200, 220), (sx - 35, sy - 10, 70, 25))
        pygame.draw.ellipse(screen, (150, 150, 170), (sx - 20, sy - 20, 40, 20))
        
        # Dome
        pygame.draw.ellipse(screen, (100, 200, 255, 150), (sx - 15, sy - 25, 30, 20))
        
        # Lights
        for i in range(5):
            lx = sx - 30 + i * 15
            color = (255, 100, 100) if i % 2 == 0 else (100, 255, 100)
            pygame.draw.circle(screen, color, (lx, sy), 4)
        
        # Tractor beam
        if self.beam_active:
            beam_alpha = int(128 + 127 * math.sin(pygame.time.get_ticks() * 0.01))
            pygame.draw.polygon(screen, (200, 255, 200, beam_alpha), [
                (sx - 20, sy + 10),
                (sx + 20, sy + 10),
                (sx + 40, sy + 80),
                (sx - 40, sy + 80)
            ])


class SpaceSnack:
    """Alien snack dropped by UFO"""
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.vx = random.uniform(-1, 1)
        self.vy = 2
        self.active = True
        self.lifetime = 500
        self.rotation = 0
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.rotation += 0.05
        self.lifetime -= 1
        if self.lifetime <= 0 or self.y > SCREEN_HEIGHT:
            self.active = False
    
    def draw(self, screen):
        if not self.active:
            return
        
        sx, sy = int(self.x), int(self.y)
        
        # Spinning alien snack
        cos_r = math.cos(self.rotation)
        sin_r = math.sin(self.rotation)
        
        points = []
        for i in range(6):
            angle = i * math.pi / 3 + self.rotation
            r = 15 if i % 2 == 0 else 8
            px = sx + math.cos(angle) * r
            py = sy + math.sin(angle) * r
            points.append((px, py))
        
        pygame.draw.polygon(screen, (255, 100, 200), points)
        pygame.draw.polygon(screen, (200, 50, 150), points, 2)
        
        # Value indicator
        if self.lifetime > 100:
            pygame.draw.circle(screen, (255, 255, 100), (sx, sy - 25), 5)


class SpaceSquirrel:
    """Nutter the Squirrel in a space pod - faster than dogs!"""
    def __init__(self):
        self.reset()
        self.name = "Nutter"
    
    def reset(self):
        self.active = False
        self.spawn_timer = random.randint(1200, 2400)  # 20-40 seconds
        self.x = -60
        self.y = random.randint(100, SCREEN_HEIGHT - 200)
        self.vx = random.uniform(4, 6)
        self.direction = 1
        self.has_acorn = True
        self.angle = 0
        self.spin = 0
    
    def spawn(self):
        self.active = True
        self.direction = random.choice([-1, 1])
        if self.direction == 1:
            self.x = -60
            self.vx = random.uniform(4, 6)
        else:
            self.x = SCREEN_WIDTH + 60
            self.vx = -random.uniform(4, 6)
        self.y = random.randint(100, SCREEN_HEIGHT - 200)
        self.has_acorn = True
        self.angle = 0 if self.direction == 1 else math.pi
    
    def update(self, dogs):
        if not self.active:
            self.spawn_timer -= 1
            if self.spawn_timer <= 0:
                self.spawn()
            return None
        
        # Space pod movement
        self.x += self.vx
        self.angle += 0.02 * self.direction
        
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
                if dist < 50:  # Caught!
                    self.has_acorn = False
                    # Drop cosmic acorn
                    return {'x': self.x, 'y': self.y, 'active': True}
        
        return None
    
    def draw(self, screen):
        if not self.active:
            return
        
        sx, sy = int(self.x), int(self.y)
        
        # Space pod (glass bubble with squirrel inside)
        # Pod body
        pygame.draw.ellipse(screen, (150, 150, 170), (sx - 25, sy - 15, 50, 30))
        pygame.draw.ellipse(screen, (100, 100, 120), (sx - 25, sy - 15, 50, 30), 2)
        
        # Glass dome
        pygame.draw.ellipse(screen, (200, 230, 255, 180), (sx - 20, sy - 20, 40, 35))
        pygame.draw.ellipse(screen, (150, 200, 255), (sx - 20, sy - 20, 40, 35), 2)
        
        # Squirrel inside
        # Body
        pygame.draw.ellipse(screen, (180, 120, 60), (sx - 12, sy - 8, 24, 18))
        # Head
        pygame.draw.circle(screen, (180, 120, 60), (sx + 8, sy - 10), 10)
        # Eye
        pygame.draw.circle(screen, (0, 0, 0), (sx + 10, sy - 12), 3)
        pygame.draw.circle(screen, (255, 255, 255), (sx + 11, sy - 13), 1)
        # Tail (fluffy, curled in pod)
        pygame.draw.ellipse(screen, (200, 140, 80), (sx - 18, sy - 15, 15, 25))
        
        # Acorn in pod (if still has it)
        if self.has_acorn:
            acorn_x = sx + 15
            pygame.draw.ellipse(screen, (160, 120, 80), (acorn_x - 4, sy - 3, 8, 10))
            pygame.draw.arc(screen, (100, 80, 60), (acorn_x - 5, sy - 6, 10, 6), 0, 3.14, 2)
        
        # Pod thrusters (small flames)
        flame_dir = -1 if self.direction == 1 else 1
        flame_x = sx + 25 * flame_dir
        pygame.draw.ellipse(screen, (255, 150, 50), 
                           (flame_x - 3, sy - 4, 8, 8))
        
        # Name tag above pod
        try:
            name_font = pygame.font.SysFont('arial', 20, bold=True)
            name_surf = name_font.render(self.name, True, (255, 220, 150))
            name_bg = pygame.Surface((name_surf.get_width() + 8, name_surf.get_height() + 4))
            name_bg.fill((60, 40, 20))
            name_bg.set_alpha(180)
            name_x = sx - name_surf.get_width() // 2
            name_y = sy - 45
            screen.blit(name_bg, (name_x - 4, name_y - 2))
            screen.blit(name_surf, (name_x, name_y))
        except:
            pass


class Bestie:
    """Bestie - The antagonist in a spaceship stealing treats!"""
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.active = False
        self.spawn_timer = random.randint(1800, 3000)  # 30-50 seconds
        self.x = SCREEN_WIDTH + 100
        self.y = random.randint(80, SCREEN_HEIGHT // 2)
        self.vx = -2.5  # Moves left
        self.target_treat = None
        self.steal_cooldown = 0
        self.stolen_treats = 0
    
    def spawn(self):
        self.active = True
        self.x = SCREEN_WIDTH + 100
        self.y = random.randint(80, SCREEN_HEIGHT // 2)
        self.vx = -2.5
        self.target_treat = None
        self.steal_cooldown = 0
    
    def update(self, treats, dogs):
        if not self.active:
            self.spawn_timer -= 1
            if self.spawn_timer <= 0:
                self.spawn()
            return
        
        # Move across screen
        self.x += self.vx
        
        # Find nearest uncollected treat to steal
        if self.steal_cooldown <= 0:
            nearest = None
            nearest_dist = 9999
            for t in treats:
                if not t.collected:
                    tdx = t.x - self.x
                    tdy = t.y - self.y
                    td = math.sqrt(tdx*tdx + tdy*tdy)
                    if td < nearest_dist and td < 300:
                        nearest_dist, nearest = td, t
            
            if nearest and nearest_dist < 80:
                # STEAL THE TREAT!
                nearest.collected = True
                nearest.respawn_timer = 600  # Longer respawn
                self.stolen_treats += 1
                self.steal_cooldown = 120  # 2 seconds before next steal
                
                # Thwart dogs - push them away!
                for dog in dogs:
                    dx = dog.x - self.x
                    dy = dog.y - self.y
                    dist = math.sqrt(dx*dx + dy*dy)
                    if dist < 150 and dist > 0:
                        dog.vx += (dx / dist) * 3  # Push away
                        dog.vy += (dy / dist) * 3
                        dog.spin = random.uniform(-0.2, 0.2)  # Spin them!
        
        if self.steal_cooldown > 0:
            self.steal_cooldown -= 1
        
        # Off screen check
        if self.x < -150:
            self.reset()
    
    def draw(self, screen):
        if not self.active:
            return
        
        sx, sy = int(self.x), int(self.y)
        
        # Beastie's ship (stereotypical "Karen" cruiser - entitled looking)
        # Main hull
        pygame.draw.ellipse(screen, (220, 220, 240), (sx - 40, sy - 20, 80, 40))
        pygame.draw.ellipse(screen, (180, 180, 200), (sx - 40, sy - 20, 80, 40), 2)
        
        # Cockpit (where Beastie is)
        pygame.draw.ellipse(screen, (200, 180, 255), (sx - 15, sy - 25, 30, 20))
        pygame.draw.ellipse(screen, (150, 150, 180), (sx - 15, sy - 25, 30, 20), 2)
        
        # Beastie's face (simplified Karen hair + angry eyes)
        face_x, face_y = sx, sy - 18
        # Hair (the "Karen" cut)
        pygame.draw.polygon(screen, (120, 80, 60), [
            (face_x - 12, face_y - 8),
            (face_x - 8, face_y - 15),
            (face_x, face_y - 12),
            (face_x + 8, face_y - 15),
            (face_x + 12, face_y - 8),
            (face_x + 10, face_y + 5),
            (face_x - 10, face_y + 5)
        ])
        # Face
        pygame.draw.ellipse(screen, (255, 220, 200), (face_x - 8, face_y - 5, 16, 14))
        # Angry eyes
        pygame.draw.line(screen, (100, 50, 50), (face_x - 6, face_y - 2), (face_x - 2, face_y), 2)
        pygame.draw.line(screen, (100, 50, 50), (face_x + 6, face_y - 2), (face_x + 2, face_y), 2)
        # Mouth (permanent frown)
        pygame.draw.arc(screen, (150, 50, 50), (face_x - 5, face_y + 2, 10, 6), 0, 3.14, 2)
        
        # Ship fins
        pygame.draw.polygon(screen, (200, 200, 220), [
            (sx - 30, sy),
            (sx - 50, sy - 15),
            (sx - 45, sy + 5)
        ])
        pygame.draw.polygon(screen, (200, 200, 220), [
            (sx - 30, sy),
            (sx - 50, sy + 15),
            (sx - 45, sy - 5)
        ])
        
        # Engine glow
        pygame.draw.ellipse(screen, (255, 100, 100), (sx - 45, sy - 8, 15, 16))
        
        # "I WANT TO SPEAK TO THE MANAGER" energy beam (when stealing)
        if self.steal_cooldown > 100:
            beam_y = sy + 30
            pygame.draw.polygon(screen, (255, 150, 150, 100), [
                (sx - 10, sy + 15),
                (sx + 10, sy + 15),
                (sx + 30, beam_y + 40),
                (sx - 30, beam_y + 40)
            ])
            # Angry text effect
            pygame.draw.circle(screen, (255, 50, 50), (sx, sy + 40), 5)


class StarField:
    """Deep space starfield with nebula"""
    def __init__(self, num_stars=200):
        self.stars = []
        for _ in range(num_stars):
            self.stars.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT),
                'size': random.randint(1, 3),
                'brightness': random.randint(50, 255),
                'twinkle': random.random() * 0.1
            })
        
        # Nebula colors
        self.nebula_spots = []
        for _ in range(5):
            self.nebula_spots.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT),
                'radius': random.randint(100, 300),
                'color': random.choice([
                    (80, 40, 120),  # Purple
                    (40, 60, 120),  # Blue
                    (120, 40, 80),  # Pink
                ])
            })
    
    def draw(self, screen):
        # Nebula background
        for nebula in self.nebula_spots:
            pygame.draw.circle(screen, nebula['color'], 
                             (nebula['x'], nebula['y']), nebula['radius'])
        
        # Stars
        for star in self.stars:
            brightness = int(star['brightness'] * 
                           (0.7 + 0.3 * math.sin(pygame.time.get_ticks() * star['twinkle'])))
            # Clamp to valid color range
            r = min(255, brightness)
            g = min(255, brightness)
            b = min(255, brightness + 20)
            pygame.draw.circle(screen, (r, g, b), 
                             (star['x'], star['y']), star['size'])


class Earth:
    """Earth visible in background"""
    def __init__(self):
        self.x = SCREEN_WIDTH - 150
        self.y = SCREEN_HEIGHT - 150
        self.radius = 120
        self.rotation = 0
    
    def draw(self, screen):
        # Planet
        pygame.draw.circle(screen, (50, 100, 200), (self.x, self.y), self.radius)
        pygame.draw.circle(screen, (40, 150, 80), (self.x - 20, self.y - 10), self.radius - 10)
        
        # Atmosphere glow
        for i in range(3):
            pygame.draw.circle(screen, (100, 150, 255, 100 - i*30), 
                             (self.x, self.y), self.radius + 5 + i*3, 2)
        
        # Clouds
        cloud_offset = pygame.time.get_ticks() * 0.0001
        for i in range(5):
            cx = self.x - 50 + i * 30 + int(cloud_offset * 20) % 60
            cy = self.y - 40 + i * 15
            pygame.draw.ellipse(screen, (200, 220, 255), (cx - 20, cy - 8, 40, 16))


class SpaceStationDoghouse:
    """Space station shaped like doghouse"""
    def __init__(self):
        self.x = SCREEN_WIDTH - 200
        self.y = 150
    
    def draw(self, screen):
        x, y = self.x, self.y
        
        # Main station body (doghouse shape)
        pygame.draw.rect(screen, (180, 180, 200), (x - 60, y - 40, 120, 80))
        pygame.draw.polygon(screen, (150, 150, 170), [
            (x - 70, y - 40),
            (x, y - 90),
            (x + 70, y - 40)
        ])
        
        # Docking port (circular)
        pygame.draw.circle(screen, (100, 100, 120), (x, y), 25)
        pygame.draw.circle(screen, (80, 80, 100), (x, y), 20)
        
        # Solar panels
        pygame.draw.rect(screen, (50, 50, 150), (x - 120, y - 10, 40, 60))
        pygame.draw.rect(screen, (50, 50, 150), (x + 80, y - 10, 40, 60))
        
        # Lights
        pygame.draw.circle(screen, (255, 100, 100), (x - 50, y + 30), 6)
        pygame.draw.circle(screen, (100, 255, 100), (x + 50, y + 30), 6)
        
        # "HOME" in space font
        try:
            font = pygame.font.Font(None, 40)
            text = font.render("HOME", True, (255, 255, 255))
            screen.blit(text, (x - text.get_width()//2, y - 70))
        except:
            pass


class SpaceGame:
    def __init__(self):
        print("Initializing TREAT QUEST: SPACE EDITION...", flush=True)
        
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
        
        pygame.display.set_caption("🚀 TREAT QUEST: SPACE EDITION 🐕‍🦺")
        self.clock = pygame.time.Clock()
        
        try:
            self.font = pygame.font.Font(None, 80)
            self.font_med = pygame.font.Font(None, 56)
            self.font_small = pygame.font.Font(None, 40)
        except:
            self.font = pygame.font.SysFont('arial', 60)
            self.font_med = pygame.font.SysFont('arial', 40)
            self.font_small = pygame.font.SysFont('arial', 30)
        
        # Space dogs!
        self.dogs = [
            SpaceDog('harley', SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2),
            SpaceDog('shanti', 2 * SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2)
        ]
        
        # Space treats
        self.treats = []
        for _ in range(5):
            self.treats.append(SpaceTreat(random.randint(200, SCREEN_WIDTH - 200),
                                         random.randint(200, SCREEN_HEIGHT - 200), 'satellite'))
        for _ in range(3):
            self.treats.append(SpaceTreat(random.randint(200, SCREEN_WIDTH - 200),
                                         random.randint(200, SCREEN_HEIGHT - 200), 'cosmic_bone'))
        for _ in range(2):
            self.treats.append(SpaceTreat(random.randint(200, SCREEN_WIDTH - 200),
                                         random.randint(200, SCREEN_HEIGHT - 200), 'alien_snack'))
        
        # Space environment
        self.starfield = StarField(300)
        self.asteroids = [Asteroid() for _ in range(6)]
        self.earth = Earth()
        self.space_station = SpaceStationDoghouse()
        self.ufo = UFO()
        self.space_snack = None
        
        # Space Squirrel in pod!
        self.space_squirrel = SpaceSquirrel()
        self.cosmic_acorn = None
        
        # BESTIE - The antagonist!
        self.bestie = Bestie()
        
        get_tampa_weather()
        
        print("Space game initialized! 🚀", flush=True)
    
    def draw(self):
        # Deep space background
        self.screen.fill((10, 15, 35))
        
        # Starfield and nebula
        self.starfield.draw(self.screen)
        
        # Earth in background
        self.earth.draw(self.screen)
        
        # Asteroids (background)
        for asteroid in self.asteroids:
            asteroid.update()
            asteroid.draw(self.screen)
        
        # Space station
        self.space_station.draw(self.screen)
        
        # UFO
        dropped_snack = self.ufo.update()
        if dropped_snack and self.space_snack is None:
            self.space_snack = SpaceSnack(dropped_snack['x'], dropped_snack['y'])
        self.ufo.draw(self.screen)
        
        # Space snack from UFO
        if self.space_snack:
            self.space_snack.update()
            self.space_snack.draw(self.screen)
            if not self.space_snack.active:
                self.space_snack = None
            else:
                # Check collection
                for dog in self.dogs:
                    dx = self.space_snack.x - dog.x
                    dy = self.space_snack.y - dog.y
                    if math.sqrt(dx*dx + dy*dy) < 50:
                        dog.score += 15  # Big UFO snack bonus!
                        self.space_snack = None
                        dog.spin = 0.5  # Victory spin!
                        break
        
        # Space Squirrel!
        dropped_acorn = self.space_squirrel.update(self.dogs)
        if dropped_acorn and self.cosmic_acorn is None:
            self.cosmic_acorn = {'x': dropped_acorn['x'], 'y': dropped_acorn['y'], 
                                'active': True, 'lifetime': 400}
        self.space_squirrel.draw(self.screen)
        
        # Cosmic acorn from squirrel
        if self.cosmic_acorn:
            self.cosmic_acorn['lifetime'] -= 1
            ca = self.cosmic_acorn
            # Draw floating acorn
            y_off = math.sin(pygame.time.get_ticks() * 0.01) * 8
            pygame.draw.ellipse(self.screen, (200, 170, 100), 
                               (int(ca['x'] - 10), int(ca['y'] + y_off - 6), 20, 12))
            pygame.draw.circle(self.screen, (255, 200, 50), (int(ca['x']), int(ca['y'] + y_off - 15)), 5)
            
            # Check dog collection
            for dog in self.dogs:
                dx = ca['x'] - dog.x
                dy = ca['y'] + y_off - dog.y
                if math.sqrt(dx*dx + dy*dy) < 50:
                    dog.score += 8  # Cosmic acorn bonus!
                    self.cosmic_acorn = None
                    dog.spin = 0.3
                    break
            
            if self.cosmic_acorn and ca['lifetime'] <= 0:
                self.cosmic_acorn = None
        
        # BEASTIE - The treat thief!
        self.bestie.update(self.treats, self.dogs)
        self.bestie.draw(self.screen)
        
        # Treats
        for treat in self.treats:
            treat.update()
            treat.draw(self.screen)
        
        # Space dogs
        for dog in self.dogs:
            dog.update(self.treats, self.dogs[1 - self.dogs.index(dog)])
            dog.draw(self.screen)
        
        # Title
        title = self.font.render("TREAT QUEST", True, (255, 200, 50))
        subtitle = self.font_med.render("SPACE EDITION", True, (150, 220, 255))
        self.screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 30))
        self.screen.blit(subtitle, (SCREEN_WIDTH//2 - subtitle.get_width()//2, 100))
        
        # Space stats
        time_str = datetime.now().strftime("%I:%M %p")
        time_surf = self.font_small.render(f"Mission Time: {time_str}", True, (200, 220, 255))
        self.screen.blit(time_surf, (SCREEN_WIDTH - 300, 30))
        
        wx = space_weather_cache
        wx_surf = self.font_small.render(f"Earth: {wx['temp']}°F", True, (200, 220, 255))
        self.screen.blit(wx_surf, (SCREEN_WIDTH - 280, 70))
        
        # Scores
        harley_surf = self.font_small.render(f"HARLEY: {self.dogs[0].score}", True, (255, 150, 150))
        shanti_surf = self.font_small.render(f"SHANTI: {self.dogs[1].score}", True, (150, 150, 255))
        self.screen.blit(harley_surf, (30, 30))
        self.screen.blit(shanti_surf, (30, 70))
        
        # Bestie status (if active)
        if self.bestie.active:
            bestie_surf = self.font_small.render(f"BESTIE: {self.bestie.stolen_treats} stolen!", True, (255, 100, 100))
            self.screen.blit(bestie_surf, (30, 110))
        
        # Zero-G indicator
        zero_g = self.font_small.render("ZERO-G ENVIRONMENT", True, (255, 200, 100))
        self.screen.blit(zero_g, (SCREEN_WIDTH//2 - zero_g.get_width()//2, SCREEN_HEIGHT - 50))
        
        pygame.display.flip()
    
    def run(self):
        running = True
        print("Starting TREAT QUEST: SPACE EDITION! 🚀🐕‍🦺", flush=True)
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
            
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    print("🚀 TREAT QUEST: SPACE EDITION v5.0 🐕‍🦺", flush=True)
    SpaceGame().run()
