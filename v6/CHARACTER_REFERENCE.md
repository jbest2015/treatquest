# Character Reference Guide

**Treat Quest v6.0 — WWI Flying Aces**

---

## Shanti (Yellow Labrador Retriever Mix)

**ID:** e5ce94e1

### Physical Description
- **Size:** Medium-to-large
- **Breed:** Yellow Labrador Retriever Mix
- **Coat:** Smooth, short-to-medium length
- **Color:** Light cream or "yellow" shade
- **Markings:** None (solid cream/yellow)
- **Build:** Muscular
- **Ears:** Floppy, triangular

### Accessories
- **Collar:** Wide pink collar

### Role in v6.0
- TBD (to be determined)
- Previously: Space pilot (blue suit)
- v6.0 design: Needs to be defined (pilot or gunner?)

### Visual Notes for Artists
- Cream/yellow body
- No spots or markings
- Pink collar prominent
- Strong, muscular build

---

## Harley (Dachshund Mix)

**ID:** 4d0820f7

### Physical Description
- **Size:** Small
- **Breed:** Dachshund Mix
- **Coat:** Long-haired
- **Color:** Primarily white
- **Markings:** 
  - Black patches around ears and eyes
  - Small brown "mask" or patch on snout
- **Build:** Long-bodied, short legs, long torso
- **Ears:** Soft, feathery fur around ears and chest

### Accessories
- **Collar:** Black with GPS tracker/training device and round black tag

### Role in v6.0
- TBD (to be determined)
- Previously: Space pilot (red suit)
- v6.0 design: Needs to be defined (pilot or gunner?)

### Visual Notes for Artists
- White body with distinct black ear/patches
- Brown snout mask
- Feathered fur on chest and ears
- Small and long-bodied (Dachshund shape)
- GPS collar with round tag

---

## Design Notes

**Previous v5.1 Design (INCORRECT — DO NOT USE):**
- Shanti = chocolate lab, perky ears (WRONG — she's yellow lab)
- Harley = cream/beagle (WRONG — he's dachshund mix, white/black/brown)

**Correct v6.0 Design:**
- Must match photos and descriptions above
- Nano Banana generation must use exact breed descriptions
- References: pink collar (Shanti), black collar with GPS (Harley)

---

## Asset Requirements

### Priority P0 (Critical)
| Asset | Description |
|-------|-------------|
| `shanti_biplane.png` | Side view of Shanti in cockpit |
| `harley_biplane.png` | Side view of Harley in cockpit |
| `combined_crew.png` | Both dogs in one biplane (for combined sprite) |

### Priority P1 (High)
| Asset | Description |
|-------|-------------|
| `shanti_headshot.png` | Close-up sprite for HUD |
| `harley_headshot.png` | Close-up sprite for HUD |
| `shanti_animation_frames` | Banking left/right, climbing, nose-down |
| `harley_animation_frames` | Banking left/right, climbing, nose-down |

---

## Prompt Template for Nano Banana

**For accurate character sprites:**

```
Pixel art illustration of [CHARACTER NAME], a [SIZE] dog.
- Breed: [BREED]
- Coat: [COAT DESCRIPTION], [COLOR]
- Markings: [MARKINGS] (or "no markings")
- Build: [BUILD]
- Ears: [EARS]
- Collar: [COLLAR]
- Pose: [POSE/ROLE]
- Style: 16-bit pixel art, transparent background, side view
- Reference photo: [attach photo if available]
```

**Example for Harley:**
```
Pixel art illustration of Harley, a small dog.
- Breed: Dachshund Mix
- Coat: Long-haired, predominantly white
- Markings: Black patches around ears and eyes, brown mask on snout
- Build: Long-bodied, short legs, long torso
- Ears: Soft, feathery
- Collar: Black with GPS tracker and round black tag
- Pose: Sitting in biplane cockpit as gunner
- Style: 16-bit pixel art, transparent background, side view
```

---

*Character reference finalized: 2026-02-22*
*Ontology IDs: Harley=4d0820f7, Shanti=e5ce94e1*
