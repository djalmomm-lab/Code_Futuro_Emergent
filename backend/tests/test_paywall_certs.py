"""
Backend tests for CodeFuturo paywall & certificate endpoints.

Coverage:
  - Paywall on GET /api/paths/{slug}
  - Paywall on GET /api/lessons/{slug}
  - Paywall enforcement on POST /api/progress/complete (HTTP 402)
  - Certificates list GET /api/certificates
  - Certificate PDF GET /api/certificates/{path_slug} (Pro completed track)
  - Certificate 403 on incomplete track for Pro user
  - Certificate 402 on non-Pro user
"""
import os
import time
import uuid
import requests
import pytest

BASE_URL = os.environ.get("REACT_APP_BACKEND_URL", "https://web-replica-128.preview.emergentagent.com").rstrip("/")
API = f"{BASE_URL}/api"

PRO_EMAIL = "cert.test@codefuturo.app"
PRO_PASSWORD = "TestPro123!"

PYTHON_PATH = "python-zero"
PRO_LESSON_SLUG = "python-zero-04-lendo-seu-nome"  # order>3, pro-locked
FREE_LESSON_SLUG_PREFIX = "python-zero-01"  # order=1, free


# ---- Fixtures ----
@pytest.fixture(scope="session")
def session():
    s = requests.Session()
    s.headers.update({"Content-Type": "application/json"})
    return s


@pytest.fixture(scope="session")
def pro_token(session):
    r = session.post(f"{API}/auth/login", json={"email": PRO_EMAIL, "password": PRO_PASSWORD})
    if r.status_code != 200:
        pytest.skip(f"Pro user login failed: {r.status_code} {r.text}")
    return r.json()["token"]


@pytest.fixture(scope="session")
def free_token(session):
    email = f"TEST_free_{uuid.uuid4().hex[:8]}@codefuturo.app"
    r = session.post(f"{API}/auth/register", json={
        "email": email, "password": "FreePass123!", "name": "TEST Free User"
    })
    assert r.status_code == 200, f"Register failed: {r.status_code} {r.text}"
    data = r.json()
    return data["token"]


def auth_headers(token):
    return {"Authorization": f"Bearer {token}"}


# ---- Health / sanity ----
def test_api_root(session):
    r = session.get(f"{API}/")
    assert r.status_code == 200
    assert r.json().get("status") == "ok"


# ---- Paywall on /paths/{slug} ----
class TestPathPaywall:
    def test_free_user_sees_requires_pro_flags(self, session, free_token):
        r = session.get(f"{API}/paths/{PYTHON_PATH}", headers=auth_headers(free_token))
        assert r.status_code == 200, r.text
        data = r.json()
        assert data["free_limit"] == 3
        assert data["is_pro"] is False
        lessons = data["lessons"]
        assert len(lessons) > 3
        # order <=3 free, order >3 locked
        for le in lessons:
            if le["order"] <= 3:
                assert le["requires_pro"] is False, f"free lesson {le['slug']} marked pro"
            else:
                assert le["requires_pro"] is True, f"pro lesson {le['slug']} not marked pro"

    def test_pro_user_has_no_locked_lessons(self, session, pro_token):
        r = session.get(f"{API}/paths/{PYTHON_PATH}", headers=auth_headers(pro_token))
        assert r.status_code == 200, r.text
        data = r.json()
        assert data["is_pro"] is True
        assert data["free_limit"] == 3
        assert all(le["requires_pro"] is False for le in data["lessons"])

    def test_anonymous_user_sees_locked_lessons(self, session):
        r = session.get(f"{API}/paths/{PYTHON_PATH}")
        assert r.status_code == 200
        data = r.json()
        assert data["is_pro"] is False
        assert any(le["requires_pro"] for le in data["lessons"] if le["order"] > 3)


# ---- Paywall on /lessons/{slug} ----
class TestLessonPaywall:
    def test_free_user_gets_minimal_pro_lesson(self, session, free_token):
        r = session.get(f"{API}/lessons/{PRO_LESSON_SLUG}", headers=auth_headers(free_token))
        assert r.status_code == 200, r.text
        data = r.json()
        assert data.get("requires_pro") is True
        assert data["slug"] == PRO_LESSON_SLUG
        assert "tests" not in data, "free user should NOT receive `tests`"
        assert "starter_code" not in data, "free user should NOT receive `starter_code`"
        assert "content" not in data or not data.get("content")
        assert data.get("free_limit") == 3

    def test_pro_user_gets_full_lesson(self, session, pro_token):
        r = session.get(f"{API}/lessons/{PRO_LESSON_SLUG}", headers=auth_headers(pro_token))
        assert r.status_code == 200, r.text
        data = r.json()
        assert data.get("requires_pro") is False
        # Full lesson should include at least one of these rich fields
        assert any(k in data for k in ("tests", "starter_code", "content", "instructions")), \
            f"full lesson missing rich fields: keys={list(data.keys())}"

    def test_free_lesson_accessible_to_everyone(self, session, free_token):
        # find the first free lesson to be robust against slug naming
        r = session.get(f"{API}/paths/{PYTHON_PATH}")
        lessons = r.json()["lessons"]
        free_lesson = next(le for le in lessons if le["order"] == 1)
        r2 = session.get(f"{API}/lessons/{free_lesson['slug']}", headers=auth_headers(free_token))
        assert r2.status_code == 200
        assert r2.json().get("requires_pro") is False


