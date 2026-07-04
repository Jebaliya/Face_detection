from fastapi import APIRouter

from ..face_service import face_service

router = APIRouter(prefix="/api", tags=["attendance"])


@router.get("/attendance")
async def get_attendance():
    return {"records": face_service.get_todays_attendance()}


@router.delete("/attendance")
async def clear_attendance():
    face_service.clear_attendance()
    return {"status": "cleared"}
