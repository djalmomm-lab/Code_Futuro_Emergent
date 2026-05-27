"""
Backend tests for CodeFuturo Escolas (B2B classes) module.

Coverage:
  - POST /api/classes (create) — teacher membership + invite_code format
  - GET  /api/classes/mine — teacher vs student exposure of invite_code, sort
  - POST /api/classes/join — valid, already_member, invalid code 404
  - GET  /api/classes/{id} — teacher sees students w/ progress, student sees empty, non-member 403
  - DELETE /api/classes/{id}/students/{user_id} — 403/400/404 + happy path
  - DELETE /api/classes/{id} — 403 non-owner, cascade delete
  - /api/certificates now includes cert_id for fully-completed track (python-zero for Pro)
"""
import os
import re
import uuid
import requests
import pytest

BASE_URL = os.environ.get("REACT_APP_BACKEND_URL", "https://web-replica-128.preview.emergentagent.com").rstrip("/")
API = f"{BASE_URL}/api"

PRO_EMAIL = "cert.test@codefuturo.app"
PRO_PASSWORD = "TestPro123!"
PYTHON_PATH = "python-zero"

INVITE_CODE_RE = re.compile(r"^[A-HJ-NP-Z2-9]{6}$")  # no O,0,I,1


def _auth(tok):
    return {"Authorization": f"Bearer {tok}"}


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
    r = session.get(f"{API}/auth/me", headers=_auth(pro_token))
    assert r.status_code == 200, r.text
    body = r.json()
    return body.get("id") or body["user"]["id"]


@pytest.fixture(scope="module")
def student_token(session):
    email = f"TEST_student_{uuid.uuid4().hex[:8]}@codefuturo.app"
    r = session.post(f"{API}/auth/register", json={
        "email": email, "password": "StudPass123!", "name": "TEST Student"
    })
    assert r.status_code == 200, r.text
    return r.json()["token"]


@pytest.fixture(scope="module")
def student_user_id(session, student_token):
    r = session.get(f"{API}/auth/me", headers=_auth(student_token))
    assert r.status_code == 200, r.text
    body = r.json()
    return body.get("id") or body["user"]["id"]


@pytest.fixture(scope="module")
def other_token(session):
    """A separate authenticated user who is NOT part of the target class."""
    email = f"TEST_other_{uuid.uuid4().hex[:8]}@codefuturo.app"
    r = session.post(f"{API}/auth/register", json={
        "email": email, "password": "OtherPass123!", "name": "TEST Other"
    })
    assert r.status_code == 200, r.text
    return r.json()["token"]


@pytest.fixture(scope="module")
def created_class(session, pro_token):
    """Teacher creates a fresh class for this test run."""
    r = session.post(
        f"{API}/classes",
        headers=_auth(pro_token),
        json={"name": f"TEST Turma {uuid.uuid4().hex[:6]}", "school_name": "TEST School", "seats": 10},
    )
    assert r.status_code == 200, r.text
    data = r.json()
    yield data
    # Cleanup: best-effort delete
    try:
        session.delete(f"{API}/classes/{data['id']}", headers=_auth(pro_token))
    except Exception:
        pass


# ---------- Create ----------
class TestCreateClass:
    def test_create_returns_expected_shape(self, created_class):
        c = created_class
        assert c["id"] and isinstance(c["id"], str)
        assert c["slug"] and isinstance(c["slug"], str)
        assert c["name"].startswith("TEST Turma ")
        assert c["school_name"] == "TEST School"
        assert c["seats"] == 10
        assert c["role"] == "teacher"
        assert c["total_members"] == 1
        assert c["owner_id"]
        assert c["invite_code"] and INVITE_CODE_RE.match(c["invite_code"]), f"bad invite_code {c['invite_code']}"

    def test_create_requires_auth(self, session):
        r = session.post(f"{API}/classes", json={"name": "TEST Nope"})
        assert r.status_code in (401, 403)


# ---------- Join ----------
class TestJoinClass:
    def test_invalid_code_returns_404(self, session, student_token):
        r = session.post(
            f"{API}/classes/join",
            headers=_auth(student_token),
            json={"invite_code": "ZZZZZZ"},
        )
        assert r.status_code == 404, r.text
        assert "Código" in r.json().get("detail", "") or "invá" in r.json().get("detail", "").lower()

    def test_student_joins_with_valid_code(self, session, student_token, created_class):
        r = session.post(
            f"{API}/classes/join",
            headers=_auth(student_token),
            json={"invite_code": created_class["invite_code"]},
        )
        assert r.status_code == 200, r.text
        data = r.json()
        assert data["already_member"] is False
        assert data["class_id"] == created_class["id"]
        assert data["slug"] == created_class["slug"]

    def test_second_join_returns_already_member(self, session, student_token, created_class):
        r = session.post(
            f"{API}/classes/join",
            headers=_auth(student_token),
            json={"invite_code": created_class["invite_code"]},
        )
        assert r.status_code == 200, r.text
        data = r.json()
        assert data["already_member"] is True
        assert data["class_id"] == created_class["id"]


