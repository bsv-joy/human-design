import os
from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session # Import Session
from enum import Enum as PyEnum # Alias Enum to avoid conflict with human_design_lib.models.Enum
import json # Import json for chart_data_json serialization

from database import engine, SessionLocal, get_db # Import from new database.py
from models import Base, UserManifesto # Import Base and UserManifesto from new models.py

# Import Human Design Library components (data structures and calculation logic)
from human_design_lib.models import (
    BirthData, # For the request model
    Gate as HDGate,
    Line as HDLine,
    Planet as HDPlanet,
    Center as HDCenter,
    GateActivation as HDGateActivation,
    Channel as HDChannel,
    DefinedCenter as HDDefinedCenter,
    PlanetaryPosition as HDPlanetaryPosition
)
from human_design_lib.calculator import (
    get_planetary_positions,
    calculate_design_imprint_datetime,
    map_degree_to_gate_and_line
)
from human_design_lib.bodygraph import calculate_defined_channels, calculate_defined_centers
from human_design_lib.chart_analyzer import (
    determine_type_and_strategy,
    determine_inner_authority,
    determine_profile,
    determine_incarnation_cross
)


# --- Pydantic Models for Human Design Calculation API ---

class PlanetEnum(PyEnum):
    SUN = "Sun"
    EARTH = "Earth"
    MOON = "Moon"
    MERCURY = "Mercury"
    VENUS = "Venus"
    MARS = "Mars"
    JUPITER = "Jupiter"
    SATURN = "Saturn"
    URANUS = "UranUS"
    NEPTUNE = "Neptune"
    PLUTO = "Pluto"
    NORTH_NODE = "North Node"
    SOUTH_NODE = "South Node"

class GateEnum(PyEnum):
    # This enum will simply hold the gate number for API representation
    GATE_1 = 1
    GATE_2 = 2
    GATE_3 = 3
    GATE_4 = 4
    GATE_5 = 5
    GATE_6 = 6
    GATE_7 = 7
    GATE_8 = 8
    GATE_9 = 9
    GATE_10 = 10
    GATE_11 = 11
    GATE_12 = 12
    GATE_13 = 13
    GATE_14 = 14
    GATE_15 = 15
    GATE_16 = 16
    GATE_17 = 17
    GATE_18 = 18
    GATE_19 = 19
    GATE_20 = 20
    GATE_21 = 21
    GATE_22 = 22
    GATE_23 = 23
    GATE_24 = 24
    GATE_25 = 25
    GATE_26 = 26
    GATE_27 = 27
    GATE_28 = 28
    GATE_29 = 29
    GATE_30 = 30
    GATE_31 = 31
    GATE_32 = 32
    GATE_33 = 33
    GATE_34 = 34
    GATE_35 = 35
    GATE_36 = 36
    GATE_37 = 37
    GATE_38 = 38
    GATE_39 = 39
    GATE_40 = 40
    GATE_41 = 41
    GATE_42 = 42
    GATE_43 = 43
    GATE_44 = 44
    GATE_45 = 45
    GATE_46 = 46
    GATE_47 = 47
    GATE_48 = 48
    GATE_49 = 49
    GATE_50 = 50
    GATE_51 = 51
    GATE_52 = 52
    GATE_53 = 53
    GATE_54 = 54
    GATE_55 = 55
    GATE_56 = 56
    GATE_57 = 57
    GATE_58 = 58
    GATE_59 = 59
    GATE_60 = 60
    GATE_61 = 61
    GATE_62 = 62
    GATE_63 = 63
    GATE_64 = 64

    @classmethod
    def from_hd_gate(cls, hd_gate: HDGate):
        return cls[hd_gate.name]

class LineEnum(PyEnum):
    LINE_1 = 1
    LINE_2 = 2
    LINE_3 = 3
    LINE_4 = 4
    LINE_5 = 5
    LINE_6 = 6

    @classmethod
    def from_hd_line(cls, hd_line: HDLine):
        return cls[hd_line.name]

class CenterEnum(PyEnum):
    HEAD = "Head"
    AJNA = "Ajna"
    THROAT = "Throat"
    G_CENTER = "G-Center"
    EGO = "Ego"
    SACRAL = "Sacral"
    SPLEEN = "SpleEN"
    ROOT = "Root"
    SOLAR_PLEXUS = "Solar Plexus"

    @classmethod
    def from_hd_center(cls, hd_center: HDCenter):
        return cls[hd_center.name]

