from typing import List
from source.liquidity_pools.liquidity_pool import LiquidityPool
from source.liquidity_pools.virtual_liquidity_pool import VirtualLiquidityPool
from source.arbitrage_optimizer.arbitrage_optimizer import ArbitrageOptimizer
from source.purchase_generators.purchase_generator import PurchaseGenerator


class MarketSimulator:
    """
    Class for simulating market interactions. Provides a structure for simulating market conditions, token
    exchanges, and arbitrage activities.

    Attributes:
        liquidity_pools (List[LiquidityPool]): List of liquidity pool instances managing token exchanges.
        virtual_liquidity_pool (VirtualLiquidityPool): Instance of a virtual liquidity pool for managing price deltas.
        purchase_generators (List[PurchaseGenerator]): List of purchase generator instances for simulating purchases.
        arbitrage_optimizer (ArbitrageOptimizer): Instance responsible for detecting and executing arbitrage
            opportunities across the liquidity pools.
    """

    def __init__(self,
                 liquidity_pools: List[LiquidityPool],
                 virtual_liquidity_pool: VirtualLiquidityPool,
                 purchase_generators: List[PurchaseGenerator],
                 arbitrage_optimizer: ArbitrageOptimizer):
        """
        Initializes the MarketSimulator with the provided attributes.

        Args:
            liquidity_pools (List[LiquidityPool]): List of liquidity pool instances.
            virtual_liquidity_pool (VirtualLiquidityPool): Virtual liquidity pool instance.
            purchase_generators (List[PurchaseGenerator]): List of purchase generator instances.
            arbitrage_optimizer (ArbitrageOptimizer): Arbitrage optimizer instance for handling arbitrage operations.
        """
        if not isinstance(liquidity_pools, list) or not all(isinstance(lp, LiquidityPool) for lp in liquidity_pools):
            raise ValueError("liquidity_pools must be a list of LiquidityPool instances.")

        if not isinstance(virtual_liquidity_pool, VirtualLiquidityPool):
            raise ValueError("virtual_liquidity_pool must be an instance of VirtualLiquidityPool.")

        if not isinstance(purchase_generators, list) or not all(
                isinstance(pg, PurchaseGenerator) for pg in purchase_generators):
            raise ValueError("purchase_generators must be a list of PurchaseGenerator instances.")

        if not isinstance(arbitrage_optimizer, ArbitrageOptimizer):
            raise ValueError("arbitrage_optimizer must be an instance of ArbitrageOptimizer.")

        self.liquidity_pools = liquidity_pools
        self.virtual_liquidity_pool = virtual_liquidity_pool
        self.purchase_generators = purchase_generators
        self.arbitrage_optimizer = arbitrage_optimizer

    def execute_random_purchases(self) -> None:
        """
        Simulates random purchase activities across liquidity pools in the market and evaluates arbitrage opportunities.

        After each simulated purchase, the arbitrage optimizer checks for and executes any profitable arbitrage
        opportunities across the pools.

        Returns:
            None
        """
        for pool, generator in zip(self.liquidity_pools, self.purchase_generators):
            amount = generator.generate_random_purchase()
            pool.swap(pool.token_a, amount)
            self.arbitrage_optimizer.leverage_arbitrage_opportunity()
