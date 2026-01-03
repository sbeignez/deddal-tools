# Repository Guidelines

## Project Structure & Module Organization
- `scripts/`: core workflow (`01-stage.py` for staging + report, `02-deploy.py` for deploy, `export_seed_data.py` legacy single-step) plus helpers (`archive_manager.py`, `diagnose_db.py`, `shared_utils.py`, `deployer.py`, `report_generator.py`, `diff_viewer.py`).
- `schemas/`: JSON Schema definitions for cases, case sets, and algorithms used by `SchemaValidator`.
- `config.yaml`: output directory and workflow notes; `.env.example` documents required Supabase vars.
- Generated assets live in `staging/<timestamp>/` (review), `deployments/` (manifests/history), and `backups/` (auto-archives); keep them out of commits unless explicitly required.
- `documentation/`: extended README and implementation status; use it for deeper context.

## Build, Test, and Development Commands
- Environment: `python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt`.
- Stage export + report: `python scripts/01-stage.py` (add `--dry-run` to avoid writes, `--file seeddata_cases_...json` to target one file, `--show-field-changes` for verbose diffs).
- Deploy staged data: `python scripts/02-deploy.py <TIMESTAMP>`; `--latest` deploys newest staging folder.
- Legacy/quick path: `python scripts/export_seed_data.py --dry-run` to preview or `python scripts/export_seed_data.py` to export directly; `--validate-only` runs validators without writing.
- Backup utilities: `python scripts/export_seed_data.py --list-archives` and `--restore <TIMESTAMP>` to inspect or roll back.

## Coding Style & Naming Conventions
- Python 3.10+ with 4-space indentation, type hints, and docstrings; favor `pathlib.Path` over raw strings and keep CLI output concise (uses `colorama`).
- Preserve DB-driven discovery: avoid hardcoding case sets or kinds—reuse helpers in `validators`/`shared_utils`.
- Export file pattern: `seeddata_{caseset|cases|algorithms}_{code}.json`; staging paths `staging/YYYY-MM-DD_HHMMSS/ios/`.
- Keep config-driven behavior (`config.yaml`) intact; treat Supabase queries and validation rules as single sources of truth.

## Testing Guidelines
- Run `python scripts/01-stage.py --dry-run` first to confirm connectivity and review diffs; prefer staged HTML report at `staging/<TS>/reports/export_report.html` for review.
- Schema checks run by default via `schemas/*.json`; only use `--skip-schema-validation` while debugging.
- For focused checks, combine `--file ...` with `--validate-only` or `--show-field-changes`; verify diff summaries printed to console.
- After deploy, inspect `DeddalInfra/Infrastructure/Persistence/SeedData/` and run `git diff` to confirm only intended JSON changes.

## Commit & Pull Request Guidelines
- Use short, imperative commit messages (e.g., `Add staging diff report for oll`); keep commits cohesive.
- In PRs, note staging timestamp deployed, commands/flags used, and whether a backup or restore occurred; link relevant issues.
- Attach key artifacts when helpful (diff summary, report screenshot) and describe any skipped validations or manual fixes.

## Security & Configuration Tips
- Store Supabase credentials only in `.env`; never commit `.env`, backups, or staging artifacts unless explicitly requested.
- Confirm `config.yaml` output paths before deploying and avoid running deploy commands against unreviewed staging exports.