# ---- Paywall on POST /progress/complete ----
class TestCompletePaywall:
    def test_free_user_blocked_on_pro_lesson(self, session, free_token):
        r = session.post(
            f"{API}/progress/complete",
            headers=auth_headers(free_token),
            json={"lesson_slug": PRO_LESSON_SLUG, "path_slug": PYTHON_PATH},
        )
        assert r.status_code == 402, f"expected 402, got {r.status_code}: {r.text}"

    def test_free_user_allowed_on_free_lesson(self, session, free_token):
        # first free lesson
        r = session.get(f"{API}/paths/{PYTHON_PATH}")
        free_lesson = next(le for le in r.json()["lessons"] if le["order"] == 1)
        r2 = session.post(
            f"{API}/progress/complete",
            headers=auth_headers(free_token),
            json={"lesson_slug": free_lesson["slug"], "path_slug": PYTHON_PATH},
        )
        assert r2.status_code == 200, r2.text


# ---- Certificates ----
class TestCertificates:
    def test_list_certificates_pro_user(self, session, pro_token):
        r = session.get(f"{API}/certificates", headers=auth_headers(pro_token))
        assert r.status_code == 200, r.text
        data = r.json()
        assert data.get("is_pro") is True
        items = data.get("items", [])
        assert len(items) > 0
        py = next((i for i in items if i["path_slug"] == PYTHON_PATH), None)
        assert py is not None, "python-zero not in certificates list"
        assert py["is_complete"] is True
        assert py["completed"] == py["total"]
        assert py["total"] > 0

    def test_list_certificates_free_user(self, session, free_token):
        r = session.get(f"{API}/certificates", headers=auth_headers(free_token))
        assert r.status_code == 200
        data = r.json()
        assert data.get("is_pro") is False
        # Should still list tracks with completion counts
        assert isinstance(data.get("items"), list) and len(data["items"]) > 0

    def test_list_certificates_requires_auth(self, session):
        r = session.get(f"{API}/certificates")
        assert r.status_code in (401, 403)

    def test_download_certificate_pro_completed(self, session, pro_token):
        r = session.get(
            f"{API}/certificates/{PYTHON_PATH}",
            headers=auth_headers(pro_token),
        )
        assert r.status_code == 200, f"got {r.status_code}: {r.text[:300]}"
        assert r.headers.get("content-type", "").startswith("application/pdf"), \
            f"unexpected content-type: {r.headers.get('content-type')}"
        assert r.content[:4] == b"%PDF", f"body does not start with %PDF: {r.content[:10]!r}"
        assert len(r.content) > 1000  # reasonable pdf size
        cd = r.headers.get("content-disposition", "")
        assert "attachment" in cd and ".pdf" in cd

    def test_download_certificate_pro_incomplete_returns_403(self, session, pro_token):
        # javascript track is NOT completed for the Pro user
        r = session.get(
            f"{API}/certificates/javascript",
            headers=auth_headers(pro_token),
        )
        assert r.status_code == 403, f"expected 403 got {r.status_code}: {r.text}"
        body = r.json()
        detail = body.get("detail", "")
        assert "Trilha incompleta" in detail or "incompleta" in detail.lower() or "/" in detail

    def test_download_certificate_free_user_returns_402(self, session, free_token):
        r = session.get(
            f"{API}/certificates/{PYTHON_PATH}",
            headers=auth_headers(free_token),
        )
        assert r.status_code == 402, f"expected 402 got {r.status_code}: {r.text}"

    def test_download_certificate_unknown_track(self, session, pro_token):
        r = session.get(
            f"{API}/certificates/nonexistent-track",
            headers=auth_headers(pro_token),
        )
        # Pro check happens before path lookup; then path lookup returns 404
        assert r.status_code in (404, 403, 402), f"got {r.status_code}: {r.text}"
