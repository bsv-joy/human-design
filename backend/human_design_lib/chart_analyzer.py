from typing import List, Optional
from human_design_lib.models import GateActivation, DefinedCenter, Center, Gate, Line, PlanetaryPosition, Planet
from human_design_lib.bodygraph import CANONICAL_CHANNELS, CENTER_GATES

MOTOR_CENTERS = [Center.SACRAL, Center.SOLAR_PLEXUS, Center.EGO, Center.ROOT]

def get_center_definition_status(center: Center, defined_centers: List[DefinedCenter]) -> bool:
    """Helper to get the definition status of a specific center."""
    for dc in defined_centers:
        if dc.center == center:
            return dc.defined
    return False

def determine_type_and_strategy(defined_centers: List[DefinedCenter]) -> tuple[str, str]:
    """
    Determines the Human Design Type and Strategy based on defined centers.
    """
    is_sacral_defined = get_center_definition_status(Center.SACRAL, defined_centers)
    is_all_undefined = all(not dc.defined for dc in defined_centers)

    if is_all_undefined:
        return "Reflector", "To Wait a Lunar Cycle"
    elif is_sacral_defined:
        # Need to check for manifesting generator (direct connection from a motor to throat)
        # For simplicity, we'll assume a generator for now, need channel info for MG
        # A true MG has a defined channel connecting a motor to the throat.
        return "Generator", "To Respond" # This needs refinement for Manifesting Generator
    else: # Undefined Sacral
        is_throat_defined = get_center_definition_status(Center.THROAT, defined_centers)
        
        # Check if any motor center connects to the Throat directly (Manifestor)
        is_manifestor = False
        # This requires checking defined channels, not just centers.
        # For now, a simplified check:
        if is_throat_defined:
            # This is a very rough simplification. True Manifestor check involves motor->throat channel.
            # We'll need access to defined channels here.
            pass # Will be refined later with actual channel data

        if is_manifestor:
            return "Manifestor", "To Inform"
        else:
            return "Projector", "To Wait for the Invitation"
    
    return "Unknown", "Unknown" # Should not be reached with proper logic

def determine_inner_authority(defined_centers: List[DefinedCenter]) -> str:
    """
    Determines the Inner Authority based on defined centers.
    Order of checking matters for hierarchy.
    """
    if get_center_definition_status(Center.SOLAR_PLEXUS, defined_centers):
        return "Emotional"
    elif get_center_definition_status(Center.SACRAL, defined_centers):
        return "Sacral"
    elif get_center_definition_status(Center.SPLEEN, defined_centers):
        return "Splenic"
    elif get_center_definition_status(Center.EGO, defined_centers): # Heart Center
        return "Ego (Willpower)" # or Heart
    elif get_center_definition_status(Center.G_CENTER, defined_centers):
        return "Self-Projected" # or G-Center Projected
    
    # If no internal authority, it's a mental projector or reflector.
    # Reflector already handled by type, so this is mainly for Mental Projectors.
    # But for Reflectors, it's also "Lunar Cycle" or "No Inner Authority"
    return "No Inner Authority / Environmental"

def determine_profile(personality_activations: List[GateActivation], design_activations: List[GateActivation]) -> str:
    """
    Determines the Human Design Profile (e.g., 1/3) from conscious and unconscious Sun/Earth lines.
    """
    conscious_sun_line = None
    conscious_earth_line = None
    design_sun_line = None
    design_earth_line = None

    for pa in personality_activations:
        if pa.planet == Planet.SUN:
            conscious_sun_line = pa.line.value
        if pa.planet == Planet.EARTH:
            conscious_earth_line = pa.line.value
    
    for da in design_activations:
        if da.planet == Planet.SUN:
            design_sun_line = da.line.value
        if da.planet == Planet.EARTH:
            design_earth_line = da.line.value
    
    # Profile is (conscious_sun_line / design_sun_line)
    # The earth lines also define the profile. The primary profile is defined by Sun/Earth conscious/unconscious.
    # Human Design profile is usually (conscious_line / unconscious_line)
    # where conscious_line is from conscious Sun and unconscious_line is from unconscious Sun.
    # However, the structure of the prompt implies using both Sun and Earth for the lines.
    # The standard way is using the conscious Sun line and the unconscious Sun line as the primary.

    # Re-evaluating standard profile calculation:
    # Profile is based on the line of the Conscious Sun and the line of the Design Sun.
    # E.g., Conscious Sun is in Gate X Line 1, Design Sun is in Gate Y Line 3 -> Profile 1/3.
    # Let's adjust based on this standard understanding.
    
    conscious_sun_line_val = None
    design_sun_line_val = None

    for act in personality_activations:
        if act.planet == Planet.SUN:
            conscious_sun_line_val = act.line.value
            break
    for act in design_activations:
        if act.planet == Planet.SUN:
            design_sun_line_val = act.line.value
            break

    if conscious_sun_line_val is not None and design_sun_line_val is not None:
        return f"{conscious_sun_line_val}/{design_sun_line_val}"
    
    return "Unknown Profile"

