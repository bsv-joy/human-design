from typing import List, Tuple
from human_design_lib.models import Gate, Center, GateActivation, Channel, DefinedCenter

# --- Center to Gate Mapping ---
# Maps each center to the list of gates associated with it.
CENTER_GATES = {
    Center.HEAD: [Gate.GATE_64, Gate.GATE_61, Gate.GATE_63],
    Center.AJNA: [Gate.GATE_17, Gate.GATE_47, Gate.GATE_11, Gate.GATE_43, Gate.GATE_24, Gate.GATE_4],
    Center.THROAT: [
        Gate.GATE_62, Gate.GATE_23, Gate.GATE_56, Gate.GATE_35, Gate.GATE_12,
        Gate.GATE_45, Gate.GATE_33, Gate.GATE_8, Gate.GATE_16, Gate.GATE_20,
        Gate.GATE_31
    ],
    Center.G_CENTER: [
        Gate.GATE_10, Gate.GATE_7, Gate.GATE_1, Gate.GATE_13, Gate.GATE_25,
        Gate.GATE_46, Gate.GATE_15, Gate.GATE_2
    ],
    Center.EGO: [Gate.GATE_21, Gate.GATE_51, Gate.GATE_26, Gate.GATE_40],
    Center.SACRAL: [
        Gate.GATE_59, Gate.GATE_9, Gate.GATE_5, Gate.GATE_14, Gate.GATE_29,
        Gate.GATE_3, Gate.GATE_42, Gate.GATE_27, Gate.GATE_34
    ],
    Center.SPLEEN: [
        Gate.GATE_48, Gate.GATE_57, Gate.GATE_20, Gate.GATE_32, Gate.GATE_44,
        Gate.GATE_50, Gate.GATE_18, Gate.GATE_28
    ],
    Center.ROOT: [
        Gate.GATE_53, Gate.GATE_60, Gate.GATE_38, Gate.GATE_54, Gate.GATE_58,
        Gate.GATE_19, Gate.GATE_39, Gate.GATE_41
    ],
    Center.SOLAR_PLEXUS: [
        Gate.GATE_36, Gate.GATE_22, Gate.GATE_37, Gate.GATE_6, Gate.GATE_49,
        Gate.GATE_55, Gate.GATE_30
    ],
}


# --- Canonical Channel Definitions ---
# Each tuple represents a channel (gate1, gate2), defined in its canonical order.
# No reversed duplicates are included. Sorted for consistent processing.
CANONICAL_CHANNELS = sorted([
    (Gate.GATE_64, Gate.GATE_47), # Channel of Abstraction (Head to Ajna)
    (Gate.GATE_61, Gate.GATE_24), # Channel of Awareness (Head to Ajna)
    (Gate.GATE_63, Gate.GATE_4),  # Channel of Logic (Head to Ajna)

    (Gate.GATE_17, Gate.GATE_62), # Channel of Acceptance (Ajna to Throat)
    (Gate.GATE_43, Gate.GATE_23), # Channel of Structuring (Ajna to Throat)
    (Gate.GATE_11, Gate.GATE_56), # Channel of Curiosity (Ajna to Throat)

    (Gate.GATE_35, Gate.GATE_36), # Channel of Transitoriness (Throat to Solar Plexus)
    (Gate.GATE_12, Gate.GATE_22), # Channel of Openness (Throat to Solar Plexus)
    (Gate.GATE_45, Gate.GATE_21), # Channel of Money (Throat to Ego)
    (Gate.GATE_33, Gate.GATE_13), # Channel of the Prodigal (Throat to G-Center)
    (Gate.GATE_8, Gate.GATE_1),   # Channel of Inspiration (Throat to G-Center)
    (Gate.GATE_16, Gate.GATE_48), # Channel of Talents (Throat to Spleen)
    (Gate.GATE_20, Gate.GATE_10), # Channel of Awakening (Throat to G-Center)
    (Gate.GATE_20, Gate.GATE_57), # Channel of Brainwave (Throat to Spleen)
    (Gate.GATE_20, Gate.GATE_34), # Channel of Charisma (Throat to Sacral)
    (Gate.GATE_31, Gate.GATE_7),  # Channel of Alpha (Throat to G-Center)

    (Gate.GATE_25, Gate.GATE_51), # Channel of Initiation (G-Center to Ego)
    (Gate.GATE_46, Gate.GATE_29), # Channel of Discovery (G-Center to Sacral)
    (Gate.GATE_15, Gate.GATE_5),  # Channel of Rhythm (G-Center to Sacral)
    (Gate.GATE_2, Gate.GATE_14),  # Channel of the Beat (G-Center to Sacral)
    (Gate.GATE_10, Gate.GATE_34), # Channel of Exploration (G-Center to Sacral)

    (Gate.GATE_40, Gate.GATE_37), # Channel of Community (Ego to Solar Plexus)
    (Gate.GATE_26, Gate.GATE_44), # Channel of Surrender (Ego to Spleen)

    (Gate.GATE_59, Gate.GATE_6),  # Channel of Mating (Sacral to Solar Plexus)
    (Gate.GATE_9, Gate.GATE_52),  # Channel of Concentration (Sacral to Root)
    (Gate.GATE_3, Gate.GATE_60),  # Channel of Mutation (Sacral to Root)
    (Gate.GATE_42, Gate.GATE_53), # Channel of Maturation (Sacral to Root)
    (Gate.GATE_27, Gate.GATE_50), # Channel of Preservation (Sacral to Spleen)
    (Gate.GATE_34, Gate.GATE_57), # Channel of Power (Sacral to Spleen)

    (Gate.GATE_32, Gate.GATE_54), # Channel of Transformation (Spleen to Root)
    (Gate.GATE_44, Gate.GATE_26), # Channel of Surrender (Spleen to Ego) - reversed duplicate removed
    (Gate.GATE_18, Gate.GATE_58), # Channel of Judgment (Spleen to Root)
    (Gate.GATE_28, Gate.GATE_38), # Channel of Struggle (Spleen to Root)

    (Gate.GATE_19, Gate.GATE_49), # Channel of Synthesis (Root to Solar Plexus)
    (Gate.GATE_39, Gate.GATE_37), # Channel of Emoting (Root to Solar Plexus)
    (Gate.GATE_41, Gate.GATE_30), # Channel of Recognition (Root to Solar Plexus)
], key=lambda x: (x[0].value[0], x[1].value[0])) # Sort the canonical channels for consistent output


