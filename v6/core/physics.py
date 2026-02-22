"""
Biplane Physics Engine for v6.0
Lift, drag, gravity, and stall mechanics
"""

import math

class Vector2:
    """Simple 2D vector"""
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    
    def length(self):
        return math.sqrt(self.x * self.x + self.y * self.y)
    
    def normalize(self):
        length = self.length()
        if length > 0:
            self.x /= length
            self.y /= length

class BiplanePhysics:
    """Realistic WWI flight physics"""
    
    GRAVITY = 0.15
    LIFT_COEFF = 0.0003
    DRAG_COEFF = 0.001
    STALL_SPEED = 3.0
    MAX_SPEED = 12.0
    
    def __init__(self):
        self.velocity = Vector2(0, 0)
        self.angle = 0  # radians
        self.thrust = 0
        self.stalled = False
        self.bank_angle = 0  # for visual rotation
    
    def apply_thrust(self, amount):
        """Apply engine thrust"""
        self.thrust = amount
        self.velocity.x += math.cos(self.angle) * amount
        self.velocity.y += math.sin(self.angle) * amount
    
    def update(self, dt):
        """Update physics for one frame"""
        speed = self.velocity.length()
        
        if speed > 0:
            # Calculate lift based on angle of attack and speed
            # Lift increases with speed squared
            lift = self.LIFT_COEFF * speed * speed * math.cos(self.angle)
            
            # Drag increases with speed squared
            drag = self.DRAG_COEFF * speed * speed
            
            # Apply gravity minus lift
            self.velocity.y += self.GRAVITY - lift
            
            # Apply drag (opposite to velocity direction)
            if speed > 0:
                self.velocity.x -= (self.velocity.x / speed) * drag
                self.velocity.y -= (self.velocity.y / speed) * drag
            
            # Check for stall condition
            if speed < self.STALL_SPEED and self.angle > math.pi / 4:
                self._enter_stall()
            else:
                self.stalled = False
            
            # Clamp max speed
            if speed > self.MAX_SPEED:
                scale = self.MAX_SPEED / speed
                self.velocity.x *= scale
                self.velocity.y *= scale
        
        # Update bank angle based on turn rate
        self._update_bank_angle(dt)
    
    def _enter_stall(self):
        """Enter stall condition - loss of lift"""
        self.stalled = True
        # Stall recovery: nose drops, speed increases
        self.velocity.y += 0.3  # Drop faster
    
    def _update_bank_angle(self, dt):
        """Update visual bank angle based on turn rate"""
        # Bank angle follows from turn rate
        target_bank = self.angle * 0.5
        self.bank_angle += (target_bank - self.bank_angle) * 0.1
    
    def turn(self, direction, dt):
        """Turn the aircraft (direction: -1 for left, 1 for right)"""
        turn_rate = 2.0 * dt
        if self.stalled:
            turn_rate *= 0.3  # Less control during stall
        self.angle += direction * turn_rate
