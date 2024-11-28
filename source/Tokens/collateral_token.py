from source.Tokens.seignorage_model_token import SeignorageModelToken

class CollateralToken(SeignorageModelToken):
    """
    Represents a collateral token in the seignorage model.
    This token does not have a fixed peg, and its price can fluctuate freely.
    It can be used as collateral in the algorithmic stablecoin model.

    Attributes:
        name (str): The name of the token.
        supply (float): The current supply of the token.
        price (float): The current price of the token.
    """

    def __init__(self, name: str, initial_supply: float, initial_price: float):
        """
        Initializes the CollateralToken with a name, initial supply, and price.

        Args:
            name (str): The name of the collateral token.
            initial_supply (float): The initial supply of the collateral token.
            initial_price (float): The initial price of the collateral token.
        """
        # Initialize the parent class (SeignorageModelToken) with the given parameters
        super().__init__(name, initial_supply, initial_price)

    def __repr__(self) -> str:
        """
        Represents the CollateralToken object as a string for debugging.

        Returns:
            str: A string representation of the CollateralToken object.
        """
        return f"CollateralToken(name={self.name}, price={self.price}, supply={self.supply})"
