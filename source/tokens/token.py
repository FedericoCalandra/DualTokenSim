from abc import ABC, abstractmethod


class Token(ABC):
    """
    Abstract class representing a cryptocurrency.
    
    Attributes:
        name (str): The name of the token.
        _supply (float): The current total supply of the token.
        _free_supply (float): The amount of tokens present in users' wallets.
        _price (float): The current price of the token.
    """
    
    def __init__(self, name: str, initial_supply: float, initial_free_supply: float, initial_price: float):
        """
        Initializes an instance of the Token class with the provided values.
        
        Args:
            name (str): The name of the token.
            initial_supply (float): The initial supply of the token. 
                                    Must be a positive number.
            initial_free_supply (float): The initial free supply of the token. 
                                         Must be a positive number, 
                                         less than or equal to initial_supply.
            initial_price (float): The initial price of the token. 
                                   Must be a positive number.
        
        Raises:
            TypeError: If the name is not a string.
            ValueError: If the initial supply is not a positive number, 
                        if the initial price is not a positive number,
                        or if initial_free_supply is greater than initial_supply.
        """
        # Argument validation
        if not isinstance(name, str):
            raise TypeError("The token name must be a string.")
        if not isinstance(initial_supply, (int, float)) or initial_supply <= 0:
            raise ValueError("The initial supply must be a positive number.")
        if not isinstance(initial_free_supply, (int, float)) or initial_free_supply < 0:
            raise ValueError("The initial free supply must be a positive number.")
        if initial_free_supply > initial_supply:
            raise ValueError("The initial free supply cannot exceed the initial supply.")
        if not isinstance(initial_price, (float, int)) or initial_price <= 0:
            raise ValueError("The initial price must be a positive number.")
        
        # Initialize attributes.
        self.name = name
        # We use private attributes.
        self._supply = float(initial_supply)
        self._free_supply = float(initial_free_supply)
        self._price = float(initial_price)  

    @property
    def supply(self):
        """Getter for the total supply of tokens."""
        return self._supply

    @property
    def free_supply(self):
        """Getter for the free supply of tokens."""
        return self._free_supply
    
    @property
    def price(self):
        """Getter for the price of the token."""
        return self._price
    
    @supply.setter
    def supply(self, new_supply: float):
        """
        Setter for the total supply of tokens. 
    
        Adjusts the supply and ensures that the free supply is consistent.
    
        Args:
            new_supply (float): The new value for the total supply.
    
        Raises:
            ValueError: If the new supply is negative or if decreasing the supply 
                        would cause the free supply to become negative.
            TypeError: If the new_supply is not an integer.
        """
        if not isinstance(new_supply, (float, int)):
            raise TypeError("Supply must be a numeric value.")
        
        if new_supply < 0:
            raise ValueError("Supply cannot be negative.")
        
        # Calculate the new free supply based on the difference in supply.
        new_free_supply = self._free_supply + (new_supply - self._supply)

        if 0.001 > new_free_supply > -0.001:
            new_free_supply = 0

        if new_free_supply < 0:
            raise ValueError("Reduction in supply cannot result in negative free supply.")

        # Update the attributes
        self._free_supply = float(new_free_supply)
        self._supply = float(new_supply)

    @free_supply.setter
    def free_supply(self, new_free_supply: float):
        """
        Setter for the free supply of tokens with validation.
        
        Ensures that free_supply cannot exceed the total supply.
        
        Args:
            new_free_supply (float): The new value for free_supply.
        
        Raises:
            ValueError: If value is greater than supply or negative.
        """
        if 0.01 > new_free_supply > -0.01:
            new_free_supply = 0
        if not isinstance(new_free_supply, (float, int)) or new_free_supply < 0:
            raise ValueError("Free supply must be a positive number.")
        if new_free_supply > self._supply:
            raise ValueError("Free supply cannot exceed total supply.")
        self._free_supply = float(new_free_supply)

    @price.setter
    def price(self, new_price: float):
        """
        Setter for the price of the token with validation.
    
        Args:
            new_price (float): The new price of the token.
    
        Raises:
            ValueError: If the new price is not a positive number.
        """
        if new_price > 0:
            self._price = float(new_price)
        else:
            raise ValueError("Invalid price. The price must be a positive number.")

    def is_equal(self, other_token) -> bool:
        """
        Checks if two tokens are the same object (instance identity).
        
        Args:
            other_token (Token): Another token object to compare.
        
        Returns:
            bool: True if the two tokens are the same object, False otherwise.
        """
        return self is other_token

    @abstractmethod
    def __repr__(self) -> str:
        """
        Abstract method for representing the token as a string.
        This method must be implemented by subclasses.
        
        Returns:
            str: The textual representation of the token.
        """
        pass
