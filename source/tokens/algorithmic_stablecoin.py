from source.tokens.seignorage_model_token import SeignorageModelToken


class AlgorithmicStablecoin(SeignorageModelToken):
    """
    Represents an algorithmic stablecoin within the seignorage model.
    This token is pegged to a stable value (typically 1 USD), and its supply
    is dynamically adjusted to maintain the peg, usually in a pair with another token.

    Attributes:
        name (str): The name of the token.
        supply (float): The current supply of the token.
        free_supply (float): The amount of tokens present in users' wallets.
        price (float): The current price of the token.
        peg (float): The target price the stablecoin is pegged to (e.g., 1.0 USD).
    """

    def __init__(self, name: str, initial_supply: float, initial_free_supply: float, initial_price: float,
                 peg: float = 1.0):
        """
        Initializes the AlgorithmicStablecoin with a name, initial supply, and peg value.

        Args:
            name (str): The name of the stablecoin.
            initial_supply (float): The initial supply of the stablecoin.
            initial_free_supply (float): The initial free supply of the stablecoin.
            initial_price (float): The initial price of the stablecoin.
            peg (float, optional): The target peg value, typically set to 1.0 for USD. Default is 1.0.

        Raises:
            ValueError: If the initial supply or peg value is invalid.
        """
        # Initialize the parent class (SeignorageModelToken) with the peg value set as the price
        super().__init__(name, initial_supply, initial_free_supply, initial_price)
        if peg <= 0:
            raise ValueError("The peg value must be positive.")
        self._peg = peg
        self._tied = False

    @property
    def peg(self):
        """
        Getter for the peg value.
        """
        return self._peg

    @peg.setter
    def peg(self, value: float):
        """
        Setter for the peg value. Raises an error if attempted to modify the peg after initialization.
        
        Args:
            value (float): The new peg value (ignored).
        
        Raises:
            AttributeError: Always raised to indicate that the peg cannot be modified.
        """
        raise AttributeError("The peg value is immutable and cannot be changed once set.")

    def __repr__(self) -> str:
        """
        Represents the AlgorithmicStablecoin object as a string.

        Returns:
            str: A string representation of the AlgorithmicStablecoin object.
        """
        return (f"AlgorithmicStablecoin(name={self.name}, price={self.price}, supply={self.supply},"
                f"free_supply={self.free_supply}, peg={self.peg})")
