import unittest
from datetime import datetime
import pytz

from human_design_lib.models import (
    BirthData, Planet, Gate, Line, GateActivation, DefinedCenter, Center, Channel
)
from human_design_lib.calculator import (
    degree_to_zodiac_sign,
    _get_kerykeion_subject,
    _get_sun_longitude_at_datetime,
    get_planetary_positions,
    calculate_design_imprint_datetime,
    map_degree_to_gate_and_line
)
from human_design_lib.bodygraph import calculate_defined_channels, calculate_defined_centers
from human_design_lib.chart_analyzer import (
    determine_type_and_strategy,
    determine_inner_authority,
    determine_profile,
    determine_incarnation_cross,
    get_center_definition_status
)


class TestHumanDesignLib(unittest.TestCase):

    def setUp(self):
        self.birth_data = BirthData(
            datetime_utc=datetime(1984, 1, 11, 12, 0, 0, tzinfo=pytz.utc),
            latitude=51.5074,
            longitude=0.1278,
            timezone_str="Europe/London"
        )
        self.london_lat = 51.5074
        self.london_lon = 0.1278
        self.london_tz = "Europe/London"

    def test_degree_to_zodiac_sign(self):
        self.assertEqual(degree_to_zodiac_sign(15), "Aries")
        self.assertEqual(degree_to_zodiac_sign(45), "Taurus")
        self.assertEqual(degree_to_zodiac_sign(270), "Capricorn")
        self.assertEqual(degree_to_zodiac_sign(359), "Pisces")
        self.assertEqual(degree_to_zodiac_sign(0), "Aries")
        self.assertEqual(degree_to_zodiac_sign(30), "Taurus")

    def test_get_kerykeion_subject(self):
        # Test valid timezone
        subject = _get_kerykeion_subject(self.birth_data.datetime_utc, self.london_lat, self.london_lon, self.london_tz)
        self.assertIsNotNone(subject)
        self.assertEqual(subject.year, 1984) # Local time for London UTC+0 is 1984, 1, 11, 12:00
        self.assertEqual(subject.month, 1)
        self.assertEqual(subject.day, 11)
        self.assertEqual(subject.hour, 12)
        self.assertEqual(subject.minute, 0)

        # Test invalid timezone (should fallback to UTC)
        invalid_tz = "Invalid/Timezone"
        subject_invalid_tz = _get_kerykeion_subject(self.birth_data.datetime_utc, self.london_lat, self.london_lon, invalid_tz)
        self.assertIsNotNone(subject_invalid_tz)
        self.assertEqual(subject_invalid_tz.hour, 12) # Should remain UTC hour

    def test_get_sun_longitude_at_datetime(self):
        sun_lon = _get_sun_longitude_at_datetime(self.birth_data.datetime_utc, self.london_lat, self.london_lon, self.london_tz)
        self.assertIsInstance(sun_lon, float)
        # Approximate value for 1984-01-11 12:00 UTC (Sun in Capricorn)
        self.assertGreater(sun_lon, 270)
        self.assertLess(sun_lon, 300)

    def test_get_planetary_positions(self):
        positions = get_planetary_positions(self.birth_data)
        self.assertIsInstance(positions, list)
        self.assertGreater(len(positions), 10) # Should have at least 10 planets + Earth
        
        # Check if Earth is present and has a sign
        earth_present = False
        for p in positions:
            if p.planet == Planet.EARTH:
                earth_present = True
                self.assertIsInstance(p.sign, str)
                self.assertNotEqual(p.sign, "")
                break
        self.assertTrue(earth_present)

    def test_calculate_design_imprint_datetime(self):
        design_dt = calculate_design_imprint_datetime(self.birth_data)
        self.assertIsInstance(design_dt, datetime)
        
        initial_sun_lon = _get_sun_longitude_at_datetime(self.birth_data.datetime_utc, self.london_lat, self.london_lon, self.london_tz)
        design_sun_lon = _get_sun_longitude_at_datetime(design_dt, self.london_lat, self.london_lon, self.london_tz)
        
        diff = (initial_sun_lon - design_sun_lon + 360) % 360
        self.assertAlmostEqual(diff, 88.0, delta=0.1) # Allowing a small delta for iterative search accuracy

    def test_map_degree_to_gate_and_line(self):
        # Test within a gate
        gate, line = map_degree_to_gate_and_line(10.0) # Within GATE_25 (approx 0-5.625) or GATE_17 (approx 5.625-11.25)
        # With the simulated uniform mapping, 10.0 should be in the second gate, second line
        self.assertEqual(gate, Gate.GATE_2)
        self.assertEqual(line, Line.LINE_5)

        # Test another point
        gate2, line2 = map_degree_to_gate_and_line(100.0)
        self.assertEqual(gate2, Gate.GATE_18)
        self.assertEqual(line2, Line.LINE_5)

        # Test at a boundary (should fall into the next gate/line due to < end_deg)
        gate_boundary, line_boundary = map_degree_to_gate_and_line(5.625)
        self.assertEqual(gate_boundary, Gate.GATE_2) # Start of second gate
        self.assertEqual(line_boundary, Line.LINE_1)

        # Test degree near 360 (wrap-around)
        gate_wrap, line_wrap = map_degree_to_gate_and_line(359.9)
        self.assertEqual(gate_wrap, Gate.GATE_64)
        self.assertEqual(line_wrap, Line.LINE_6)


    def test_calculate_defined_channels(self):
        # Gates 64 and 47 form a channel
        activation1 = GateActivation(gate=Gate.GATE_64, line=Line.LINE_1, planet=Planet.SUN, conscious=True)
        activation2 = GateActivation(gate=Gate.GATE_47, line=Line.LINE_1, planet=Planet.EARTH, conscious=False)
        
        defined_chans_none = calculate_defined_channels([])
        self.assertEqual(len(defined_chans_none), 0)

        defined_chans_one_gate = calculate_defined_channels([activation1])
        self.assertEqual(len(defined_chans_one_gate), 0)

        defined_chans_both_gates = calculate_defined_channels([activation1, activation2])
        self.assertEqual(len(defined_chans_both_gates), 1)
        self.assertEqual(defined_chans_both_gates[0].gate_1, Gate.GATE_64)
        self.assertEqual(defined_chans_both_gates[0].gate_2, Gate.GATE_47)
        self.assertTrue(defined_chans_both_gates[0].conscious) # Because one activation is conscious


    def test_calculate_defined_centers(self):
        # Assuming channel (64, 47) is defined (Head to Ajna)
        mock_defined_channels_head_ajna = [
            Channel(gate_1=Gate.GATE_64, gate_2=Gate.GATE_47, conscious=True)
        ]
        defined_centers = calculate_defined_centers(mock_defined_channels_head_ajna)
        
        head_center_defined = get_center_definition_status(Center.HEAD, defined_centers)
        ajna_center_defined = get_center_definition_status(Center.AJNA, defined_centers)
        throat_center_defined = get_center_definition_status(Center.THROAT, defined_centers)

        self.assertTrue(head_center_defined)
        self.assertTrue(ajna_center_defined)
        self.assertFalse(throat_center_defined) # Should not be defined

    def test_determine_type_and_strategy(self):
        # Reflector
        reflector_centers = [DefinedCenter(center=c, defined=False) for c in Center]
        _type, strategy = determine_type_and_strategy(reflector_centers)
        self.assertEqual(_type, "Reflector")
        self.assertEqual(strategy, "To Wait a Lunar Cycle")

        # Generator (simplified)
        generator_centers = [DefinedCenter(center=dc.center, defined=dc.defined) for dc in reflector_centers]
        for dc in generator_centers:
            if dc.center == Center.SACRAL:
                dc.defined = True
        _type, strategy = determine_type_and_strategy(generator_centers)
        self.assertEqual(_type, "Generator")
        self.assertEqual(strategy, "To Respond")

        # Projector (simplified: Undefined Sacral, but not a Reflector or Manifestor)
        projector_centers = [DefinedCenter(center=dc.center, defined=dc.defined) for dc in reflector_centers]
        for dc in projector_centers:
            if dc.center == Center.G_CENTER: # Define G-Center for projector without Sacral
                dc.defined = True
        _type, strategy = determine_type_and_strategy(projector_centers)
        self.assertEqual(_type, "Projector")
        self.assertEqual(strategy, "To Wait for the Invitation")

    def test_determine_inner_authority(self):
        # Emotional
        emotional_centers = [DefinedCenter(center=c, defined=False) for c in Center]
        for dc in emotional_centers:
            if dc.center == Center.SOLAR_PLEXUS:
                dc.defined = True
        self.assertEqual(determine_inner_authority(emotional_centers), "Emotional")

        # Sacral
        sacral_centers = [DefinedCenter(center=c, defined=False) for c in Center]
        for dc in sacral_centers:
            if dc.center == Center.SACRAL:
                dc.defined = True
        self.assertEqual(determine_inner_authority(sacral_centers), "Sacral")

        # Splenic
        splenic_centers = [DefinedCenter(center=c, defined=False) for c in Center]
        for dc in splenic_centers:
            if dc.center == Center.SPLEEN:
                dc.defined = True
        self.assertEqual(determine_inner_authority(splenic_centers), "Splenic")

        # No Inner Authority
        no_authority_centers = [DefinedCenter(center=c, defined=False) for c in Center]
        self.assertEqual(determine_inner_authority(no_authority_centers), "No Inner Authority / Environmental")


    def test_determine_profile(self):
        p_activations = [GateActivation(gate=Gate.GATE_1, line=Line.LINE_1, planet=Planet.SUN, conscious=True)]
        d_activations = [GateActivation(gate=Gate.GATE_3, line=Line.LINE_2, planet=Planet.SUN, conscious=False)]
        self.assertEqual(determine_profile(p_activations, d_activations), "1/2")

        p_activations_no_sun = [GateActivation(gate=Gate.GATE_1, line=Line.LINE_1, planet=Planet.MARS, conscious=True)]
        d_activations_no_sun = [GateActivation(gate=Gate.GATE_3, line=Line.LINE_2, planet=Planet.VENUS, conscious=False)]
        self.assertEqual(determine_profile(p_activations_no_sun, d_activations_no_sun), "Unknown Profile")

    def test_determine_incarnation_cross(self):
        p_activations = [
            GateActivation(gate=Gate.GATE_1, line=Line.LINE_1, planet=Planet.SUN, conscious=True),
            GateActivation(gate=Gate.GATE_2, line=Line.LINE_2, planet=Planet.EARTH, conscious=True),
        ]
        d_activations = [
            GateActivation(gate=Gate.GATE_3, line=Line.LINE_3, planet=Planet.SUN, conscious=False),
            GateActivation(gate=Gate.GATE_4, line=Line.LINE_4, planet=Planet.EARTH, conscious=False),
        ]
        expected_cross = "Conscious Sun: 1, Conscious Earth: 2, Design Sun: 3, Design Earth: 4"
        self.assertEqual(determine_incarnation_cross(p_activations, d_activations), expected_cross)


if __name__ == '__main__':
    unittest.main()
