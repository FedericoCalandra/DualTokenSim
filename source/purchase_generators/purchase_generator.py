from abc import ABC, abstractmethod
from source.wallets_generators.wallets_generator import WalletsGenerator
from source.Tokens.token import Token

class PurchaseGenerator(ABC):
    """
    Abstract base class for generating random purchase events. This class is 
    designed to work with a wallets generator, which provides wallet balances for
    simulating purchase events.

    Attributes:
        token (Token): token whose purchase amount is simulated.
        wallets_generator (WalletsGenerator): An instance of WalletsGenerator 
                                              used to provide wallet balances 
                                              for the simulated purchases.
    """

    def __init__(self, token: Token, wallets_generator: WalletsGenerator):
        """
        Initializes the PurchaseGenerator with a WalletsGenerator.

        Args:
            token (Token): token whose purchase amount is simulated.
            wallets_generator (WalletsGenerator): An instance of WalletsGenerator 
                                                responsible for generating wallet
                                                balances for purchase simulation.

        Raises:
            TypeError: If wallets_generator is not an instance of WalletsGenerator and
                       if token is not an instance of Token.
        """
        if not isinstance(token, Token):
            raise TypeError("The token argument must be an instance of Token.")
        if not isinstance(wallets_generator, WalletsGenerator):
            raise TypeError("The wallets_generator argument must be an instance of WalletsGenerator.")
        # Initializing attributes.
        self.token = Token
        self.wallets_generator = wallets_generator

    @abstractmethod
    def generate_random_purchase(self) -> float:
        """
        Abstract method for calculating the amount of tokens to buy or sell.

        This method should be implemented to compute the amount of tokens that 
        would be involved in a purchase or sale event based on the specific 
        logic of the subclass.

        Returns:
            float: The amount of tokens to be purchased or sold.
        """
        pass

