import unittest
from unittest.mock import MagicMock
from source.liquidity_pools.liquidity_pool import LiquidityPool
from source.liquidity_pools.virtual_liquidity_pool import VirtualLiquidityPool
from source.tokens.algorithmic_stablecoin import AlgorithmicStablecoin
from source.tokens.collateral_token import CollateralToken
from source.tokens.reference_token import ReferenceToken
from source.purchase_generators.purchase_generator import PurchaseGenerator
from source.simulations.three_pools_simulation import ThreePoolsSimulation


class TestThreePoolsSimulation(unittest.TestCase):
    def setUp(self):
        """
        Set up the environment for testing the ThreePoolsSimulation class.
        Creates mock objects and initializes the simulation instance.
        """
        # Mock tokens
        self.stablecoin_token = MagicMock(spec=AlgorithmicStablecoin)
        self.stablecoin_token.price = 1.0
        self.stablecoin_token.supply = 1000000.0
        self.stablecoin_token.free_supply = 800000.0

        self.collateral_token = MagicMock(spec=CollateralToken)
        self.collateral_token.price = 50.0
        self.collateral_token.supply = 50000.0
        self.collateral_token.free_supply = 40000.0

        self.reference_token = MagicMock(spec=ReferenceToken)

        # Mock pools
        self.stablecoin_pool = MagicMock(spec=LiquidityPool)
        self.collateral_pool = MagicMock(spec=LiquidityPool)
        self.virtual_pool = MagicMock(spec=VirtualLiquidityPool)
        self.virtual_pool.delta = 0.0

        # Mock purchase generators
        self.stablecoin_purchase_generator = MagicMock(spec=PurchaseGenerator)
        self.collateral_purchase_generator = MagicMock(spec=PurchaseGenerator)

        # Initial parameters
        self.initial_collateral_token_price = 50.0
        self.number_of_iterations = 5

        # Initialize the simulation
        self.simulation = ThreePoolsSimulation(
            stablecoin_token=self.stablecoin_token,
            collateral_token=self.collateral_token,
            reference_token=self.reference_token,
            stablecoin_pool=self.stablecoin_pool,
            collateral_pool=self.collateral_pool,
            virtual_pool=self.virtual_pool,
            stablecoin_purchase_generator=self.stablecoin_purchase_generator,
            collateral_purchase_generator=self.collateral_purchase_generator,
            initial_collateral_token_price=self.initial_collateral_token_price,
            number_of_iterations=self.number_of_iterations
        )

    def test_initialization(self):
        """
        Test that the ThreePoolsSimulation is initialized correctly.
        """
        self.assertIs(self.simulation.stablecoin_token, self.stablecoin_token)
        self.assertIs(self.simulation.collateral_token, self.collateral_token)
        self.assertIs(self.simulation.reference_token, self.reference_token)
        self.assertIs(self.simulation.stablecoin_pool, self.stablecoin_pool)
        self.assertIs(self.simulation.collateral_pool, self.collateral_pool)
        self.assertIs(self.simulation.virtual_pool, self.virtual_pool)
        self.assertEqual(self.simulation.initial_collateral_token_price, self.initial_collateral_token_price)
        self.assertEqual(self.simulation.number_of_iterations, self.number_of_iterations)

    def test_run_simulation(self):
        """
        Test that the run_simulation method executes correctly and returns the expected structure.
        """
        # Mock the behavior of market simulator
        self.simulation.market_simulator.execute_random_purchases = MagicMock()

        # Run the simulation
        result = self.simulation.run_simulation()

        # Check the structure of the result
        self.assertIsInstance(result, dict)
        expected_keys = [
            "stablecoin_price_history",
            "collateral_price_history",
            "stablecoin_supply_history",
            "collateral_supply_history",
            "stablecoin_free_supply_history",
            "collateral_free_supply_history",
            "virtual_pool_delta"
        ]
        self.assertCountEqual(result.keys(), expected_keys)

        # Ensure the lengths of history arrays match the number of iterations
        for key in expected_keys:
            self.assertEqual(len(result[key]), self.number_of_iterations)

        # Verify market simulator is called the expected number of times
        self.assertEqual(self.simulation.market_simulator.execute_random_purchases.call_count,
                         self.number_of_iterations)

    def test_run_simulation_data_consistency(self):
        """
        Test that the run_simulation method collects data correctly.
        """
        # Mock token and virtual pool updates
        self.stablecoin_token.price = 1.0
        self.stablecoin_token.supply = 1000000.0
        self.stablecoin_token.free_supply = 800000.0

        self.collateral_token.price = 50.0
        self.collateral_token.supply = 50000.0
        self.collateral_token.free_supply = 40000.0

        self.virtual_pool.delta = 0.0

        def mock_execute_random_purchases():
            self.stablecoin_token.price += 0.01
            self.collateral_token.price -= 0.5
            self.virtual_pool.delta += 0.1

        self.simulation.market_simulator.execute_random_purchases = mock_execute_random_purchases

        # Run the simulation
        result = self.simulation.run_simulation()

        # Verify the data collected reflects the expected changes
        self.assertEqual(result["stablecoin_price_history"][0], 1.0)
        self.assertAlmostEqual(result["stablecoin_price_history"][-1], 1.0 + 0.01 * (self.number_of_iterations - 1),
                               places=6)

        self.assertEqual(result["collateral_price_history"][0], 50.0)
        self.assertAlmostEqual(result["collateral_price_history"][-1], 50.0 - 0.5 * (self.number_of_iterations - 1),
                               places=6)

        self.assertEqual(result["virtual_pool_delta"][0], 0.0)
        self.assertAlmostEqual(result["virtual_pool_delta"][-1], 0.1 * (self.number_of_iterations - 1), places=6)


if __name__ == '__main__':
    unittest.main()
