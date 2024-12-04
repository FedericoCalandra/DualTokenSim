from typing import Callable
from source.wallets_generators.wallets_generator import WalletsGenerator
from source.purchase_generators.purchase_generator import PurchaseGenerator
from source.tokens.seignorage_model_token import SeignorageModelToken
from source.tokens.algorithmic_stablecoin import AlgorithmicStablecoin
from source.tokens.collateral_token import CollateralToken
import numpy as np


class SeignorageModelPurchaseGenerator(PurchaseGenerator):
    """
    A concrete implementation of the PurchaseGenerator abstract class for generating
    random purchase events within a seigniorage model. In this context, the token 
    whose quantity is bought or sold must be an instance of either
    AlgorithmicStablecoin or CollateralToken.

    The nature of the purchase or sale is influenced by the price of an 
    algorithmic stablecoin within the seigniorage model.
    """
    
    def __init__(self, token: SeignorageModelToken, wallets_generator: WalletsGenerator, sigma: float = 1,
                 mean: float = 0, volume: float = 1000, delta_variation: Callable[[float], float] = lambda x: 1 / x,
                 threshold: float = 0.05):
        """
        Initializes the PurchaseGeneratorConcrete instance with the provided parameters.

        Args:
            token (AlgorithmicStablecoin or CollateralToken): The token whose
            quantity is being simulated for purchase or sale.
            wallets_generator (WalletsGenerator): An instance of WalletsGenerator 
            used to generate wallet balances for simulation.
            sigma (float): The variance of the Gaussian distribution used 
            to determine the sale quantity.
            mean (float): The mean of the Gaussian distribution used to determine 
            the sale quantity.
            volume (float): A scaling factor applied to the trade size based on
            market volatility.
            delta_variation (function): A mathematical function that adjusts 
            the average sale quantity based on the stablecoin's price.
            threshold (float): The price level below which market panic is triggered. 
            A value of 0.05 indicates normal market conditions if the price is 
            between 0.95 and 1.05.

        Raises:
            TypeError: If token is not an instance of either
                       `AlgorithmicStablecoin` or `CollateralToken`.
            ValueError: If `threshold`, `sigma`, or `mean` are not floats, or 
                        if `delta_variation` is not a function.
        """
        super().__init__(token, wallets_generator)
        if not isinstance(token, (AlgorithmicStablecoin, CollateralToken)):
            raise TypeError("token must be an instance of AlgorithmicStablecoin or CollateralToken.")
        if not all(isinstance(x, float) for x in [threshold, sigma, mean]):
            raise ValueError("threshold, sigma, and mean must be floats.") 
        if not isinstance(volume, float) or volume < 0:
            raise TypeError("volatility must be a float and must be positive.")
        if not callable(delta_variation):
            raise ValueError("delta_variation must be a function.")   

        # Initialization of arguments.   
        self.volume = volume
        self._initial_mean = mean
        self.threshold = threshold
        self.sigma = sigma
        self.mean = mean
        self.delta_variation = delta_variation

    def generate_random_purchase(self) -> float:
        """
        Computes the amount of tokens to be bought or sold. A negative amount
        indicates a sale, while a positive amount indicates a purchase. This amount
        is determined using a Gaussian distribution, where the mean depends on whether
        the market is in a normal state or a panic situation.

        If the stablecoin price falls outside the panic threshold, the function generates
        trades that mimic market panic behavior.

        Returns:
            A float representing the amount of tokens to be bought or sold, ensuring 
            the user cannot trade more tokens than available in their wallet.
        """
        if isinstance(self.token, AlgorithmicStablecoin):
            self.compute_mean_variation(self.token)
        else:
            self.compute_mean_variation(self.token.algorithmic_stablecoin())

        dollars_trade_amount = np.random.normal(self.mean, self.sigma) * self.volume
        trade_amount = dollars_trade_amount / self.token.price

        random_wallet_balance = self.wallets_generator.get_random_wallet(self.token.free_supply)

        return min(trade_amount, random_wallet_balance)

    def compute_mean_variation(self, stablecoin: AlgorithmicStablecoin):
        """
        Updates the mean of the Gaussian distribution based on the current token price.

        This method adjusts the `mean` attribute by applying the `delta_variation` 
        function to the provided token price. The `delta_variation` function defines
        how the Gaussian mean should vary in response to price changes, allowing
        the model to reflect market behavior dynamically in normal or panic situations.

        Args:
            stablecoin(float): The stablecoin of the seignorage model.
        """
        if not isinstance(stablecoin, AlgorithmicStablecoin):
            raise TypeError("Input of 'compute_mean_variation' must be an instance of AlgorithmicStablecoin.")
        if stablecoin.price > stablecoin.peg - self.threshold:
            self.mean = 0
        else:
            self.mean = self._initial_mean + self.delta_variation(stablecoin.price)
   
    def update_volume(self, volume: float):
        if not isinstance(volume, float) or volume < 0:
            raise TypeError("volatility must be a float and must be positive.")
        self.volume = volume
