from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.models.repair import Repair
from backend.app.schemas.repair import RepairCreate, RepairRead, RepairUpdate
from backend.app.core.database import get_db

router = APIRouter(prefix="/api/repairs", tags=["Repairs"])

@router.get("/", response_model=list[RepairRead])
def list_repairs(db: Session = Depends(get_db)):
    return db.query(Repair).all()

@router.post("/", response_model=RepairRead)
def create_repair(repair: RepairCreate, db: Session = Depends(get_db)):
    db_repair = Repair(**repair.dict())
    db.add(db_repair)
    db.commit()
    db.refresh(db_repair)
    return db_repair

@router.put("/{repair_id}", response_model=RepairRead)
def update_repair(repair_id: int, repair: RepairUpdate, db: Session = Depends(get_db)):
    db_repair = db.query(Repair).get(repair_id)
    if not db_repair:
        raise HTTPException(status_code=404, detail="Repair not found")
    for key, value in repair.dict(exclude_unset=True).items():
        setattr(db_repair, key, value)
    db.commit()
    db.refresh(db_repair)
    return db_repair

@router.delete("/{repair_id}")
def delete_repair(repair_id: int, db: Session = Depends(get_db)):
    db_repair = db.query(Repair).get(repair_id)
    if not db_repair:
        raise HTTPException(status_code=404, detail="Repair not found")
    db.delete(db_repair)
    db.commit()
    return {"ok": True}
