from abc import ABC, abstractmethod

class Token(ABC):
    def __init__(self, name: str, initial_supply: int, initial_price: float):
        """Initializes the token with a name, initial supply, and initial price."""
        # Type checks
        if not isinstance(name, str):
            raise TypeError("The name must be a string.")
        if not isinstance(initial_supply, int) or initial_supply <= 0:
            raise ValueError("The initial supply must be a positive integer.")
        if not isinstance(initial_price, (float, int)) or initial_price <= 0:
            raise ValueError("The initial price must be a positive number.")
        # Initializing the parameters of the abstract class Token.
        self.name = name
        self.supply = initial_supply
        self.price = float(initial_price)  # Ensure price is always stored as a float

    def is_equal(self, other_token):
        """Control if two tokens are the same object."""
        return self is other_token

    def increase_supply(self, amount: int):
        """Increases the supply of a token.
        
        Args:
            amount (int): The number of tokens to mint and add to the supply.
        
        Raises:
            ValueError: If the amount is non-positive.
        """
        if amount > 0:
            self.supply += amount
        else:
            raise ValueError("Invalid amount. The amount of tokens to mint must be positive!")

    def reduce_supply(self, amount: int):
        """Reduces the supply of a token.
        
        Args:
            amount (int): The number of tokens to remove from the supply.
        
        Raises:
            ValueError: If the amount is non-positive or greater than current supply.
        """
        if 0 < amount <= self.supply:
            self.supply -= amount
        else:
            raise ValueError( "Invalid amount. The amount of tokens to burn must be positive \
                and not greater than current supply.")

    def set_new_price(self, new_price: float):
        """Sets a new price for the token.
        
        Args:
            new_price (float): The new price of the token.
        
        Raises:
            ValueError: If the new price is non-positive.
        """
        if new_price > 0:
            self.price = new_price
        else:
            raise ValueError("Invalid price. Price must be positive.")
        
    @abstractmethod
    def __repr__(self) -> str:
        """
        Abstract method for representing the token as a string.
        Must be implemented by subclasses.
        """
        pass
