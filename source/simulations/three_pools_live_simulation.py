from source.liquidity_pools.liquidity_pool import LiquidityPool
from source.liquidity_pools.virtual_liquidity_pool import VirtualLiquidityPool
import threading
import time
from source.purchase_generators.purchase_generator import PurchaseGenerator
from source.simulations.three_pools_simulation import ThreePoolsSimulation
from source.tokens.algorithmic_stablecoin import AlgorithmicStablecoin
from source.tokens.collateral_token import CollateralToken
from source.tokens.reference_token import ReferenceToken


class ThreePoolsLiveSimulation(ThreePoolsSimulation):
    """
    A live simulation class for an algorithmic stablecoin system with a dual-token mechanism.
    Includes functions to pause and resume the simulation execution. Include a function to execute a custom swap.
    """

    def __init__(self, stablecoin_token: AlgorithmicStablecoin,
                 collateral_token: CollateralToken,
                 reference_token: ReferenceToken,
                 stablecoin_pool: LiquidityPool, collateral_pool: LiquidityPool, virtual_pool: VirtualLiquidityPool,
                 stablecoin_purchase_generator: PurchaseGenerator, collateral_purchase_generator: PurchaseGenerator,
                 number_of_iterations: int = 0):
        super().__init__(stablecoin_token, collateral_token, reference_token, stablecoin_pool, collateral_pool,
                         virtual_pool, stablecoin_purchase_generator, collateral_purchase_generator,
                         number_of_iterations)
        self.paused = False
        self.stop_condition = 0.0
        self.thread = None
        self.stop_signal = False
        self.delay = 0.1

        self.stablecoin_price_history = []
        self.collateral_price_history = []
        self.delta_variation_history = []

    def run_simulation(self):
        """
        Starts the live simulation in a separate thread, updating continuously unless paused or stopped.
        """
        def simulation_loop():
            while not self.stop_signal:
                if not self.paused:
                    if self.stablecoin_token.price < self.stop_condition:
                        print("Stop condition met: Stablecoin price below threshold.")
                        self.stop_signal = True
                        break

                    self.step_simulation()
                    time.sleep(self.delay)
                else:
                    time.sleep(1)

        self.thread = threading.Thread(target=simulation_loop)
        self.thread.start()

    def pause_simulation(self):
        """
        Pauses the simulation.
        """
        self.paused = True
        print("Simulation paused.")

    def resume_simulation(self):
        """
        Resumes the simulation.
        """
        self.paused = False
        print("Simulation resumed.")

    def step_simulation(self):
        """
        Executes a single step of the simulation.
        """
        self.stablecoin_price_history.append(self.stablecoin_token.price)
        self.collateral_price_history.append(self.collateral_token.price)
        self.delta_variation_history.append(self.virtual_pool.delta)
        self.market_simulator.execute_random_purchases()
        self.number_of_iterations += 1

        print(f"Stablecoin Price: {self.stablecoin_token.price}, Collateral Price: {self.collateral_token.price}")

    def add_custom_swap(self, token, quantity, pool):
        """
        Adds a custom swap immediately to the simulation.
        """
        print(f"Custom swap added: {quantity} of {token} in pool {pool}")
        pool.swap(token, quantity)

    def stop_simulation(self):
        """
        Stops the simulation.
        """
        self.stop_signal = True
        print("Simulation stopped.")
        if self.thread:
            self.thread.join()

    def change_simulation_speed(self, speed):
        """
        Changes the live simulation speed.
        """
        if speed < 1 or speed > 600:
            raise ValueError("Speed must be between 1 and 600.")

        self.delay = 1 / speed
