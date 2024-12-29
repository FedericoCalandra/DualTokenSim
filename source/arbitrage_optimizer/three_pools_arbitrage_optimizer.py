from typing import List, Tuple
from scipy.optimize import minimize_scalar
from source.liquidity_pools.liquidity_pool import LiquidityPool
from source.liquidity_pools.virtual_liquidity_pool import VirtualLiquidityPool
from source.arbitrage_optimizer.arbitrage_optimizer import ArbitrageOptimizer


class ThreePoolsArbitrageOptimizer(ArbitrageOptimizer):
    """
    Implementation of the ArbitrageOptimizer for a system involving two liquidity pools and one virtual pool.

    This class handles the detection and execution of arbitrage opportunities by evaluating price differences
    across the pools and optimizing input quantities for maximum profit.
    """

    def __init__(self, liquidity_pools: List[LiquidityPool], virtual_liquidity_pool: VirtualLiquidityPool):
        """
        Initializes the ThreePoolsArbitrageOptimizer with the provided liquidity pools and virtual pool.

        Args:
            liquidity_pools (List[LiquidityPool]): A list of two liquidity pool instances representing the main pools in
                                                    the market.
            virtual_liquidity_pool (VirtualLiquidityPool): A virtual liquidity pool used for swaps between AS and CT.
        """
        super().__init__(liquidity_pools, virtual_liquidity_pool)
        self.max_arbitrage_input = 10 ** 6
        self.threshold = 0.001

    def leverage_arbitrage_opportunity(self):
        """
        Executes arbitrage operations when opportunities are detected.

        Depending on the type of arbitrage detected, performs swaps across the liquidity pools and the virtual pool
        to exploit price differences and maximize profits.
        """
        arbitrage_type, arbitrage_available = self.detect_arbitrage()

        if arbitrage_available:
            if arbitrage_type == 'Type 1':  # Arbitrage Type 1 (AS price over the peg)
                if self.liquidity_pools[0].token_a.price < 1:
                    print("Warning: T1 but price < 1")
                trade_amount = min(self.compute_max_arbitrage_profit("Type 1"), self.max_arbitrage_input)

                token, x = self.liquidity_pools[1].swap(self.liquidity_pools[1].token_b, trade_amount)
                token, x = self.virtual_liquidity_pool.swap(token, x)
                self.liquidity_pools[0].swap(token, x)

            else:  # Arbitrage Type 2 (AS price below the peg)
                if self.liquidity_pools[0].token_a.price > 1:
                    print("Warning: T2 but price > 1")
                trade_amount = min(self.compute_max_arbitrage_profit("Type 2"), self.max_arbitrage_input)

                token, x = self.liquidity_pools[0].swap(self.liquidity_pools[0].token_b, trade_amount)
                token, x = self.virtual_liquidity_pool.swap(token, x)
                self.liquidity_pools[1].swap(token, x)

    def detect_arbitrage(self) -> Tuple[str, bool]:
        """
        Identifies whether arbitrage opportunities exist and determines the type.

        Returns:
            Tuple[str, bool]: A tuple where:
                - str: The type of arbitrage ('Type 1' or 'Type 2') if an opportunity exists, otherwise ''.
                - bool: True if an arbitrage opportunity exists, False otherwise.
        """
        t1_profit = self.get_arbitrage_profit("Type 1", 1)
        t2_profit = self.get_arbitrage_profit("Type 2", 1)

        if t1_profit > 0:
            if self.liquidity_pools[0].token_a.price < 1:
                print("Alert.")
            return 'Type 1', True
        elif t2_profit > 0:
            if self.liquidity_pools[0].token_a.price > 1:
                print("Alert.")
            return 'Type 2', True
        return '', False

    def compute_max_arbitrage_profit(self, arbitrage_type: str):
        """
        Computes the input quantity that maximizes arbitrage profit for a given arbitrage type.

        Uses a bounded optimization technique to find the input amount that yields the highest profit.

        Args:
            arbitrage_type (str): The arbitrage type ('Type 1' or 'Type 2').

        Returns:
            float: The input quantity that yields the maximum arbitrage profit.

        Raises:
            ValueError: If the optimization process fails.
        """

        def negative_yield(rt_input_quantity):
            # Negate the yield because we are minimizing
            return -self.get_arbitrage_profit(arbitrage_type, rt_input_quantity)

        # Set bounds for the optimization
        bounds = (1, self.max_arbitrage_input)

        # Perform bounded optimization using SciPy
        result = minimize_scalar(negative_yield, bounds=bounds, method='bounded')

        if result.success:
            if -result.fun < 0:
                print("ERROR!!!")
            return result.x
        else:
            raise ValueError("Optimization failed.")

    def get_arbitrage_profit(self, arbitrage_type: str, rt_input_quantity: float):
        """
        Calculates the profit from an arbitrage operation based on the input quantity and arbitrage type.

        The arbitrage process involves:
        - Type1: Buying CT in Pool 2, swapping CT for AS in the virtual pool, and selling AS in Pool 1.
        - Type2: Buying AS in Pool 1, swapping AS for CT in the virtual pool, and selling CT in Pool 2.

        Args:
            arbitrage_type (str): The arbitrage type ('Type 1' or 'Type 2').
            rt_input_quantity (float): The input quantity of RT (USD-equivalent).

        Returns:
            float: The profit (in RT) from the arbitrage operation.

        Note:
            If the input quantity is zero or invalid, returns 0 profit.
        """
        if arbitrage_type == "Type 1":
            first_pool = self.liquidity_pools[1]
            second_pool = self.liquidity_pools[0]
        else:
            first_pool = self.liquidity_pools[0]
            second_pool = self.liquidity_pools[1]

        if rt_input_quantity > 0:
            x = first_pool.compute_swap_value(rt_input_quantity,
                                              first_pool.quantity_token_b,
                                              first_pool.quantity_token_a)

            if arbitrage_type == "Type 1":
                y = self.virtual_liquidity_pool.compute_swap_value(x,
                                                                   self.virtual_liquidity_pool.quantity_token_b,
                                                                   self.virtual_liquidity_pool.quantity_token_a)
            else:
                y = self.virtual_liquidity_pool.compute_swap_value(x,
                                                                   self.virtual_liquidity_pool.quantity_token_a,
                                                                   self.virtual_liquidity_pool.quantity_token_b)
            rt_output_quantity = second_pool.compute_swap_value(y,
                                                                second_pool.quantity_token_a,
                                                                second_pool.quantity_token_b)

            return rt_output_quantity - rt_input_quantity

        return 0
