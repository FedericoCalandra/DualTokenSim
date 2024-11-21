from source.Tokens.seignorage_model_token import SeignorageModelToken

class AlgorithmicStablecoin(SeignorageModelToken):
    """
    Represents an algorithmic stablecoin within the seignorage model.
    This token is pegged to a stable value (typically 1 USD), and its supply
    is dynamically adjusted to maintain the peg, usually in a pair with another token.

    Attributes:
        name (str): The name of the token.
        supply (int): The current supply of the token.
        price (float): The current price of the token.
        peg (float): The target price the stablecoin is pegged to (e.g., 1.0 for USD).
    """

    def __init__(self, name: str, initial_supply: int, initial_price: float, peg: float = 1.0):
        """
        Initializes the AlgorithmicStablecoin with a name, initial supply, and peg value.

        Args:
            name (str): The name of the stablecoin.
            initial_supply (int): The initial supply of the stablecoin.
            initial_price (float): The initial price of the stablecoin.
            peg (float, optional): The target peg value, typically set to 1.0 for USD. Default is 1.0.

        Raises:
            ValueError: If the initial supply or peg value is invalid.
        """
        # Initialize the parent class (SeignorageModelToken) with the peg value set as the price
        super().__init__(name=name, initial_supply=initial_supply, initial_price=initial_price)
        if peg <= 0:
            raise ValueError("The peg value must be positive.")
        self.peg = peg

    def __repr__(self) -> str:
        """
        Represents the AlgorithmicStablecoin object as a string.

        Returns:
            str: A string representation of the AlgorithmicStablecoin object.
        """
        return f"AlgorithmicStablecoin(name={self.name}, price={self.price}, supply={self.supply}, peg={self.peg})"
