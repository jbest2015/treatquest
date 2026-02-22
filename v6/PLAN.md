# Treat Quest v6.0 — WWI Flying Aces
## Complete Technical Plan & Architecture

**Theme:** Time Pilot 84 style side-scrolling aerial combat
**Dogs:** Harley & Shanti as WWI flying aces in biplanes
**Objective:** Chase balloon-borne treats across oversized scrolling world

---

## v5.1 → v6.0 Improvements

### 1. Improved Graphics (32-bit Art Style)
| v5.1 (Space) | v6.0 (Flying Aces) |
|--------------|-------------------|
| Solid color shapes | Textured sprites with alpha |
| Procedural planets | Parallax cloud layers |
| Single-screen | 2000x1200 world, 800x600 viewport |
| Basic starfield | Volumetric clouds, sun rays |
| Simple particles | Frame-based explosions, smoke trails |
| Solid color dogs | Sprite animation with 4-frame cycles |

**Key Additions:**
- **Parallax Background System:** 5 layers (sky, clouds x3, foreground)
- **Sprite-Based Rendering:** Move from `pygame.draw` to `pygame.image` with spritesheets
- **Camera System:** Smooth tracking with prediction/lerp
- **Particle Engine:** Smoke, fire, contrails, explosions with physics
- **Lighting Effects:** Sun glare, cloud shadows, sunset tinting

### 2. Improved Logic (AI Behavior Trees)
| v5.1 (Space) | v6.0 (Flying Aces) |
|--------------|-------------------|
| Simple seek-to-treat | Behavior tree with states |
| Screen wrap | World bounds with auto-scroll |
| Fixed speed | Physics: thrust, drag, gravity |
| Solo AI | Formation flying, wingman support |
| No pathing | B-spline spline paths for enemies |

**Key Additions:**
- **Physics Engine:** Lift, drag, gravity, stall mechanics
- **Formation System:** Vic formation, trail positions, breakaway
- **Dogfight AI:** Evasive maneuvers (Immelmann, split-S)
- **Balloon AI:** Drift with wind, altitude variance
- **Scoring System:** Chain combos, multipliers, ace medals

### 3. Improved Animation
| v5.1 (Space) | v6.0 (Flying Aces) |
|--------------|-------------------|
| Rotated ellipses | Sprite rotation with frame anims |
| Static rotation | Bank angle based on turn rate |
| No prop effects | Blurred prop disc at high RPM |
| Static treats | Bobbing, spinning, parachute deploy |
| Instant spawn | Entry animations (fly-in from edge) |

**Key Additions:**
- **Sprite Animation System:** Frame-based looping with state machines
- **Rotation Banking:** Smooth angle interpolation based on velocity
- **Propeller Blur:** Dynamic alpha based on speed
- **Damage States:** Smoke trails, wing damage, spinning crash
- **Celebration Anim:** Victory roll, treat-chomp animation

---

## Architecture

### Module Structure
```
treatquest_v6/
├── main.py                    # Game entry point
├── config.py                  # Constants, settings
├── assets/
│   ├── sprites/
│   │   ├── harley/
│   │   │   ├── idle.png       # 4 frames
│   │   │   ├── bank_left.png  # 4 frames
│   │   │   ├── bank_right.png # 4 frames
│   │   │   └── chomp.png      # 4 frames
│   │   ├── shanti/
│   │   ├── treats/
│   │   │   ├── bone_small.png
│   │   │   ├── bone_large.png
│   │   │   └── golden.png
│   │   ├── balloons/
│   │   ├── biplanes/
│   │   ├── clouds/
│   │   ├── explosions/
│   │   └── ui/
│   ├── audio/
│   └── backgrounds/
├── core/
│   ├── __init__.py
│   ├── camera.py              # Smooth tracking camera
│   ├── physics.py             # Lift/drag/gravity
│   ├── particle.py            # Particle system
│   └── animation.py           # Sprite animation manager
├── entities/
│   ├── __init__.py
│   ├── aircraft.py            # Base aircraft, biplane
│   ├── dog.py                 # Harley/Shanti extensions
│   ├── balloon.py             # Treat-carrying balloons
│   ├── cloud.py               # Volumetric clouds
│   ├── treat.py               # Collectibles
│   └── effects.py             # Explosions, smoke
├── ai/
│   ├── __init__.py
│   ├── behavior_tree.py       # BT nodes
│   ├── dog_ai.py              # Harley/Shanti intelligence
│   └── enemy_ai.py            # Balloon/formation AI
├── world/
│   ├── __init__.py
│   ├── level.py               # World/level data
│   └── parallax.py            # Background layers
├── game/
│   ├── __init__.py
│   ├── game_state.py          # Score, lives, level
│   └── session.py             # Game loop
└── utils/
    ├── __init__.py
    └── helpers.py
```

