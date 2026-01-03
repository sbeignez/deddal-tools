# Deddal iOS Tool Context

This directory contains utility scripts and tools for maintaining the Deddal iOS project.

## Scripts

### generate-tree.sh

Generates a formatted directory tree structure documentation for any directory in the Deddal project.

**Default Behavior:**
When called with no arguments, automatically generates tree structures for:
- `Deddal` → `documentation/Deddal-Tree-Structure.md`
- `DeddalCore` → `documentation/DeddalCore-Tree-Structure.md`
- `DeddalTests` → `documentation/DeddalTests-Tree-Structure.md`

**Usage:**
```bash
./tool-context/generate-tree.sh [target_directory] [output_file]
```

**Parameters:**
- `target_directory`: (Optional) Directory to generate tree for (relative to deddal-ios root)
  - If omitted: Generates for both Deddal and DeddalCore
- `output_file`: (Optional) Output markdown file path (relative to deddal-ios root)
  - Required if target_directory is provided

**Examples:**

Generate trees for Deddal, DeddalCore, and DeddalTests (default):
```bash
cd /Users/trophee-mini/code/deddal/deddal-ios
./tool-context/generate-tree.sh
# Generates:
#   documentation/Deddal-Tree-Structure.md
#   documentation/DeddalCore-Tree-Structure.md
#   documentation/DeddalTests-Tree-Structure.md
```

Generate tree for a single specific directory:
```bash
./tool-context/generate-tree.sh Deddal documentation/Deddal-Tree-Structure.md
```

Generate tree for a subdirectory:
```bash
./tool-context/generate-tree.sh Deddal/Views documentation/Views-Tree-Structure.md
```

Generate tree for DeddalAdapters:
```bash
./tool-context/generate-tree.sh DeddalAdapters documentation/DeddalAdapters-Tree-Structure.md
```

**Output:**
- Creates a markdown file with:
  - Header with directory name
  - Generation timestamp
  - Formatted tree structure in code block
  - Excludes .DS_Store files
  - Sorted alphabetically

**Location:**
- Script: `/Users/trophee-mini/code/deddal/deddal-ios/tool-context/generate-tree.sh`
- Default outputs:
  - `/Users/trophee-mini/code/deddal/deddal-ios/documentation/Deddal-Tree-Structure.md`
  - `/Users/trophee-mini/code/deddal/deddal-ios/documentation/DeddalCore-Tree-Structure.md`
  - `/Users/trophee-mini/code/deddal/deddal-ios/documentation/DeddalTests-Tree-Structure.md`

**Notes:**
- Script automatically creates output directory if it doesn't exist
- Uses relative paths from deddal-ios root directory
- Tree structure includes all files and directories recursively
- Format uses indentation and pipe characters for readability
- Run from deddal-ios directory for best results
