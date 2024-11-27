from abc import ABC, abstractmethod
from typing import Tuple

from source.Tokens.token import Token


class PurchaseGenerator(ABC):
    """
    Abstract base class for generating random purchase events. This class ties purchase events to a specific liquidity
    pool and provides a template for subclasses to implement event generation logic.

    Attributes:
        liquidity_pool (LiquidityPool): Reference to the liquidity pool where purchases are simulated.
    """

    def __init__(self, liquidity_pool):
        """
        Initializes the PurchaseGenerator with a specific liquidity pool.

        Args:
            liquidity_pool (LiquidityPool): The liquidity pool associated with this generator.
        """
        self.liquidity_pool = liquidity_pool

    @abstractmethod
    def generate_random_purchase(self) -> Tuple[Token, float]:
        """
        Abstract method to generate a random purchase event.

        Returns:
            dict: A representation of the purchase event, including details such as the token purchased and the amount.

        Note:
            This method must be implemented by subclasses to define the specific logic for generating purchases.
        """
        pass
