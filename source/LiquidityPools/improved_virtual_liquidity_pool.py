from source.LiquidityPools.virtual_liquidity_pool import VirtualLiquidityPool


class ImprovedVirtualLiquidityPool(VirtualLiquidityPool):
    """
    Implements an enhanced virtual liquidity pool with a more sophisticated recovery system
    that includes restore_values to adjust delta dynamically.
    """

    def __init__(self, stablecoin, collateral, stablecoin_base_quantity, fee, formula, pool_recovery_period):
        """
        Initializes the improved virtual liquidity pool with restore_values.

        Args:
            pool_recovery_period (int): The recovery period for the pool.
        """
        super().__init__(stablecoin, collateral, stablecoin_base_quantity, fee, formula)
        self.pool_recovery_period = pool_recovery_period
        self.restore_values = [0] * pool_recovery_period
        self.stablecoin_price = stablecoin.price
        self.values = [0.95 + i * 0.005 for i in range(9)]  # Thresholds: [0.95, 0.955, ..., 0.990]

    def restore_delta(self):
        """
        Adjusts delta based on restore_values and delta variation, computing a new restore_values length
        and redistributing excess values.
        """

        new_length = self.compute_restore_values_new_length()

        # Shrink restore_values to the new length
        self.shrink_restore_values(new_length)

        # Update delta using the first value in restore_values and perform a circular shift
        self.delta -= self.restore_values[0]
        self.restore_values = self.restore_values[1:] + [0]  # Circular shift (left)

    def compute_restore_values_new_length(self):
        new_length = 1
        for i, val in enumerate(reversed(self.values)):
            if self.stablecoin_price > val:
                new_length = int(round(self.pool_recovery_period * (1 - (i * 0.1)), 5))
                break
        return new_length

    def shrink_restore_values(self, new_length: int):
        """
        Shrinks restore_values to new_length by redistributing the excess sum across the first new_length elements.

        Args:
            new_length (int): The new length for restore_values.
        """
        if new_length < 1 or type(new_length) != int:
            raise ValueError("new_length must be an integer greater than or equal to 1")

        if new_length >= len(self.restore_values):
            self.restore_values += [0] * (new_length - len(self.restore_values))
            return

        excess_sum = sum(self.restore_values[new_length:])
        self.restore_values = self.restore_values[:new_length]

        # Redistribute excess sum across the reduced restore_values
        if new_length > 0:
            distribute_amount = excess_sum / new_length
            self.restore_values = [val + distribute_amount for val in self.restore_values]

    def update_delta(self, delta_variation):
        """
        Updates delta and spreads delta_variation across restore_values.

        Args:
            delta_variation (float): The change to apply to delta.
        """
        self.delta += delta_variation
        spread_amount = delta_variation / len(self.restore_values)
        self.restore_values = [val + spread_amount for val in self.restore_values]

    def reset_replenishing_system(self):
        """
        Resets delta to zero and reinitializes restore_values to zeros.
        """
        self.delta = 0
        self.restore_values = [0] * self.pool_recovery_period

    def update_stablecoin_price(self, stablecoin_price):
        self.stablecoin_price = stablecoin_price
