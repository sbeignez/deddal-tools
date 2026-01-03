#!/usr/bin/env python3
"""
Report Generator

Generates HTML reports for staged exports showing changes, validation results,
and deployment instructions.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List


class ReportGenerator:
    """Generates HTML reports for export results."""

    def __init__(self):
        """Initialize report generator."""
        pass

    def generate_html_report(
        self,
        export_data: Dict[str, Any],
        comparisons: List[Dict],
        stats: Dict[str, Any],
        output_path: Path
    ):
        """
        Generate HTML report for export.

        Args:
            export_data: Export metadata (timestamp, database, etc.)
            comparisons: List of file diff comparisons
            stats: Export statistics
            output_path: Path to write HTML report
        """
        timestamp = export_data.get('timestamp', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        database = export_data.get('database', 'unknown')
        total_records = stats.get('total_records', 0)
        files_exported = stats.get('files_exported', 0)

        # Count changes
        files_unchanged = sum(1 for c in comparisons if c['status'] == 'unchanged')
        files_changed = sum(1 for c in comparisons if c['status'] == 'changed')
        files_new = sum(1 for c in comparisons if c['status'] == 'new')
        files_with_warnings = sum(1 for c in comparisons if c.get('warnings'))

        # Generate HTML
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Seed Data Export Report - {timestamp}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
            padding: 20px;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
        }}
        .header h1 {{
            font-size: 28px;
            margin-bottom: 10px;
        }}
        .header p {{
            opacity: 0.9;
            font-size: 14px;
        }}
        .section {{
            padding: 30px;
            border-bottom: 1px solid #eee;
        }}
        .section:last-child {{
            border-bottom: none;
        }}
        .section h2 {{
            font-size: 20px;
            margin-bottom: 20px;
            color: #667eea;
        }}
        .summary-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }}
        .summary-card {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 6px;
            border-left: 4px solid #667eea;
        }}
        .summary-card .label {{
            font-size: 12px;
            text-transform: uppercase;
            color: #666;
            margin-bottom: 8px;
        }}
        .summary-card .value {{
            font-size: 32px;
            font-weight: bold;
            color: #333;
        }}
        .status-badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
        }}
        .status-unchanged {{
            background: #e3f2fd;
            color: #1976d2;
        }}
        .status-changed {{
            background: #fff3e0;
            color: #f57c00;
        }}
        .status-new {{
            background: #e8f5e9;
            color: #388e3c;
        }}
        .warning {{
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 15px;
            margin: 10px 0;
            border-radius: 4px;
        }}
        .warning strong {{
            color: #856404;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #eee;
        }}
        th {{
            background: #f8f9fa;
            font-weight: 600;
            color: #666;
            font-size: 12px;
            text-transform: uppercase;
        }}
        tr:hover {{
            background: #f8f9fa;
        }}
        .diff-positive {{
            color: #388e3c;
            font-weight: 600;
        }}
        .diff-negative {{
            color: #d32f2f;
            font-weight: 600;
        }}
        .action-box {{
            background: #e8f5e9;
            border: 2px solid #4caf50;
            border-radius: 8px;
            padding: 20px;
            margin: 20px 0;
        }}
        .action-box h3 {{
            color: #2e7d32;
            margin-bottom: 15px;
        }}
        code {{
            background: #f5f5f5;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Monaco', 'Courier New', monospace;
            font-size: 14px;
        }}
        .command {{
            background: #263238;
            color: #aed581;
            padding: 15px;
            border-radius: 6px;
            font-family: 'Monaco', 'Courier New', monospace;
            font-size: 14px;
            margin: 10px 0;
            overflow-x: auto;
        }}
        details {{
            margin: 10px 0;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 6px;
        }}
        summary {{
            cursor: pointer;
            font-weight: 600;
            color: #667eea;
            padding: 5px;
        }}
        summary:hover {{
            color: #764ba2;
        }}
        .record-list {{
            margin: 10px 0;
            padding-left: 20px;
        }}
        .record-list li {{
            padding: 4px 0;
            font-family: 'Monaco', 'Courier New', monospace;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <h1>Seed Data Export Report</h1>
            <p>Generated: {timestamp}</p>
            <p>Database: {database}</p>
        </div>

        <!-- Summary -->
        <div class="section">
            <h2>Export Summary</h2>
            <div class="summary-grid">
                <div class="summary-card">
                    <div class="label">Files Exported</div>
                    <div class="value">{files_exported}</div>
                </div>
                <div class="summary-card">
                    <div class="label">Total Records</div>
                    <div class="value">{total_records:,}</div>
                </div>
                <div class="summary-card">
                    <div class="label">Files Changed</div>
                    <div class="value">{files_changed}</div>
                </div>
                <div class="summary-card">
                    <div class="label">Warnings</div>
                    <div class="value">{files_with_warnings}</div>
                </div>
            </div>
"""

        # Validation status
        if stats.get('errors'):
            html += """
            <div class="warning">
                <strong>⚠ Validation Errors</strong><br>
                Export completed with validation errors. See details below.
            </div>
"""
        elif stats.get('warnings'):
            html += """
            <div class="warning">
                <strong>⚠ Validation Warnings</strong><br>
                Export completed with warnings. Review before deploying.
            </div>
"""
        else:
            html += """
            <div class="action-box" style="background: #e8f5e9; border-color: #4caf50;">
                <strong style="color: #2e7d32;">✓ All Validation Checks Passed</strong>
            </div>
"""

        html += """
        </div>

        <!-- File Changes -->
        <div class="section">
            <h2>File Changes</h2>
"""

        if files_unchanged == files_exported and files_changed == 0:
            html += """
            <p style="color: #666; font-style: italic;">No changes detected. All files match existing data.</p>
"""
        else:
            html += f"""
            <p>
                <span class="status-badge status-unchanged">{files_unchanged} Unchanged</span>
                <span class="status-badge status-changed">{files_changed} Changed</span>
                <span class="status-badge status-new">{files_new} New</span>
            </p>

            <table>
                <thead>
                    <tr>
                        <th>File</th>
                        <th>Status</th>
                        <th>Old Count</th>
                        <th>New Count</th>
                        <th>Diff</th>
                        <th>Warnings</th>
                    </tr>
                </thead>
                <tbody>
"""

            for comp in comparisons:
                status = comp['status']
                file_name = comp['file_name']
                old_count = comp.get('old_count', 0)
                new_count = comp.get('new_count', 0)
                diff = comp.get('diff', 0)
                warnings = comp.get('warnings', [])

                status_class = f"status-{status}"
                diff_class = "diff-positive" if diff > 0 else ("diff-negative" if diff < 0 else "")
                diff_str = f"+{diff}" if diff > 0 else str(diff)

                warning_text = ""
                if warnings:
                    warning_text = f"<br><small style='color: #f57c00;'>{warnings[0]}</small>"

                html += f"""
                    <tr>
                        <td><code>{file_name}</code></td>
                        <td><span class="status-badge {status_class}">{status}</span></td>
                        <td>{old_count if status != 'new' else '-'}</td>
                        <td>{new_count}</td>
                        <td class="{diff_class}">{diff_str if status != 'new' else 'new'}</td>
                        <td>{warning_text}</td>
                    </tr>
"""

            html += """
                </tbody>
            </table>
"""

        html += """
        </div>

        <!-- Detailed Changes -->
        <div class="section">
            <h2>Detailed Changes</h2>
"""

        has_details = any(comp['status'] == 'changed' for comp in comparisons)
        if not has_details:
            html += """
            <p style="color: #666; font-style: italic;">No detailed changes to display.</p>
"""
        else:
            for comp in comparisons:
                if comp['status'] != 'changed':
                    continue

                file_name = comp['file_name']
                added_ids = list(comp.get('added_ids', set()))
                removed_ids = list(comp.get('removed_ids', set()))

                html += f"""
            <details>
                <summary>{file_name} - {len(added_ids)} added, {len(removed_ids)} removed</summary>
"""

                if added_ids:
                    html += f"""
                <h4>Added Records ({len(added_ids)})</h4>
                <ul class="record-list">
"""
                    for record_id in added_ids[:20]:
                        html += f"                    <li>{record_id}</li>\n"
                    if len(added_ids) > 20:
                        html += f"                    <li><em>... and {len(added_ids) - 20} more</em></li>\n"
                    html += """
                </ul>
"""

                if removed_ids:
                    html += f"""
                <h4>Removed Records ({len(removed_ids)})</h4>
                <ul class="record-list">
"""
                    for record_id in removed_ids[:20]:
                        html += f"                    <li>{record_id}</li>\n"
                    if len(removed_ids) > 20:
                        html += f"                    <li><em>... and {len(removed_ids) - 20} more</em></li>\n"
                    html += """
                </ul>
"""

                html += """
            </details>
"""

        html += """
        </div>

        <!-- Deployment Instructions -->
        <div class="section">
            <h2>Ready to Deploy?</h2>
            <div class="action-box">
                <h3>Next Steps</h3>
                <ol>
                    <li>Review the changes above carefully</li>
                    <li>Check for breaking changes or warnings</li>
                    <li>If everything looks correct, deploy with:</li>
                </ol>
"""

        staged_timestamp = export_data.get('staged_timestamp', 'TIMESTAMP')
        html += f"""
                <div class="command">python export_seed_data.py --deploy {staged_timestamp}</div>
"""

        html += """
                <p style="margin-top: 15px;"><strong>After deployment:</strong></p>
                <ul>
                    <li>Run iOS app to verify seed data loads correctly</li>
                    <li>Run tests to ensure no regressions</li>
                    <li>Review git diff and commit if tests pass</li>
                </ul>
            </div>
        </div>

    </div>
</body>
</html>
"""

        # Write HTML report
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            f.write(html)

    def generate_metadata(
        self,
        export_data: Dict[str, Any],
        stats: Dict[str, Any],
        output_path: Path
    ):
        """
        Generate machine-readable export metadata JSON.

        Args:
            export_data: Export metadata
            stats: Export statistics
            output_path: Path to write metadata JSON
        """
        metadata = {
            'timestamp': export_data.get('timestamp'),
            'database': export_data.get('database'),
            'files_exported': stats.get('files_exported', 0),
            'files_skipped': stats.get('files_skipped', 0),
            'total_records': stats.get('total_records', 0),
            'errors': stats.get('errors', []),
            'warnings': stats.get('warnings', []),
            'staged_timestamp': export_data.get('staged_timestamp')
        }

        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(metadata, f, indent=2)

    def generate_summary(
        self,
        comparisons: List[Dict],
        output_path: Path
    ):
        """
        Generate diff summary JSON.

        Args:
            comparisons: List of file comparisons
            output_path: Path to write summary JSON
        """
        summary = {
            'files': []
        }

        for comp in comparisons:
            file_summary = {
                'file_name': comp['file_name'],
                'status': comp['status'],
                'old_count': comp.get('old_count', 0),
                'new_count': comp.get('new_count', 0),
                'diff': comp.get('diff', 0),
                'added_count': len(comp.get('added_ids', set())),
                'removed_count': len(comp.get('removed_ids', set())),
                'warnings': comp.get('warnings', [])
            }
            summary['files'].append(file_summary)

        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(summary, f, indent=2)


def main():
    """Demo/testing entry point."""
    print("ReportGenerator - use as module, not standalone")


if __name__ == "__main__":
    main()
