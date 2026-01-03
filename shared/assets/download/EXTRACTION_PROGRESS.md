# Move Diagram Extraction Progress

## ✅ Completed

### 1. PDF Extraction Setup
- ✅ Installed `pdf2svg` via Homebrew for vector extraction
- ✅ Installed Inkscape for manual diagram editing
- ✅ Downloaded reference PDF: `rubiks_guide.pdf` (5.3 MB, 39 pages)

### 2. Page Extraction
Extracted 6 pages containing move diagrams:

| Page | File | Size | Contains |
|------|------|------|----------|
| 7 | `page-07.svg` | 265 KB | U, U', D, D' |
| 9 | `page-09.svg` | 335 KB | F, F', B, B' |
| 18 | `page-18.svg` | 491 KB | TBD (needs review) |
| 21 | `page-21.svg` | 597 KB | TBD (needs review) |
| 28 | `page-28.svg` | 534 KB | TBD (needs review) |
| 31 | `page-31.svg` | 525 KB | TBD (needs review) |

### 3. Individual Move Extraction
User has manually extracted 3 move diagrams from page-07.svg:

| Move | File | Status |
|------|------|--------|
| U | `move_U.svg` | ✅ Aligned & cropped |
| D | `move_D.svg` | ✅ Aligned & cropped |
| D' | `move_Dp.svg` | ✅ Aligned & cropped |

**Alignment details:**
- Original canvas: 210mm x 297mm (A4 size)
- Cropped canvas: 60mm x 50mm
- ViewBox: `0 0 60 50` (starts at origin)
- Transform adjusted to position content at 0,0

---

## 📋 Next Steps

### Immediate Tasks

1. **Review pages 18, 21, 28, 31** (Priority: High)
   - Open each page SVG in Inkscape or browser
   - Identify which move diagrams each page contains
   - Document findings

2. **Extract remaining diagrams from page-07** (From: U, U', D, D')
   - ❌ U' (not yet extracted)

3. **Extract diagrams from page-09** (Contains: F, F', B, B')
   - ❌ F (not yet extracted)
   - ❌ F' (not yet extracted)
   - ❌ B (not yet extracted)
   - ❌ B' (not yet extracted)

4. **Extract diagrams from additional pages**
   - After reviewing pages 18, 21, 28, 31, extract individual diagrams

### Workflow for Each New Diagram

The established workflow for extracting additional diagrams:

1. **Manual extraction in Inkscape:**
   - Open page SVG (e.g., `page-07.svg`)
   - Select the diagram for a specific move (e.g., U')
   - Copy selection
   - Create new document: File → New
   - Paste diagram
   - Save as `move_<NAME>.svg` (e.g., `move_Up.svg` for U')

2. **Auto-alignment (Claude):**
   - Claude will adjust the viewBox and transform to position content at 0,0:
   ```xml
   <svg
      width="60mm"
      height="50mm"
      viewBox="0 0 60 50"  <!-- Always starts at origin -->
      ...>
   <g transform="matrix(...)">  <!-- Transform adjusted per diagram -->
   ```

3. **Verification:**
   - Open aligned SVG in browser or vector editor
   - Verify cube diagram is properly cropped and positioned

---

## 📁 File Structure

```
tool-assets/download/
├── rubiks_guide.pdf                    # Source PDF
├── move_diagrams_from_pdf/
│   ├── page-07.svg                     # ✅ Extracted (U, U', D, D')
│   ├── page-09.svg                     # ✅ Extracted (F, F', B, B')
│   ├── page-18.svg                     # ✅ Extracted (TBD moves)
│   ├── page-21.svg                     # ✅ Extracted (TBD moves)
│   ├── page-28.svg                     # ✅ Extracted (TBD moves)
│   ├── page-31.svg                     # ✅ Extracted (TBD moves)
│   ├── move_U.svg                      # ✅ Extracted & aligned
│   ├── move_D.svg                      # ✅ Extracted & aligned
│   └── move_Dp.svg                     # ✅ Extracted & aligned (D')
└── EXTRACTION_PROGRESS.md              # This file
```

---

## 🎯 Expected Final Output

Once extraction is complete, we should have individual SVG files for all moves:

### Face Turns (6 base moves × 2 directions = 12)
- U, U', D, D', F, F', B, B', R, R', L, L'

### Additional Moves (if in PDF)
- Face 180° turns: U2, D2, F2, B2, R2, L2
- Wide moves: u, u', d, d', f, f', b, b', r, r', l, l'
- Slice moves: M, M', E, E', S, S'
- Cube rotations: x, x', y, y', z, z'

**Note:** The PDF may only contain the 12 basic face turns. Additional moves may need to be created programmatically or found in other sources.

---

## 📝 Notes

- **Naming convention:** Use `_prime` for prime moves (e.g., `move_Up.svg` for U', `move_Fp.svg` for F')
- **ViewBox adjustments:** Each diagram may need slightly different viewBox values depending on position in the source page
- **Background colors:** All diagrams have a green/blue rounded rectangle background (preserved from PDF)
- **Arrow styles:** White rotation arrows with black outlines, red accent arrows for direction
- **File sizes:** Individual aligned SVGs are ~15 KB each (much smaller than full pages)

---

Generated: 2025-11-16
