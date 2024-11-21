from source.Tokens.token import Token

class ReferenceToken(Token):
    """
    Represents a reference token with a fixed price of 1.0$ and no defined supply.
    This token is typically used in liquidity pools to ensure that the other token 
    in the pool is priced relative to a stable dollar value.

    Attributes:
        name (str): The name of the ReferenceToken.
        price (float): Fixed price, always set to 1.0.
        supply (float): Set to infinity to indicate that supply is undefined.
    """
    
    def __init__(self, name: str):
        """
        Initializes a ReferenceToken instance with a fixed price of 1.0 
        and an undefined (infinite) supply.
        
        Args:
            name (str): The name of the ReferenceToken.
        """
        # Call the parent constructor with a fixed price of 1.0 and infinite supply
        super().__init__(name=name, initial_supply=float('inf'), initial_price=1.0)

    def set_new_price(self, new_price: float):
        """
        Prevents the price of the ReferenceToken from being changed.
        
        Args:
            new_price (float): The new price to be set (ignored).
        
        Raises:
            ValueError: Always, because the price of a ReferenceToken is fixed at 1.0.
        """
        raise ValueError("The price of a ReferenceToken is fixed at 1.0 and cannot be changed.")

    def __repr__(self) -> str:
        """
        Returns a string representation of the ReferenceToken object.
        
        Returns:
            str: A string representation of the ReferenceToken, including its name and price.
        """
        return f"ReferenceToken(name={self.name}, price={self.price})"

