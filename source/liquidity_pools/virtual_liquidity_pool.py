from abc import ABC, abstractmethod

from source.liquidity_pools.formula import Formula
from source.liquidity_pools.liquidity_pool import LiquidityPool
from source.tokens.seignorage_model_token import SeignorageModelToken
from source.tokens.token import Token


class VirtualLiquidityPool(LiquidityPool, ABC):
    """
    An abstract base class representing a virtual liquidity pool.
    Manages the relationship and price adjustments between two tokens.

    Attributes:
        collateral_price (float): The price of token_b.
        delta (float): Represents the deviation between the base quantity of token_a and its actual value.

    Methods:
        restore_delta: Abstract method to restore the delta value based on specific rules.
        Must be implemented by subclasses.
        update_delta: Abstract method to update the delta value based on trading activity.
        Must be implemented by subclasses.
        update_token_b_price: Updates the price_token_b attribute with the provided value.
    """

    def __init__(self, stablecoin: Token, collateral: Token, stablecoin_base_quantity: float, fee: float,
                 formula: Formula):
        """
        Initializes the VirtualLiquidityPool with tokens, their quantities, a transaction fee,
        a swap formula, and parameters for managing token_b's price and deviation.

        Args:
            stablecoin (Token): The first token in the pool.
            collateral (Token): The second token in the pool.
            stablecoin_base_quantity (float): Initial quantity of stablecoin in the pool.
            fee (float): Transaction fee percentage applied to swaps.
            formula (Formula): Formula instance defining the swap computation logic.
        """
        if stablecoin_base_quantity < 0 or fee < 0:
            raise ValueError("Invalid inputs for this virtual liquidity pool.")

        quantity_collateral = stablecoin_base_quantity / collateral.price
        super().__init__(stablecoin, collateral, stablecoin_base_quantity, quantity_collateral, fee, formula)
        self.stablecoin_base_quantity = stablecoin_base_quantity
        self.collateral_price = collateral.price
        self.delta = 0

    def swap(self, token: SeignorageModelToken, amount: float):
        """
        Overrides swap method defined in LiquidityPool to include the delta dynamics.
        Executes a swap between stablecoin and collateral, adjusting the pool quantities accordingly.

        Args:
            token (Token): The token being provided to the pool (either stablecoin or collateral).
            amount (float): The amount of the input token to swap.

        Returns:
            tuple: The output token and the amount of the output token after swap and fee deduction.

        Raises:
            ValueError: If the input token is not recognized or if input_amount is invalid.
        """
        self.quantity_token_a = self.stablecoin_base_quantity + self.delta
        self.quantity_token_b = self.stablecoin_base_quantity / self.collateral_price
        output_token, output_amount = super().swap(token, amount)

        if token.is_equal(self.token_a):
            delta_variation = amount
        else:
            delta_variation = -output_amount
        self.update_delta(delta_variation)

        return output_token, output_amount

    def update_token_quantities(self):
        """
        Updates stablecoin and collateral quantities based on delta value.
        """
        new_quantity_token_a = self.stablecoin_base_quantity + self.delta
        self.quantity_token_b = self.formula.compute_reserve(self.quantity_token_a, self.quantity_token_b,
                                                             new_quantity_token_a)
        self.quantity_token_a = new_quantity_token_a

    def perform_pool_replenishing(self):
        """
        Coordinates the restoration mechanism of the virtual liquidity pool.
        It depends on the abstract restore_delta method.
        """
        self.restore_delta()
        self.update_token_quantities()

    @abstractmethod
    def restore_delta(self):
        """
        Abstract method to restore the delta value to go back to the desired equilibrium state.
        This method must be implemented by subclasses.
        """
        pass

    @abstractmethod
    def update_delta(self, delta_variation):
        """
        Abstract method to update the delta value based on trading activity.
        This method must be implemented by subclasses.
        """
        pass

    def update_collateral_price(self, new_price):
        """
        Updates the reference price of token_b.

        Args:
            new_price (float): The new price to set for collateral token.
        """
        self.collateral_price = new_price

    def update_supplies(self, token, other_token, amount, other_amount):
        token.burn(amount)
        other_token.mint(other_amount)