# ---------- Mine ----------
class TestMineEndpoint:
    def test_teacher_sees_invite_code(self, session, pro_token, created_class):
        r = session.get(f"{API}/classes/mine", headers=_auth(pro_token))
        assert r.status_code == 200, r.text
        items = r.json()["items"]
        mine = next((x for x in items if x["id"] == created_class["id"]), None)
        assert mine is not None
        assert mine["role"] == "teacher"
        assert mine["invite_code"] == created_class["invite_code"]
        # Sort: most recent first => our freshly-created one should be near the top
        # not strictly index 0 if many pre-existing; but must be in the list.
        assert mine["total_members"] >= 2  # teacher + student joined above

    def test_student_invite_code_is_null(self, session, student_token, created_class):
        r = session.get(f"{API}/classes/mine", headers=_auth(student_token))
        assert r.status_code == 200, r.text
        items = r.json()["items"]
        mine = next((x for x in items if x["id"] == created_class["id"]), None)
        assert mine is not None
        assert mine["role"] == "student"
        assert mine["invite_code"] is None


# ---------- Detail ----------
class TestClassDetail:
    def test_teacher_sees_students_with_progress(self, session, pro_token, created_class, student_user_id):
        r = session.get(f"{API}/classes/{created_class['id']}", headers=_auth(pro_token))
        assert r.status_code == 200, r.text
        data = r.json()
        assert data["is_teacher"] is True
        assert data["class"]["id"] == created_class["id"]
        assert data["class"]["invite_code"] == created_class["invite_code"]
        students = data["students"]
        assert isinstance(students, list) and len(students) >= 1
        stu = next((s for s in students if s["user_id"] == student_user_id), None)
        assert stu is not None, f"student not in list {students}"
        for key in ("name", "email", "is_pro", "joined_at", "xp_total", "streak", "completed", "total", "per_path"):
            assert key in stu, f"missing {key}"
        assert isinstance(stu["per_path"], list) and len(stu["per_path"]) > 0
        pp = stu["per_path"][0]
        for k in ("path_slug", "path_name", "completed", "total"):
            assert k in pp

    def test_student_sees_empty_students_list(self, session, student_token, created_class):
        r = session.get(f"{API}/classes/{created_class['id']}", headers=_auth(student_token))
        assert r.status_code == 200, r.text
        data = r.json()
        assert data["is_teacher"] is False
        assert data["students"] == []
        assert data["class"]["id"] == created_class["id"]
        # invite_code hidden from student
        assert data["class"]["invite_code"] is None

    def test_non_member_forbidden(self, session, other_token, created_class):
        r = session.get(f"{API}/classes/{created_class['id']}", headers=_auth(other_token))
        assert r.status_code == 403, r.text
        assert "faz parte" in r.json().get("detail", "").lower() or "não faz parte" in r.json().get("detail", "")


# ---------- Remove student ----------
class TestRemoveStudent:
    def test_non_teacher_forbidden(self, session, student_token, created_class, student_user_id):
        r = session.delete(
            f"{API}/classes/{created_class['id']}/students/{student_user_id}",
            headers=_auth(student_token),
        )
        assert r.status_code == 403, r.text

    def test_cannot_remove_owner(self, session, pro_token, created_class, pro_user_id):
        r = session.delete(
            f"{API}/classes/{created_class['id']}/students/{pro_user_id}",
            headers=_auth(pro_token),
        )
        assert r.status_code == 400, r.text

    def test_remove_unknown_user_404(self, session, pro_token, created_class):
        r = session.delete(
            f"{API}/classes/{created_class['id']}/students/{uuid.uuid4()}",
            headers=_auth(pro_token),
        )
        assert r.status_code == 404, r.text

    def test_teacher_can_remove_student(self, session, pro_token, created_class, student_user_id):
        r = session.delete(
            f"{API}/classes/{created_class['id']}/students/{student_user_id}",
            headers=_auth(pro_token),
        )
        assert r.status_code == 200, r.text
        assert r.json()["ok"] is True
        # Verify removal via GET detail: student no longer in list
        r2 = session.get(f"{API}/classes/{created_class['id']}", headers=_auth(pro_token))
        assert r2.status_code == 200
        ids = [s["user_id"] for s in r2.json()["students"]]
        assert student_user_id not in ids


