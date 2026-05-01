"""CodeFuturo Escolas — minimal B2B classroom layer.

Any authenticated user can create a class, becoming its owner (teacher).
Students join via a 6-character invite code. Teacher gets a dashboard with
each student's per-track progress.

Models are intentionally lean — no separate role table. Membership is stored
in `class_memberships` with role=teacher|student.
"""
from __future__ import annotations
import secrets
import string
import uuid
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field


def _new_id() -> str:
    return str(uuid.uuid4())


def _gen_invite_code() -> str:
    alphabet = string.ascii_uppercase + string.digits
    # avoid look-alikes
    alphabet = alphabet.replace("O", "").replace("0", "").replace("I", "").replace("1", "")
    return "".join(secrets.choice(alphabet) for _ in range(6))


def _slugify(name: str) -> str:
    keep = []
    for ch in name.lower():
        if ch.isalnum():
            keep.append(ch)
        elif ch in " -_":
            keep.append("-")
    base = "".join(keep).strip("-") or "turma"
    return base[:40]


class CreateClassIn(BaseModel):
    name: str = Field(min_length=2, max_length=80)
    school_name: Optional[str] = Field(default=None, max_length=120)
    seats: int = Field(default=30, ge=1, le=500)


class JoinClassIn(BaseModel):
    invite_code: str = Field(min_length=4, max_length=12)


