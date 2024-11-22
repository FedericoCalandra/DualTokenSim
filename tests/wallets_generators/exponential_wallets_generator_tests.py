import math
import unittest
import matplotlib.pyplot as plt
import numpy as np
from source.wallets_generators.exponential_wallets_generator import ExponentialWalletsGenerator


class TestExponentialWalletsGenerator(unittest.TestCase):

    def test_init_valid_probability(self):
        """Test initialization with a valid probability."""
        gen = ExponentialWalletsGenerator(0.5)
        self.assertEqual(gen.probability_associated_to_total_free_token, 0.5)

    def test_init_invalid_probability_le_zero(self):
        """Test initialization with probability <= 0."""
        with self.assertRaises(ValueError):
            ExponentialWalletsGenerator(0)
        with self.assertRaises(ValueError):
            ExponentialWalletsGenerator(-0.1)

    def test_init_invalid_probability_ge_one(self):
        """Test initialization with probability >= 1."""
        with self.assertRaises(ValueError):
            ExponentialWalletsGenerator(1)
        with self.assertRaises(ValueError):
            ExponentialWalletsGenerator(1.5)

    def test_get_random_wallet_valid_supply(self):
        """Test get_random_wallet with valid total_free_token_supply."""
        gen = ExponentialWalletsGenerator(0.5)
        total_free = 100.0
        balance = gen.get_random_wallet(total_free)
        self.assertGreaterEqual(balance, 0.0)
        self.assertLessEqual(balance, total_free)

    def test_get_random_wallet_invalid_supply(self):
        """Test get_random_wallet with non-positive total_free_token_supply."""
        gen = ExponentialWalletsGenerator(0.5)
        with self.assertRaises(ValueError):
            gen.get_random_wallet(-100.0)

    def test_statistical_properties(self):
        """Test statistical properties of generated wallet balances."""
        p = 0.0001
        gen = ExponentialWalletsGenerator(0.0001)
        total_free = 100.0
        num_samples = 10000
        samples = [gen.get_random_wallet(total_free) for _ in range(num_samples)]

        emp_mean = sum(samples) / num_samples
        emp_var = sum((x - emp_mean) ** 2 for x in samples) / num_samples

        rate = -math.log(p) / total_free
        theoretical_mean = 1 / rate
        theoretical_var = 1 / (rate ** 2)

        tolerance = 0.1
        self.assertAlmostEqual(emp_mean, theoretical_mean, delta=tolerance * theoretical_mean)
        self.assertAlmostEqual(emp_var, theoretical_var, delta=tolerance * theoretical_var)

    def test_edge_case_large_values(self):
        """Test with large total_free_token_supply and probability."""
        gen = ExponentialWalletsGenerator(0.999)
        total_free = 1e12
        balance = gen.get_random_wallet(total_free)
        self.assertGreaterEqual(balance, 0.0)
        self.assertLessEqual(balance, total_free)

    def test_edge_case_small_probability(self):
        """Test with a small probability near zero."""
        gen = ExponentialWalletsGenerator(0.001)
        total_free = 100.0
        balance = gen.get_random_wallet(total_free)
        self.assertGreaterEqual(balance, 0.0)
        self.assertLessEqual(balance, total_free)

    def test_randomness(self):
        """Test that generated wallets vary."""
        gen = ExponentialWalletsGenerator(0.5)
        total_free = 100.0
        samples = [gen.get_random_wallet(total_free) for _ in range(100)]
        self.assertTrue(len(set(samples)) > 1)

    def test_visual_distribution_with_counts(self):
        """Test visual distribution of generated wallet balances with histogram counts."""
        # Set parameters
        # Set parameters
        p = 0.01
        total_free = 1000
        num_samples = 10000

        # Initialize generator
        gen = ExponentialWalletsGenerator(p)

        # Generate samples
        samples = [gen.get_random_wallet(total_free) for _ in range(num_samples)]

        # Calculate histogram
        bins = np.linspace(0, total_free, 50)
        hist_counts, bin_edges = np.histogram(samples, bins=bins, density=False)

        # Bin width for scaling
        bin_width = np.diff(bin_edges)  # Width of each bin

        # Plot sample counts histogram
        plt.figure(figsize=(10, 6))
        plt.bar(
            bin_edges[:-1],
            hist_counts,
            width=bin_width,
            alpha=0.7,
            color="blue",
            label="Sample Counts",
            align="edge",
        )
        plt.title("Distribution of Wallet Balances")
        plt.xlabel("Wallet Balance")
        plt.ylabel("Sample Counts")
        plt.legend(loc="upper right")
        plt.show()


if __name__ == '__main__':
    unittest.main()
