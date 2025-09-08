from main.models.service import Service
from main.schemas.service import ServiceRequest
from main.database.utils import db_dependency
from main.database.auth import user_dependency
from fastapi import APIRouter, HTTPException, Path

router = APIRouter(
    prefix="/service",
    tags=["service"]
)

@router.get("/")
async def get_service(db: db_dependency, user: user_dependency):
    try:
        if user is None:
            raise HTTPException(status_code=401, detail="Authentication failed...")
        
        return db.query(Service).filter(Service.user_id == user.id).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/{service_id}")
async def get_service_by_id(db: db_dependency, user: user_dependency, service_id: int = Path(gt=0)):
    try:
        if user is None:
            raise HTTPException(status_code=401, detail="Authentication failed...")

        service_model = db.query(Service).filter(Service.id == service_id).filter(Service.user_id == user.id).first()

        if service_model is None:
            raise HTTPException(status_code=404, detail="Service not found...")

        return service_model
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.post("/")
async def add_service(service_request: ServiceRequest, db: db_dependency, user: user_dependency):
    try:
        if user is None:
            raise HTTPException(status_code=401, detail="Authentication failed...")

        service_model = Service(
            **service_request.dict(), 
            user_id=user.id
        )

        db.add(service_model)
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.put("/{service_id}")
async def change_service(service_request: ServiceRequest, db: db_dependency, user: user_dependency, service_id: int = Path(gt=0)):
    try:
        if user is None:
            raise HTTPException(status_code=401, detail="Authentification failed...")

        service_model = db.query(Service).filter(Service.id == service_id).filter(Service.user_id == user.id).first()

        if service_model is None:
            raise HTTPException(status_code=404, detail="Service not found...")

        service_model.title = service_request.title
        service_model.description = service_request.description
        service_model.importance = service_request.importance

        db.add(service_model)
        db.commit()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.delete("/{service_id}")
async def delete_service(db: db_dependency, user: user_dependency, service_id: int = Path(gt=0)):
    try:
        if user is None:
            raise HTTPException(status_code=401, detail="Authentication failed...")

        service_model = db.query(Service).filter(Service.id == service_id).filter(Service.user_id == user.id).first()

        if service_model is None:
            raise HTTPException(status_code=404, detail="Service not found...")

        db.query(Service).filter(Service.id == service_id).filter(Service.user_id == user.id).delete()
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")