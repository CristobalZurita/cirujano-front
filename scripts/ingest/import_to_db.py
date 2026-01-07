#!/usr/bin/env python3
"""Import normalized items into a SQLite database (idempotent).

Writes into `backend/instance/cirujano.sqlite` and records an import_run entry.
"""
from __future__ import annotations
import os
import json
import sqlite3
import uuid
from datetime import datetime

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
NORMALIZED = os.path.join(REPO_ROOT, 'reports', 'normalized_items.json')
DB_PATH = os.path.join(REPO_ROOT, 'backend', 'instance', 'cirujano.sqlite')


def ensure_db(path=DB_PATH):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    conn = sqlite3.connect(path)
    return conn


def run_import():
    if not os.path.exists(NORMALIZED):
        raise SystemExit('Run normalize_excel.py first to produce normalized_items.json')
    with open(NORMALIZED, 'r', encoding='utf-8') as fh:
        items = json.load(fh)

    conn = ensure_db()
    cur = conn.cursor()

    # create tables if not exist (simple DDL that mirrors database/ddl_cirujano.sql)
    cur.executescript(open(os.path.join(REPO_ROOT, 'database', 'ddl_cirujano.sql'), 'r', encoding='utf-8').read())

    run_id = str(uuid.uuid4())
    started = datetime.utcnow().isoformat() + 'Z'
    cur.execute('INSERT INTO import_runs (run_id, source_file, started_at, status) VALUES (?, ?, ?, ?)', (run_id, os.path.basename(NORMALIZED), started, 'running'))
    conn.commit()

    inserted = 0
    updated = 0
    for it in items:
        sku = it.get('sku')
        name = it.get('name')
        category = it.get('category')

        # find or create category
        cur.execute('SELECT id FROM categories WHERE name = ?', (category,))
        row = cur.fetchone()
        if row:
            cat_id = row[0]
        else:
            cur.execute('INSERT INTO categories (name) VALUES (?)', (category,))
            cat_id = cur.lastrowid

        # upsert item by sku
        cur.execute('SELECT id FROM items WHERE sku = ?', (sku,))
        r = cur.fetchone()
        if r:
            cur.execute('UPDATE items SET name = ?, category_id = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?', (name, cat_id, r[0]))
            updated += 1
        else:
            cur.execute('INSERT INTO items (sku, name, category_id, stock) VALUES (?, ?, ?, ?)', (sku, name, cat_id, 0))
            inserted += 1

    finished = datetime.utcnow().isoformat() + 'Z'
    summary = f'inserted={inserted},updated={updated}'
    cur.execute('UPDATE import_runs SET finished_at = ?, status = ?, summary = ? WHERE run_id = ?', (finished, 'finished', summary, run_id))
    conn.commit()
    conn.close()
    print(f'Import finished: {summary} (run_id={run_id})')


if __name__ == '__main__':
    run_import()