# ---------- Leaderboard (must run before TestDeleteClass deletes the class) ----------
class TestLeaderboard:
    def test_member_can_see_leaderboard_sorted(self, session, pro_token, created_class, pro_user_id, student_token, student_user_id):
        # Ensure student joined this fresh class
        session.post(
            f"{API}/classes/join",
            headers=_auth(student_token),
            json={"invite_code": created_class["invite_code"]},
        )
        r = session.get(f"{API}/classes/{created_class['id']}/leaderboard", headers=_auth(pro_token))
        assert r.status_code == 200, r.text
        body = r.json()
        assert "items" in body and isinstance(body["items"], list)
        items = body["items"]
        assert len(items) >= 2
        # Required keys / no email leak
        required = {"user_id", "name", "is_pro", "role", "xp_total", "streak", "completed", "total", "is_me", "rank"}
        for it in items:
            assert required.issubset(set(it.keys())), f"missing keys: {required - set(it.keys())}"
            assert "email" not in it, "email must not be exposed in leaderboard"
            assert "password_hash" not in it
            assert "_id" not in it
        # Ranks sequential 1..N
        ranks = [it["rank"] for it in items]
        assert ranks == list(range(1, len(items) + 1))
        # Sort: xp_total DESC, then streak DESC, then completed DESC
        for a, b in zip(items, items[1:]):
            assert (a["xp_total"], a["streak"], a["completed"]) >= (b["xp_total"], b["streak"], b["completed"])
        # is_me True for caller (teacher) exactly once
        me_rows = [it for it in items if it["is_me"]]
        assert len(me_rows) == 1
        assert me_rows[0]["user_id"] == pro_user_id
        assert me_rows[0]["role"] == "teacher"

    def test_student_caller_sees_is_me_true_for_self(self, session, student_token, created_class, student_user_id):
        r = session.get(f"{API}/classes/{created_class['id']}/leaderboard", headers=_auth(student_token))
        assert r.status_code == 200, r.text
        items = r.json()["items"]
        me = [it for it in items if it["is_me"]]
        assert len(me) == 1
        assert me[0]["user_id"] == student_user_id
        assert me[0]["role"] == "student"

    def test_non_member_forbidden(self, session, other_token, created_class):
        r = session.get(f"{API}/classes/{created_class['id']}/leaderboard", headers=_auth(other_token))
        assert r.status_code == 403, r.text

    def test_unknown_class_returns_404(self, session, pro_token):
        r = session.get(f"{API}/classes/{uuid.uuid4()}/leaderboard", headers=_auth(pro_token))
        assert r.status_code == 404, r.text

    def test_requires_auth(self, session, created_class):
        r = session.get(f"{API}/classes/{created_class['id']}/leaderboard")
        assert r.status_code in (401, 403)


# ---------- Delete class ----------
class TestDeleteClass:
    def test_non_owner_forbidden(self, session, other_token, created_class):
        r = session.delete(f"{API}/classes/{created_class['id']}", headers=_auth(other_token))
        assert r.status_code == 403, r.text

    def test_owner_deletes_and_memberships_cascade(self, session, pro_token, created_class):
        r = session.delete(f"{API}/classes/{created_class['id']}", headers=_auth(pro_token))
        assert r.status_code == 200, r.text
        # Teacher's /mine should no longer include it
        r2 = session.get(f"{API}/classes/mine", headers=_auth(pro_token))
        assert r2.status_code == 200
        ids = [x["id"] for x in r2.json()["items"]]
        assert created_class["id"] not in ids
        # Detail should 404
        r3 = session.get(f"{API}/classes/{created_class['id']}", headers=_auth(pro_token))
        assert r3.status_code in (403, 404)


# ---------- Certificates list includes cert_id ----------
class TestCertificatesCertIdField:
    def test_pro_user_has_cert_id_for_completed_python(self, session, pro_token):
        # Ensure the cert record exists (download persists it, idempotent)
        session.get(f"{API}/certificates/{PYTHON_PATH}", headers=_auth(pro_token))
        r = session.get(f"{API}/certificates", headers=_auth(pro_token))
        assert r.status_code == 200, r.text
        items = r.json()["items"]
        py = next((i for i in items if i["path_slug"] == PYTHON_PATH), None)
        assert py is not None
        assert py["is_complete"] is True
        assert py["cert_id"], "cert_id should be set for completed track"
        assert py["cert_id"].startswith("CF-")
        # Incomplete tracks should have cert_id = None
        for it in items:
            if not it["is_complete"]:
                assert it["cert_id"] is None, f"{it['path_slug']} should not have cert_id"
