from typing import Callable
from source.wallets_generators import WalletsGenerator
from source.purchase_generators.purchase_generator import PurchaseGenerator
from source.Tokens.algorithmic_stablecoin import AlgorithmicStablecoin
import numpy as np

class SeignorageModel(PurchaseGenerator):
    """
    A concrete implementation of the PurchaseGenerator abstract class, 
    representing a seignorage-based economic model.

    Attributes:
        wallets_generator (WalletsGenerator): An instance of WalletsGenerator used for
                                              generating wallet balances involved in 
                                              purchase events.
        stablecoin (AlgorithmicStablecoin): The algorithmic stablecoin associated 
                                            with this model.
        threshold (float): A  threshold parameter that defines when the stablecoin 
                           is considered to be in a normal state. (default: 0.05)
        sigma (float): Standard deviation (default: 1).
        mean (float): Mean (default: 0).
        delta_variation (Callable[[float], float]): A mathematical function.
    """

    def __init__(self, wallets_generator: WalletsGenerator, 
                 stablecoin: AlgorithmicStablecoin,
                 delta_variation: Callable[[float], float],
                 threshold: float = 0.05, 
                 sigma: float = 1.0, 
                 mean: float = 0.0):
        """
        Initializes the SeignorageModel with the provided parameters.

        Args:
            wallets_generator (WalletsGenerator): An instance of WalletsGenerator 
                                                  responsible for generating 
                                                  wallet balances for purchase 
                                                  simulations.
            stablecoin (AlgorithmicStablecoin): The algorithmic stablecoin associated
                                                 with this model.
            threshold (float): A  threshold parameter that defines when the stablecoin 
                               is considered to be in a normal state. (default: 0.05)
            delta_variation (Callable[[float], float]): A mathematical function 
            sigma (float): Standard deviation. Default is 1.0. 
            mean (float): Mean value. Default is 0.0.

        Raises:
            TypeError: If any argument is not of the expected type.
            ValueError: If `threshold` or `sigma` are not positive.
        """
        # Type checks
        if not isinstance(wallets_generator, WalletsGenerator):
            raise TypeError("wallets_generator must be an instance of WalletsGenerator.")
        if not isinstance(stablecoin, AlgorithmicStablecoin):
            raise TypeError("stablecoin must be an instance of AlgorithmicStablecoin.")
        if not isinstance(threshold, (float, int)) or threshold <= 0:
            raise ValueError("threshold must be a positive number.")
        if not isinstance(sigma, (float, int)) or sigma <= 0:
            raise ValueError("sigma must be a positive number.")
        if not isinstance(mean, (float, int)):
            raise TypeError("mean must be a number.")
        if not callable(delta_variation):
            raise TypeError("delta_variation must be a callable function.")

        # Attribute initialization
        self.stablecoin = stablecoin
        self.threshold = float(threshold)
        self.sigma = float(sigma)
        self.mean = float(mean)
        self.delta_variation = delta_variation

        # Initialize the parent class
        super().__init__(wallets_generator)


    def generate_random_purchase(self):
        self.compute_mean_variation()
        # A quantity of the token is determined using a Gaussian distribution. If 
        # q is positive, the token is sold; otherwise, it is purchased.
        gaussian_value = np.random.normal(self.mean, self.sigma)
        gaussian_value = 
        # A user's balance is randomly drawn.
        user_wallet = self.wallets_generator.get_random_wallet
        # The actual transaction amount is the minimum between the value obtained 
        # from the Gaussian and the randomly extracted wallet balance.
        transaction_amount = gaussian_value if abs(gaussian_value) \
            < abs(user_wallet) else user_wallet
        return transaction_amount

    def compute_mean_variation(self):


