import sqlite3
import json
import uuid
import os
import threading
from datetime import datetime, timezone


class JobStore:
    """Simple SQLite-backed job store.

    For TESTING we recommend using `:memory:` as the db_path which keeps job
    state ephemeral. When db_path is a filesystem path the store persists
    across restarts.
    """

    def __init__(self, db_path):
        self.db_path = db_path
        self._lock = threading.Lock()
        self.conn = None
        self._connect()

    def _connect(self):
        needs_init = self.db_path != ":memory:" and not os.path.exists(self.db_path)
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        if needs_init or self.db_path == ":memory:":
            self._init_db()

    def _ensure_conn(self):
        if self.conn is None:
            self._connect()

    def _init_db(self):
        cur = self.conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                id TEXT PRIMARY KEY,
                payload TEXT,
                status TEXT,
                result TEXT,
                created_at TEXT
            )
            """)
        self.conn.commit()

    def enqueue(self, payload):
        job_id = uuid.uuid4().hex
        now = datetime.now(timezone.utc).isoformat()
        with self._lock:
            self._ensure_conn()
            cur = self.conn.cursor()
            cur.execute(
                "INSERT INTO jobs (id, payload, status, result, created_at) VALUES (?, ?, ?, ?, ?)",
                (job_id, json.dumps(payload), "queued", None, now),
            )
            self.conn.commit()
        return job_id

    def process_next(self):
        with self._lock:
            self._ensure_conn()
            cur = self.conn.cursor()
            cur.execute("BEGIN IMMEDIATE")
            cur.execute(
                "SELECT * FROM jobs WHERE status = 'queued' ORDER BY created_at LIMIT 1"
            )
            row = cur.fetchone()
            if not row:
                self.conn.rollback()
                return None
            job_id = row["id"]
            payload = json.loads(row["payload"] or "{}")

            cur.execute(
                "UPDATE jobs SET status = ? WHERE id = ?",
                ("processing", job_id),
            )

            # simulate processing result (same shape as previous stub)
            result = {
                "job_id": job_id,
                "summary": f"Processed {len(payload.get('inputs', []))} inputs",
                "findings": [
                    {
                        "engine_id": "mock-engine-1",
                        "confidence": 0.92,
                        "output": "sample finding",
                    }
                ],
            }

            cur.execute(
                "UPDATE jobs SET status = ?, result = ? WHERE id = ?",
                ("done", json.dumps(result), job_id),
            )
            self.conn.commit()
            return result

    def get_job(self, job_id):
        with self._lock:
            self._ensure_conn()
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM jobs WHERE id = ?", (job_id,))
            row = cur.fetchone()
            if not row:
                return None
            res = {
                "status": row["status"],
                "result": json.loads(row["result"]) if row["result"] else None,
            }
            return res

    def close(self):
        with self._lock:
            if self.conn is not None:
                self.conn.close()
                self.conn = None
