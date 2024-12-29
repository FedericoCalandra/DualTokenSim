import unittest
import numpy as np
from scipy.stats import norm
from matplotlib import pyplot as plt
from source.liquidity_pools.constant_product_formula import ConstantProductFormula
from source.liquidity_pools.liquidity_pool import LiquidityPool
from source.tokens.reference_token import ReferenceToken
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
            "TestStablecoin", 100000.0, 10000.0, 1.0, 1.0)
        # Initialize a collateral token for additional tests.
        self.collateral_token = CollateralToken(
            "TestCollateralToken", 100000.0, 10000.0, 1.0, self.token)
        # Create a wallet generator.

    def test_random_purchase_generator_initialization(self):
        """Test correct initialization of SeignorageModelRandomPurchaseGenerator."""
        generator = SeignorageModelRandomPurchaseGenerator(
            token=self.token,
            volatility_variance=500,
            initial_volatility=1000,
            amount_variance=1.0,
            amount_mean=1.0,
            delta_variation=lambda x: x * 0.1,
            threshold=0.05
        )
        self.assertEqual(generator.volatility_variance, 500)
        self.assertEqual(generator.volatility, [1000])
        self.assertEqual(generator.amount_variance, 1.0)
        self.assertEqual(generator.amount_mean, 1.0)
        self.assertEqual(generator.threshold, 0.05)

    def test_random_purchase_generator_invalid_token(self):
        """Test whether an error is raised when the token is invalid."""
        with self.assertRaises(TypeError):
            SeignorageModelRandomPurchaseGenerator(
                token=Token("InvalidToken"),  # Invalid token
            )

    def test_random_purchase_generator_transaction_amount(self):
        """
        Test that the transaction amount generated can be both positive or negative.
        Ensures correct handling of market dynamics.
        """
        generator = SeignorageModelRandomPurchaseGenerator(
            token=self.token
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
            token=self.token
        )
        generator._compute_volatility()
        updated_volatility = generator.volatility[1]
        self.assertGreater(updated_volatility, 0)

    def test_seignorage_purchase_generator_initialization(self):
        """Test correct initialization of SeignorageModelPurchaseGenerator."""
        initial_volatility = [1000, 2000, 3000]
        generator = SeignorageModelPurchaseGenerator(
            self.token,
            initial_volatility
        )
        self.assertEqual(generator.volatility, initial_volatility)
        self.assertEqual(generator.amount_mean, 0.0)
        self.assertEqual(generator.amount_variance, 1.0)

    def test_seignorage_purchase_generator_invalid_volumes(self):
        """Test error when initial volumes are invalid."""
        with self.assertRaises(TypeError):
            SeignorageModelPurchaseGenerator(
                token=self.token
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
        self.assertEqual(generator.volatility, [2000.0, 3000.0])

    def test_seignorage_purchase_generator_empty_volumes(self):
        """Test exception handling when no volumes are left to process."""
        generator = SeignorageModelPurchaseGenerator(
            token=self.token,
            volatility=[]  # Empty volume list
        )
        with self.assertRaises(IndexError):
            generator.generate_transaction_amount()

    def test_compute_mean_variation(self):
        """Test correct computation of mean variation based on stablecoin price."""
        generator = SeignorageModelRandomPurchaseGenerator(
            token=self.token,
        )
        self.token.price = 1
        generator._compute_mean_variation(self.token)
        self.assertEqual(generator.amount_mean, 0.0)  # Stable market

        self.token.price = 1.05
        generator._compute_mean_variation(self.token)
        self.assertEqual(generator.amount_mean, 0.0)  # Stable market

        self.token.price = 0.97
        generator._compute_mean_variation(self.token)
        self.assertEqual(generator.amount_mean, 0.0)  # Stable market

        self.token.price = 0.80
        generator._compute_mean_variation(self.token)
        self.assertNotEqual(generator.amount_mean, 0.0)  # Market panic
        self.assertGreater(generator.amount_mean, 0.0)  # Market panic

    def test_generate_transaction_amount_distribution(self):
        """
        Test that the generate_transaction_amount method produces a mix of positive and negative trades.
        """
        generator = SeignorageModelRandomPurchaseGenerator(
            token=self.token,
            volatility_variance=1.0,
            initial_volatility=100.0,
            amount_variance=10.0,
            amount_mean=0.0,
            delta_variation=lambda x: 1 / x,
            threshold=0.05
        )

        transaction_amounts = []
        for _ in range(1000):
            transaction_amount = generator.generate_transaction_amount()
            transaction_amounts.append(transaction_amount)

        # Log some statistics
        mean_value = np.mean(transaction_amounts)
        positive_count = sum(1 for x in transaction_amounts if x > 0)
        negative_count = sum(1 for x in transaction_amounts if x < 0)

        print(f"Mean transaction amount: {mean_value}")
        print(f"Positive trades: {positive_count}")
        print(f"Negative trades: {negative_count}")

        # Visualization (optional for debugging)
        plt.hist(transaction_amounts, bins=50, color="blue", alpha=0.7)
        plt.axvline(0, color="red", linestyle="--", label="Zero Line")
        plt.title("Distribution of Transaction Amounts")
        plt.xlabel("Transaction Amount")
        plt.ylabel("Frequency")
        plt.legend()
        plt.show()

        # Check if there is a reasonable mix of positive and negative trades
        self.assertGreater(positive_count, 0, "No positive trades generated!")
        self.assertGreater(negative_count, 0, "No negative trades generated!")
        self.assertTrue(
            0.4 <= positive_count / len(transaction_amounts) <= 0.6,
            "Positive and negative trades are not balanced."
        )

    def test_market_dynamics_simulation(self):
        """
        Simulate market dynamics and analyze the final stablecoin prices.
        Expected behavior: Prices should follow a Gaussian distribution with mean equal to the initial price.
        """
        # Parameters
        stablecoin_initial_price = 0.9997794183
        stablecoin_initial_supply = 18_490_738_908
        stablecoin_initial_free_supply = stablecoin_initial_supply * 0.995
        stablecoin_pool_fee = 0.1
        num_simulations = 1000
        num_iterations_per_simulation = 1000

        # Initialize stablecoin and its liquidity pool
        cpf = ConstantProductFormula()
        stablecoin = AlgorithmicStablecoin(
            name="AS",
            peg=1.0,
            initial_price=stablecoin_initial_price,
            initial_supply=stablecoin_initial_supply,
            initial_free_supply=stablecoin_initial_free_supply
        )
        reference_token = ReferenceToken(
            name="USD"
        )
        stablecoin_pool_quantity = stablecoin_initial_supply - stablecoin_initial_free_supply
        stablecoin_pool_reference_quantity = stablecoin_pool_quantity * stablecoin_initial_price

        stablecoin_pool = LiquidityPool(
            token_a=stablecoin,
            token_b=reference_token,
            quantity_token_a=stablecoin_pool_quantity,
            quantity_token_b=stablecoin_pool_reference_quantity,
            formula=cpf,
            fee=stablecoin_pool_fee
        )

        # Initialize purchase generator
        stablecoin_purchase_generator = SeignorageModelRandomPurchaseGenerator(
            token=stablecoin,
            volatility_variance=10.0,
            initial_volatility=38_033.764375,
            amount_variance=1.0,
            amount_mean=0.0,
            delta_variation=lambda x: 1 / x - 1,
            threshold=0.05,
            pool_fee=stablecoin_pool_fee
        )

        # Simulation
        final_prices = []
        mean_amounts = []
        for i in range(num_simulations):
            generated_amounts = []
            stablecoin_pool.quantity_token_a = stablecoin_pool_quantity
            stablecoin_pool.quantity_token_b = stablecoin_pool_reference_quantity
            for _ in range(num_iterations_per_simulation):
                amount = stablecoin_purchase_generator.generate_transaction_amount()
                stablecoin_pool.swap(stablecoin, amount)
                stablecoin.price = stablecoin_pool.quantity_token_b / stablecoin_pool.quantity_token_a
                generated_amounts.append(amount)
            mean_amounts.append(np.mean(generated_amounts))
            final_prices.append(stablecoin.price)

        # Analyze the results
        mean_price = np.mean(final_prices)
        std_price = np.std(final_prices)

        # Print/log statistics
        print(f"Mean final price: {mean_price}")
        print(f"Standard deviation of final prices: {std_price}")
        print(f"Mean generated amounts: {np.mean(mean_amounts)}")

        # Visualization (optional for debugging)
        plt.figure(figsize=(12, 6))
        plt.subplot(1, 2, 1)

        # Define plot range centered around 1.0 with limits based on standard deviation
        x_center = stablecoin_initial_price
        x_min = x_center - 4 * std_price
        x_max = x_center + 4 * std_price

        # Plot histogram
        plt.hist(final_prices, bins=50, color="blue", alpha=0.7, density=True, label="Observed Prices")

        # Plot expected Gaussian curve
        x = np.linspace(x_min, x_max, 100)
        plt.plot(x, norm.pdf(x, loc=stablecoin_initial_price, scale=std_price), 'r-', label="Expected Gaussian")

        # Configure plot limits and labels
        plt.xlim(x_min, x_max)
        plt.title("Final Stablecoin Prices (Centered Around Initial Price)")
        plt.xlabel("Price")
        plt.ylabel("Frequency")
        plt.legend()
        plt.grid(True)

        # Generated Amount Plot
        plt.subplot(1, 2, 2)

        plt.hist(mean_amounts, bins=50, color="green", alpha=0.7, label="Generated Amounts")
        plt.axvline(x=0, color="red", linestyle="--", label="Zero Line")
        plt.title("Generated Transaction Amounts")
        plt.xlabel("Transaction Amount")
        plt.ylabel("Frequency")
        plt.legend()
        plt.grid(True)

        # Show both plots
        plt.tight_layout()
        plt.show()

        # Verify results
        self.assertAlmostEqual(float(mean_price), stablecoin_initial_price, delta=0.1,
                               msg="Mean final price deviates significantly from the initial price.")
        self.assertGreater(
            std_price, 0, "Standard deviation of final prices should be positive."
        )


if __name__ == "__main__":
    unittest.main()

