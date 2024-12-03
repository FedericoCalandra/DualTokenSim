import unittest
from unittest.mock import Mock, patch
from source.liquidity_pools.constant_product_formula import ConstantProductFormula
from source.liquidity_pools.liquidity_pool import LiquidityPool
from source.liquidity_pools.simple_virtual_liquidity_pool import SimpleVirtualLiquidityPool
from source.tokens.algorithmic_stablecoin import AlgorithmicStablecoin
from source.tokens.collateral_token import CollateralToken
from source.tokens.generic_token import GenericToken
from source.arbitrage_optimizer.three_pools_arbitrage_optimizer import ThreePoolsArbitrageOptimizer


class TestThreePoolsArbitrageOptimizer(unittest.TestCase):
    def setUp(self):
        # LiquidityPool instances
        self.stablecoin = AlgorithmicStablecoin("TOKEN_A", initial_supply=100000, initial_price=1.0)
        self.collateral = CollateralToken("TOKEN_B", initial_supply=100000, initial_price=5.0)
        self.reference_token = GenericToken("REFERENCE", initial_supply=10 ** 12, initial_price=1.0)
        self.pool_initial_token_quantity = 10000
        self.virtual_pool_base_quantity = 1000
        self.pools_initialization()

    def pools_initialization(self):
        self.pool1 = LiquidityPool(self.stablecoin, self.reference_token,
                                   self.pool_initial_token_quantity/self.stablecoin.price,
                                   self.pool_initial_token_quantity,
                                   0, ConstantProductFormula())
        self.pool2 = LiquidityPool(self.collateral, self.reference_token,
                                   self.pool_initial_token_quantity/self.collateral.price,
                                   self.pool_initial_token_quantity,
                                   0, ConstantProductFormula())
        self.virtual_pool = SimpleVirtualLiquidityPool(self.stablecoin, self.collateral,
                                                       self.virtual_pool_base_quantity,
                                                       0, ConstantProductFormula(),
                                                       pool_recovery_period=10)
        # Initialize optimizer
        self.optimizer = ThreePoolsArbitrageOptimizer(
            liquidity_pools=[self.pool1, self.pool2],
            virtual_liquidity_pool=self.virtual_pool
        )

    def test_initialization(self):
        """Test proper initialization of the optimizer."""
        self.assertEqual(self.optimizer.liquidity_pools, [self.pool1, self.pool2])
        self.assertEqual(self.optimizer.virtual_liquidity_pool, self.virtual_pool)
        self.assertEqual(self.optimizer.max_arbitrage_input, 10 ** 6)
        self.assertEqual(self.optimizer.threshold, 0.001)

    def test_detect_arbitrage_no_opportunity(self):
        """Test detect_arbitrage when no arbitrage opportunity exists."""
        self.pool1.token_a.price = 1.0
        self.pool2.token_a.price = 5.0
        self.virtual_pool.quantity_token_a = 1000
        self.virtual_pool.quantity_token_b = 1000 / self.pool2.token_a.price

        arbitrage_type, exists = self.optimizer.detect_arbitrage()
        self.assertFalse(exists)
        self.assertEqual(arbitrage_type, '')

    def test_detect_arbitrage_type1(self):
        """Test detect_arbitrage detects Type 1 arbitrage."""
        self.pool1.token_a.price = 1.2
        self.pool2.token_a.price = 5.0
        self.virtual_pool.quantity_token_a = 1000
        self.virtual_pool.quantity_token_b = 1000 / self.pool2.token_a.price

        arbitrage_type, exists = self.optimizer.detect_arbitrage()
        self.assertTrue(exists)
        self.assertEqual(arbitrage_type, 'Type 1')

    def test_detect_arbitrage_type2(self):
        """Test detect_arbitrage detects Type 2 arbitrage."""
        self.pool1.token_a.price = 0.8
        self.pool2.token_a.price = 5.0
        self.virtual_pool.quantity_token_a = 1000
        self.virtual_pool.quantity_token_b = 1000 / self.pool2.token_a.price

        arbitrage_type, exists = self.optimizer.detect_arbitrage()
        self.assertTrue(exists)
        self.assertEqual(arbitrage_type, 'Type 2')

    @patch('source.arbitrage_optimizer.three_pools_arbitrage_optimizer.minimize_scalar')
    def test_compute_max_arbitrage_profit_success(self, mock_minimize):
        """Test compute_max_arbitrage_profit when optimization is successful."""
        mock_minimize.return_value.success = True
        mock_minimize.return_value.x = 50.0

        result = self.optimizer.compute_max_arbitrage_profit("Type 1")
        self.assertEqual(result, 50.0)
        mock_minimize.assert_called_once()

    @patch('source.arbitrage_optimizer.three_pools_arbitrage_optimizer.minimize_scalar')
    def test_compute_max_arbitrage_profit_failure(self, mock_minimize):
        """Test compute_max_arbitrage_profit when optimization fails."""
        mock_minimize.return_value.success = False

        with self.assertRaises(ValueError):
            self.optimizer.compute_max_arbitrage_profit("Type 1")

    def test_get_arbitrage_profit_type1(self):
        """Test get_arbitrage_profit for Type 1 arbitrage."""
        self.pool1.token_a.price = 1.2
        self.pool2.token_a.price = 5.0
        self.pools_initialization()

        profit = self.optimizer.get_arbitrage_profit("Type 1", 1.0)
        self.assertAlmostEqual(profit, 0.2, places=2)

    def test_get_arbitrage_profit_type2(self):
        """Test get_arbitrage_profit for Type 2 arbitrage."""
        self.pool1.token_a.price = 0.8
        self.pool2.token_a.price = 5.0
        self.pools_initialization()

        profit = self.optimizer.get_arbitrage_profit("Type 2", 1.0)
        self.assertAlmostEqual(profit, 0.25, places=2)

    def test_get_arbitrage_profit_no_input(self):
        """Test get_arbitrage_profit when input quantity is zero."""
        profit = self.optimizer.get_arbitrage_profit("Type 1", 0.0)
        self.assertEqual(profit, 0)

    def test_leverage_arbitrage_opportunity_type1(self):
        """Test leverage_arbitrage_opportunity for Type 1."""
        self.pool1.token_a.price = 1.2
        self.pool2.token_a.price = 5.0
        self.pools_initialization()

        self.optimizer.leverage_arbitrage_opportunity()

        self.assertEqual(self.stablecoin.price, 1.0)

    def test_leverage_arbitrage_opportunity_type2(self, mock_compute_profit):
        """Test leverage_arbitrage_opportunity for Type 2."""
        self.pool1.token_a.price = 0.8
        self.pool2.token_a.price = 5.0
        self.pools_initialization()

        self.optimizer.leverage_arbitrage_opportunity()

        self.assertEqual(self.stablecoin.price, 1.0)


if __name__ == '__main__':
    unittest.main()
