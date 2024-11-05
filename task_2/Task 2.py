import numpy as np
import unittest


def generate_random_data(mean, variance, num_samples):
    lower_bound = max(mean - variance, 0)
    upper_bound = min(mean + variance + 1, 90)

    if lower_bound >= upper_bound:
        lower_bound = upper_bound - 1

    return np.random.randint(lower_bound, upper_bound, num_samples)


def calculate_aggregated_threat_score(department_data):
    total_weighted_score = 0
    total_importance = 0

    for importance, threat_scores in department_data:
        department_mean_score = np.mean(threat_scores)
        weighted_score = department_mean_score * importance
        total_weighted_score += weighted_score
        total_importance += importance

    # Normalize to maintain the score within the 0 - 90 range
    aggregated_score = total_weighted_score / total_importance
    return min(90, max(0, aggregated_score))  # Ensure it's in 0-90 range


class TestAggregatedThreatScore(unittest.TestCase):

    def setUp(self):
        # Define common values for test cases
        self.num_samples = 50

    def test_case1_no_outliers(self):
        # Case 1: Similar mean threat scores, equal importance, no outliers
        '''No Outliers, Similar Means, Equal Importance
        This case tests a normal scenario with no significant variances in the
        threat scores and equal department importance.'''
        data = [
            (3, generate_random_data(45, 5, self.num_samples)),
            (3, generate_random_data(50, 5, self.num_samples)),
            (3, generate_random_data(48, 5, self.num_samples)),
            (3, generate_random_data(47, 5, self.num_samples)),
            (3, generate_random_data(46, 5, self.num_samples))
        ]
        score = calculate_aggregated_threat_score(data)
        self.assertTrue(0 <= score <= 90, "Score out of range")

    def test_case2_high_variance(self):
        # Case 2: High variance in some departments' threat scores
        '''This case checks if the function handles scenarios where some departments have high variance in threat scores.
        It also verifies that these variations impact the aggregated score as expected.'''
        data = [
            (5, generate_random_data(60, 20, self.num_samples)),
            (2, generate_random_data(30, 25, self.num_samples)),
            (1, generate_random_data(25, 30, self.num_samples)),
            (4, generate_random_data(45, 10, self.num_samples)),
            (3, generate_random_data(50, 15, self.num_samples))
        ]
        score = calculate_aggregated_threat_score(data)
        self.assertTrue(0 <= score <= 90, "Score out of range")

    def test_case3_varying_importance(self):
        # Case 3: Departments with varying levels of importance
        '''This case simulates realistic conditions where each department has a different importance.
        Higher importance should have a larger effect on the overall score.'''
        data = [
            (1, generate_random_data(20, 5, self.num_samples)),
            (2, generate_random_data(35, 5, self.num_samples)),
            (5, generate_random_data(70, 5, self.num_samples)),
            (4, generate_random_data(55, 5, self.num_samples)),
            (3, generate_random_data(45, 5, self.num_samples))
        ]
        score = calculate_aggregated_threat_score(data)
        self.assertTrue(0 <= score <= 90, "Score out of range")

    def test_case4_extreme_values(self):
        # Case 4: Extreme values with high importance
        '''Here, departments have high threat scores, representing a high-risk scenario.
        This case ensures the function still caps the score at 90 if the average crosses the maximum threshold.'''
        data = [
            (5, generate_random_data(85, 2, self.num_samples)),
            (5, generate_random_data(80, 2, self.num_samples)),
            (5, generate_random_data(90, 0, self.num_samples)),
            (5, generate_random_data(87, 1, self.num_samples)),
            (5, generate_random_data(86, 1, self.num_samples))
        ]
        score = calculate_aggregated_threat_score(data)
        self.assertTrue(0 <= score <= 90, "Score out of range")

    def test_case5_all_low_threat(self):
        # Case 5: Low threat scores across all departments
        '''All departments have low threat scores, simulating a low-risk environment.
        This verifies the lower bound of the output.'''
        data = [
            (2, generate_random_data(5, 2, self.num_samples)),
            (3, generate_random_data(10, 3, self.num_samples)),
            (1, generate_random_data(2, 1, self.num_samples)),
            (4, generate_random_data(8, 2, self.num_samples)),
            (5, generate_random_data(6, 1, self.num_samples))
        ]
        score = calculate_aggregated_threat_score(data)
        self.assertTrue(0 <= score <= 90, "Score out of range")


if __name__ == "__main__":
    unittest.main()
