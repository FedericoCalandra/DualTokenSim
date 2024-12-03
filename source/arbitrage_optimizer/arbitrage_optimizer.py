from abc import ABC, abstractmethod
from typing import List
from source.liquidity_pools.liquidity_pool import LiquidityPool
from source.liquidity_pools.virtual_liquidity_pool import VirtualLiquidityPool


class ArbitrageOptimizer(ABC):
    """
    Abstract base class for arbitrage optimization in a market simulation ecosystem.

    This class provides a blueprint for detecting arbitrage opportunities, calculating
    optimal trade quantities for maximum profit, and executing arbitrage operations
    across liquidity pools and a virtual liquidity pool. Concrete implementations must
    define the behavior of all abstract methods.
    """

    def __init__(self, liquidity_pools: List[LiquidityPool], virtual_liquidity_pool: VirtualLiquidityPool):
        """
        Initializes the ArbitrageOptimizer with the given liquidity pools and virtual liquidity pool.

        Args:
            liquidity_pools (List[LiquidityPool]): A list of liquidity pools representing the market.
            virtual_liquidity_pool (VirtualLiquidityPool): The virtual liquidity pool for swaps between AS and CT.
        """
        self.liquidity_pools = liquidity_pools
        self.virtual_liquidity_pool = virtual_liquidity_pool

    @abstractmethod
    def leverage_arbitrage_opportunity(self):
        """
        Abstract method to determine and execute the sequence of arbitrage operations.

        This method must be implemented by subclasses to detect arbitrage opportunities,
        calculate optimal trade quantities, and execute the required trades across the
        liquidity pools and the virtual liquidity pool.

        Subclasses are expected to:
                1. Detect arbitrage opportunities using the respective conditions.
                2. Compute the optimal input quantities to maximize arbitrage profit.
                3. Execute the trade sequence to capitalize on the opportunity.

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.
        """
        pass
