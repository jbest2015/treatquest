"""
Treat Quest v6.0 — WWI Flying Aces Configuration
"""

# Display Settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
FULLSCREEN = True

# World Settings (Time Pilot 84 style oversized world)
WORLD_WIDTH = 2000
WORLD_HEIGHT = 1200

# Camera Settings
CAMERA_LERP = 0.1
CAMERA_DEADZONE = 100

# Physics Constants
GRAVITY = 0.15
LIFT_COEFFICIENT = 0.0003
DRAG_COEFFICIENT = 0.001
STALL_SPEED = 3.0
MAX_SPEED = 12.0

# Animation Settings
ANIMATION_FPS = 12
FRAME_DURATION = 1.0 / ANIMATION_FPS

# Asset Paths
ASSET_PATH = "assets"
SPRITE_PATH = f"{ASSET_PATH}/sprites"
BG_PATH = f"{ASSET_PATH}/backgrounds"
AUDIO_PATH = f"{ASSET_PATH}/audio"

# Scoring
TREAT_VALUES = {
    'bone_small': 1,
    'bone_large': 3,
    'golden': 10,
    'parachute': 5
}

# Version
VERSION = "6.0.0"
VERSION_NAME = "Flying Aces"
