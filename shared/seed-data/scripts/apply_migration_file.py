#!/usr/bin/env python3
"""
Apply a SQL migration file to Supabase database.

Usage:
    python apply_migration_file.py --file PATH --project-id ID
"""

import argparse
import os
import sys
from pathlib import Path

# Add parent directory to path to import from scripts
sys.path.insert(0, str(Path(__file__).parent))

try:
    import psycopg2
    from dotenv import load_dotenv
except ImportError:
    print("❌ Error: Required packages not installed")
    print("   Run: pip install psycopg2-binary python-dotenv")
    sys.exit(1)


def get_supabase_connection_string(project_id: str) -> str:
    """Get Supabase connection string from environment or construct it.

    Args:
        project_id: Supabase project ID

    Returns:
        PostgreSQL connection string
    """
    # Try to load from .env file in scripts directory
    env_path = Path(__file__).parent / '.env'
    load_dotenv(env_path)

    # Check for direct connection string
    conn_str = os.getenv('SUPABASE_CONNECTION_STRING')
    if conn_str:
        return conn_str

    # Construct from components (using same variable names as export scripts)
    host = os.getenv('SUPABASE_HOST')
    port = os.getenv('SUPABASE_PORT', '5432')
    database = os.getenv('SUPABASE_DATABASE') or os.getenv('SUPABASE_DB')
    user = os.getenv('SUPABASE_USER')
    password = os.getenv('SUPABASE_PASSWORD')

    if not all([host, database, user, password]):
        print("❌ Error: Required Supabase credentials not found in environment")
        print("   Required variables: SUPABASE_HOST, SUPABASE_DATABASE, SUPABASE_USER, SUPABASE_PASSWORD")
        print(f"   Found: host={bool(host)}, database={bool(database)}, user={bool(user)}, password={bool(password)}")
        sys.exit(1)

    # Construct PostgreSQL connection string
    return f"postgresql://{user}:{password}@{host}:{port}/{database}"


def apply_migration(filepath: str, project_id: str) -> None:
    """Apply SQL migration file to Supabase database.

    Args:
        filepath: Path to SQL file
        project_id: Supabase project ID
    """
    # Read SQL file
    sql_path = Path(filepath)
    if not sql_path.exists():
        print(f"❌ Error: SQL file not found: {sql_path}")
        sys.exit(1)

    print(f"📖 Reading SQL file: {sql_path}")
    print(f"   File size: {sql_path.stat().st_size:,} bytes")

    sql_content = sql_path.read_text()

    # Get connection string
    conn_str = get_supabase_connection_string(project_id)

    print(f"\n🔌 Connecting to Supabase (project: {project_id})...")

    try:
        # Connect to database
        conn = psycopg2.connect(conn_str)
        conn.autocommit = False  # Use transaction

        cursor = conn.cursor()

        print("✅ Connected successfully")
        print("\n🔨 Executing SQL migration...")

        try:
            # Execute SQL
            cursor.execute(sql_content)

            # Commit transaction
            conn.commit()

            print("✅ Migration applied successfully")

            # Get statistics
            cursor.execute("SELECT COUNT(*) FROM lib_cases WHERE kind = 'zbll'")
            case_count = cursor.fetchone()[0]

            cursor.execute("""
                SELECT COUNT(*) FROM lib_algorithms a
                JOIN lib_cases c ON a.case_id = c.id
                WHERE c.kind = 'zbll'
            """)
            alg_count = cursor.fetchone()[0]

            cursor.execute("""
                SELECT COUNT(*) FROM lib_caseset_cases
                WHERE caseset_id = (SELECT id FROM lib_casesets WHERE code = 'zbll')
            """)
            junction_count = cursor.fetchone()[0]

            print(f"\n📊 Database Statistics:")
            print(f"   ZBLL cases: {case_count}")
            print(f"   ZBLL algorithms: {alg_count}")
            print(f"   Junction table entries: {junction_count}")

        except Exception as e:
            print(f"\n❌ Error executing SQL: {e}")
            conn.rollback()
            raise

        finally:
            cursor.close()
            conn.close()

    except psycopg2.Error as e:
        print(f"\n❌ Database error: {e}")
        sys.exit(1)


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description='Apply SQL migration file to Supabase database'
    )
    parser.add_argument(
        '--file',
        required=True,
        help='Path to SQL migration file'
    )
    parser.add_argument(
        '--project-id',
        default='qoglsyykgrqalsemigii',
        help='Supabase project ID (default: qoglsyykgrqalsemigii)'
    )

    args = parser.parse_args()

    apply_migration(args.file, args.project_id)


if __name__ == '__main__':
    main()
