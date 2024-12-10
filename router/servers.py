
from fastapi import APIRouter,Depends,status,HTTPException
import schemas
from database import SessionLocal,engine
from sqlalchemy.orm import Session
import models

router = APIRouter(
    tags=['Servers'],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/server_addition")
async def server_addition(server_data: schemas.server_info_schema, db: Session = Depends(get_db) ):
    new_server_info = models.serverinfo_model(os_name=server_data.os_name, ip=server_data.ip)
    db.add(new_server_info)
    db.commit()
    db.refresh(new_server_info)
    return "os_eol_updated for {}".format(server_data.ip)

@router.get("/list_servers", response_model=list[schemas.reponse_server_info])
async def list_servers(db: Session = Depends(get_db)):
    get_ip=db.query(models.serverinfo_model).filter(models.serverinfo_model.ip).all()
    return get_ip


@router.delete("/server_removal")
def delete_eol(server_ip_delete: schemas.server_ip_delete, db: Session = Depends(get_db), response_model=list[schemas.server_info_schema]):
    del_ip =  db.query(models.serverinfo_model).filter(models.serverinfo_model.id == server_ip_delete.id).first()
    if not del_ip:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ip not found") 
    db.delete(del_ip)
    db.commit()
    return del_ip



