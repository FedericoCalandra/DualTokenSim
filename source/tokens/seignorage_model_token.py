from abc import ABC, abstractmethod
from source.tokens.token import Token

class SeignorageModelToken(Token, ABC):
    """
    Represents a token within an algorithmic stablecoin model, such as the Terra/Luna model.
    This class allows for minting (increasing the supply) and burning (decreasing the supply) of tokens
    in response to changes in market conditions, helping to maintain the peg to a stable value.

    In this model, one token (the stablecoin) is kept at a stable price, while the other (the 
    'collateral token') adjusts in supply to balance the system and maintain the peg.

    Attributes:
        name (str): The name of the token.
        supply (float): The current supply of the token.
        free_supply (float): The amount of tokens present in users' wallets.
        price (float): The current price of the token.
    """

    def __init__(self, name: str, initial_supply: float, initial_free_supply: float, \
                  initial_price: float):
        """
        Initializes the SeignorageModelToken with a given name, initial supply, initial_free_supply and price.

        This token will serve as part of an algorithmic stablecoin pair. The price and supply of the token
        may change over time to help maintain the peg with the stablecoin counterpart.

        Args:
            name (str): The name of the token.
            initial_supply (float): The initial supply of the token.
            initial_free_supply (float): The initial free supply of the token.
            initial_price (float): The initial price of the token.

        """
        # Initialize the parent Token class
        super().__init__(name, initial_supply, initial_free_supply, initial_price)

    def mint(self, amount_to_mint: float):
        """
        This method is essential for increasing the supply of the token in order to stabilize the system.

        Args:
            amount (float): The number of tokens to mint (increase the supply).
        Raises:
            ValueError: If the amount is negative.
        """
        if amount_to_mint <= 0:
            raise ValueError("Amount to mint must be positive.")
        # The parent class setter is invoked to ensure the free_supply attribute is
        # consistent with the change in the total supply.
        self.supply += amount_to_mint

    def burn(self, amount_to_burn: float):
        """
        This method is essential for decreasing the supply of the token in order to stabilize the system 
        and prevent the price from falling too low.

        Args:
            amount (float): The number of tokens to burn (decrease the supply).

        Raises:
            ValueError: If the amount is negative or greater than the current supply.
        """
        if amount_to_burn <= 0:
            raise ValueError("Amount to burn must be positive.")
        if amount_to_burn > self.supply:
            raise ValueError("Cannot burn more tokens than the current supply.")
        # The parent class setter is invoked to ensure the free_supply attribute is
        # consistent with the change in the total supply.
        self.supply -= amount_to_burn

    @abstractmethod
    def __repr__(self) -> str:
        """
        Abstract method to represent the SeignorageModelToken object as a string.
        Must be implemented by subclasses to provide a custom string representation.
        """
        pass
