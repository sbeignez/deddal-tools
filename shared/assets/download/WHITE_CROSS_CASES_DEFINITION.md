# White Cross Case Definitions

## Overview

The White Cross is the first step in the CFOP method (Cross → F2L → OLL → PLL). This document defines the comprehensive set of White Cross cases to be implemented in the Deddal iOS app.

## Case Set Information

- **Code**: `cross-basic`
- **Name**: White Cross Basics
- **Subtitle**: Common cross edge scenarios
- **Category**: 3x3 - CFOP Cross
- **Expected Count**: 8 cases
- **Pattern From**: Scrambled
- **Pattern To**: Cross

## Design Philosophy

The White Cross is primarily **intuitive** rather than algorithmic. However, we define standard cases for:
- **Educational purposes** - helping beginners recognize common patterns
- **Practice/Drill mode** - targeted training for specific scenarios
- **Progress tracking** - monitoring cross solving efficiency

## Case Definitions

### **Case 1: Edge in U Layer (Oriented)**
- **Code**: `3x3_cross_u-oriented-01`
- **Title**: U Layer Oriented
- **Long Name**: White edge in U layer already matches its center
- **Description**: White edge located in top layer with side color correctly facing its matching center. Simplest case - just align and insert.
- **Recognition**: White sticker faces down (when solving cross-down); side color lines up with center
- **Scramble Setup**: `F2 D F2` (brings solved F edge to U layer)
- **Algorithms**:
  1. Simple Insert (Standard): `F2` - 2 moves
  2. Alternative (R face): `R2` - 2 moves
- **Difficulty**: 1/5 (Easiest)
- **Popularity**: 100
- **Story**: "The edge is already in perfect position - just bring it home!"

---

### **Case 2: Edge in U Layer (Flipped)**
- **Code**: `3x3_cross_u-flipped-01`
- **Title**: U Layer Flipped
- **Long Name**: White edge in U layer but oriented incorrectly
- **Description**: White sticker faces up (when solving cross-down); side color doesn't match its center. Requires flip before insertion.
- **Recognition**: White sticker visible on U face; side color misaligned
- **Scramble Setup**: `R U R'` (creates flipped edge on U)
- **Algorithms**:
  1. Flip Right (Standard): `R U R'` - 3 moves
  2. Flip Left (Mirror): `L' U' L` - 3 moves
  3. Alternative: `F U F'` - 3 moves
- **Difficulty**: 2/5
- **Popularity**: 95
- **Story**: "The edge is upside down - flip it over first, then insert."

---

### **Case 3: Edge in U Layer (Adjacent Swap)**
- **Code**: `3x3_cross_u-adjacent-01`
- **Title**: U Layer Adjacent
- **Long Name**: White edge in U layer but in adjacent slot
- **Description**: Edge is oriented correctly but needs to move to adjacent position before insertion.
- **Recognition**: White faces down, but edge is one slot away from target
- **Scramble Setup**: `U F2` (moves F edge to R position)
- **Algorithms**:
  1. Realign: `U F2` - 2 moves (U move + insert)
  2. Direct: `R2 U' F2` - 3 moves
- **Difficulty**: 1/5
- **Popularity**: 90
- **Story**: "Almost there - just rotate U and drop it in."

---

### **Case 4: Edge in U Layer (Opposite)**
- **Code**: `3x3_cross_u-opposite-01`
- **Title**: U Layer Opposite
- **Long Name**: White edge in U layer opposite to target slot
- **Description**: Edge is correctly oriented but on the opposite face. Requires U2 to align.
- **Recognition**: White faces down, edge is directly opposite (180°) from target
- **Scramble Setup**: `U2 F2`
- **Algorithms**:
  1. Align & Insert: `U2 F2` - 2 moves
- **Difficulty**: 1/5
- **Popularity**: 85
- **Story**: "Spin halfway around and insert."

---

### **Case 5: Edge in D Layer (Misaligned)**
- **Code**: `3x3_cross_d-misaligned-01`
- **Title**: D Layer Misaligned
- **Long Name**: White edge already in D layer but wrong slot
- **Description**: Edge is solved on bottom layer but doesn't match its side center. Must extract to U layer, realign, then reinsert.
- **Recognition**: Edge on D layer, white faces down, but side color doesn't match center
- **Scramble Setup**: `F2 U2 F2` (F edge in B position on D)
- **Algorithms**:
  1. Extract & Realign: `F2 U2 F2` - 4 moves
  2. Direct (R face): `R2 U R2` - 3 moves
- **Difficulty**: 2/5
- **Popularity**: 80
- **Story**: "It's in the wrong spot - pull it out and put it back correctly."

---

### **Case 6: Edge in D Layer (Flipped)**
- **Code**: `3x3_cross_d-flipped-01`
- **Title**: D Layer Flipped
- **Long Name**: White edge in D layer but oriented incorrectly
- **Description**: Edge is in correct slot but flipped (white faces up instead of down). Requires special flip sequence.
- **Recognition**: Edge in D layer, correct slot, but white sticker visible on D face
- **Scramble Setup**: `F' U' R U F2` (creates flipped edge in D)
- **Algorithms**:
  1. Flip in Place: `F U R U' R' F'` - 6 moves
  2. Extract & Flip: `F2 R U R' F2` - 5 moves
- **Difficulty**: 3/5
- **Popularity**: 60
- **Story**: "It's in the right place but upside down - flip it without breaking the rest."

