import unittest
from source.LiquidityPools.constant_product_formula import ConstantProductFormula
from source.LiquidityPools.improved_virtual_liquidity_pool import ImprovedVirtualLiquidityPool
from source.LiquidityPools.simple_virtual_liquidity_pool import SimpleVirtualLiquidityPool
from source.Tokens.algorithmic_stablecoin import AlgorithmicStablecoin
from source.Tokens.collateral_token import CollateralToken


class TestSimpleVirtualLiquidityPool(unittest.TestCase):
    def setUp(self):
        """
        Initialize a test instance of SimpleVirtualLiquidityPool with valid values.
        """
        stablecoin = AlgorithmicStablecoin("Stablecoin", 1000000, 1.0)
        collateral = CollateralToken("Collateral", 1000000, 5.0)
        formula = ConstantProductFormula()

        self.pool = SimpleVirtualLiquidityPool(
            stablecoin=stablecoin,
            collateral=collateral,
            stablecoin_base_quantity=1000,
            fee=0.003,
            formula=formula,
            pool_recovery_period=10
        )

    def test_initialization(self):
        """
        Verify that the pool initializes with correct attributes.
        """
        self.assertEqual(self.pool.delta, 0)
        self.assertEqual(self.pool.collateral_price, 5.0)

    def test_restore_delta_normal(self):
        """
        Test restore_delta reduces delta as expected in normal conditions.
        """
        self.pool.delta = 100.0
        self.pool.restore_delta()
        expected_delta = 100 * (1 - 1 / self.pool.pool_recovery_period)
        self.assertAlmostEqual(self.pool.delta, expected_delta, places=5)

    def test_restore_delta_high_delta(self):
        """
        Test restore_delta when delta is very high.
        """
        self.pool.delta = 1e6
        self.pool.restore_delta()
        expected_delta = 1e6 * (1 - 1 / self.pool.pool_recovery_period)
        self.assertAlmostEqual(self.pool.delta, expected_delta, places=5)

    def test_update_delta_increase(self):
        """
        Test update_delta increases delta by the specified variation.
        """
        self.pool.update_delta(0.05)
        self.assertEqual(self.pool.delta, 0.05)

    def test_update_delta_decrease(self):
        """
        Test update_delta decreases delta when variation is negative.
        """
        self.pool.update_delta(-0.05)
        self.assertEqual(self.pool.delta, -0.05)

    def test_reset_replenishing_system(self):
        """
        Test that reset_replenishing_system resets delta to zero.
        """
        self.pool.delta = 100
        self.pool.reset_replenishing_system()
        self.assertEqual(self.pool.delta, 0)

    def test_invalid_initialization(self):
        """
        Ensure invalid inputs for collateral_price raise exceptions.
        """
        with self.assertRaises(ValueError):
            SimpleVirtualLiquidityPool(
                stablecoin=AlgorithmicStablecoin("Stablecoin", 1000000, 1.0),
                collateral=CollateralToken("Collateral", 1000000, 5.0),
                stablecoin_base_quantity=-10,
                fee=-1.0,
                formula=ConstantProductFormula(),
                pool_recovery_period=0
            )

    def test_swap_stablecoin_for_collateral_and_replenishing_mechanism(self):
        """
        Test stablecoin swap adjusts delta as expected.
        """
        self.pool.delta = 0
        stablecoin_quantity = self.pool.stablecoin_base_quantity
        initial_collateral_quantity = self.pool.quantity_token_b
        token, obtained_collateral_quantity = self.pool.swap(self.pool.token_a, 10.0)
        self.assertEqual(self.pool.delta, 10.0)
        self.assertEqual(self.pool.quantity_token_a, stablecoin_quantity + 10.0)
        self.pool.perform_pool_replenishing()
        self.assertAlmostEqual(self.pool.quantity_token_a, stablecoin_quantity + 9.0, places=1)
        self.assertAlmostEqual(self.pool.quantity_token_b,
                               initial_collateral_quantity - obtained_collateral_quantity * 0.9, places=1)

    def test_swap_collateral_for_stablecoin(self):
        """
        Test collateral swap adjusts delta as expected.
        """
        self.pool.delta = 0
        stablecoin_quantity = self.pool.stablecoin_base_quantity
        initial_collateral_quantity = self.pool.quantity_token_b
        token, obtained_stablecoin_quantity = self.pool.swap(self.pool.token_b, 10.0)
        self.assertEqual(self.pool.delta, -obtained_stablecoin_quantity)
        self.assertEqual(self.pool.quantity_token_b, initial_collateral_quantity + 10.0)
        self.pool.perform_pool_replenishing()
        self.assertAlmostEqual(self.pool.quantity_token_a, stablecoin_quantity - obtained_stablecoin_quantity * 0.9,
                               places=1)
        self.assertAlmostEqual(self.pool.quantity_token_b, initial_collateral_quantity + 9.0, places=1)