### Class Hierarchy

```
Entity (base)
├── AnimatedSprite
│   ├── Biplane
│   │   ├── HarleyPlane
│   │   └── ShantiPlane
│   ├── Balloon
│   │   ├── RedBalloon (1pt)
│   │   ├── BlueBalloon (3pt)
│   │   └── GoldBalloon (10pt)
│   └── Cloud
│       ├── Cumulus
│       └── Stratus
│
├── Particle
│   ├── Smoke
│   ├── Fire
│   └── Spark
│
├── Treat (collectible)
│   ├── FloatingBone
│   ├── GoldenBone
│   └── DogBiscuit
│
└── Effect
    ├── Explosion
    ├── Contrail
    └── PropBlur

Camera
├── Position
├── Target
└── SmoothFollow (lerp)

World
├── ParallaxLayer x5
├── Boundaries
└── WindZones

GameState
├── Score
├── Time
├── Aces (dogs)
└── Medals
```

---

## Asset Inventory

### Sprites (PNG with alpha)
| Asset | Frames | Size | Notes |
|-------|--------|------|-------|
| Harley Biplane | 16 | 64x64 | 4 directions × 4 frames |
| Shanti Biplane | 16 | 72x72 | Larger, blue color |
| Propeller Blur | 4 | 64x20 | Rotating disc effect |
| Balloons | 8 | 48x64 | 2 colors × bobbing |
| Bone Treats | 4 | 32x32 | Spinning animation |
| Clouds | 12 | 128-256 | various sizes |
| Explosion | 12 | 64x64 | frame sequence |
| Smoke puff | 8 | 32x32 | fade out |
| HUD Elements | - | - | Score, medals |

### Audio (OGG)
| Sound | Use |
|-------|-----|
| engine_loop.ogg | Constant biplane hum |
| prop_wind.ogg | Speed-based pitch |
| collect.ogg | Treat grab |
| balloon_pop.ogg | Balloon burst |
| explosion.ogg | Crash |
| ace_medal.ogg | Milestone |
| bgm_wwi.ogg | Background music loop |

### Backgrounds
| Layer | Parallax | Type |
|-------|----------|------|
| Sky | 0% | Gradient (time of day) |
| Distant clouds | 10% | Tileable sprites |
| Mid clouds | 30% | Tileable sprites |
| Near clouds | 60% | Alpha sprites |
| Terrain | 100% | Hills/silhouette |

---

## Code Sections Required

### 1. Core Engine (`core/`)
```python
# camera.py
class TrackingCamera:
    def __init__(self, viewport, world_bounds):
        self.viewport = viewport  # (800, 600)
        self.world = world_bounds  # (2000, 1200)
        self.x, self.y = 0, 0
        self.target = None
        self.lerp_factor = 0.1
        self.deadzone = 100
    
    def update(self, dt):
        if self.target:
            target_x = self.target.x - self.viewport[0] // 2
            target_y = self.target.y - self.viewport[1] // 2
            self.x += (target_x - self.x) * self.lerp_factor
            self.y += (target_y - self.y) * self.lerp_factor
            self._clamp_to_world()
    
    def apply(self, entity):
        return entity.x - self.x, entity.y - self.y
```

