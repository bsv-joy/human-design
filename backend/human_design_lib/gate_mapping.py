from human_design_lib.models import Gate, Line

# Helper function to convert astrological degree (e.g., Aries 15°07'30") to absolute degree (0-360)
def to_absolute_degree(sign: str, degrees: int, minutes: int, seconds: int) -> float:
    zodiac_order = {
        "Aries": 0, "Taurus": 1, "Gemini": 2, "Cancer": 3, "Leo": 4, "Virgo": 5,
        "Libra": 6, "Scorpio": 7, "Sagittarius": 8, "Capricorn": 9, "Aquarius": 10, "Pisces": 11
    }
    sign_start_degree = zodiac_order[sign] * 30
    total_degrees = degrees + (minutes / 60) + (seconds / 3600)
    return sign_start_degree + total_degrees

# Simulated GATE_DEGREE_MAPPING for all 64 gates, assuming uniform distribution
# Each gate is approximately 360 / 64 = 5.625 degrees wide.
# This is a simplification for development purposes. Real mapping is more complex.
GATE_WIDTH = 360 / 64
GATE_DEGREE_MAPPING = []
for i in range(64):
    start_degree = i * GATE_WIDTH
    end_degree = (i + 1) * GATE_WIDTH
    # Gates are 1-indexed in Human Design, so map i (0-63) to Gate.GATE_1 to Gate.GATE_64
    gate = getattr(Gate, f"GATE_{i + 1}")
    GATE_DEGREE_MAPPING.append((start_degree, end_degree, gate))

# Line mapping within each gate (relative degrees from 0 to GATE_WIDTH)
# Each line is approximately GATE_WIDTH / 6 = 0.9375 degrees wide.
LINE_WIDTH = GATE_WIDTH / 6
LINE_MAPPING = {}
for gate_enum in Gate:
    LINE_MAPPING[gate_enum] = []
    for i in range(6):
        start_line_degree = i * LINE_WIDTH
        end_line_degree = (i + 1) * LINE_WIDTH
        line = getattr(Line, f"LINE_{i + 1}")
        LINE_MAPPING[gate_enum].append((start_line_degree, end_line_degree, line))

# The more accurate mapping, if available, would be structured like this:
# GATE_DEGREE_MAPPING_ACCURATE = [
#     (to_absolute_degree("Aries", 0, 0, 0), to_absolute_degree("Aries", 3, 52, 30), Gate.GATE_25),
#     (to_absolute_degree("Aries", 3, 52, 30), to_absolute_degree("Aries", 9, 30, 0), Gate.GATE_17),
#     # ... and so on for all 64 gates with precise boundaries.
# ]
#
# LINE_MAPPING_ACCURATE = {
#     Gate.GATE_1: [
#         (0.0, 0.9375, Line.LINE_1), # These are relative degrees within the gate's span
#         (0.9375, 1.875, Line.LINE_2),
#         # ... precise line boundaries for each gate based on its actual span
#     ],
#     # ... for all 64 gates
# }