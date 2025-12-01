import os
from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import List
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError

from database import engine, SessionLocal, get_db # Import from new database.py
from models import Base, UserManifesto # Import Base and UserManifesto from new models.py

# --- Pydantic Models for Request/Response ---
class ManifestoBase(BaseModel):
    title: str
    content: str
    author: str = "Anonymous"

class ManifestoCreate(ManifestoBase):
    pass

class ManifestoResponse(ManifestoBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# --- FastAPI App ---
app = FastAPI()

@app.on_event("startup")
async def startup_event():
    # Base.metadata.create_all(bind=engine) # Alembic handles table creation/updates
    pass

@app.get("/health")
async def health_check():
    return {"status": "ok"}

# Placeholder for a generate-like endpoint, adjusted for human designs
@app.post("/generate-design")
async def generate_design(db: Depends(get_db), design_request: ManifestoCreate):
    # This is a placeholder. In a real scenario, this might involve AI generating content
    # or preparing a template. For now, it just creates a new manifesto.
    db_manifesto = UserManifesto(
        title=design_request.title,
        content=design_request.content,
        author=design_request.author
    )
    try:
        db.add(db_manifesto)
        db.commit()
        db.refresh(db_manifesto)
        return ManifestoResponse.from_orm(db_manifesto)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")

# Example: Read all manifestos
@app.get("/manifestos", response_model=List[ManifestoResponse])
async def read_manifestos(db: Depends(get_db), skip: int = 0, limit: int = 100):
    manifestos = db.query(UserManifesto).offset(skip).limit(limit).all()
    return manifestos

# Example: Read a single manifesto
@app.get("/manifestos/{manifesto_id}", response_model=ManifestoResponse)
async def read_manifesto(manifesto_id: int, db: Depends(get_db)):
    manifesto = db.query(UserManifesto).filter(UserManifesto.id == manifesto_id).first()
    if manifesto is None:
        raise HTTPException(status_code=404, detail="Manifesto not found")
    return manifesto

# Example: Update a manifesto
class ManifestoUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    author: str | None = None

@app.patch("/manifestos/{manifesto_id}", response_model=ManifestoResponse)
async def update_manifesto(manifesto_id: int, db: Depends(get_db), manifesto_update: ManifestoUpdate):
    db_manifesto = db.query(UserManifesto).filter(UserManifesto.id == manifesto_id).first()
    if db_manifesto is None:
        raise HTTPException(status_code=404, detail="Manifesto not found")

    update_data = manifesto_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_manifesto, key, value)
    
    try:
        db.add(db_manifesto)
        db.commit()
        db.refresh(db_manifesto)
        return ManifestoResponse.from_orm(db_manifesto)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")

# Example: Delete a manifesto
@app.delete("/manifestos/{manifesto_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_manifesto(manifesto_id: int, db: Depends(get_db)):
    db_manifesto = db.query(UserManifesto).filter(UserManifesto.id == manifesto_id).first()
    if db_manifesto is None:
        raise HTTPException(status_code=404, detail="Manifesto not found")
    
    try:
        db.delete(db_manifesto)
        db.commit()
        return {"message": "Manifesto deleted successfully"}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)