# Treat Quest v6.0 - Asset Inventory

**Updated:** 2026-02-22
**Status:** In Progress
**Location:** `~/.openclaw/workspace/treatquest/assets/`

---

## WHAT WE HAVE ✅

### Biplanes (5 assets)
| File | Description | Status | Notes |
|------|-------------|--------|-------|
| `biplane-crew-accurate.png` | **THE ONE** - Shanti (lead) + Harley (rear), proper labels | ✅ READY | Use as main sprite |
| `biplane-frame1.png` | Biplane frame (cat pilot - wrong species) | ⚠️ REVIEW | May not use |
| `biplane-frame2.png` | Biplane frame 2 (cat pilot) | ⚠️ REVIEW | May not use |
| `biplane-frame3.png` | Biplane frame 3 (cat pilot) | ⚠️ REVIEW | May not use |
| `biplane-frame4.png` | Biplane frame 4 (cat pilot) | ⚠️ REVIEW | May not use |

### Clouds - Parallax Backgrounds (4 assets)
| File | Description | Status | Layer |
|------|-------------|--------|-------|
| `cloud-sprite.png` | Single fluffy cloud | ✅ READY | Mid |
| `cloud-layer1-far.png` | Distant clouds | ✅ READY | Layer 1 (slowest) |
| `cloud-layer2-mid.png` | Mid-distance clouds | ✅ READY | Layer 2 |
| `cloud-layer3-near.png` | Close clouds | ✅ READY | Layer 3 (fastest) |

### Balloons & Treats (4 assets)
| File | Description | Status | Notes |
|------|-------------|--------|-------|
| `hotair-prize.png` | Hot air balloon with bone | ✅ READY | Main collectible |
| `hotair-rainbow.png` | Rainbow hot air balloon | ⚠️ REVIEW | Alt design? |
| `blimp.png` | Gray blimp/zeppelin | ⚠️ REVIEW | Maybe for background |
| `blimp-rearprop.png` | Rear-facing blimp | ⚠️ REVIEW | Different angle |

### Effects (3 assets)
| File | Description | Status | Use Case |
|------|-------------|--------|----------|
| `lightning1-straight.png` | Straight lightning bolt | ✅ READY | Storm weather |
| `lightning2-angle.png` | Angled lightning bolt | ✅ READY | Storm weather |
| `lightning3-branched.png` | Branched lightning | ✅ READY | Storm weather |

### Characters (3 assets)
| File | Description | Status | Notes |
|------|-------------|--------|-------|
| `squirrel-frame1.png` | Squirrel in frame | ⚠️ REVIEW | v5.1 carryover? |
| `squirrel-biplane.png` | Squirrel in biplane | ⚠️ REVIEW | NPC or enemy? |
| `bestie-frame1.png` | Bestie in frame | ⚠️ REVIEW | v5.1 carryover? |

### Props - Animation Frames (8 assets)
| File | Description | Status | Use Case |
|------|-------------|--------|----------|
| `propeller-horiz.png` | Horizontal propeller | ✅ READY | Animation overlay |
| `propeller-vert.png` | Vertical propeller | ✅ READY | Animation overlay |
| `propeller-diag1.png` | Diagonal propeller (/) | ✅ READY | Animation overlay |
| `propeller-diag2.png` | Diagonal propeller (\) | ✅ READY | Animation overlay |
| `propeller-rear.png` | Rear-facing prop | ⚠️ REVIEW | Tail prop variant |
| `scarf-up.png` | Scarf blowing up | ✅ READY | Animation |
| `scarf-straight.png` | Scarf straight back | ✅ READY | Animation |
| `scarf-down.png` | Scarf drooping | ✅ READY | Animation |

### UI Elements (5 assets)
| File | Description | Status | Use Case |
|------|-------------|--------|----------|
| `banner-blank.png` | Blank banner/flag | ✅ READY | Score display? |
| `banner-wave1-straight.png` | Straight waving banner | ✅ READY | UI decoration |
| `banner-wave2-curved.png` | Curved waving banner | ✅ READY | UI decoration |
| `banner-wave3-flapping.png` | Flapping banner | ✅ READY | UI decoration |
| `bestie-banner.png` | Bestie with banner | ⚠️ REVIEW | Specific to Bestie |

