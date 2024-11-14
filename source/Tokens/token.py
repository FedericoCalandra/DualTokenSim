from abc import ABC, abstractmethod

class Token(ABC):
    def __init__(self, name, initial_supply, initial_price):
        """Initializes the token with a name, initial supply, and initial price."""
        self.name = name                # Token name (e.g., "Bitcoin")
        self.supply = initial_supply     # Total supply of the token
        self.price = initial_price       # Price of a single token

    def is_equal(self, other_token):
        """Abstract method for comparing if two tokens are the same object."""
        return self is other_token

    def increase_supply(self, amount):
        """Increases the supply of tokens.
        
        Args:
            amount (int): The number of tokens to mint and add to the supply.
        
        Raises:
            ValueError: If the amount is non-positive.
        """
        if amount > 0:
            self.supply += amount
        else:
            raise ValueError("Invalid amount. The amount of tokens to mint must be positive!")

    def reduce_supply(self, amount):
        """Reduces the supply of tokens.
        
        Args:
            amount (int): The number of tokens to remove from the supply.
        
        Raises:
            ValueError: If the amount is non-positive or greater than current supply.
        """
        if 0 < amount <= self.supply:
            self.supply -= amount
        else:
            raise ValueError(
                "Invalid amount. The amount of tokens to burn must be positive and not greater than current supply."
            )

    def set_new_price(self, new_price):
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
