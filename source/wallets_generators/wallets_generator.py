from abc import ABC, abstractmethod


class WalletsGenerator(ABC):
    """
    Abstract base class for generating wallets with random distributions of token supplies.

    Attributes:
        probability_associated_to_total_free_token (float): Probability associated to the total amount of tokens
                                                            available for distribution.
    Methods:
        get_random_wallet: Abstract method to generate a wallet with a specific allocation of tokens.
    """

    def __init__(self, probability_associated_to_total_free_token: float):
        """
        Initializes the WalletsGenerator with a total supply of tokens available for distribution.

        Args:
            probability_associated_to_total_free_token (float): Probability associated to total amount of tokens to be
                                                                distributed. Must be positive.

        Raises:
            ValueError: If total_free_token_supply is not positive.
        """
        if probability_associated_to_total_free_token < 0:
            raise ValueError("Probability associated to total free token supply must be a non-negative value.")

        self.probability_associated_to_total_free_token = probability_associated_to_total_free_token

    @abstractmethod
    def get_random_wallet(self, total_free_token_supply):
        """
        Abstract method to generate a random wallet with a specific allocation of tokens.

        Derived classes must implement this method to define how token distributions are determined.

        Returns:
            float: The balance of a random wallet.
        """
        pass