```python
# physics.py
class BiplanePhysics:
    GRAVITY = 0.15
    LIFT_COEFF = 0.0003
    DRAG_COEFF = 0.001
    
    def __init__(self):
        self.velocity = Vector2(0, 0)
        self.angle = 0
        self.thrust = 0
        self.stall_speed = 3.0
    
    def update(self, dt):
        # Calculate lift based on angle and speed
        speed = self.velocity.length()
        lift = self.LIFT_COEFF * speed * speed * math.cos(self.angle)
        
        # Drag increases with speed squared
        drag = self.DRAG_COEFF * speed * speed
        
        # Apply forces
        self.velocity.y += self.GRAVITY - lift
        self.velocity.x -= drag * math.cos(self.angle)
        self.velocity.y -= drag * math.sin(self.angle)
        
        # Stall check
        if speed < self.stall_speed and self.angle > math.pi / 4:
            self._enter_stall()
```

```python
# animation.py
class SpriteAnimator:
    def __init__(self, spritesheet, frame_count, fps):
        self.frames = self._parse_spritesheet(spritesheet, frame_count)
        self.frame_time = 1.0 / fps
        self.current_frame = 0
        self.timer = 0
        self.playing = True
    
    def update(self, dt):
        if not self.playing:
            return
        self.timer += dt
        if self.timer >= self.frame_time:
            self.timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)
    
    def get_current_frame(self):
        return self.frames[self.current_frame]
```

### 2. Entities (`entities/`)
```python
# aircraft.py
class Biplane(Entity):
    def __init__(self, name, x, y):
        super().__init__(x, y)
        self.name = name
        self.physics = BiplanePhysics()
        self.animator = SpriteAnimator(f"sprites/{name}/", 16, 12)
        self.prop_angle = 0
        self.health = 100
        self.score = 0
        self.contrail_timer = 0
    
    def update(self, dt, world, camera):
        # AI decision
        action = self.behavior_tree.tick(self, world)
        self._apply_action(action, dt)
        
        # Physics
        self.physics.update(dt)
        self.x += self.physics.velocity.x
        self.y += self.physics.velocity.y
        
        # Animation
        self._update_animation(dt)
        self.prop_angle = (self.prop_angle + 30) % 360
        
        # Contrails at high speed
        if self.physics.velocity.length() > 8:
            self._spawn_contrail()
    
    def draw(self, screen, camera):
        screen_pos = camera.apply(self)
        frame = self.animator.get_current_frame()
        rotated = pygame.transform.rotate(frame, -math.degrees(self.angle))
        screen.blit(rotated, rotated.get_rect(center=screen_pos))
        
        # Draw prop blur
        self._draw_propeller(screen, screen_pos)
```

```python
# balloon.py
class TreatBalloon(Entity):
    def __init__(self, x, y, treat_type):
        super().__init__(x, y)
        self.treat = Treat(treat_type)
        self.float_offset = random.random() * math.pi * 2
        self.altitude = y
        self.drift_speed = random.uniform(0.2, 0.5)
    
    def update(self, dt, wind):
        # Bobbing motion
        self.float_offset += dt * 2
        self.y = self.altitude + math.sin(self.float_offset) * 20
        
        # Wind drift
        self.x += self.drift_speed + wind * 0.5
    
    def pop(self):
        self.treat.deploy_parachute(self.x, self.y)
        return ParticleSystem.explosion(self.x, self.y)
```

### 3. AI System (`ai/`)
```python
# behavior_tree.py
class BehaviorTree:
    def __init__(self, root):
        self.root = root
    
    def tick(self, actor, world):
        return self.root.execute(actor, world)

class SeekNearestTreat(BehaviorNode):
    def execute(self, actor, world):
        nearest = world.find_nearest_treat(actor)
        if nearest:
            direction = (nearest.x - actor.x, nearest.y - actor.y)
            return Action("turn_toward", direction)
        return Action("cruise", None)

class AvoidCollision(BehaviorNode):
    def execute(self, actor, world):
        nearby = world.get_nearby(actor, radius=100)
        if len(nearby) > 1:
            return Action("evade", nearby)
        return None

# Priority: Avoid > Seek > Wander
```

