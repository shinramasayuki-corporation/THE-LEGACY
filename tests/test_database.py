import sqlite3

import pytest

from legacy.database import initialize_database, MemberRepository

def create_repository(tmp_path):
    database_path = tmp_path / "test.db"
    initialize_database(database_path)
    return MemberRepository(database_path)

def test_database_initializes_roles(tmp_path):
    repository = create_repository(tmp_path)

    with sqlite3.connect(repository.database_path) as connection:
        roles = connection.execute(
            "SELECT role_key FROM roles ORDER BY role_key"
        ).fetchall()

    assert len(roles) == 5

def test_create_and_retrieve_member(tmp_path):
    repository = create_repository(tmp_path)

    member = repository.create_member(
        username="TestMember",
        discord_id="123456789",
        preferred_language="fr",
    )

    assert member["username"] == "TestMember"
    assert member["discord_id"] == "123456789"
    assert member["account_status"] == "active"
    assert repository.get_member(member["id"])["id"] == member["id"]

def test_find_member_by_discord_id(tmp_path):
    repository = create_repository(tmp_path)
    member = repository.create_member("TestMember", "987654321")

    found = repository.get_by_discord_id("987654321")

    assert found["id"] == member["id"]

def test_duplicate_discord_id_is_rejected(tmp_path):
    repository = create_repository(tmp_path)
    repository.create_member("First", "111222333")

    with pytest.raises(sqlite3.IntegrityError):
        repository.create_member("Second", "111222333")

def test_empty_username_is_rejected(tmp_path):
    repository = create_repository(tmp_path)

    with pytest.raises(ValueError):
        repository.create_member("   ")

def test_member_can_receive_role(tmp_path):
    repository = create_repository(tmp_path)
    member = repository.create_member("TestMember")

    repository.assign_role(member["id"], "member")

    with sqlite3.connect(repository.database_path) as connection:
        result = connection.execute(
            """
            SELECT roles.role_key
            FROM member_roles
            JOIN roles ON roles.id = member_roles.role_id
            WHERE member_roles.member_id = ?
            """,
            (member["id"],),
        ).fetchone()

    assert result[0] == "member"

def test_member_consent_can_be_recorded(tmp_path):
    repository = create_repository(tmp_path)
    member = repository.create_member("TestMember")

    consent_id = repository.record_consent(
        member["id"],
        "privacy_policy",
        "1.0",
    )

    assert consent_id