class TestImprovedVirtualLiquidityPool(unittest.TestCase):
    def setUp(self):
        """
        Sets up an instance of ImprovedVirtualLiquidityPool for testing.
        """
        stablecoin = AlgorithmicStablecoin("Stablecoin", 1000000, 1.0)
        collateral = CollateralToken("Collateral", 1000000, 5.0)
        formula = ConstantProductFormula()

        self.pool = ImprovedVirtualLiquidityPool(
            stablecoin=stablecoin,
            collateral=collateral,
            stablecoin_base_quantity=1000,
            fee=0.003,
            formula=formula,
            pool_recovery_period=10
        )

    def test_initialization(self):
        """
        Verify that the pool initializes with correct attributes, including restore_values.
        """
        self.assertEqual(self.pool.delta, 0)
        self.assertEqual(self.pool.collateral_price, 5.0)
        self.assertEqual(self.pool.restore_values, [0] * self.pool.pool_recovery_period)

    def test_restore_delta_normal(self):
        """
        Test restore_delta adjusts delta based on restore_values.
        """
        self.pool.delta = 10.0
        self.pool.restore_values = [0.02] * self.pool.pool_recovery_period
        self.pool.restore_delta()
        expected_delta = 10.0 - 0.02
        self.assertAlmostEqual(self.pool.delta, expected_delta, places=5)

    def test_restore_delta_with_shrink(self):
        """
        Test restore_delta shrinks restore_values based on stablecoin price.
        """
        self.pool.delta = 10.0
        self.pool.update_stablecoin_price(0.91)
        self.pool.restore_values = [1.0] * self.pool.pool_recovery_period
        self.pool.restore_delta()
        self.assertLess(len(self.pool.restore_values), 10)
        self.assertEqual(self.pool.delta, 0)

    def test_update_delta(self):
        """
        Test update_delta updates delta and redistributes delta_variation across restore_values.
        """
        self.pool.delta = 0.1
        self.pool.update_delta(0.1)
        self.assertAlmostEqual(self.pool.delta, 0.2)
        self.assertTrue(all(val > 0 for val in self.pool.restore_values))

    def test_shrink_restore_values(self):
        """
        Test shrink_restore_values reduces restore_values and redistributes excess sum.
        """
        self.pool.restore_values = [0.02] * 10
        self.pool.shrink_restore_values(5)
        self.assertEqual(len(self.pool.restore_values), 5)
        self.assertAlmostEqual(float(sum(self.pool.restore_values)), 0.2)

    def test_reset_replenishing_system(self):
        """
        Test that reset_replenishing_system resets delta and restore_values.
        """
        self.pool.delta = 10.0
        self.pool.reset_replenishing_system()
        self.assertEqual(self.pool.delta, 0)
        self.assertEqual(self.pool.restore_values, [0] * 10)

    def test_invalid_shrink_restore_values(self):
        """
        Ensure shrink_restore_values handles invalid lengths gracefully.
        """
        with self.assertRaises(ValueError):
            self.pool.shrink_restore_values(-1)

    def test_price_below_all_thresholds(self):
        """
        Test when stablecoin_price is below all thresholds in values.
        """
        self.pool.stablecoin_price = 0.949
        new_length = self.pool.compute_restore_values_new_length()
        self.assertEqual(1, new_length, "New length should be 1 when price is below all thresholds.")

    def test_price_exceeds_some_thresholds(self):
        """
        Test when stablecoin_price exceeds some thresholds in values.
        """
        self.pool.stablecoin_price = 0.981
        new_length = self.pool.compute_restore_values_new_length()
        expected_length = self.pool.pool_recovery_period * (1 - (2 * 0.1))
        self.assertAlmostEqual(new_length, expected_length, places=2, msg="New length does not match expected value.")

    def test_price_exceeds_all_thresholds(self):
        """
        Test when stablecoin_price exceeds all thresholds in values.
        """
        self.pool.stablecoin_price = 1.0
        new_length = self.pool.compute_restore_values_new_length()
        expected_length = self.pool.pool_recovery_period
        self.assertEqual(new_length, expected_length, "New length should be maximum when price exceeds all thresholds.")

    def test_threshold_edge_case(self):
        """
        Test when stablecoin_price is exactly on a threshold.
        """
        self.pool.stablecoin_price = 0.95
        new_length = self.pool.compute_restore_values_new_length()
        self.assertEqual(new_length, 1, "New length should be 1 when price is exactly on the first threshold.")

    def test_invalid_initialization(self):
        """
        Ensure invalid inputs for collateral_price raise exceptions.
        """
        with self.assertRaises(ValueError):
            ImprovedVirtualLiquidityPool(
                stablecoin=AlgorithmicStablecoin("Stablecoin", 1000000, 1.0),
                collateral=CollateralToken("Collateral", 1000000, 5.0),
                stablecoin_base_quantity=-10,
                fee=-1.0,
                formula=ConstantProductFormula(),
                pool_recovery_period=0
            )

    def test_swap_stablecoin_for_collateral_and_replenishing_mechanism(self):
        """
        Test stablecoin swap adjusts delta as expected.
        """
        self.pool.delta = 0
        stablecoin_quantity = self.pool.stablecoin_base_quantity
        initial_collateral_quantity = self.pool.quantity_token_b
        token, obtained_collateral_quantity = self.pool.swap(self.pool.token_a, 10.0)
        self.assertEqual(self.pool.delta, 10.0)
        self.assertEqual(self.pool.quantity_token_a, stablecoin_quantity + 10.0)
        self.pool.perform_pool_replenishing()
        self.assertAlmostEqual(self.pool.quantity_token_a, stablecoin_quantity + 9.0, places=1)
        self.assertAlmostEqual(self.pool.quantity_token_b,
                               initial_collateral_quantity - obtained_collateral_quantity * 0.9, places=1)

    def test_swap_collateral_for_stablecoin(self):
        """
        Test collateral swap adjusts delta as expected.
        """
        self.pool.delta = 0
        stablecoin_quantity = self.pool.stablecoin_base_quantity
        initial_collateral_quantity = self.pool.quantity_token_b
        token, obtained_stablecoin_quantity = self.pool.swap(self.pool.token_b, 10.0)
        self.assertEqual(self.pool.delta, -obtained_stablecoin_quantity)
        self.assertEqual(self.pool.quantity_token_b, initial_collateral_quantity + 10.0)
        self.pool.perform_pool_replenishing()
        self.assertAlmostEqual(self.pool.quantity_token_a, stablecoin_quantity - obtained_stablecoin_quantity * 0.9,
                               places=1)
        self.assertAlmostEqual(self.pool.quantity_token_b, initial_collateral_quantity + 9.0, places=1)


if __name__ == "__main__":
    unittest.main()