class BirthDataRequest(BaseModel):
    datetime_utc: datetime
    latitude: float
    longitude: float
    timezone_str: str

class PlanetaryPositionResponse(BaseModel):
    planet: PlanetEnum
    degree: float
    sign: str

    @classmethod
    def from_hd_planetary_position(cls, hd_pos: HDPlanetaryPosition):
        return cls(planet=PlanetEnum[hd_pos.planet.name], degree=hd_pos.degree, sign=hd_pos.sign)


class GateActivationResponse(BaseModel):
    gate: GateEnum
    line: LineEnum
    planet: PlanetEnum
    conscious: bool

    @classmethod
    def from_hd_gate_activation(cls, hd_activation: HDGateActivation):
        return cls(
            gate=GateEnum.from_hd_gate(hd_activation.gate),
            line=LineEnum.from_hd_line(hd_activation.line),
            planet=PlanetEnum[hd_activation.planet.name],
            conscious=hd_activation.conscious
        )

class ChannelResponse(BaseModel):
    gate_1: GateEnum
    gate_2: GateEnum
    conscious: bool

    @classmethod
    def from_hd_channel(cls, hd_channel: HDChannel):
        return cls(
            gate_1=GateEnum.from_hd_gate(hd_channel.gate_1),
            gate_2=GateEnum.from_hd_gate(hd_channel.gate_2),
            conscious=hd_channel.conscious
        )

class DefinedCenterResponse(BaseModel):
    center: CenterEnum
    defined: bool

    @classmethod
    def from_hd_defined_center(cls, hd_defined_center: HDDefinedCenter):
        return cls(
            center=CenterEnum.from_hd_center(hd_defined_center.center),
            defined=hd_defined_center.defined
        )

class HumanDesignChartResponse(BaseModel):
    birth_data: BirthDataRequest # Reuse the request model for input data display
    personality_activations: List[GateActivationResponse]
    design_activations: List[GateActivationResponse]
    defined_channels: List[ChannelResponse]
    defined_centers: List[DefinedCenterResponse]
    type: str
    strategy: str
    inner_authority: str
    profile: str
    incarnation_cross: str

