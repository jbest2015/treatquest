# Changelog

All notable changes to Treat Quest are documented here.
This project follows [Semantic Versioning](https://semver.org/).

## [5.1.0] - 2026-02-19

### Added
- 🐿️ **Space Squirrel** — In a glass space pod, drops cosmic acorns worth 8 points
- 👩‍🚀 **BEASTIE** — The antagonist! A "Karen" in a spaceship who steals treats and pushes dogs away
- Beastie counter showing how many treats she's stolen
- Entitled energy beam effect when Beastie is stealing

### Changed
- Updated README with comprehensive project description
- Added OpenClaw reference and "surprise feature" explanation

## [5.0.0] - 2026-02-19

### Major Release — SPACE EDITION! 🚀
Complete transformation from ground-based dog park to **zero-G space adventure**.

### Added
- **Zero-G physics** — Dogs float freely with momentum-based movement
- **Space suits** — Harley (red) and Shanti (blue) with jetpacks and helmets
- **Jetpack trails** — Particle effects when dogs boost
- **Earth view** — Earth visible in background with live weather overlay
- **Asteroid field** — Floating space rocks drifting through scene
- **Nebula starfield** — Deep space background with colored nebula clouds
- **Space Station Doghouse** — Replaced Snoopy house with space station
- **UFO** — Drops alien snacks worth 15 points
- **Space treats**:
  - Satellites (1 point)
  - Cosmic Bones (3 points, glowing)
  - Alien Snacks (10 points from UFO)
- "Zero-G Environment" warning indicator
- Spin effects when dogs collect treats

### Removed
- Ground/grass (no gravity in space!)
- Fire hydrant
- Hills background
- Butterflies (replaced with birds)
- Puddles

### Changed
- Complete physics rewrite for zero-G
- Dogs now rotate freely and wrap around screen edges
- Background now deep space instead of sky

## [4.1.0] - 2026-02-17

### Added
- 🎾 **Beach Ball** — Physics-based bouncing ball that dogs can chase
- Real Tampa weather integration via Open-Meteo API
- Dynamic time of day (sunrise, day, sunset, night)

### Added — Creatures
- 🦋 **Butterflies** (6, daytime only, colorful)
- ✨ **Fireflies** (15, nighttime only, glowing)

## [4.0.0] - 2026-02-17

### Added
- **Golden Treats** — Rare 5-point glowing bones
- **Puddles** — Slow dogs down to 70% speed
- **Dog Sleep Mode** — Dogs curl up and show "Zzz" bubbles at night (9 PM - 6 AM)
- **Birds** — V-formations flying across the sky

## [3.0.0] - 2026-02-17

### Added
- 🐿️ **Squirrel NPC** — Runs across screen with acorn, drops 5-point bonus if caught
- **Squirrel** — Fast runner (speed 5-7), appears every 30-60 seconds

## [2.0.0] - 2026-02-14

### Added — Dog Park Environment
- Rolling hills background with parallax
- **Fire hydrant** (classic dog element)
- **Snoopy-style doghouse** with "HOME" sign
- Dynamic weather cycling (sunny → cloudy → rainy)
- Rain particle effects
- Live scoreboard (HARLEY vs SHANTI with color-coded collars)

### Added — Behaviors
- Dog collision avoidance
- Happy tail wagging
- Name tags visible above dogs

## [1.0.0] - 2026-02-13

### Initial Release — Treat Quest: Dog Park Edition

### Added
- **Harley** — Small, cream-colored, floppy ears, red collar
- **Shanti** — Big, brown, perky triangle ears, blue collar
- **Treat collection** with scoring system
- Golden bone treats (1 point each)
- Arcade "attract mode" — runs automatically, no controls needed
- Auto-running AI — dogs seek nearest treats
- Sniffing and idle behaviors
- 16-bit pixel art style (PyGame)
- Fullscreen display on Raspberry Pi
- systemd service for 24/7 operation

---

## Project Evolution Summary

| Version | Theme | Key Feature |
|---------|-------|-------------|
| 1.0 | Ground | Basic dog park |
| 2.0 | Ground | Weather, hills, doghouse |
| 3.0 | Ground | Squirrel NPC |
| 4.0 | Ground | Beach ball, puddles, sleep mode |
| 4.1 | Ground | Butterflies, fireflies, real weather |
| 5.0 | **SPACE** | **Zero-G, jetpacks, asteroids** |
| 5.1 | Space | **Space Squirrel, BEASTIE** |

*Total lines of code: 1,400+*
*Features added via AI "surprise" mechanic: 20+*
*Built with OpenClaw 🤖*
