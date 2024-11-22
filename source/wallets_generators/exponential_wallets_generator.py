import math
import random
from source.wallets_generators.wallets_generator import WalletsGenerator


class ExponentialWalletsGenerator(WalletsGenerator):
    """
    Generates random wallet balances based on an exponential distribution of token allocations.

    Attributes:
        probability_associated_to_total_free_token (float): Minimum probability
                                                                for the random variable W
                                                                assuming a value equal to total_free_tokens.
    Methods:
        get_random_wallet: Generates a random wallet balance using the exponential distribution.
    """

    def __init__(self, probability_associated_to_total_free_token: float):
        """
        Initializes the ExponentialWalletsGenerator.

        Args:
            probability_associated_to_total_free_token (float): Minimum probability for
                                                                    the random variable W
                                                                    assuming a value equal to
                                                                    total_free_tokens.
        Raises:
            ValueError: If total_free_token_supply is non-positive or the probability is not in (0, 1).
        """
        super().__init__(probability_associated_to_total_free_token)
        if not (0 < probability_associated_to_total_free_token < 1):
            raise ValueError("min_probability_associated_to_total_free_token must be between 0 and 1.")

        self.probability_associated_to_total_free_token = probability_associated_to_total_free_token

    def get_random_wallet(self, total_free_token_supply):
        """
        Generates a random wallet balance using an exponential distribution.

        Returns:
            float: The random wallet balance based on the exponential distribution, ensuring
                   it does not exceed the remaining total_free_token_supply.
        """
        if total_free_token_supply < 0:
            raise ValueError("Total free token supply must be positive.")

        if total_free_token_supply == 0:
            return 0

        exp_rate = -math.log(self.probability_associated_to_total_free_token) / total_free_token_supply
        if exp_rate <= 0:
            raise ValueError("The computed exponential rate (exp_rate) must be positive.")

        while True:
            wallet_balance = random.expovariate(exp_rate)

            if wallet_balance <= total_free_token_supply:
                return wallet_balance
