from source.LiquidityPools.virtual_liquidity_pool import VirtualLiquidityPool


class SimpleVirtualLiquidityPool(VirtualLiquidityPool):
    """
    Implements a basic virtual liquidity pool model with simple delta adjustment mechanisms.
    This is directly inspired by the original virtual liquidity pool implemented in the Terra protocol.
    """

    def __init__(self, stablecoin, collateral, quantity_stablecoin, quantity_collateral, fee, formula, collateral_price,
                 pool_recovery_period):
        super().__init__(stablecoin, collateral, quantity_stablecoin, quantity_collateral, fee, formula, collateral_price)
        self.pool_recovery_period = pool_recovery_period

    def restore_delta(self):
        """
        Reduces delta over time using an exponential decay formula:
        delta *= (1 - 1 / pool_recovery_period).
        """
        self.delta *= (1 - 1 / self.pool_recovery_period)

    def update_delta(self, delta_variation):
        """
        Updates delta by adding a variation.

        Args:
            delta_variation (float): The change to apply to delta.
        """
        self.delta += delta_variation

    def reset_replenishing_system(self):
        """
        Resets delta to zero.
        """
        self.delta = 0