class ManifestoBase(BaseModel):
    title: str
    content: str
    author: str = "Anonymous"
    
    # Human Design Chart Fields (Optional)
    birth_datetime_utc: Optional[datetime] = None
    birth_latitude: Optional[float] = None
    birth_longitude: Optional[float] = None
    birth_timezone_str: Optional[str] = None
    chart_type: Optional[str] = None
    chart_strategy: Optional[str] = None
    chart_inner_authority: Optional[str] = None
    chart_profile: Optional[str] = None
    chart_incarnation_cross: Optional[str] = None
    chart_data_json: Optional[str] = None # JSON string of the full chart response

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
async def generate_design(design_request: ManifestoCreate, db: Session = Depends(get_db)):
    db_manifesto = UserManifesto(
        title=design_request.title,
        content=design_request.content,
        author=design_request.author,
        birth_datetime_utc=design_request.birth_datetime_utc,
        birth_latitude=design_request.birth_latitude,
        birth_longitude=design_request.birth_longitude,
        birth_timezone_str=design_request.birth_timezone_str,
        chart_type=design_request.chart_type,
        chart_strategy=design_request.chart_strategy,
        chart_inner_authority=design_request.chart_inner_authority,
        chart_profile=design_request.chart_profile,
        chart_incarnation_cross=design_request.chart_incarnation_cross,
        chart_data_json=design_request.chart_data_json
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


@app.post("/calculate-chart", response_model=HumanDesignChartResponse)
async def calculate_human_design_chart(
    birth_data_request: BirthDataRequest
):
    try:
        # Create BirthData object for the library
        birth_data_lib = BirthData(
            datetime_utc=birth_data_request.datetime_utc,
            latitude=birth_data_request.latitude,
            longitude=birth_data_request.longitude,
            timezone_str=birth_data_request.timezone_str
        )

        # 1. Get Planetary Positions (Personality Imprint)
        personality_positions = get_planetary_positions(birth_data_lib)
        personality_activations = []
        for pos in personality_positions:
            gate, line = map_degree_to_gate_and_line(pos.degree)
            personality_activations.append(HDGateActivation(
                gate=gate, line=line, planet=pos.planet, conscious=True
            ))

        # 2. Calculate Design Imprint Datetime (88 degrees solar arc)
        design_dt = calculate_design_imprint_datetime(birth_data_lib)
        design_birth_data_lib = BirthData(
            datetime_utc=design_dt,
            latitude=birth_data_request.latitude,
            longitude=birth_data_request.longitude,
            timezone_str=birth_data_request.timezone_str
        )

        # 3. Get Planetary Positions (Design Imprint)
        design_positions = get_planetary_positions(design_birth_data_lib)
        design_activations = []
        for pos in design_positions:
            gate, line = map_degree_to_gate_and_line(pos.degree)
            design_activations.append(HDGateActivation(
                gate=gate, line=line, planet=pos.planet, conscious=False
            ))
        
        # Combine all activations for channel/center calculation
        all_activations = personality_activations + design_activations

        # 4. Calculate Defined Channels
        defined_channels = calculate_defined_channels(all_activations)

        # 5. Calculate Defined Centers
        defined_centers = calculate_defined_centers(defined_channels)

        # 6. Determine Type and Strategy
        chart_type, strategy = determine_type_and_strategy(defined_centers)

        # 7. Determine Inner Authority
        inner_authority = determine_inner_authority(defined_centers)

        # 8. Determine Profile
        profile = determine_profile(personality_activations, design_activations)

        # 9. Determine Incarnation Cross
        incarnation_cross = determine_incarnation_cross(personality_activations, design_activations)

        # Construct response
        response_personality_activations = [GateActivationResponse.from_hd_gate_activation(ga) for ga in personality_activations]
        response_design_activations = [GateActivationResponse.from_hd_gate_activation(ga) for ga in design_activations]
        response_defined_channels = [ChannelResponse.from_hd_channel(ch) for ch in defined_channels]
        response_defined_centers = [DefinedCenterResponse.from_hd_defined_center(dc) for dc in defined_centers]

        return HumanDesignChartResponse(
            birth_data=birth_data_request,
            personality_activations=response_personality_activations,
            design_activations=response_design_activations,
            defined_channels=response_defined_channels,
            defined_centers=response_defined_centers,
            type=chart_type,
            strategy=strategy,
            inner_authority=inner_authority,
            profile=profile,
            incarnation_cross=incarnation_cross
        )

    except HTTPException:
        raise # Re-raise FastAPI HTTPExceptions
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Input error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred during chart calculation: {e}")

# Example: Read all manifestos
@app.get("/manifestos", response_model=List[ManifestoResponse])
async def read_manifestos(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    manifestos = db.query(UserManifesto).offset(skip).limit(limit).all()
    return manifestos

# Example: Read a single manifesto
@app.get("/manifestos/{manifesto_id}", response_model=ManifestoResponse)
async def read_manifesto(manifesto_id: int, db: Session = Depends(get_db)):
    manifesto = db.query(UserManifesto).filter(UserManifesto.id == manifesto_id).first()
    if manifesto is None:
        raise HTTPException(status_code=404, detail="Manifesto not found")
    return manifesto

# Example: Update a manifesto
class ManifestoUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    author: Optional[str] = None
    
    # Human Design Chart Fields (Optional)
    birth_datetime_utc: Optional[datetime] = None
    birth_latitude: Optional[float] = None
    birth_longitude: Optional[float] = None
    birth_timezone_str: Optional[str] = None
    chart_type: Optional[str] = None
    chart_strategy: Optional[str] = None
    chart_inner_authority: Optional[str] = None
    chart_profile: Optional[str] = None
    chart_incarnation_cross: Optional[str] = None
    chart_data_json: Optional[str] = None

@app.patch("/manifestos/{manifesto_id}", response_model=ManifestoResponse)
async def update_manifesto(manifesto_id: int, manifesto_update: ManifestoUpdate, db: Session = Depends(get_db)):
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
async def delete_manifesto(manifesto_id: int, db: Session = Depends(get_db)):
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