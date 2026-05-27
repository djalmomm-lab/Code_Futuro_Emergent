"""
Tests for public certificate verification endpoint.
- GET /api/certificates/{path_slug} by Pro user persists a cert and returns the PDF.
- GET /api/verify/{cert_id} returns public cert info for valid ids; 404 for invalid.
"""
import os
import hashlib
import requests
import pytest

BASE_URL = os.environ.get("REACT_APP_BACKEND_URL", "https://web-replica-128.preview.emergentagent.com").rstrip("/")
API = f"{BASE_URL}/api"

PRO_EMAIL = "cert.test@codefuturo.app"
PRO_PASSWORD = "TestPro123!"
PATH_SLUG = "python-zero"


@pytest.fixture(scope="module")
def session():
    s = requests.Session()
    s.headers.update({"Content-Type": "application/json"})
    return s


@pytest.fixture(scope="module")
def pro_token(session):
    r = session.post(f"{API}/auth/login", json={"email": PRO_EMAIL, "password": PRO_PASSWORD})
    if r.status_code != 200:
        pytest.skip(f"Pro login failed: {r.status_code} {r.text}")
    return r.json()["token"]


@pytest.fixture(scope="module")
def pro_user_id(session, pro_token):
    r = session.get(f"{API}/auth/me", headers={"Authorization": f"Bearer {pro_token}"})
    assert r.status_code == 200, r.text
    body = r.json()
    # supports both {id:..} or {user:{id:..}}
    if "id" in body:
        return body["id"]
    return body["user"]["id"]


@pytest.fixture(scope="module")
def persisted_cert_id(session, pro_token, pro_user_id):
    # Hit cert download to trigger persistence
    r = session.get(
        f"{API}/certificates/{PATH_SLUG}",
        headers={"Authorization": f"Bearer {pro_token}"},
    )
    assert r.status_code == 200, f"certificate download failed: {r.status_code} {r.text[:300]}"
    assert r.headers.get("content-type", "").startswith("application/pdf")
    # Deterministic cert id
    return "CF-" + hashlib.sha1(f"{pro_user_id}:{PATH_SLUG}".encode()).hexdigest()[:12].upper()


class TestVerifyEndpoint:
    def test_valid_cert_returns_public_fields(self, session, persisted_cert_id):
        r = session.get(f"{API}/verify/{persisted_cert_id}")
        assert r.status_code == 200, f"expected 200, got {r.status_code}: {r.text}"
        data = r.json()
        assert data.get("valid") is True
        assert data.get("cert_id") == persisted_cert_id
        assert data.get("path_slug") == PATH_SLUG
        # Required public fields per spec
        for field in ("student_name", "track_name", "total_lessons", "xp_earned", "issued_at"):
            assert field in data, f"missing field '{field}' in verify response: {list(data.keys())}"
        assert isinstance(data["total_lessons"], int) and data["total_lessons"] > 0
        assert isinstance(data["xp_earned"], int) and data["xp_earned"] >= 0
        assert isinstance(data["student_name"], str) and data["student_name"]
        assert isinstance(data["track_name"], str) and data["track_name"]
        # Leaks: _id / user_id must NOT be exposed
        assert "_id" not in data
        assert "user_id" not in data

    def test_response_keys_are_strict_allow_list(self, session, persisted_cert_id):
        """Allow-list projection: response keys must be EXACTLY this set."""
        r = session.get(f"{API}/verify/{persisted_cert_id}")
        assert r.status_code == 200, r.text
        data = r.json()
        expected = {"valid", "cert_id", "student_name", "track_name", "path_slug", "total_lessons", "xp_earned", "issued_at"}
        actual = set(data.keys())
        assert actual == expected, f"expected exactly {expected}, got {actual} (extras={actual - expected}, missing={expected - actual})"

    def test_invalid_cert_returns_404(self, session):
        r = session.get(f"{API}/verify/CF-DEADBEEF1234")
        assert r.status_code == 404, f"expected 404, got {r.status_code}: {r.text}"
        body = r.json()
        assert "detail" in body
        assert len(body["detail"]) > 0

    def test_verify_is_public_no_auth_required(self, session, persisted_cert_id):
        # Explicitly do NOT send Authorization header
        s2 = requests.Session()
        r = s2.get(f"{API}/verify/{persisted_cert_id}")
        assert r.status_code == 200
        assert r.json().get("valid") is True
