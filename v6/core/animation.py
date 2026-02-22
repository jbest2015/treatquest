"""
Frame-Based Animation System for v6.0
Sprite animation with state machines
"""

import pygame

class SpriteAnimator:
    """Manages frame-based sprite animations"""
    
    def __init__(self, frames, fps=12):
        """
        Args:
            frames: List of pygame.Surface objects
            fps: Animation frames per second
        """
        self.frames = frames
        self.frame_time = 1.0 / fps
        self.current_frame = 0
        self.timer = 0
        self.playing = True
        self.loop = True
        self.finished = False
    
    def update(self, dt):
        """Update animation frame"""
        if not self.playing or self.finished:
            return
        
        self.timer += dt
        
        if self.timer >= self.frame_time:
            self.timer = 0
            self.current_frame += 1
            
            if self.current_frame >= len(self.frames):
                if self.loop:
                    self.current_frame = 0
                else:
                    self.current_frame = len(self.frames) - 1
                    self.finished = True
    
    def get_frame(self):
        """Get current animation frame"""
        return self.frames[self.current_frame]
    
    def set_state(self, state_name):
        """Switch to a different animation state (requires state machine)"""
        pass
    
    def play(self):
        """Resume animation"""
        self.playing = True
    
    def pause(self):
        """Pause animation"""
        self.playing = False
    
    def reset(self):
        """Reset to first frame"""
        self.current_frame = 0
        self.timer = 0
        self.finished = False


class AnimationStateMachine:
    """Manages animation states for complex entities"""
    
    def __init__(self):
        self.states = {}
        self.current_state = None
        self.previous_state = None
    
    def add_state(self, name, animator):
        """Add an animation state"""
        self.states[name] = animator
    
    def set_state(self, name):
        """Change to a new state"""
        if name not in self.states:
            return
        
        self.previous_state = self.current_state
        self.current_state = name
        
        # Reset the new state's animation
        self.states[name].reset()
    
    def update(self, dt):
        """Update current state's animation"""
        if self.current_state:
            self.states[self.current_state].update(dt)
    
    def get_frame(self):
        """Get current state's frame"""
        if self.current_state:
        return self.states[self.current_state].get_frame()
        return None
