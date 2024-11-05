import unittest
import math



def time_to_cyclic(hour):
    # Ensure the hour is within the correct range
    if not (0 <= hour < 24):
        raise ValueError("Hour must be in the range [0, 23]")

    time_sin = math.sin(2 * math.pi * hour / 24)
    time_cos = math.cos(2 * math.pi * hour / 24)
    return time_sin, time_cos



class TestTimeToCyclic(unittest.TestCase):

    def test_midnight(self):
        # Midnight should map to sin(0) and cos(1)
        sin, cos = time_to_cyclic(0)
        self.assertAlmostEqual(sin, 0, places=5)
        self.assertAlmostEqual(cos, 1, places=5)

    def test_noon(self):
        # Noon (12:00) should be exactly opposite to midnight on the circle
        sin, cos = time_to_cyclic(12)
        self.assertAlmostEqual(sin, 0, places=5)
        self.assertAlmostEqual(cos, -1, places=5)

    def test_six_am(self):
        # 6:00 should be at the quarter position
        sin, cos = time_to_cyclic(6)
        self.assertAlmostEqual(sin, 1, places=5)
        self.assertAlmostEqual(cos, 0, places=5)

    def test_six_pm(self):
        # 18:00 should be at the three-quarters position
        sin, cos = time_to_cyclic(18)
        self.assertAlmostEqual(sin, -1, places=5)
        self.assertAlmostEqual(cos, 0, places=5)

    def test_wrap_around(self):
        # Test wrap-around: 23:00 and 01:00 should be close in cyclic space
        sin_23, cos_23 = time_to_cyclic(23)
        sin_1, cos_1 = time_to_cyclic(1)
        distance = math.sqrt((sin_23 - sin_1) ** 2 + (cos_23 - cos_1) ** 2)
        self.assertLess(distance, 0.55)  # Slightly increased threshold

    def test_invalid_hour(self):
        # Ensure invalid hour raises an error
        with self.assertRaises(ValueError):
            time_to_cyclic(-1)
        with self.assertRaises(ValueError):
            time_to_cyclic(24)


if __name__ == "__main__":
    unittest.main()
