from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import List, Optional

@dataclass
class BirthData:
    datetime_utc: datetime
    latitude: float
    longitude: float
    timezone_str: str

class Planet(Enum):
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

@dataclass
class PlanetaryPosition:
    planet: Planet
    degree: float  # 0-360 degrees in the zodiac
    sign: str # Aries, Taurus, etc.

class Gate(Enum):
    GATE_1 = (1, "The Creative")
    GATE_2 = (2, "The Receptive")
    GATE_3 = (3, "Difficulty at the Beginning")
    GATE_4 = (4, "Youthful Folly")
    GATE_5 = (5, "Waiting")
    GATE_6 = (6, "Conflict")
    GATE_7 = (7, "The Army")
    GATE_8 = (8, "Holding Together")
    GATE_9 = (9, "The Taming Power of the Small")
    GATE_10 = (10, "The Treading")
    GATE_11 = (11, "Peace")
    GATE_12 = (12, "Standstill")
    GATE_13 = (13, "The Fellowship of Men")
    GATE_14 = (14, "Possession in Great Measure")
    GATE_15 = (15, "Modesty")
    GATE_16 = (16, "Enthusiasm")
    GATE_17 = (17, "Following")
    GATE_18 = (18, "Correction")
    GATE_19 = (19, "Approach")
    GATE_20 = (20, "Contemplation")
    GATE_21 = (21, "Biting Through")
    GATE_22 = (22, "Grace")
    GATE_23 = (23, "Splitting Apart")
    GATE_24 = (24, "Returning")
    GATE_25 = (25, "Innocence")
    GATE_26 = (26, "The Taming Power of the Great")
    GATE_27 = (27, "Nourishment")
    GATE_28 = (28, "Preponderance of the Great")
    GATE_29 = (29, "The Abysmal")
    GATE_30 = (30, "The Clinging Fire")
    GATE_31 = (31, "Influence")
    GATE_32 = (32, "Duration")
    GATE_33 = (33, "Retreat")
    GATE_34 = (34, "The Power of the Great")
    GATE_35 = (35, "Progress")
    GATE_36 = (36, "Darkening of the Light")
    GATE_37 = (37, "The Family")
    GATE_38 = (38, "Opposition")
    GATE_39 = (39, "Provocation")
    GATE_40 = (40, "Deliverance")
    GATE_41 = (41, "Decrease")
    GATE_42 = (42, "Increase")
    GATE_43 = (43, "Breakthrough")
    GATE_44 = (44, "Coming to Meet")
    GATE_45 = (45, "Gathering Together")
    GATE_46 = (46, "Pushing Upward")
    GATE_47 = (47, "Oppression")
    GATE_48 = (48, "The Well")
    GATE_49 = (49, "Revolution")
    GATE_50 = (50, "The Cauldron")
    GATE_51 = (51, "The Arousing")
    GATE_52 = (52, "Keeping Still")
    GATE_53 = (53, "Development")
    GATE_54 = (54, "The Marrying Maiden")
    GATE_55 = (55, "Abundance")
    GATE_56 = (56, "The Wanderer")
    GATE_57 = (57, "The Gentle")
    GATE_58 = (58, "The Joyous")
    GATE_59 = (59, "Dispersion")
    GATE_60 = (60, "Limitation")
    GATE_61 = (61, "Inner Truth")
    GATE_62 = (62, "Preponderance of the Small")
    GATE_63 = (63, "After Completion")
    GATE_64 = (64, "Before Completion")


class Line(Enum):
    LINE_1 = 1
    LINE_2 = 2
    LINE_3 = 3
    LINE_4 = 4
    LINE_5 = 5
    LINE_6 = 6

@dataclass
class GateActivation:
    gate: Gate
    line: Line
    planet: Planet
    conscious: bool  # True for Personality, False for Design

@dataclass
class Channel:
    gate_1: Gate
    gate_2: Gate
    conscious: bool # True if defined by personality planets, False if by design, or both if mixed

class Center(Enum):
    HEAD = "Head"
    AJNA = "Ajna"
    THROAT = "Throat"
    G_CENTER = "G-Center"
    EGO = "Ego"
    SACRAL = "Sacral"
    SPLEEN = "SpleEN"
    ROOT = "Root"
    SOLAR_PLEXUS = "Solar Plexus"

@dataclass
class DefinedCenter:
    center: Center
    defined: bool = False

@dataclass
class HumanDesignChart:
    birth_data: BirthData
    personality_activations: List[GateActivation]
    design_activations: List[GateActivation]
    defined_channels: List[Channel]
    defined_centers: List[DefinedCenter]
    type: Optional[str] = None
    strategy: Optional[str] = None
    inner_authority: Optional[str] = None
    profile: Optional[str] = None
    incarnation_cross: Optional[str] = None