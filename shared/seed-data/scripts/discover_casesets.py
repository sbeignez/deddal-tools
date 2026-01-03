#!/usr/bin/env python3
"""Discover all case sets in database for dynamic export"""

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

print('=== ALL CASE SETS (with counts) ===\n')
cur.execute('''
    SELECT
        cs.id,
        cs.code,
        cs.category,
        COUNT(DISTINCT cc.case_id) as num_cases,
        (SELECT COUNT(*)
         FROM lib_algorithms a
         JOIN lib_cases c ON a.case_id = c.id
         JOIN lib_caseset_cases cc2 ON c.id = cc2.case_id
         WHERE cc2.caseset_id = cs.id) as num_algorithms
    FROM lib_casesets cs
    LEFT JOIN lib_caseset_cases cc ON cs.id = cc.caseset_id
    GROUP BY cs.id, cs.code, cs.category
    ORDER BY cs.code
''')

print(f"{'Code':<35} | {'Category':<35} | {'Cases':>5} | {'Algs':>5}")
print('-' * 90)

for row in cur.fetchall():
    code, category, cases, algs = row[1], row[2], row[3], row[4]
    print(f"{code:<35} | {category:<35} | {cases:>5} | {algs:>5}")

print(f"\n✓ Found {cur.rowcount} case sets")
print(f"  Expected files: {cur.rowcount * 3} (3 per case set)")

cur.close()
conn.close()
