from datetime import datetime, timedelta
from typing import List, Tuple
import pytz
from kerykeion import AstrologicalSubjectFactory # Changed from AstrologicalSubject
from kerykeion.schemas.kerykeion_exception import KerykeionException # Import KerykeionException

from human_design_lib.models import BirthData, PlanetaryPosition, Planet, Gate, Line, GateActivation
from human_design_lib.gate_mapping import GATE_DEGREE_MAPPING, LINE_MAPPING, GATE_WIDTH

ZODIAC_SIGN_START_DEGREES = {
    "Ari": 0, "Tau": 30, "Gem": 60, "Can": 90, "Leo": 120, "Vir": 150,
    "Lib": 180, "Sco": 210, "Sag": 240, "Cap": 270, "Aqu": 300, "Pis": 330
}

def degree_to_zodiac_sign(degree: float) -> str:
    """Converts a degree (0-360) to its corresponding zodiac sign."""
    # Zodiac signs start at 0 Aries
    # Each sign is 30 degrees
    signs = [
        "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
        "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
    ]
    index = int(degree / 30)
    return signs[index % 12]

def _get_kerykeion_subject(dt_utc: datetime, latitude: float, longitude: float, timezone_str: str, name: str = "temp") -> AstrologicalSubjectFactory: # Changed return type
    """Helper to create an AstrologicalSubject from UTC datetime and timezone string."""
    validated_timezone_str = timezone_str
    try:
        # Validate timezone_str before passing to kerykeion, as it uses pytz internally
        pytz.timezone(timezone_str)
    except pytz.UnknownTimeZoneError:
        validated_timezone_str = "UTC" # Fallback to UTC if timezone is unknown

    return AstrologicalSubjectFactory.from_birth_data(
        name=name,
        year=dt_utc.year,
        month=dt_utc.month,
        day=dt_utc.day,
        hour=dt_utc.hour,
        minute=dt_utc.minute,
        lat=latitude,
        lng=longitude, # Kerykeion expects 'lng'
        tz_str=validated_timezone_str, # Use validated timezone string
        online=False # Bypass GeoNames
    )

def _get_sun_longitude_at_datetime(dt_utc: datetime, latitude: float, longitude: float, timezone_str: str) -> float:
    """Helper to get Sun's longitude for a given datetime (UTC)."""
    subject = _get_kerykeion_subject(dt_utc, latitude, longitude, timezone_str)
    
    # Kerykeion's .position gives degrees within the sign (0-30)
    # .sign gives the sign name (e.g., "Capricorn")
    degree_in_sign = float(subject.sun.position)
    sign_name = subject.sun.sign
    
    sign_start_degree = ZODIAC_SIGN_START_DEGREES.get(sign_name)
    if sign_start_degree is None:
        raise ValueError(f"Unknown zodiac sign: {sign_name}")
        
    absolute_longitude = sign_start_degree + degree_in_sign
    return absolute_longitude

def get_planetary_positions(birth_data: BirthData) -> List[PlanetaryPosition]:
    """
    Calculates planetary positions for a given birth data.
    """
    subject = _get_kerykeion_subject(
        birth_data.datetime_utc,
        birth_data.latitude,
        birth_data.longitude,
        birth_data.timezone_str
    )

    positions = []
    planet_mapping = {
        "Sun": Planet.SUN,
        "Moon": Planet.MOON,
        "Mercury": Planet.MERCURY,
        "Venus": Planet.VENUS,
        "Mars": Planet.MARS,
        "Jupiter": Planet.JUPITER,
        "Saturn": Planet.SATURN,
        "Uranus": Planet.URANUS,
        "Neptune": Planet.NEPTUNE,
        "Pluto": Planet.PLUTO,
        "True Node": Planet.NORTH_NODE,
        "South Node": Planet.SOUTH_NODE,
    }

    for planet_name, planet_enum in planet_mapping.items():
        kerykeion_name = planet_name.lower().replace(" ", "_")
        # Handle True Node as 'north_node' in kerykeion subject attribute
        if kerykeion_name == "true_node":
            kerykeion_name = "north_node"

        if hasattr(subject, kerykeion_name):
            planet_data = getattr(subject, kerykeion_name)
            # Access attributes directly, not dictionary keys
            if hasattr(planet_data, 'position') and hasattr(planet_data, 'sign'):
                positions.append(PlanetaryPosition(
                    planet=planet_enum,
                    degree=float(planet_data.position), # Changed from planet_data['degree']
                    sign=planet_data.sign # Changed from planet_data['sign']
                ))

    # Calculate Earth's position (opposite the Sun)
    sun_degree = None
    for p in positions:
        if p.planet == Planet.SUN:
            sun_degree = p.degree
            break
    if sun_degree is not None:
        earth_degree = (sun_degree + 180) % 360
        earth_sign = degree_to_zodiac_sign(earth_degree)
        positions.append(PlanetaryPosition(planet=Planet.EARTH, degree=earth_degree, sign=earth_sign))

    return positions


