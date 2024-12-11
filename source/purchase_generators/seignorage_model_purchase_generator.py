from typing import List
from source.tokens.algorithmic_stablecoin import AlgorithmicStablecoin
from source.tokens.collateral_token import CollateralToken
from source.tokens.seignorage_model_token import SeignorageModelToken
from source.purchase_generators.purchase_generator import PurchaseGenerator
from source.wallets_generators.exponential_wallets_generator import ExponentialWalletsGenerator
import numpy as np

class SeignorageModelPurchaseGenerator(PurchaseGenerator):
    """
    In this version, `volume` is a list of pre-generated volumes. 
    Each trade consumes and removes the first element of the list. 
    If all the volumes in the list are processed, an exception 
    is raised.
    """
    def __init__(self, 
                 token: SeignorageModelToken, 
                 initial_volumes: List[float],
                 mean: float = 0.0,  
                 variance: float = 1.0
                ):
        """
        Args:
            token (SeignorageModelToken): The token for which purchase or sale 
            volumes are generated.
            initial_volumes (List[float]): Initial list of trade volumes.
            variance (float): Variance of the Gaussian distribution for trade amounts
            and their nature (sale or purchase).
            mean (float): Mean of the Gaussian distribution for trade amounts.

        Raises:
            TypeError: If token is not an instance of
                       `AlgorithmicStablecoin` or `CollateralToken`.
            ValueError: `variance`, or `mean` are not positive floats.
        """
        # The instance is initialized with a dummy wallet generator (it is not
        # used within the class).
        super().__init__(token, ExponentialWalletsGenerator(0.01))
        if not isinstance(initial_volumes, list):
            raise TypeError("Volumes must be a list!")
        if not isinstance(token, (AlgorithmicStablecoin, CollateralToken)):
            raise TypeError("Token must be an instance of AlgorithmicStablecoin or CollateralToken.")
        for param, name in [
            (variance, "variance"),
            (mean, "mean"),
        ]:
            if not isinstance(param, (float, int)) or param < 0:
                raise ValueError(f"{name} must be a positive float or integer.") 

        # Initialize instance attributes.
        self.volumes = initial_volumes
        self.variance = float(variance)
        self.mean = float(mean)

    def generate_transaction_amount(self) -> float:
        """
        Consumes the first volume in the list. If the list is empty, it raises
        an exception.

        Returns:
            float: The amount of tokens to be bought or sold.
                   Positive values indicate sales, negative values indicate purchases.
        """
        if not self.volumes:
            raise IndexError("No more volumes available to process.")       
        # Retrieve and remove the first volume from the list
        volume = self.volumes.pop(0)
        # Calculation of the actual quantity to be exchanged using a Gaussian.
        trade_amount  = np.random.normal(self.mean, self.variance) * volume    
        # Return the final transaction amount.
        return float(trade_amount)
