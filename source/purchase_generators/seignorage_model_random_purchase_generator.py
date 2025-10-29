from typing import Callable
from source.purchase_generators.seignorage_model_purchase_generator import SeignorageModelPurchaseGenerator
from source.tokens.seignorage_model_token import SeignorageModelToken
import numpy as np


class SeignorageModelRandomPurchaseGenerator(SeignorageModelPurchaseGenerator):
    """
    Extends the SeignorageModelPurchaseGenerator to include dynamic volatility adjustments for trade simulation.
    This generator introduces randomness in volatility over time to better simulate market dynamics.

    Attributes:
        volatility (list[float]): A list containing the current and historical volatility values.
        volatility_variance (float): Variance used to add randomness to the volatility at each step.
    """

    def __init__(self,
                 token: SeignorageModelToken,
                 volatility_variance=1000.0,
                 initial_volatility: float = 1000.0,
                 amount_variance: float = 1.0,
                 amount_mean: float = 0.0,
                 delta_variation: Callable[[float], float] = lambda x: 1 / x,
                 threshold: float = 0.05,
                 pool_fee: float = 0.0
                 ):
        """
        Initializes the SeignorageModelRandomPurchaseGenerator with parameters for volatility, Gaussian distribution,
        and market behavior adjustments.

        Args:
            token (SeignorageModelToken): The token whose trade amounts are generated.
            volatility_variance (float, optional): Variance used for generating random volatility changes. Default is 1000.0.
            initial_volatility (float, optional): Initial volatility value. Default is 1000.0.
            amount_variance (float, optional): Variance of the Gaussian distribution for trade amounts. Default is 1.0.
            amount_mean (float, optional): Mean of the Gaussian distribution for trade amounts. Default is 0.0.
            delta_variation (Callable[[float], float], optional): Function to adjust the mean based on token price.
                                                                  Default is a lambda function `1 / x`.
            threshold (float, optional): Price threshold for determining market conditions. Default is 0.05.
            pool_fee (float, optional): Fee applied to transactions. Default is 0.0.
        """
        self.volatility = [float(initial_volatility)]
        super().__init__(token, self.volatility, amount_variance, amount_mean, [0], delta_variation, threshold, pool_fee)

        self.volatility_variance = float(volatility_variance)

    def _compute_volatility(self):
        """
        Computes and appends a new volatility value by adding Gaussian noise to the previous volatility.

        The new volatility value is ensured to be non-negative.

        Raises:
            ValueError: If `volatility_variance` is not a positive value.
        """
        new_volatility = abs(self.volatility[0] + np.random.normal(0, self.volatility_variance))
        self.volatility.append(float(new_volatility))

    def generate_transaction_amount(self) -> float:
        """
        Generates a random trade amount based on current market conditions and dynamically adjusted volatility.

        Overrides the base class method to incorporate volatility adjustments before generating the transaction amount.

        Returns:
            float: The amount of tokens to be bought or sold. Positive values indicate sales,
                   and negative values indicate purchases.
        """
        self._compute_volatility()
        return super().generate_transaction_amount()