---

### **Case 7: Edge in Middle Layer (E Slice)**
- **Code**: `3x3_cross_middle-01`
- **Title**: Middle Layer Edge
- **Long Name**: White edge trapped in middle layer (E slice)
- **Description**: Edge sits between two centers in the equator. Must be extracted upward to U layer.
- **Recognition**: White edge between F-R, R-B, B-L, or L-F centers
- **Scramble Setup**: `R U' R'` (edge in FR position)
- **Algorithms**:
  1. Extract Right: `R U R'` - 3 moves
  2. Extract Left: `L' U' L` - 3 moves
  3. Extract Front: `F U F'` - 3 moves
- **Difficulty**: 2/5
- **Popularity**: 75
- **Story**: "It's stuck in the middle - pull it up to the top first."

---

### **Case 8: Edge in Middle Layer (Flipped)**
- **Code**: `3x3_cross_middle-flipped-01`
- **Title**: Middle Layer Flipped
- **Long Name**: White edge in middle layer but oriented incorrectly
- **Description**: Edge in E slice with white facing outward (not toward center). Requires extraction and flip.
- **Recognition**: White sticker visible on side face in middle layer
- **Scramble Setup**: `R' F R` (creates flipped edge in middle)
- **Algorithms**:
  1. Extract & Flip (Right): `R U' R' U R U R'` - 7 moves
  2. Extract & Flip (Front): `F' U F U' F' U' F` - 7 moves
  3. Simpler: `R' U R U' R' U' R` - 7 moves (sledgehammer variant)
- **Difficulty**: 3/5
- **Popularity**: 50
- **Story**: "It's stuck in the middle AND upside down - pull it out and flip it."

---

## Case Statistics

| Case # | Code | Difficulty | Popularity | Move Count | Category |
|--------|------|------------|------------|------------|----------|
| 1 | u-oriented-01 | 1/5 | 100 | 2 | U Layer |
| 2 | u-flipped-01 | 2/5 | 95 | 3 | U Layer |
| 3 | u-adjacent-01 | 1/5 | 90 | 2-3 | U Layer |
| 4 | u-opposite-01 | 1/5 | 85 | 2 | U Layer |
| 5 | d-misaligned-01 | 2/5 | 80 | 3-4 | D Layer |
| 6 | d-flipped-01 | 3/5 | 60 | 5-6 | D Layer |
| 7 | middle-01 | 2/5 | 75 | 3 | Middle |
| 8 | middle-flipped-01 | 3/5 | 50 | 7 | Middle |

## Algorithm Notes

### Notation
- **U/D/F/R/L/B**: Face turns (clockwise)
- **U'/D'/F'/R'/L'/B'**: Counter-clockwise turns
- **U2/D2/F2/R2/L2/B2**: Double turns (180°)
- **d**: D + y (down layer + whole cube rotation)

### Efficiency Guidelines
- Target: 6-8 moves per edge (average)
- Best case: 2 moves (oriented in U)
- Worst case: 7 moves (middle layer flipped)

### Common Patterns
- **Simple insert**: F2, R2 (2 moves)
- **Flip then insert**: R U R', F U F' (3 moves)
- **Extract from middle**: R U R' (3 moves)
- **Flip in D layer**: F U R U' R' F' (6 moves)

## Implementation Notes

### VisualCube Parameters
For generating SVG images:
- **Base URL**: `https://visualcube.api.cubing.net/visualcube.php?fmt=svg`
- **Size**: 300px
- **Stage**: `cross` (highlights cross edges)
- **Case**: Use scramble setup (URL-encoded)
- **View**: Default 3D isometric (or `plan` for top-down)
- **Rotation**: Optional `r=y30x-35` for angled view

### Example VisualCube URL
```
https://visualcube.api.cubing.net/visualcube.php?fmt=svg&size=300&stage=cross&case=F2%20D%20F2
```

### JSON Data Structure
Each case will have:
- UUID-based IDs for all entities
- Cross-referenced `case_set_id` and `case_id`
- Multiple algorithms per case (beginner, advanced, alternative)
- Metadata: difficulty (1-5), popularity (0-100)
- Image asset names matching SVG filenames

## Mapping to Existing Hardcoded Cases

| Hardcoded Code | New Code | Match |
|----------------|----------|-------|
| CROSS-U-ORIENTED | 3x3_cross_u-oriented-01 | ✓ Exact |
| CROSS-U-FLIPPED | 3x3_cross_u-flipped-01 | ✓ Exact |
| CROSS-D-MISALIGNED | 3x3_cross_d-misaligned-01 | ✓ Exact |
| CROSS-MIDDLE-EXTRACT | 3x3_cross_middle-01 | ✓ Similar |
| CROSS-PAIR-FLIP | *(removed)* | ✗ Out of scope (F2L) |

**Note**: The "Solved pair flipped" case (CROSS-PAIR-FLIP) is actually an F2L case, not a pure cross case. We'll exclude it from the cross case set.

## Next Steps

1. ✓ Case definitions complete
2. → Generate UUIDs for all entities
3. → Create 3 JSON files (case_sets, cases, algorithms)
4. → Write download script for SVG images
5. → Import assets to Xcode
6. → Integrate with MethodsSeedLoader

---

**Document Version**: 1.0
**Created**: 2025-11-16
**Author**: Claude (Deddal iOS Project)
