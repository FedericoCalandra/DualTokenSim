from abc import ABC, abstractmethod
from typing import List

from source.LiquidityPools.liquidity_pool import LiquidityPool
from source.LiquidityPools.virtual_liquidity_pool import VirtualLiquidityPool
from source.purchase_generators.purchase_generator import PurchaseGenerator
from source.wallets_generators.wallets_generator import WalletsGenerator


class MarketSimulator(ABC):
    """
    Abstract base class for simulating market interactions. Provides a structure for simulating market conditions, token
     exchanges, and arbitrage activities.

    Attributes:
        volatility (List[float]): Array representing market volatility values affecting conditions.
        liquidity_pools (List[LiquidityPool]): List of liquidity pool instances managing token exchanges.
        virtual_liquidity_pool (VirtualLiquidityPool): Instance of a virtual liquidity pool for managing price deltas.
        wallets_generators (List[WalletsGenerator]): List of wallet generator instances for simulating user wallets.
        purchase_generators (List[PurchaseGenerator]): List of purchase generator instances for simulating purchases.
        total_free_stablecoin_supply (float): Total free supply of stablecoins available in the simulation.
        total_free_collateral_supply (float): Total free supply of collateral tokens available in the simulation.
        total_free_reference_supply (float): Total free supply of reference tokens available in the simulation.
    """

    def __init__(self,
                 volatility: List[float],
                 liquidity_pools: List[LiquidityPool],
                 virtual_liquidity_pool: VirtualLiquidityPool,
                 wallets_generators: List[WalletsGenerator],
                 purchase_generators: List[PurchaseGenerator],
                 total_free_stablecoin_supply: float,
                 total_free_collateral_supply: float,
                 total_free_reference_supply: float):
        """
        Initializes the MarketSimulator with the provided attributes.

        Args:
            volatility (List[float]): Market volatility values.
            liquidity_pools (List[LiquidityPool]): List of liquidity pool instances.
            virtual_liquidity_pool (VirtualLiquidityPool): Virtual liquidity pool instance.
            wallets_generators (List[WalletsGenerator]): List of wallet generator instances.
            purchase_generators (List[PurchaseGenerator]): List of purchase generator instances.
            total_free_stablecoin_supply (float): Total stablecoin supply available.
            total_free_collateral_supply (float): Total collateral token supply available.
            total_free_reference_supply (float): Total reference token supply available.
        """
        self.volatility = volatility
        self.liquidity_pools = liquidity_pools
        self.virtual_liquidity_pool = virtual_liquidity_pool
        self.wallets_generators = wallets_generators
        self.purchase_generators = purchase_generators
        self.total_free_stablecoin_supply = total_free_stablecoin_supply
        self.total_free_collateral_supply = total_free_collateral_supply
        self.total_free_reference_supply = total_free_reference_supply

    @abstractmethod
    def random_purchases(self) -> None:
        """
        Simulates random purchase activities across liquidity pools in the market. This method should be implemented by
        subclasses to distribute purchases realistically based on market conditions and liquidity pool states.

        Returns:
            None
        """
        pass

    @abstractmethod
    def leverage_arbitrage_opportunity(self) -> None:
        """
        Identifies and acts upon arbitrage opportunities in the market. This method should reflect market dynamics and
        generate swaps in liquidity pools to leverage arbitrage opportunities.

        Returns:
            None
        """
        pass
