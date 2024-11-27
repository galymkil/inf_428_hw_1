import numpy as np
import unittest


def generate_random_data(mean, variance, num_samples):
    """Generate random threat scores within the range."""
    lower_bound = max(mean - variance, 0)
    upper_bound = min(mean + variance + 1, 90)

    # Ensure bounds are valid
    if lower_bound >= upper_bound:
        lower_bound = max(0, upper_bound - 1)  # Prevent errors when bounds are invalid

    return np.random.randint(lower_bound, upper_bound, num_samples)


def calculate_aggregated_threat_score(department_data):
    """Calculate the mean threat score across all departments."""
    all_scores = []
    for threat_scores in department_data:
        if len(threat_scores) > 0:  # Skip empty lists
            all_scores.extend(threat_scores)

    if not all_scores:  # Handle case where no scores are present
        return 0

    aggregated_score = np.mean(all_scores)  # Calculate the mean threat score
    return min(90, max(0, aggregated_score))  # Ensure the score is in the range 0-90


class TestAggregatedThreatScore(unittest.TestCase):

    def setUp(self):
        """Define common values for test cases."""
        self.num_samples = 50

    def test_case1_no_outliers(self):
        """Case 1: Similar mean threat scores, no outliers."""
        data = [
            generate_random_data(45, 5, self.num_samples),
            generate_random_data(50, 5, self.num_samples),
            generate_random_data(48, 5, self.num_samples),
            generate_random_data(47, 5, self.num_samples),
            generate_random_data(46, 5, self.num_samples),
        ]
        score = calculate_aggregated_threat_score(data)
        expected_mean = 47.2  # Approximate mean of all generated ranges
        self.assertTrue(0 <= score <= 90, "Score out of range")
        self.assertAlmostEqual(score, expected_mean, delta=5, msg="Mean is not as expected")

    def test_case2_high_variance(self):
        """Case 2: High variance in some departments' threat scores."""
        data = [
            generate_random_data(60, 20, self.num_samples),
            generate_random_data(30, 25, self.num_samples),
            generate_random_data(25, 30, self.num_samples),
            generate_random_data(45, 10, self.num_samples),
            generate_random_data(50, 15, self.num_samples),
        ]
        score = calculate_aggregated_threat_score(data)
        self.assertTrue(0 <= score <= 90, "Score out of range")

    def test_case3_single_high_outlier(self):
        """Case 3: One department has a single high threat score outlier."""
        data = [
            generate_random_data(20, 5, self.num_samples),
            generate_random_data(35, 5, self.num_samples),
            generate_random_data(70, 5, self.num_samples),
            generate_random_data(55, 5, self.num_samples),
            np.append(generate_random_data(45, 5, self.num_samples - 1), [90]),  # High outlier
        ]
        score = calculate_aggregated_threat_score(data)
        self.assertTrue(0 <= score <= 90, "Score out of range")
        self.assertGreater(score, 45, "Outlier not influencing score")

    def test_case4_extreme_values(self):
        """Case 4: Extreme values across all departments."""
        data = [
            generate_random_data(85, 2, self.num_samples),
            generate_random_data(80, 2, self.num_samples),
            generate_random_data(90, 0, self.num_samples),
            generate_random_data(87, 1, self.num_samples),
            generate_random_data(86, 1, self.num_samples),
        ]
        score = calculate_aggregated_threat_score(data)
        self.assertTrue(0 <= score <= 90, "Score out of range")
        self.assertAlmostEqual(score, 86.6, delta=2, msg="Mean is not as expected")

    def test_case5_all_low_threat(self):
        """Case 5: All departments have low threat scores."""
        data = [
            generate_random_data(5, 2, self.num_samples),
            generate_random_data(10, 3, self.num_samples),
            generate_random_data(2, 1, self.num_samples),
            generate_random_data(8, 2, self.num_samples),
            generate_random_data(6, 1, self.num_samples),
        ]
        score = calculate_aggregated_threat_score(data)
        self.assertTrue(0 <= score <= 90, "Score out of range")
        self.assertLess(score, 10, "Low threat scores producing unexpected result")


if __name__ == "__main__":
    unittest.main()
