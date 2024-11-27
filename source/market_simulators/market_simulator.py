from typing import List
from source.LiquidityPools.liquidity_pool import LiquidityPool
from source.LiquidityPools.virtual_liquidity_pool import VirtualLiquidityPool
from source.arbitrage_optimizer.arbitrage_optimizer import ArbitrageOptimizer
from source.purchase_generators.purchase_generator import PurchaseGenerator
from source.wallets_generators.wallets_generator import WalletsGenerator


class MarketSimulator:
    """
    Class for simulating market interactions. Provides a structure for simulating market conditions, token
    exchanges, and arbitrage activities.

    Attributes:
        volatility (List[float]): Array representing market volatility values affecting conditions.
        liquidity_pools (List[LiquidityPool]): List of liquidity pool instances managing token exchanges.
        virtual_liquidity_pool (VirtualLiquidityPool): Instance of a virtual liquidity pool for managing price deltas.
        wallets_generators (List[WalletsGenerator]): List of wallet generator instances for simulating user wallets.
        purchase_generators (List[PurchaseGenerator]): List of purchase generator instances for simulating purchases.
        arbitrage_optimizer (ArbitrageOptimizer): Instance responsible for detecting and executing arbitrage
            opportunities across the liquidity pools.
    """

    def __init__(self,
                 volatility: List[float],
                 liquidity_pools: List[LiquidityPool],
                 virtual_liquidity_pool: VirtualLiquidityPool,
                 wallets_generators: List[WalletsGenerator],
                 purchase_generators: List[PurchaseGenerator],
                 arbitrage_optimizer: ArbitrageOptimizer):
        """
        Initializes the MarketSimulator with the provided attributes.

        Args:
            volatility (List[float]): Market volatility values.
            liquidity_pools (List[LiquidityPool]): List of liquidity pool instances.
            virtual_liquidity_pool (VirtualLiquidityPool): Virtual liquidity pool instance.
            wallets_generators (List[WalletsGenerator]): List of wallet generator instances.
            purchase_generators (List[PurchaseGenerator]): List of purchase generator instances.
            arbitrage_optimizer (ArbitrageOptimizer): Arbitrage optimizer instance for handling arbitrage operations.
        """
        self.volatility = volatility
        self.liquidity_pools = liquidity_pools
        self.virtual_liquidity_pool = virtual_liquidity_pool
        self.wallets_generators = wallets_generators
        self.purchase_generators = purchase_generators
        self.arbitrage_optimizer = arbitrage_optimizer

    def random_purchases(self) -> None:
        """
        Simulates random purchase activities across liquidity pools in the market and evaluates arbitrage opportunities.

        After each simulated purchase, the arbitrage optimizer checks for and executes any profitable arbitrage
        opportunities across the pools.

        Returns:
            None
        """
        for pool, generator in zip(self.liquidity_pools, self.purchase_generators):
            input_token, input_amount = generator.generate_random_purchase()
            pool.swap(input_token, input_amount)
            self.arbitrage_optimizer.leverage_arbitrage_opportunity()
