# 🚀 Treat Quest: Harley & Shanti's Space Adventure

A 16-bit arcade-style **zero-G dog adventure** running 24/7 on a Raspberry Pi display.

> 🎮 **Live Game**: Running on a living room TV in Tampa, FL — completely autonomous "attract mode" that evolves over time.

---

## 🐕‍🦺 The Story

Harley (small, cream, floppy ears) and Shanti (big, brown, perky ears) are now **space dogs**! They float through the cosmos in their space suits, collecting cosmic treats while dodging asteroids and their new nemesis...

### 👩‍🚀 Meet BEASTIE — The Antagonist

Beastie is the entitled treat-thief in her spaceship who actively tries to **steal treats** from Harley and Shanti and **push them away** with her energy beam. She appears every 30-50 seconds to wreak havoc!

---

## ✨ Features

### 🌌 Space Environment
- **Zero-G physics** — Dogs float freely with jetpacks
- **Dynamic starfield** with nebula clouds
- **Earth visible** in the background (with real Tampa weather!)
- **Floating asteroids** drifting through space
- **Space station doghouse** (the "HOME" base)

### 🎭 Characters
- **Harley** — Red space suit, fast and hyper
- **Shanti** — Blue space suit, steady and clever
- **Space Squirrel** — In a glass pod, drops cosmic acorns (8 points)
- **UFO** — Drops alien snacks (15 points)
- **Beastie** — The antagonist who steals treats and thwarts dogs

### 🦴 Treats
- **Satellites** — 1 point (common)
- **Cosmic Bones** — 3 points (glowing)
- **Alien Snacks** — 10 points (dropped by UFO)
- **Cosmic Acorns** — 8 points (from Space Squirrel)

### 🌤️ Real-World Integration
- **Live Tampa weather** via Open-Meteo API (updates every 10 min)
- **Time of day** affects space lighting
- **Weather conditions** displayed on screen

---

## 🛠️ Built With

- **PyGame 2.6** — Game engine
- **Python 3.13** — Logic and physics
- **Raspberry Pi** — Hardware ( fullscreen display)
- **OpenClaw** — AI assistant that built and evolves this game!

> 🤖 **An OpenClaw Production**
> 
> This game was built by [OpenClaw](https://github.com/openclaw/openclaw) — an AI assistant framework. The "surprise feature" mechanic means new elements (creatures, obstacles, power-ups) are added automatically every few hours without human intervention. The game literally evolves on its own!

---

## 🚀 Deployment

```bash
# Location on Pi
/opt/doggame/dog_park.py

# Service
systemctl status doggame

# Restart
cd /opt/doggame && git pull && systemctl restart doggame
```

---

## 📊 Stats

- **1,400+ lines** of Python
- **24/7 runtime** since February 2026
- **20+ features** added via surprise deployments
- **Git versioned** with full history

---

## 🔮 Evolution

The game has transformed over time:

1. **v1.0** — Basic dog park (ground-based)
2. **v2.0** — Added weather, time of day, hills
3. **v3.0** — Butterflies, fireflies, squirrels
4. **v4.0** — Beach ball, puddles, golden treats, sleep mode
5. **v5.0** — **SPACE EDITION** — Zero-G, jetpacks, UFOs, asteroids
6. **v5.1** — Space Squirrel + BEASTIE the antagonist!

What's next? Who knows! The AI decides... 🤖✨

---

## 📺 Live Display

Running on a living room TV in Tampa, Florida as an autonomous "attract mode" display — no interaction needed, just sit back and watch the space dogs adventure unfold!

---

*Built with 💜 by OpenClaw for John Best*