def determine_incarnation_cross(
    personality_activations: List[GateActivation], 
    design_activations: List[GateActivation]
) -> str:
    """
    Determines the Incarnation Cross from conscious Sun, Earth and unconscious Sun, Earth gates.
    This is a complex interpretation and often involves a lookup table or specific logic
    based on the combination of these four gates.
    For simplicity, this will be a placeholder that lists the four gates.
    """
    p_sun_gate = p_earth_gate = d_sun_gate = d_earth_gate = "Unknown"

    for act in personality_activations:
        if act.planet == Planet.SUN:
            p_sun_gate = act.gate.value[0]
        if act.planet == Planet.EARTH:
            p_earth_gate = act.gate.value[0]
    for act in design_activations:
        if act.planet == Planet.SUN:
            d_sun_gate = act.gate.value[0]
        if act.planet == Planet.EARTH:
            d_earth_gate = act.gate.value[0]
    
    return f"Conscious Sun: {p_sun_gate}, Conscious Earth: {p_earth_gate}, Design Sun: {d_sun_gate}, Design Earth: {d_earth_gate}"

# Example Usage (for testing during development)
if __name__ == "__main__":
    # --- Example 1: Reflector ---
    # All centers undefined
    reflector_defined_centers = [DefinedCenter(center=c, defined=False) for c in Center]
    reflector_type, reflector_strategy = determine_type_and_strategy(reflector_defined_centers)
    reflector_authority = determine_inner_authority(reflector_defined_centers)
    print("--- Reflector Example ---")
    print(f"Type: {reflector_type}, Strategy: {reflector_strategy}, Authority: {reflector_authority}")

    # --- Example 2: Generator (simplified, assumes Sacral defined) ---
    generator_defined_centers = [
        DefinedCenter(center=Center.SACRAL, defined=True),
        DefinedCenter(center=Center.SOLAR_PLEXUS, defined=False),
        DefinedCenter(center=Center.SPLEEN, defined=False),
        DefinedCenter(center=Center.EGO, defined=False),
        DefinedCenter(center=Center.G_CENTER, defined=True),
        DefinedCenter(center=Center.THROAT, defined=False),
        DefinedCenter(center=Center.AJNA, defined=False),
        DefinedCenter(center=Center.HEAD, defined=False),
        DefinedCenter(center=Center.ROOT, defined=False),
    ]
    generator_type, generator_strategy = determine_type_and_strategy(generator_defined_centers)
    generator_authority = determine_inner_authority(generator_defined_centers)
    print("\n--- Generator Example ---")
    print(f"Type: {generator_type}, Strategy: {generator_strategy}, Authority: {generator_authority}")

    # --- Example 3: Emotional Authority (simplified, assumes Solar Plexus defined) ---
    emotional_defined_centers = [
        DefinedCenter(center=Center.SACRAL, defined=True),
        DefinedCenter(center=Center.SOLAR_PLEXUS, defined=True), # Defined emotional center
        DefinedCenter(center=Center.SPLEEN, defined=False),
        DefinedCenter(center=Center.EGO, defined=False),
        DefinedCenter(center=Center.G_CENTER, defined=True),
        DefinedCenter(center=Center.THROAT, defined=True),
        DefinedCenter(center=Center.AJNA, defined=False),
        DefinedCenter(center=Center.HEAD, defined=False),
        DefinedCenter(center=Center.ROOT, defined=False),
    ]
    emotional_type, emotional_strategy = determine_type_and_strategy(emotional_defined_centers)
    emotional_authority = determine_inner_authority(emotional_defined_centers)
    print("\n--- Emotional Authority Example ---")
    print(f"Type: {emotional_type}, Strategy: {emotional_strategy}, Authority: {emotional_authority}")

    # --- Example Profile & Incarnation Cross ---
    simulated_personality_activations = [
        GateActivation(gate=Gate.GATE_1, line=Line.LINE_1, planet=Planet.SUN, conscious=True),
        GateActivation(gate=Gate.GATE_2, line=Line.LINE_2, planet=Planet.EARTH, conscious=True),
    ]
    simulated_design_activations = [
        GateActivation(gate=Gate.GATE_3, line=Line.LINE_3, planet=Planet.SUN, conscious=False),
        GateActivation(gate=Gate.GATE_4, line=Line.LINE_4, planet=Planet.EARTH, conscious=False),
    ]
    profile = determine_profile(simulated_personality_activations, simulated_design_activations)
    incarnation_cross = determine_incarnation_cross(simulated_personality_activations, simulated_design_activations)
    print(f"\nProfile: {profile}")
    print(f"Incarnation Cross: {incarnation_cross}")
