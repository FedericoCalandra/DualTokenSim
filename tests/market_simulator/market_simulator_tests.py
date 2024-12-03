import unittest
from typing import Tuple
from source.arbitrage_optimizer.arbitrage_optimizer import ArbitrageOptimizer
from source.market_simulators.market_simulator import MarketSimulator
from source.liquidity_pools.constant_product_formula import ConstantProductFormula
from source.liquidity_pools.liquidity_pool import LiquidityPool
from source.liquidity_pools.simple_virtual_liquidity_pool import SimpleVirtualLiquidityPool
from source.tokens.algorithmic_stablecoin import AlgorithmicStablecoin
from source.tokens.collateral_token import CollateralToken
from source.tokens.generic_token import GenericToken
from source.tokens.token import Token
from source.purchase_generators.purchase_generator import PurchaseGenerator
from source.wallets_generators.wallets_generator import WalletsGenerator


class TestMarketSimulator(unittest.TestCase):

    def setUp(self):
        self.stablecoin = AlgorithmicStablecoin("TOKEN_A", initial_supply=100000, initial_price=1.0)
        self.collateral = CollateralToken("TOKEN_B", initial_supply=100000, initial_price=5.0)
        self.reference_token = GenericToken("REFERENCE", initial_supply=10 ** 12, initial_price=1.0)
        self.pool_initial_token_quantity = 10000
        self.virtual_pool_base_quantity = 1000
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

        class MockArbitrageOptimizer(ArbitrageOptimizer):
            def leverage_arbitrage_opportunity(self):
                pass

        class MockArbitrageOptimizer2(ArbitrageOptimizer):
            def leverage_arbitrage_opportunity(self):
                self.liquidity_pools[0].swap(self.liquidity_pools[0].token_a, 100)

        self.optimizer1 = MockArbitrageOptimizer(
            liquidity_pools=[self.pool1, self.pool2],
            virtual_liquidity_pool=self.virtual_pool
        )
        self.optimizer2 = MockArbitrageOptimizer2(
            liquidity_pools=[self.pool1, self.pool2],
            virtual_liquidity_pool=self.virtual_pool
        )

        class MockPurchaseGenerator(PurchaseGenerator):
            def generate_random_purchase(self) -> Tuple[Token, float]:
                return self.liquidity_pool.token_a, 1

        self.purchase_generator_1 = MockPurchaseGenerator(self.pool1)
        self.purchase_generator_2 = MockPurchaseGenerator(self.pool2)

        class MockWalletsGenerator(WalletsGenerator):
            def get_random_wallet(self, total_free_token_supply):
                return 10

        self.wallets_generator = MockWalletsGenerator(0.01)

        # Initialize 2 MarketSimulator
        self.simulator1 = MarketSimulator(
            liquidity_pools=[self.pool1, self.pool2],
            virtual_liquidity_pool=self.virtual_pool,
            purchase_generators=[self.purchase_generator_1, self.purchase_generator_2],
            arbitrage_optimizer=self.optimizer1
        )

        self.simulator2 = MarketSimulator(
            liquidity_pools=[self.pool1, self.pool2],
            virtual_liquidity_pool=self.virtual_pool,
            purchase_generators=[self.purchase_generator_1, self.purchase_generator_2],
            arbitrage_optimizer=self.optimizer2
        )

    def test_initialization_valid(self):
        self.assertEqual(len(self.simulator1.liquidity_pools), 2)
        self.assertEqual(self.simulator1.virtual_liquidity_pool, self.virtual_pool)
        self.assertEqual(len(self.simulator1.purchase_generators), 2)
        self.assertEqual(self.simulator1.arbitrage_optimizer, self.optimizer1)

    # noinspection PyTypeChecker
    def test_initialization_invalid_inputs(self):
        with self.assertRaises(ValueError):
            MarketSimulator(liquidity_pools=[], virtual_liquidity_pool=None, purchase_generators=[],
                            arbitrage_optimizer=None)

    def test_random_purchases_success(self):
        self.simulator1.execute_random_purchases()
        self.assertEqual(self.pool1.quantity_token_a, self.pool_initial_token_quantity + 1)
        self.assertEqual(self.pool2.quantity_token_a, self.pool_initial_token_quantity + 1)

    def test_random_purchases_and_arbitrage(self):
        self.simulator2.execute_random_purchases()
        self.assertAlmostEqual(self.pool1.quantity_token_a, self.pool_initial_token_quantity + 100, places=1)


if __name__ == '__main__':
    unittest.main()
