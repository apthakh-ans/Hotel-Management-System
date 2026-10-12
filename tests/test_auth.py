"""Tests for password hashing — no DB/network needed, pure functions."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import db  # noqa: E402


def test_hash_password_is_not_plaintext():
    hashed = db.hash_password("admin123")
    assert hashed != "admin123"
    assert "$" in hashed


def test_hash_password_is_randomly_salted():
    a = db.hash_password("same-password")
    b = db.hash_password("same-password")
    assert a != b, "two hashes of the same password must differ (random salt)"


def test_verify_password_accepts_correct_password():
    hashed = db.hash_password("correct horse battery staple")
    assert db.verify_password("correct horse battery staple", hashed) is True


def test_verify_password_rejects_wrong_password():
    hashed = db.hash_password("correct horse battery staple")
    assert db.verify_password("wrong password", hashed) is False


def test_verify_password_handles_malformed_stored_value():
    assert db.verify_password("anything", "not-a-valid-hash-format") is False


def test_default_admin_seed_hash_matches_admin123():
    # The exact value seeded into UserLogin by SQLTABLES.sql for the default admin user.
    seeded = (
        "00112233445566778899aabbccddeeff$"
        "be8187761f01504afba863a09eda647c096c7cac8cc7f0b3351fc32dba1e014e"
    )
    assert db.verify_password("admin123", seeded) is True
    assert db.verify_password("wrong", seeded) is False
