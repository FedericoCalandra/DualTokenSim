import unittest
from source.wallets_generators.exponential_wallets_generator import ExponentialWalletsGenerator
from source.tokens.token import Token
from source.tokens.algorithmic_stablecoin import AlgorithmicStablecoin
from source.tokens.collateral_token import CollateralToken
from source.purchase_generators.seignorage_model_random_purchase_generator import SeignorageModelRandomPurchaseGenerator
from source.purchase_generators.seignorage_model_purchase_generator import SeignorageModelPurchaseGenerator


class TestPurchaseGenerators(unittest.TestCase):
    
    def setUp(self):
        """
        The setUp method is called before each test. It initializes shared objects 
        like the wallet generator and tokens used in multiple tests.
        """
        # Initialize an algorithmic stablecoin with full parameters.
        self.token = AlgorithmicStablecoin(
            "TestStablecoin", 100000.0, 100000.0, 1.0, 1.0)
        # Initialize a collateral token for additional tests.
        self.collateral_token = CollateralToken(
            "TestCollateralToken", 100000.0, 100000.0, 1.0, self.token)
        # Create a wallet generator.
        self.wallets_generator = ExponentialWalletsGenerator(0.1)

    def test_random_purchase_generator_initialization(self):
        """Test correct initialization of SeignorageModelRandomPurchaseGenerator."""
        generator = SeignorageModelRandomPurchaseGenerator(
            token=self.token,
            wallets_generator=self.wallets_generator,
            volume_variance=500,
            initial_volume=1000,
            variance=1.0,
            mean=1.0,
            delta_variation=lambda x: x * 0.1,
            threshold=0.05
        )
        self.assertEqual(generator.volume_variance, 500)
        self.assertEqual(generator.volume, 1000)
        self.assertEqual(generator.variance, 1.0)
        self.assertEqual(generator.mean, 1.0)
        self.assertEqual(generator.threshold, 0.05)

    def test_random_purchase_generator_invalid_token(self):
        """Test whether an error is raised when the token is invalid."""
        with self.assertRaises(TypeError):
            SeignorageModelRandomPurchaseGenerator(
                token=Token("InvalidToken"),  # Invalid token
                wallets_generator=self.wallets_generator
            )

    def test_random_purchase_generator_transaction_amount(self):
        """
        Test that the transaction amount generated can be both positive or negative.
        Ensures correct handling of market dynamics.
        """
        generator = SeignorageModelRandomPurchaseGenerator(
            token=self.token,
            wallets_generator=self.wallets_generator,
        )
        amount = generator.generate_transaction_amount()
        # The amount can be positive or negative, so no direct assertion on sign.
        self.assertIsInstance(amount, float)

    def test_purchase_generator_compute_volume(self):
        """
        Test the _compute_volume function of the Random Generator.
        Ensures that the updated volume remains greater than zero.
        """
        generator = SeignorageModelRandomPurchaseGenerator(
            token=self.token,
            wallets_generator=self.wallets_generator
        )
        updated_volume = generator._compute_volume()
        self.assertGreater(updated_volume, 0)


    def test_seignorage_purchase_generator_initialization(self):
        """Test correct initialization of SeignorageModelPurchaseGenerator."""
        initial_volumes = [1000, 2000, 3000]
        generator = SeignorageModelPurchaseGenerator(
            self.token,
            initial_volumes
        )
        self.assertEqual(generator.volumes, initial_volumes)
        self.assertEqual(generator.mean, 0.0)
        self.assertEqual(generator.variance, 1.0)

    def test_seignorage_purchase_generator_invalid_volumes(self):
        """Test error when initial volumes are invalid."""
        with self.assertRaises(TypeError):
            SeignorageModelPurchaseGenerator(
                token=self.token,
                initial_volumes="invalid_volumes"  # Volumes must be a list
            )

    def test_seignorage_purchase_generator_transaction_amount(self):
        """
        Test correct generation of transaction amounts using pre-defined volumes.
        Checks that the generated amount matches expected behavior.
        """
        initial_volumes = [1000.0, 2000.0, 3000.0]
        generator = SeignorageModelPurchaseGenerator(
            self.token,
            initial_volumes
        )
        amount = generator.generate_transaction_amount()
        self.assertIsInstance(amount, float)
        self.assertEqual(generator.volumes, [2000.0, 3000.0])

    def test_seignorage_purchase_generator_empty_volumes(self):
        """Test exception handling when no volumes are left to process."""
        generator = SeignorageModelPurchaseGenerator(
            token=self.token,
            initial_volumes=[]  # Empty volume list
        )
        with self.assertRaises(IndexError):
            generator.generate_transaction_amount()

    def test_compute_mean_variation(self):
        """Test correct computation of mean variation based on stablecoin price."""
        generator = SeignorageModelRandomPurchaseGenerator(
            token=self.token,
            wallets_generator=self.wallets_generator,
        )
        self.token.price = 1
        generator._compute_mean_variation(self.token)
        self.assertEqual(generator.mean, 0.0)  # Stable market

        self.token.price = 1.05
        generator._compute_mean_variation(self.token)
        self.assertEqual(generator.mean, 0.0)  # Stable market

        self.token.price = 0.97
        generator._compute_mean_variation(self.token)
        self.assertEqual(generator.mean, 0.0)  # Stable market

        self.token.price = 0.80
        generator._compute_mean_variation(self.token)
        self.assertNotEqual(generator.mean, 0.0)  # Market panic
        self.assertGreater(generator.mean, 0.0) # Market panic


if __name__ == "__main__":
    unittest.main()