---

## WHAT WE NEED ❌

### Missing Biplane Animation Frames
**Priority: HIGH**
We have 1 correct biplane (crew-accurate) but need animation frames for banking.

| Asset | Priority | Description |
|-------|----------|-------------|
| `biplane-level.png` | P0 | Level flight (straight) |
| `biplane-bank-left.png` | P0 | Banking left (left wing down) |
| `biplane-bank-right.png` | P0 | Banking right (right wing down) |
| `biplane-nose-up.png` | P1 | Nose up (climbing) |
| `biplane-nose-down.png` | P1 | Nose down (diving) |

**OR:** Generate 3 more frames matching `biplane-crew-accurate.png` style

### Missing Balloon Variants
**Priority: MEDIUM**

| Asset | Priority | Description |
|-------|----------|-------------|
| `balloon-red.png` | P0 | Standard red balloon |
| `balloon-blue.png` | P1 | Blue balloon (3 pts) |
| `balloon-gold.png` | P1 | Gold balloon (10 pts) |
| `balloon-pop-frame1-4.png` | P2 | Pop animation frames |

### Missing Backgrounds
**Priority: HIGH**

| Asset | Priority | Description |
|-------|----------|-------------|
| `sky-gradient.png` | P0 | Blue gradient background |
| `horizon-line.png` | P0 | Ground/horizon silhouette |
| `sun.png` | P2 | Sun graphic |
| `distant-mountains.png` | P2 | Far terrain |

### Missing Treats
**Priority: MEDIUM**

| Asset | Priority | Description |
|-------|----------|-------------|
| `treat-bone-small.png` | P0 | Regular bone (1 pt) |
| `treat-bone-large.png` | P1 | Large bone (3 pts) |
| `treat-golden.png` | P1 | Golden bone (10 pts) |

### Missing Explosion/Smoke Effects
**Priority: MEDIUM**

| Asset | Priority | Description |
|-------|----------|-------------|
| `explosion-frame1-6.png` | P1 | Balloon pop explosion |
| `smoke-puff.png` | P2 | Engine smoke |
| `contrail.png` | P2 | Plane contrails |

### Missing UI
**Priority: LOW**

| Asset | Priority | Description |
|-------|----------|-------------|
| `score-bg.png` | P2 | Score display background |
| `medal-ace.png` | P3 | Ace medal graphic |
| `life-icon.png` | P3 | Lives/health indicator |

---

## ORGANIZED TOTALS

| Category | Have | Need | Total |
|----------|------|------|-------|
| Biplanes | 5 | 5 | 10 |
| Clouds | 4 | 0 | 4 |
| Balloons | 4 | 4 | 8 |
| Effects | 3 | 5 | 8 |
| Characters | 3 | 0 | 3 |
| Props | 8 | 0 | 8 |
| UI | 5 | 3 | 8 |
| **TOTAL** | **32** | **17** | **49** |

---

## NEXT ACTIONS

### Immediate (This Session)
1. ✅ Copy existing assets to Pi v6 directory
2. ✅ Mark ready assets in ontology as "ready"
3. 🔄 Generate missing biplane animation frames (3 more)

### This Week
4. Generate balloon variants (red, blue, gold)
5. Generate background elements (sky, horizon)
6. Generate treat sprites
7. Test sprite loading in pygame

### Before v6.0 Release
8. All assets finalized and compressed
9. Alpha channel verified on all sprites
10. Game integration tested

---

## FILE PATHS

**Local (workspace):**
```
~/.openclaw/workspace/treatquest/
├── assets/
│   ├── biplanes/
│   ├── clouds/
│   ├── balloons/
│   ├── effects/
│   ├── characters/
│   ├── props/
│   └── ui/
└── FLYING_ACES_PLAN.md
```

**Pi (target):**
```
/opt/doggame/v6/assets/
├── sprites/
│   ├── harley/
│   ├── shanti/
│   ├── balloons/
│   └── effects/
└── backgrounds/
    └── clouds/
```

---

*Last updated by SamClaw - 2026-02-22*
