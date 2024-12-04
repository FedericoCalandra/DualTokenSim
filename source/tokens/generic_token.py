from source.tokens.token import Token


class GenericToken(Token):
    """
    A standard token whose price and supply can vary freely.
    This class represents a generic token, such as Bitcoin, where the supply 
    and price can change without being tied to a specific algorithmic model.
    
    Attributes:
        name (str): The name of the GenericToken.
        _supply (float): The current supply of the token.
        _free_supply (float): The amount of tokens present in users' wallets.
        _price (float): The current price of the token.
    """

    def __init__(self, name: str, initial_supply: float, initial_free_supply: float, initial_price: float):
        """
        Initializes the GenericToken instance with the provided name, supply, and price.
        
        Args:
            name (str): The name of the GenericToken.
            initial_supply (float): The initial supply of the token. Should be a positive number.
            initial_free_supply (float): The initial free supply of the token. Should be a positive number.
            initial_price (float): The initial price of the token. Should be a positive number.
        """
        # Initialize using the parent class constructor
        super().__init__(name, initial_supply, initial_free_supply, initial_price)

    def __repr__(self) -> str:
        """
        Represents the GenericToken object as a string.
        
        Returns:
            str: A string representation of the GenericToken, including its name, price, and supply.
        """
        return (f"GenericToken(name={self.name}, price={self.price}, supply={self.supply},"
                f"free_supply={self.free_supply})")
