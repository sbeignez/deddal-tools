#!/usr/bin/env python3
"""Diagnostic script to verify database field values"""

import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    host=os.getenv('SUPABASE_HOST'),
    database=os.getenv('SUPABASE_DB'),
    user=os.getenv('SUPABASE_USER'),
    password=os.getenv('SUPABASE_PASSWORD'),
    port=os.getenv('SUPABASE_PORT', 5432)
)

cur = conn.cursor()

print('=== CATEGORY NAMES IN lib_casesets ===')
cur.execute('SELECT DISTINCT category FROM lib_casesets ORDER BY category')
for row in cur.fetchall():
    print(f'  "{row[0]}"')

print('\n=== PARITY KIND PATTERNS IN lib_cases ===')
cur.execute("SELECT DISTINCT kind FROM lib_cases WHERE kind LIKE '%parity%' ORDER BY kind")
for row in cur.fetchall():
    print(f'  "{row[0]}"')

print('\n=== TAG FIELD STRUCTURE IN lib_algorithms ===')
cur.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'lib_algorithms' AND column_name LIKE '%tag%'")
for row in cur.fetchall():
    print(f'  {row[0]}: {row[1]}')

print('\n=== BEGINNER TAG COUNTS ===')
cur.execute("SELECT COUNT(*) FROM lib_algorithms WHERE tag = 'beginner'")
print(f'  Using "tag = beginner": {cur.fetchone()[0]}')

try:
    cur.execute("SELECT COUNT(*) FROM lib_algorithms WHERE 'beginner' = ANY(tags)")
    print(f'  Using "ANY(tags)": {cur.fetchone()[0]}')
except Exception as e:
    print(f'  Using "ANY(tags)": ERROR - {type(e).__name__}')

cur.close()
conn.close()
