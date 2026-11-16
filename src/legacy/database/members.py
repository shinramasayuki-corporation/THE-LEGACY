"""Member identity repository."""

import uuid
from datetime import datetime, timezone
from pathlib import Path

from legacy.database.connection import connect_database

def _now() -> str:
    return datetime.now(timezone.utc).isoformat()

class MemberRepository:
    def __init__(self, database_path: str | Path):
        self.database_path = database_path

    def create_member(
        self,
        username: str,
        discord_id: str | None = None,
        preferred_language: str = "fr",
    ) -> dict:
        if not username.strip():
            raise ValueError("Username cannot be empty.")

        member_id = str(uuid.uuid4())
        timestamp = _now()

        with connect_database(self.database_path) as connection:
            connection.execute(
                """
                INSERT INTO members (
                    id, discord_id, username, preferred_language,
                    account_status, created_at, updated_at
                )
                VALUES (?, ?, ?, ?, 'active', ?, ?)
                """,
                (
                    member_id,
                    discord_id,
                    username.strip(),
                    preferred_language.strip().lower(),
                    timestamp,
                    timestamp,
                ),
            )

        return self.get_member(member_id)

    def get_member(self, member_id: str) -> dict | None:
        with connect_database(self.database_path) as connection:
            row = connection.execute(
                "SELECT * FROM members WHERE id = ?",
                (member_id,),
            ).fetchone()

        return dict(row) if row else None

    def get_by_discord_id(self, discord_id: str) -> dict | None:
        with connect_database(self.database_path) as connection:
            row = connection.execute(
                "SELECT * FROM members WHERE discord_id = ?",
                (discord_id,),
            ).fetchone()

        return dict(row) if row else None

    def assign_role(self, member_id: str, role_key: str) -> None:
        with connect_database(self.database_path) as connection:
            role = connection.execute(
                "SELECT id FROM roles WHERE role_key = ?",
                (role_key.strip().lower(),),
            ).fetchone()

            if role is None:
                raise ValueError(f"Unknown role: {role_key}")

            connection.execute(
                """
                INSERT INTO member_roles (member_id, role_id, assigned_at)
                VALUES (?, ?, ?)
                """,
                (member_id, role["id"], _now()),
            )

    def record_consent(
        self,
        member_id: str,
        category: str,
        policy_version: str,
    ) -> str:
        consent_id = str(uuid.uuid4())

        with connect_database(self.database_path) as connection:
            connection.execute(
                """
                INSERT INTO consent_records (
                    id, member_id, category, policy_version, granted_at
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    consent_id,
                    member_id,
                    category,
                    policy_version,
                    _now(),
                ),
            )

        return consent_id