def calculate_design_imprint_datetime(birth_data: BirthData) -> datetime:
    """
    Calculates the datetime for the Design Imprint (88 degrees solar arc before birth).
    """
    initial_sun_longitude = _get_sun_longitude_at_datetime(
        birth_data.datetime_utc,
        birth_data.latitude,
        birth_data.longitude,
        birth_data.timezone_str
    )

    target_sun_longitude = (initial_sun_longitude - 88) % 360
    if target_sun_longitude < 0:
        target_sun_longitude += 360

    # Start search approximately 88 days before birth
    search_dt = birth_data.datetime_utc - timedelta(days=88)
    # Define a small tolerance for matching the longitude
    coarse_tolerance = 0.5 # degrees, for the initial hourly search
    fine_tolerance = 0.01 # degrees, for the minute-level refinement

    # Coarse search to find the approximate datetime (within hours)
    found_rough_dt = None
    # Search within a window of roughly 95 to 80 days before birth
    # This covers the 88-day solar arc and provides a buffer.
    
    # Define search boundaries
    start_search_dt = birth_data.datetime_utc - timedelta(days=95)
    end_search_dt = birth_data.datetime_utc - timedelta(days=80)
    
    current_search_dt = start_search_dt
    
    # We will iterate through hours in this window
    while current_search_dt <= end_search_dt:
        try:
            current_sun_longitude = _get_sun_longitude_at_datetime(
                current_search_dt,
                birth_data.latitude,
                birth_data.longitude,
                birth_data.timezone_str
            )
        except KerykeionException as e:
            # Check if the exception is due to an ambiguous time
            if "Ambiguous time error" in str(e):
                # If ambiguous, fall back to UTC for this specific time
                current_sun_longitude = _get_sun_longitude_at_datetime(
                    current_search_dt,
                    birth_data.latitude,
                    birth_data.longitude,
                    "UTC" # Force UTC for this ambiguous time
                )
            else:
                raise e # Re-raise if it's another KerykeionException
        
        # Calculate angular difference, considering wrap-around at 0/360
        diff = abs(current_sun_longitude - target_sun_longitude)
        angular_diff = min(diff, 360 - diff)
        
        if angular_diff < coarse_tolerance:
            found_rough_dt = current_search_dt
            break
            
        current_search_dt += timedelta(hours=1)

    if found_rough_dt is None:
        raise ValueError("Could not find approximate Design Imprint datetime for solar arc.")

    # Refine by minute around the found_rough_dt
    step = timedelta(minutes=1)
    # Search within a window of +/- 12 hours around the found rough datetime
    start_refine_dt = found_rough_dt - timedelta(hours=12)
    end_refine_dt = found_rough_dt + timedelta(hours=12)
    
    best_match_dt = None
    min_angular_diff = 360 # Max possible difference

    current_dt_to_check = start_refine_dt
    while current_dt_to_check <= end_refine_dt:
        try:
            current_sun_longitude = _get_sun_longitude_at_datetime(
                current_dt_to_check,
                birth_data.latitude,
                birth_data.longitude,
                birth_data.timezone_str
            )
        except KerykeionException as e:
            if "Ambiguous time error" in str(e):
                current_sun_longitude = _get_sun_longitude_at_datetime(
                    current_dt_to_check,
                    birth_data.latitude,
                    birth_data.longitude,
                    "UTC" # Force UTC for this ambiguous time
                )
            else:
                raise e
        
        # Calculate angular difference, considering wrap-around at 0/360
        diff = abs(current_sun_longitude - target_sun_longitude)
        angular_diff = min(diff, 360 - diff)

        if angular_diff < min_angular_diff:
            min_angular_diff = angular_diff
            best_match_dt = current_dt_to_check
        
        # If we found a match within fine_tolerance, we can stop early
        if min_angular_diff < fine_tolerance:
            break
        current_dt_to_check += step
    
    if best_match_dt is None:
        raise ValueError("Could not find Design Imprint datetime with required precision.")

    return best_match_dt

