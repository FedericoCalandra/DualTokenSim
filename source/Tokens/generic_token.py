from source.Tokens.token import Token

class GenericToken(Token):
    """
    A standard token whose price and supply can vary freely.
    This class represents a generic token, such as Bitcoin, where the supply 
    and price can change without being tied to a specific algorithmic model.
    
    Attributes:
        name (str): The name of the GenericToken.
        supply (int): The current supply of the token.
        price (float): The current price of the token.
    """

    def __init__(self, name: str, initial_supply: int, initial_price: float):
        """
        Initializes the GenericToken instance with the provided name, supply, and price.
        
        Args:
            name (str): The name of the GenericToken.
            initial_supply (int): The initial supply of the token. Should be a positive integer.
            initial_price (float): The initial price of the token. Should be a positive number.
        
        Raises:
            ValueError: If the initial supply or price is invalid (non-positive).
        """
        # Initialize using the parent class constructor
        super().__init__(name=name, initial_supply=initial_supply, initial_price=initial_price)

    def change_supply(self, delta: int):
        """
        Increases or decreases the supply of the token by the specified delta.
        
        Args:
            delta (int): The amount to increase or decrease the supply by. Can be positive or negative.
        
        Raises:
            ValueError: If the new supply after applying delta is negative.
        """
        new_supply = self.supply + delta
        if new_supply < 0:
            raise ValueError("Supply cannot be negative.")
        self.supply = new_supply

    def __repr__(self) -> str:
        """
        Represents the GenericToken object as a string.
        
        Returns:
            str: A string representation of the GenericToken, including its name, price, and supply.
        """
        return f"GenericToken(name={self.name}, price={self.price}, supply={self.supply})"

