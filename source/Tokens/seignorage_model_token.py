from abc import ABC, abstractmethod
from source.Tokens.token import Token

class SeignorageModelToken(Token, ABC):
    """
    Represents a token within an algorithmic stablecoin model, such as the Terra/Luna model.
    This class allows for minting (increasing the supply) and burning (decreasing the supply) of tokens
    in response to changes in market conditions, helping to maintain the peg to a stable value.

    In this model, one token (the stablecoin) is kept at a stable price, while the other (the 
    'collateral token') adjusts in supply to balance the system and maintain the peg.

    Attributes:
        name (str): The name of the token.
        supply (int): The current supply of the token.
        price (float): The current price of the token.
    """

    def __init__(self, name: str, initial_supply: int, initial_price: float):
        """
        Initializes the SeignorageModelToken with a given name, initial supply, and price.

        This token will serve as part of an algorithmic stablecoin pair. The price and supply of the token
        may change over time to help maintain the peg with the stablecoin counterpart.

        Args:
            name (str): The name of the token.
            initial_supply (int): The initial supply of the token.
            initial_price (float): The initial price of the token.

        Raises:
            ValueError: If the initial supply or price is invalid (non-positive).
        """
        # Initialize the parent Token class
        super().__init__(name=name, initial_supply=initial_supply, initial_price=initial_price)

    def mint(self, amount: int):
        """
        This method is essential for increasing the supply of the token in order to stabilize the system.

        Args:
            amount (int): The number of tokens to mint (increase the supply).

        Raises:
            ValueError: If the amount is negative.
        """
        if amount <= 0:
            raise ValueError("Amount to mint must be positive.")
        self.supply += amount
        print(f"Minted {amount} tokens. New supply is {self.supply}.")

    def burn(self, amount: int):
        """
        This method is essential for decreasing the supply of the token in order to stabilize the system 
        and prevent the price from falling too low.

        Args:
            amount (int): The number of tokens to burn (decrease the supply).

        Raises:
            ValueError: If the amount is negative or greater than the current supply.
        """
        if amount <= 0:
            raise ValueError("Amount to burn must be positive.")
        if amount > self.supply:
            raise ValueError("Cannot burn more tokens than the current supply.")
        self.supply -= amount
        print(f"Burned {amount} tokens. New supply is {self.supply}.")

    @abstractmethod
    def __repr__(self) -> str:
        """
        Abstract method to represent the SeignorageModelToken object as a string.
        Must be implemented by subclasses to provide a custom string representation.
        """
        pass
