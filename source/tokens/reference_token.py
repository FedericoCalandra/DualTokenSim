from source.tokens.token import Token

class ReferenceToken(Token):
    """
    Represents a reference token with a fixed price of 1.0$ and no defined supply.
    This token is typically used in liquidity pools to ensure that the other token 
    in the pool is priced relative to a stable dollar value.

    Attributes:
        name (str): The name of the ReferenceToken.
        price (float): Fixed price, always set to 1.0.
        supply (float): Set to infinity to indicate that supply is undefined.
        free_supply (float): Set to infinity to indicate that free supply is undefined.
    """
    
    def __init__(self, name: str):
        """
        Initializes a ReferenceToken instance with a fixed price of 1.0 
        and an undefined (infinite) supply.
        
        Args:
            name (str): The name of the ReferenceToken.
        """
        # Call the parent constructor with a fixed price of 1.0 and infinite supply.
        super().__init__(name, float('inf'), float('inf'), 1.0)

    @property
    def price(self):
        """The price of the ReferenceToken (always 1.0)."""
        return 1.0

    @property
    def supply(self):
        """The total supply of the ReferenceToken (always inf)."""
        return float('inf')

    @property
    def free_supply(self):
        """The free supply of the ReferenceToken (always inf)."""
        return float('inf')


    def __repr__(self) -> str:
        """
        Returns a string representation of the ReferenceToken object.
        
        Returns:
            str: A string representation of the ReferenceToken, including its name and price.
        """
        return f"ReferenceToken(name={self.name}, price={self.price})"

