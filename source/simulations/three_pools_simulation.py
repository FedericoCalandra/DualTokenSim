from source.arbitrage_optimizer.three_pools_arbitrage_optimizer import ThreePoolsArbitrageOptimizer
from source.liquidity_pools.liquidity_pool import LiquidityPool
from source.liquidity_pools.virtual_liquidity_pool import VirtualLiquidityPool
from source.market_simulators.market_simulator import MarketSimulator
from source.purchase_generators.purchase_generator import PurchaseGenerator
from source.tokens.algorithmic_stablecoin import AlgorithmicStablecoin
from source.tokens.collateral_token import CollateralToken
from source.tokens.reference_token import ReferenceToken


class ThreePoolsSimulation:
    """
    A simulation class for an algorithmic stablecoin system with a dual-token mechanism.
    """

    def __init__(self, stablecoin_token: AlgorithmicStablecoin,
                 collateral_token: CollateralToken,
                 reference_token: ReferenceToken,
                 stablecoin_pool: LiquidityPool,
                 collateral_pool: LiquidityPool,
                 virtual_pool: VirtualLiquidityPool,
                 stablecoin_purchase_generator: PurchaseGenerator,
                 collateral_purchase_generator: PurchaseGenerator,
                 number_of_iterations: int):
        """
        Initializes the AlgorithmicStablecoinSimulation instance with the necessary components.
        """
        self.stablecoin_token = stablecoin_token
        self.collateral_token = collateral_token
        self.reference_token = reference_token

        self.stablecoin_pool = stablecoin_pool
        self.collateral_pool = collateral_pool
        self.virtual_pool = virtual_pool

        self.stablecoin_purchase_generator = stablecoin_purchase_generator
        self.collateral_purchase_generator = collateral_purchase_generator

        self.number_of_iterations = number_of_iterations

        liquidity_pools = [self.stablecoin_pool, self.collateral_pool]

        self.arbitrage_optimizer = ThreePoolsArbitrageOptimizer(liquidity_pools=liquidity_pools,
                                                                virtual_liquidity_pool=self.virtual_pool)

        self.market_simulator = MarketSimulator(liquidity_pools=liquidity_pools,
                                                virtual_liquidity_pool=self.virtual_pool,
                                                purchase_generators=[self.stablecoin_purchase_generator,
                                                                     self.collateral_purchase_generator],
                                                arbitrage_optimizer=self.arbitrage_optimizer)

    def run_simulation(self):
        """
        Executes the simulation loop for a specified number of iterations.

        Each iteration models a timestep in the algorithmic stablecoin ecosystem,
        capturing the following metrics:
        - Stablecoin price and supply.
        - Collateral token price and supply.
        - Free supplies of both stablecoin and collateral tokens.
        - Delta from the virtual liquidity pool.

        Returns:
            dict: A dictionary containing the simulation history:
                {
                    "stablecoin_price_history": List[float],
                    "collateral_price_history": List[float],
                    "stablecoin_supply_history": List[float],
                    "collateral_supply_history": List[float],
                    "stablecoin_free_supply_history": List[float],
                    "collateral_free_supply_history": List[float],
                    "virtual_pool_delta": List[float]
                }
        """
        simulation_data = {
            "stablecoin_price_history": [],
            "collateral_price_history": [],
            "stablecoin_supply_history": [],
            "collateral_supply_history": [],
            "stablecoin_free_supply_history": [],
            "collateral_free_supply_history": [],
            "virtual_pool_delta": []
        }

        for iteration in range(self.number_of_iterations):
            print(f"Running simulation iteration {iteration + 1}/{self.number_of_iterations}")

            simulation_data["stablecoin_price_history"].append(self.stablecoin_token.price)
            simulation_data["collateral_price_history"].append(self.collateral_token.price)
            simulation_data["stablecoin_supply_history"].append(self.stablecoin_token.supply)
            simulation_data["collateral_supply_history"].append(self.collateral_token.supply)
            simulation_data["stablecoin_free_supply_history"].append(self.stablecoin_token.free_supply)
            simulation_data["collateral_free_supply_history"].append(self.collateral_token.free_supply)
            simulation_data["virtual_pool_delta"].append(self.virtual_pool.delta)

            if self.collateral_token.supply * self.collateral_token.price < \
                    (self.stablecoin_token.supply * self.stablecoin_token.price) / 10e5:
                print(
                    "Simulation terminated early: The collateral capitalization is insufficient to support "
                    "the stablecoin system. The algorithmic stablecoin is considered collapsed."
                )
                break

            self.market_simulator.execute_random_purchases()

        return simulation_data
