"""
Tracking Camera System for v6.0
Smooth camera with lerp following, deadzone, and world clamping
"""

class TrackingCamera:
    """Camera that smoothly follows a target entity"""
    
    def __init__(self, viewport_width, viewport_height, world_bounds):
        self.viewport = (viewport_width, viewport_height)
        self.world = world_bounds  # (x, y, width, height)
        self.x = 0
        self.y = 0
        self.target = None
        self.lerp = 0.1
        self.deadzone = 100
    
    def set_target(self, entity):
        """Set the entity to track"""
        self.target = entity
    
    def update(self, dt):
        """Update camera position based on target"""
        if not self.target:
            return
        
        # Calculate desired position (center target in viewport)
        target_x = self.target.x - self.viewport[0] // 2
        target_y = self.target.y - self.viewport[1] // 2
        
        # Smooth interpolation
        self.x += (target_x - self.x) * self.lerp
        self.y += (target_y - self.y) * self.lerp
        
        # Clamp to world bounds
        self._clamp_to_bounds()
    
    def _clamp_to_bounds(self):
        """Keep camera within world bounds"""
        x_min, y_min, width, height = self.world
        x_max = x_min + width - self.viewport[0]
        y_max = y_min + height - self.viewport[1]
        
        self.x = max(x_min, min(self.x, x_max))
        self.y = max(y_min, min(self.y, y_max))
    
    def apply(self, entity):
        """Convert world coordinates to screen coordinates"""
        return (int(entity.x - self.x), int(entity.y - self.y))
    
    def apply_rect(self, rect):
        """Convert world rect to screen rect"""
        return rect.move(-int(self.x), -int(self.y))