### 4. World System (`world/`)
```python
# parallax.py
class ParallaxBackground:
    def __init__(self):
        self.layers = []
        for i, speed in enumerate([0.0, 0.1, 0.3, 0.6, 1.0]):
            self.layers.append(ParallaxLayer(speed, f"bg_layer_{i}.png"))
    
    def draw(self, screen, camera_x):
        for layer in self.layers:
            offset = camera_x * layer.speed
            layer.draw(screen, offset)

# level.py
class Level:
    BOUNDS = (0, 0, 2000, 1200)  # x, y, width, height
    
    def __init__(self):
        self.balloons = []
        self.clouds = []
        self.wind_zones = []
        self._generate()
    
    def _generate(self):
        # Scatter balloons
        for _ in range(15):
            x = random.randint(100, 1900)
            y = random.randint(100, 800)
            self.balloons.append(TreatBalloon(x, y, random.choice(TREAT_TYPES)))
        
        # Wind currents
        for i in range(5):
            self.wind_zones.append(WindZone(
                x=i * 400, y=0, width=200, height=1200, 
                direction=random.choice([-1, 1]), strength=random.uniform(0.3, 0.8)
            ))
```

---

## Migration Steps

### Phase 1: Infrastructure
1. Create new branch `flying-aces-v6`
2. Set up module directory structure
3. Copy utility functions from v5.1
4. Create asset placeholder files

### Phase 2: Core Systems
1. Implement Camera class
2. Implement Physics class
3. Implement Animation system
4. Implement Particle engine

### Phase 3: Entities
1. Create Biplane base class
2. Port Harley/Shanti behaviors
3. Create Balloon system
4. Create Cloud/parallax system

### Phase 4: AI
1. Implement behavior tree framework
2. Port treat-seeking logic
3. Add formation flying
4. Add dogfight maneuvers

### Phase 5: Assets
1. Generate sprites (or placeholder rectangles with colors)
2. Create parallax backgrounds
3. Add particle effects
4. Polish animations

### Phase 6: Polish
1. Add combo scoring
2. Add ace medals
3. Add day/night cycle
4. Final testing

---

## File Size Estimates

| Component | Lines | Notes |
|-----------|-------|-------|
| Camera | ~80 | Smooth tracking |
| Physics | ~120 | Lift/drag/stall |
| Animation | ~100 | Frame management |
| Particles | ~150 | Smoke/fire/explosions |
| Aircraft | ~300 | Biplane + dogs |
| Balloon | ~100 | Treat carriers |
| AI | ~200 | Behavior trees |
| World | ~150 | Parallax + level |
| Game | ~200 | State management |
| **Total** | **~1,400** | Slightly larger than v5.1 |

---

## Asset Generation Plan

### Option A: Procedural (like v5.1)
- Keep using `pygame.draw` but add more shapes
- Dynamic prop blur (rotating ellipses)
- Procedural clouds (overlapping circles)
- Simple particle effects
- **Pros:** No external assets, fast iteration
- **Cons:** Lower visual fidelity

### Option B: Sprite-Based (recommended)
- Create spritesheet with ComfyUI/FLUX
- 32x32 to 128x128 per sprite
- Alpha channels for transparency
- **Pros:** Higher quality, real art style
- **Cons:** Requires asset pipeline

### Recommendation: Hybrid
- Core entities: Spritesheets (Harley/Shanti/balloons)
- Effects: Procedural (smoke, fire, contrails)
- Background: Parallax tileable sprites
- UI: Simple drawing (score, medals)

---

## Success Metrics

1. **Frame Rate:** Maintain 60 FPS on Pi 4
2. **Memory:** Stay under 256MB usage
3. **Load Time:** <3 seconds from service start
4. **Code Quality:** Modular, well-commented
5. **Feature Parity:** All v5.1 features + new improvements

---

## Next Steps

1. ✅ Create plan (this document)
2. ⏳ Create Git branch `flying-aces-v6`
3. ⏳ Scaffold module structure
4. ⏳ Implement Camera + World
5. ⏳ Implement Biplane physics
6. ⏳ Port Harley/Shanti AI
7. ⏳ Add balloon/treat system
8. ⏳ Generate assets
9. ⏳ Test on Pi
10. ⏳ Deploy

---

*Plan created: 2026-02-22*
*Target: v6.0 Flying Aces*
*Reference: Time Pilot 84*
