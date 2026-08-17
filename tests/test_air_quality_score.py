import unittest

from core.air_quality_score import (
    calculate_scores,
    score_co2,
    score_global,
    score_humidity,
    score_particulate_matter,
    score_temperature,
)


class AirQualityScoreTest(unittest.TestCase):
    def test_humidity_score_boundaries(self):
        self.assertEqual(score_humidity(30), 10)
        self.assertEqual(score_humidity(70), 10)
        self.assertEqual(score_humidity(75), 5)
        self.assertEqual(score_humidity(25), 5)
        self.assertEqual(score_humidity(20), 0)
        self.assertEqual(score_humidity(80), 0)

    def test_co2_score_boundaries(self):
        self.assertEqual(score_co2(0), 10)
        self.assertEqual(score_co2(2499), 10)
        self.assertEqual(score_co2(2500), 10)
        self.assertEqual(score_co2(3500), 5)
        self.assertEqual(score_co2(4500), 0)
        self.assertEqual(score_co2(4501), 0)

    def test_temperature_score_boundaries(self):
        self.assertEqual(score_temperature(20), 10)
        self.assertEqual(score_temperature(25), 10)
        self.assertEqual(score_temperature(17.5), 5)
        self.assertEqual(score_temperature(30), 5)
        self.assertEqual(score_temperature(15), 0)
        self.assertEqual(score_temperature(35), 0)

    def test_particulate_matter_score_boundaries(self):
        self.assertEqual(score_particulate_matter(0), 10)
        self.assertEqual(score_particulate_matter(24.9), 10)
        self.assertEqual(score_particulate_matter(25), 10)
        self.assertEqual(score_particulate_matter(30), 5)
        self.assertEqual(score_particulate_matter(35), 0)

    def test_global_score_uses_weighted_average(self):
        self.assertAlmostEqual(score_global(10, 5, 0, 10), 6.1111111111)

    def test_calculate_scores_returns_individual_and_global_scores(self):
        scores = calculate_scores(
            temperature=22,
            humidity=50,
            co2=600,
            particulate_matter=10,
        )

        self.assertEqual(scores["temperature"], 10)
        self.assertEqual(scores["humidity"], 10)
        self.assertEqual(scores["co2"], 10)
        self.assertEqual(scores["particulate_matter"], 10)
        self.assertEqual(scores["global"], 10)


if __name__ == "__main__":
    unittest.main()