def calculate_defined_channels(gate_activations: List[GateActivation]) -> List[Channel]:
    """
    Determines which channels are defined based on a list of active gates.
    A channel is defined if both of its gates are activated.
    """
    activated_gates = {ga.gate for ga in gate_activations}
    defined_channels = []

    for gate1, gate2 in CANONICAL_CHANNELS:
        if gate1 in activated_gates and gate2 in activated_gates:
            # Determine if the channel is conscious (personality), unconscious (design), or both
            conscious_definition = False
            for ga in gate_activations:
                if (ga.gate == gate1 or ga.gate == gate2) and ga.conscious:
                    conscious_definition = True
                    break
            
            defined_channels.append(Channel(gate_1=gate1, gate_2=gate2, conscious=conscious_definition))
    
    return defined_channels

def calculate_defined_centers(defined_channels: List[Channel]) -> List[DefinedCenter]:
    """
    Determines which centers are defined based on a list of defined channels.
    A center is defined if it is connected to at least one other defined center via a defined channel.
    This requires a graph traversal or connectivity check.
    """
    defined_center_names = set()
    
    # Create a graph of centers connected by defined channels
    center_graph = {center: [] for center in Center}
    
    for channel in defined_channels:
        # Find centers for gate1
        centers_for_gate1 = [center for center, gates in CENTER_GATES.items() if channel.gate_1 in gates]
        # Find centers for gate2
        centers_for_gate2 = [center for center, gates in CENTER_GATES.items() if channel.gate_2 in gates]
        
        # Add edges to the graph
        for c1 in centers_for_gate1:
            for c2 in centers_for_gate2:
                if c1 != c2: # A channel connects two *different* centers
                    center_graph[c1].append(c2)
                    center_graph[c2].append(c1)
    
    # Perform a connectivity check. A center is defined if it's part of a "defined" network.
    # The simplest rule for definition is if it has at least one channel connected to it.
    # This is a simplification, true definition requires more nuance (e.g., connection to motor centers).
    # For now, if a center has any connections due to defined channels, we mark it as defined.
    for center, connections in center_graph.items():
        if connections:
            defined_center_names.add(center)

    return [DefinedCenter(center=center, defined=center in defined_center_names) for center in Center]

# Example Usage (for testing during development)
if __name__ == "__main__":
    # Simulate some gate activations for testing
    simulated_gate_activations = [
        GateActivation(gate=Gate.GATE_64, line=Line.LINE_1, planet=Planet.SUN, conscious=True),
        GateActivation(gate=Gate.GATE_47, line=Line.LINE_1, planet=Planet.EARTH, conscious=True),
        GateActivation(gate=Gate.GATE_21, line=Line.LINE_1, planet=Planet.MARS, conscious=False),
        GateActivation(gate=Gate.GATE_45, line=Line.LINE_1, planet=Planet.MERCURY, conscious=False),
        GateActivation(gate=Gate.GATE_3, line=Line.LINE_1, planet=Planet.MOON, conscious=True),
        GateActivation(gate=Gate.GATE_60, line=Line.LINE_1, planet=Planet.JUPITER, conscious=True),
    ]

    # Calculate defined channels
    defined_chans = calculate_defined_channels(simulated_gate_activations)
    print("Defined Channels:")
    for ch in defined_chans:
        print(f"  Channel between Gate {ch.gate_1.value[0]} and Gate {ch.gate_2.value[0]} (Conscious: {ch.conscious})")

    # Calculate defined centers
    defined_cents = calculate_defined_centers(defined_chans)
    print("\nDefined Centers:")
    for dc in defined_cents:
        print(f"  {dc.center.value}: {dc.defined}")
