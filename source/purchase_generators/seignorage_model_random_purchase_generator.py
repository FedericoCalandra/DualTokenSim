from typing import Callable
from source.tokens.algorithmic_stablecoin import AlgorithmicStablecoin
from source.tokens.collateral_token import CollateralToken
from source.tokens.seignorage_model_token import SeignorageModelToken
from source.purchase_generators.purchase_generator import PurchaseGenerator
from source.wallets_generators.wallets_generator import WalletsGenerator
import numpy as np

class SeignorageModelRandomPurchaseGenerator(PurchaseGenerator):
    """
    A concrete implementation of the PurchaseGenerator abstract class for generating
    random trade events within a seigniorage model. In this context, the token 
    whose quantity is bought or sold must be an instance of either
    AlgorithmicStablecoin or CollateralToken.

    The nature of the purchase or sale is influenced by the price of an 
    algorithmic stablecoin within the seigniorage model.
    """
    
    def __init__(self, 
                 token: SeignorageModelToken, 
                 wallets_generator: WalletsGenerator,
                 volume_variance = 1000.0,
                 initial_volume: float = 1000.0, 
                 variance: float = 1.0,
                 mean: float = 0.0,  
                 delta_variation: Callable[[float], float] = lambda x: 1 / x,
                 threshold: float = 0.05
                 ):
        """
        Initialize the purchase generator with parameters for Gaussian distributions
        and market behavior adjustments.

        Args:
            token (SeignorageModelToken): The token for which purchase or sale 
            volumes are generated.
            wallets_generator (WalletsGenerator):  Generates wallet balances for simulation.
            volume_variance (float): Variance for random volume updates.
            initial_volume (float): Initial trade volume scaling factor.
            variance (float): Variance of the Gaussian distribution for trade amounts
            and his nature (sale or purchase).
            mean (float): Mean of the Gaussian distribution for trade amounts.
            delta_variation (Callable[[float], float]): Function to adjust mean trade
            amount based on the stablecoin's price.
            threshold (float): Panic threshold; defines the price range where
            market panic occurs.

        Raises:
            TypeError: If token is not an instance of
                       `AlgorithmicStablecoin` or `CollateralToken`.
            ValueError: If `volume_variance`, `initial_volume`, `variance`, or `mean`
                        are not positive floats.
            ValueError: If `delta_variation` is not callable.
        """
        super().__init__(token, wallets_generator)
        if not isinstance(token, (AlgorithmicStablecoin, CollateralToken)):
            raise TypeError("Token must be an instance of AlgorithmicStablecoin or CollateralToken.")
        if not callable(delta_variation):
            raise ValueError("delta_variation must be a callable function.")  
        for param, name in [
            (volume_variance, "volume_variance"),
            (initial_volume, "initial_volume"),
            (variance, "variance"),
            (mean, "mean"),
        ]:
            if not isinstance(param, (float, int)) or param < 0:
                raise ValueError(f"{name} must be a positive float or integer.") 

        # Initialize instance attributes.
        self.volume_variance = float(volume_variance)
        self.volume = float(initial_volume)
        self.variance = float(variance)
        self.mean = float(mean)
        self._initial_mean = float(mean)
        self.delta_variation = delta_variation
        self.threshold = float(threshold)

    def _compute_volume(self) -> float:
        """
        Updates and returns the current trade volume based on a random 
        Gaussian variation.

        Returns:
            float: The updated volume.
        """
        self.volume = abs(self.volume + np.random.normal(0, self.volume_variance))
        return float(self.volume) 

    def generate_transaction_amount(self) -> float:
        """
        Generates a random purchase or sale amount based on the current market conditions.
        The amount is scaled by the volume and influenced by a Gaussian distribution.

        Returns:
            float: The amount of tokens to be bought or sold.
                   Positive values indicate sales, negative values indicate purchases.
        """
        # Adjust the Gaussian mean based on stablecoin's price
        if isinstance(self.token, AlgorithmicStablecoin):
            self._compute_mean_variation(self.token)
        else:
            self._compute_mean_variation(self.token.algorithmic_stablecoin())
        # Compute trade amount in dollar terms.
        dollars_trade_amount = np.random.normal(self.mean, self.variance) * \
              self._compute_volume()
        # Convert trade amount to token units using the current token price.
        trade_amount = dollars_trade_amount / self.token.price
        # A random wallet balance is randomly drawn.
        random_wallet_balance = self._wallets_generator.get_random_wallet(self.token.free_supply)
        # Ensure trade amount does not exceed wallet balance
        return float(min(trade_amount, random_wallet_balance))

    def _compute_mean_variation(self, stablecoin: AlgorithmicStablecoin):
        """
        Adjusts the Gaussian mean based on the stablecoin's current price.
        Reflects market conditions such as panic or stability.

        Args:
            stablecoin (AlgorithmicStablecoin): The stablecoin whose price determines mean adjustments.

        Raises:
            TypeError: If `stablecoin` is not an instance of AlgorithmicStablecoin.
        """
        if not isinstance(stablecoin, AlgorithmicStablecoin):
            raise TypeError("Input must be an instance of AlgorithmicStablecoin.")
        # Market stability
        if stablecoin.price > stablecoin.peg - self.threshold:
            self.mean = 0
        else:
            # Market panic behaviour
            self.mean = self._initial_mean + self.delta_variation(stablecoin.price)
   