def build_router(db, current_user_dep):
    router = APIRouter(prefix="/api/classes", tags=["classes"])

    async def _serialize_class(c: dict, *, role: str, total_members: int) -> dict:
        return {
            "id": c["id"],
            "slug": c["slug"],
            "name": c["name"],
            "school_name": c.get("school_name"),
            "seats": c.get("seats", 30),
            "invite_code": c["invite_code"] if role == "teacher" else None,
            "owner_id": c["owner_id"],
            "created_at": c.get("created_at"),
            "role": role,
            "total_members": total_members,
        }

    @router.post("")
    async def create_class(data: CreateClassIn, user=Depends(current_user_dep)):
        slug = _slugify(data.name) + "-" + secrets.token_hex(2)
        invite_code = _gen_invite_code()
        # Ensure invite_code unique
        while await db.classes.find_one({"invite_code": invite_code}):
            invite_code = _gen_invite_code()

        now = datetime.utcnow().isoformat()
        doc = {
            "id": _new_id(),
            "slug": slug,
            "name": data.name,
            "school_name": data.school_name,
            "seats": data.seats,
            "owner_id": user["id"],
            "invite_code": invite_code,
            "created_at": now,
        }
        await db.classes.insert_one(doc)
        # Insert teacher membership
        await db.class_memberships.insert_one({
            "id": _new_id(),
            "class_id": doc["id"],
            "user_id": user["id"],
            "role": "teacher",
            "joined_at": now,
        })
        return await _serialize_class(doc, role="teacher", total_members=1)

    @router.get("/mine")
    async def my_classes(user=Depends(current_user_dep)):
        memberships = await db.class_memberships.find(
            {"user_id": user["id"]}, {"_id": 0}
        ).to_list(200)
        items = []
        for m in memberships:
            c = await db.classes.find_one({"id": m["class_id"]}, {"_id": 0})
            if not c:
                continue
            total = await db.class_memberships.count_documents({"class_id": c["id"]})
            items.append(await _serialize_class(c, role=m["role"], total_members=total))
        # Most recent first
        items.sort(key=lambda x: x.get("created_at") or "", reverse=True)
        return {"items": items}

    @router.post("/join")
    async def join_class(data: JoinClassIn, user=Depends(current_user_dep)):
        code = data.invite_code.strip().upper()
        c = await db.classes.find_one({"invite_code": code}, {"_id": 0})
        if not c:
            raise HTTPException(404, "Código de convite inválido")
        existing = await db.class_memberships.find_one(
            {"class_id": c["id"], "user_id": user["id"]}
        )
        if existing:
            return {"already_member": True, "class_id": c["id"], "slug": c["slug"]}

        # Seat enforcement (excluding teacher seat)
        student_count = await db.class_memberships.count_documents(
            {"class_id": c["id"], "role": "student"}
        )
        if student_count >= int(c.get("seats", 30)):
            raise HTTPException(409, "Turma lotada — peça mais vagas ao professor.")

        await db.class_memberships.insert_one({
            "id": _new_id(),
            "class_id": c["id"],
            "user_id": user["id"],
            "role": "student",
            "joined_at": datetime.utcnow().isoformat(),
        })
        return {"already_member": False, "class_id": c["id"], "slug": c["slug"]}

    async def _membership_of(class_id: str, user_id: str) -> Optional[dict]:
        return await db.class_memberships.find_one(
            {"class_id": class_id, "user_id": user_id}, {"_id": 0}
        )

    async def _student_progress_summary(user_id: str) -> dict:
        # Aggregate completion across all paths
        paths = await db.paths.find({}, {"_id": 0, "slug": 1, "name": 1, "color": 1}).to_list(50)
        per_path = []
        total_completed = 0
        total_lessons = 0
        for p in paths:
            lessons = await db.lessons.find({"path_slug": p["slug"]}, {"_id": 0, "slug": 1}).to_list(500)
            slugs = [le["slug"] for le in lessons]
            count = await db.lesson_completions.count_documents({
                "user_id": user_id, "lesson_slug": {"$in": slugs},
            }) if slugs else 0
            per_path.append({
                "path_slug": p["slug"],
                "path_name": p["name"],
                "color": p.get("color"),
                "completed": count,
                "total": len(slugs),
            })
            total_completed += count
            total_lessons += len(slugs)
        prog = await db.progress.find_one({"user_id": user_id}, {"_id": 0}) or {}
        return {
            "xp_total": int(prog.get("xp_total", 0)),
            "streak": int(prog.get("streak", 0)),
            "completed": total_completed,
            "total": total_lessons,
            "per_path": per_path,
        }

    @router.get("/{class_id}")
    async def class_detail(class_id: str, user=Depends(current_user_dep)):
        c = await db.classes.find_one({"id": class_id}, {"_id": 0})
        if not c:
            raise HTTPException(404, "Turma não encontrada")
        my_m = await _membership_of(class_id, user["id"])
        if not my_m:
            raise HTTPException(403, "Você não faz parte desta turma")

        is_teacher = my_m["role"] == "teacher"
        memberships = await db.class_memberships.find(
            {"class_id": class_id}, {"_id": 0}
        ).to_list(500)

        # For students: hide other students' progress; expose only the class basics.
        students = []
        if is_teacher:
            for m in memberships:
                if m["role"] != "student":
                    continue
                u = await db.users.find_one({"id": m["user_id"]}, {"_id": 0})
                if not u:
                    continue
                summary = await _student_progress_summary(u["id"])
                students.append({
                    "user_id": u["id"],
                    "name": u.get("name"),
                    "email": u.get("email"),
                    "is_pro": bool(u.get("is_pro")),
                    "joined_at": m["joined_at"],
                    **summary,
                })

        return {
            "class": await _serialize_class(c, role=my_m["role"], total_members=len(memberships)),
            "is_teacher": is_teacher,
            "students": students,
        }

    @router.delete("/{class_id}/students/{user_id}")
    async def remove_student(class_id: str, user_id: str, user=Depends(current_user_dep)):
        c = await db.classes.find_one({"id": class_id}, {"_id": 0, "owner_id": 1})
        if not c:
            raise HTTPException(404, "Turma não encontrada")
        if c["owner_id"] != user["id"]:
            raise HTTPException(403, "Apenas o professor pode remover alunos")
        if user_id == user["id"]:
            raise HTTPException(400, "Use a exclusão da turma para sair como professor")
        res = await db.class_memberships.delete_one({
            "class_id": class_id, "user_id": user_id, "role": "student",
        })
        if res.deleted_count == 0:
            raise HTTPException(404, "Aluno não encontrado nessa turma")
        return {"ok": True, "removed": user_id}

    @router.delete("/{class_id}")
    async def delete_class(class_id: str, user=Depends(current_user_dep)):
        c = await db.classes.find_one({"id": class_id}, {"_id": 0, "owner_id": 1})
        if not c:
            raise HTTPException(404, "Turma não encontrada")
        if c["owner_id"] != user["id"]:
            raise HTTPException(403, "Apenas o professor pode excluir a turma")
        await db.classes.delete_one({"id": class_id})
        await db.class_memberships.delete_many({"class_id": class_id})
        return {"ok": True}

    return router
