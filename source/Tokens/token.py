from abc import ABC, abstractmethod

class Token(ABC):
    """
    Abstract class representing a generic token.
    
    Attributes:
        name (str): The name of the token.
        supply (int): The current supply of the token.
        free_supply(int): The amount of tokens present in users' wallets.
        price (float): The current price of the token.
    """
    
    def __init__(self, name: str, initial_supply: int, initial_price: float):
        """
        Initializes an instance of the Token class with the provided values.
        
        Args:
            name (str): The name of the token.
            initial_supply (int): The initial supply of the token. Must be a positive integer.
            initial_price (float): The initial price of the token. Must be a positive number.
        
        Raises:
            TypeError: If the name is not a string.
            ValueError: If the initial supply is not a positive integer or 
                        if the initial price is not a positive number.
        """
        # Argument validation
        if not isinstance(name, str):
            raise TypeError("The token name must be a string.")
        if not isinstance(initial_supply, int) or initial_supply <= 0:
            raise ValueError("The initial supply must be a positive integer.")
        if not isinstance(initial_price, (float, int)) or initial_price <= 0:
            raise ValueError("The initial price must be a positive number.")
        
        # Initialize attributes
        self.name = name
        self.supply = initial_supply
        self.price = float(initial_price)  # Ensure the price is always stored as a float.
        self._free_supply = initial_supply # Use a private attribute for internal storage.

    @property
    def free_supply(self):
        """Getter for the free supply of tokens."""
        return self._free_supply

    @free_supply.setter
    def free_supply(self, value):
        """
        Setter for the free supply of tokens with validation.
        
        Ensures that free_supply cannot exceed the total supply.
        
        Args:
            value (int): The new value for free_supply.
        
        Raises:
            ValueError: If value is greater than supply or negative.
        """
        if not isinstance(value, int) or value < 0:
            raise ValueError("Free supply must be a non-negative integer.")
        if value > self.supply:
            raise ValueError("Free supply cannot exceed total supply.")
        self._free_supply = value

    def is_equal(self, other_token) -> bool:
        """
        Checks if two tokens are the same object (instance identity).
        
        Args:
            other_token (Token): Another token object to compare.
        
        Returns:
            bool: True if the two tokens are the same object, False otherwise.
        """
        return self is other_token

    def set_new_price(self, new_price: float):
        """
        Sets a new price for the token.
        
        Args:
            new_price (float): The new price of the token.
        
        Raises:
            ValueError: If the new price is not a positive number.
        """
        if new_price > 0:
            self.price = float(new_price)
        else:
            raise ValueError("Invalid price. The price must be a positive number.")
        
    @abstractmethod
    def __repr__(self) -> str:
        """
        Abstract method for representing the token as a string.
        This method must be implemented by subclasses.
        
        Returns:
            str: The textual representation of the token.
        """
        pass

