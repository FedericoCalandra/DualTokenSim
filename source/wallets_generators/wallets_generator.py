from abc import ABC, abstractmethod


class WalletsGenerator(ABC):
    """
    Abstract base class for generating wallets with random distributions of token supplies.

    Attributes:
        total_free_token_supply (float): The total amount of tokens available for distribution
                                         across all generated wallets.
    Methods:
        get_random_wallet: Abstract method to generate a wallet with a specific allocation of tokens.
    """

    def __init__(self, total_free_token_supply: float):
        """
        Initializes the WalletsGenerator with a total supply of tokens available for distribution.

        Args:
            total_free_token_supply (float): Total amount of tokens to be distributed. Must be positive.

        Raises:
            ValueError: If total_free_token_supply is not positive.
        """
        if total_free_token_supply < 0:
            raise ValueError("Total free token supply must be a non-negative value.")

        self.total_free_token_supply = total_free_token_supply

    @abstractmethod
    def get_random_wallet(self):
        """
        Abstract method to generate a random wallet with a specific allocation of tokens.

        Derived classes must implement this method to define how token distributions are determined.

        Returns:
            float: The balance of a random wallet.
        """
        pass