def map_degree_to_gate_and_line(degree: float) -> Tuple[Gate, Line]:
    """
    Maps an absolute zodiac degree (0-360) to a Human Design Gate and Line.
    Uses the GATE_DEGREE_MAPPING and LINE_MAPPING from gate_mapping.py.
    """
    target_gate = None
    gate_start_degree = 0.0

    # Find the gate
    for start_deg, end_deg, gate_enum in GATE_DEGREE_MAPPING:
        if start_deg <= degree < end_deg:
            target_gate = gate_enum
            gate_start_degree = start_deg
            break
    
    if target_gate is None:
        # Handle wrap-around for 360 degrees
        if degree >= 360.0 and GATE_DEGREE_MAPPING[0][0] <= (degree % 360) < GATE_DEGREE_MAPPING[0][1]:
            target_gate = GATE_DEGREE_MAPPING[0][2]
            gate_start_degree = GATE_DEGREE_MAPPING[0][0]
        else:
            raise ValueError(f"Degree {degree} out of mapped gate range.")

    # Calculate relative degree within the found gate
    relative_degree_in_gate = degree - gate_start_degree
    
    # Find the line
    target_line = None
    # We use the fixed GATE_WIDTH and LINE_WIDTH for simulated mapping
    # In a real scenario, each gate might have a slightly different width.
    line_index = int(relative_degree_in_gate / (GATE_WIDTH / 6))
    target_line = getattr(Line, f"LINE_{min(line_index + 1, 6)}") # Ensure line index is within 1-6

    if target_line is None:
        raise ValueError(f"Could not determine line for degree {degree} within gate {target_gate.value}.\n")

    return target_gate, target_line


# Example Usage (for testing during development)
if __name__ == "__main__":
    # Example birth data: someone born in London on a specific date
    birth_datetime_utc = datetime(1984, 1, 11, 12, 0, 0, tzinfo=pytz.utc) # UTC time, now with tzinfo
    london_latitude = 51.5074
    london_longitude = 0.1278
    london_timezone_str = "Europe/London"

    birth_data = BirthData(
        datetime_utc=birth_datetime_utc,
        latitude=london_latitude,
        longitude=london_longitude,
        timezone_str=london_timezone_str
    )

    personality_positions = get_planetary_positions(birth_data)
    print("Personality Positions:")
    for pos in personality_positions:
        gate, line = map_degree_to_gate_and_line(pos.degree)
        print(f"  {pos.planet.value}: {pos.degree:.2f} {pos.sign} -> Gate {gate.value[0]}, Line {line.value}")

    design_dt = calculate_design_imprint_datetime(birth_data)
    print(f"\nDesign Imprint Datetime (UTC): {design_dt}")

    design_birth_data = BirthData(
        datetime_utc=design_dt,
        latitude=london_latitude,
        longitude=london_longitude,
        timezone_str=london_timezone_str
    )
    design_positions = get_planetary_positions(design_birth_data)
    print("\nDesign Positions:")
    for pos in design_positions:
        gate, line = map_degree_to_gate_and_line(pos.degree)
        print(f"  {pos.planet.value}: {pos.degree:.2f} {pos.sign} -> Gate {gate.value[0]}, Line {line.value}")

    # Verify the 88-degree arc for Sun
    initial_sun_lon_at_birth = _get_sun_longitude_at_datetime(
        birth_data.datetime_utc,
        birth_data.latitude,
        birth_data.longitude,
        birth_data.timezone_str
    )
    design_sun_lon = _get_sun_longitude_at_datetime(
        design_dt,
        birth_data.latitude,
        birth_data.longitude,
        birth_data.timezone_str
    )
    diff_sun_lon = (initial_sun_lon_at_birth - design_sun_lon + 360) % 360
    print(f"\nSun longitude at birth: {initial_sun_lon_at_birth:.2f}")
    print(f"Sun longitude at design imprint: {design_sun_lon:.2f}")
    print(f"Difference: {diff_sun_lon:.2f} (should be ~88)")
