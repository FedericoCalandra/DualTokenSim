from source.tokens.seignorage_model_token import SeignorageModelToken
from source.tokens.algorithmic_stablecoin import AlgorithmicStablecoin

class CollateralToken(SeignorageModelToken):
    """
    Represents a collateral token in the seignorage model.
    This token does not have a fixed peg, and its price can fluctuate freely.
    It can be used as collateral in the algorithmic stablecoin model.

    Attributes:
        name (str): The name of the token.
        supply (float): The current supply of the token.
        free_supply (float): The current free supply of the token.
        price (float): The current price of the token.
        algorithmic_stablecoin (AlgorithmicStablecoin): The associated stablecoin.
    """

    def __init__(self, name: str, initial_supply: float, initial_free_supply: float, \
                 initial_price: float, algorithmic_stablecoin: AlgorithmicStablecoin):
        """
        Initializes the CollateralToken with a name, initial supply, price,
        and a reference to an algorithmic stablecoin.

        Args:
            name (str): The name of the collateral token.
            initial_supply (float): The initial supply of the collateral token.
            initial_free_supply (float): The initial free supply of the collateral token.
            initial_price (float): The initial price of the collateral token.
            algorithmic_stablecoin (AlgorithmicStablecoin): The stablecoin associated 
                                                            with this collateral token.

        Raises:
            TypeError: If algorithmic_stablecoin is not an instance of AlgorithmicStablecoin.
            RuntimeError: If the stablecoin is already tied to another CollateralToken.
        """
        # Validate the algorithmic_stablecoin argument
        if not isinstance(algorithmic_stablecoin, AlgorithmicStablecoin):
            raise TypeError("algorithmic_stablecoin must be an instance of AlgorithmicStablecoin.")

        # Check if the stablecoin is already tied to another collateral token
        if algorithmic_stablecoin._tied:
            raise RuntimeError("This stablecoin is already tied to another CollateralToken.")       

        # Set the stablecoin reference as an immutable property
        self._algorithmic_stablecoin = algorithmic_stablecoin
        # Mark the stablecoin as tied to this collateral token
        self._algorithmic_stablecoin._tied = True
        # Initialize the parent class (SeignorageModelToken) with the given parameters
        super().__init__(name, initial_supply, initial_free_supply, initial_price)

    @property
    def algorithmic_stablecoin(self):
        """
        Gets the associated AlgorithmicStablecoin.

        Returns:
            AlgorithmicStablecoin: The stablecoin associated with this collateral token.
        """
        return self._algorithmic_stablecoin

    def __repr__(self) -> str:
        """
        Represents the CollateralToken object as a string for debugging.

        Returns:
            str: A string representation of the CollateralToken object.
        """
        return (f"CollateralToken(name={self.name}, price={self.price}, "
                f"supply={self.supply}, free_supply={self.free_supply}, "
                f"algorithmic_stablecoin={self.algorithmic_stablecoin.name})")

