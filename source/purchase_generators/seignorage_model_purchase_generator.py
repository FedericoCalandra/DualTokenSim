from typing import Callable
from scipy.stats import truncnorm
from source.tokens.algorithmic_stablecoin import AlgorithmicStablecoin
from source.tokens.collateral_token import CollateralToken
from source.tokens.seignorage_model_token import SeignorageModelToken
from source.purchase_generators.purchase_generator import PurchaseGenerator


class SeignorageModelPurchaseGenerator(PurchaseGenerator):

    """
    A concrete implementation of the PurchaseGenerator abstract class for simulating
    random trade events within a seigniorage model. This generator adjusts the
    generated transaction amounts based on token price dynamics and volatility.

    Attributes:
        volatility (list[float]): A list of volatility values that influences the trade volume.
        amount_variance (float): Variance of the Gaussian distribution used to generate trade amounts.
        amount_mean (float): Mean of the Gaussian distribution used to generate trade amounts.
        delta_variation (Callable[[float], float]): A callable function to adjust the mean based on
                                                    the token's price.
        threshold (float): Threshold for determining market stability or panic conditions.
        pool_fee (float): Fee applied to transactions, influencing the amount distribution.
    """
    def __init__(self,
                 token: SeignorageModelToken,
                 volatility: list[float],
                 amount_variance: float = 1.0,
                 amount_mean: float = 0.0,
                 amount_mean_variation: list = None,
                 delta_variation: Callable[[float], float] = lambda x: 1 / x,
                 threshold: float = 0.05,
                 pool_fee: float = 0.0
                 ):
        """
        Initializes the SeignorageModelPurchaseGenerator with parameters for
        Gaussian distributions, market behavior adjustments, and transaction fees.

        Args:
            token (SeignorageModelToken): The token whose trade amounts are generated.
            volatility (list[float]): List of volatility values affecting trade volumes.
            amount_variance (float, optional): Variance of the Gaussian distribution for trade amounts. Default is 1.0.
            amount_mean (float, optional): Mean of the Gaussian distribution for trade amounts. Default is 0.0.
            delta_variation (Callable[[float], float], optional): Function to adjust the mean based on token price.
                                                                  Default is a lambda function `1 / x`.
            threshold (float, optional): Price threshold for determining market conditions. Default is 0.05.
            pool_fee (float, optional): Fee applied to transactions. Default is 0.0.

        Raises:
            TypeError: If `volatility` is not a list, or if `token` is not an instance of
                       AlgorithmicStablecoin or CollateralToken.
            ValueError: If `amount_variance`, `amount_mean`, or `pool_fee` are not positive floats or integers.
            ValueError: If `delta_variation` is not callable.
        """
        super().__init__(token)
        if amount_mean_variation is None:
            amount_mean_variation = [0.0]
        if not isinstance(volatility, list):
            raise TypeError("Volatility must be a list!")
        if not isinstance(token, (AlgorithmicStablecoin, CollateralToken)):
            raise TypeError("Token must be an instance of AlgorithmicStablecoin or CollateralToken.")
        if not callable(delta_variation):
            raise ValueError("delta_variation must be a callable function.")
        for param, name in [
            (amount_variance, "variance"),
            (amount_mean, "mean"),
            (pool_fee, "pool_fee")
        ]:
            if not isinstance(param, (float, int)) or param < 0:
                raise ValueError(f"{name} must be a positive float or integer.")

        self.volatility = volatility
        self.amount_variance = float(amount_variance)
        self._initial_mean = float(amount_mean)
        self.amount_mean = self._initial_mean
        self.amount_mean_variation = amount_mean_variation
        self.delta_variation = delta_variation
        self.threshold = float(threshold)
        self.pool_fee = float(pool_fee)

    def generate_transaction_amount(self) -> float:
        """
        Generates a random trade amount based on current market conditions and volatility.
        The amount is drawn from a truncated Gaussian distribution and adjusted for transaction fees.

        Returns:
            float: The amount of tokens to be bought or sold. Positive values indicate sales,
                   and negative values indicate purchases.

        Raises:
            ValueError: If `amount_variance` is not a positive value.
        """
        if self.amount_variance <= 0:
            raise ValueError("Variance must be a positive value.")

        if isinstance(self.token, AlgorithmicStablecoin):
            self._compute_mean_variation(self.token)
        else:
            self._compute_mean_variation(self.token.algorithmic_stablecoin)

        volatility = self.volatility.pop(0)

        min_value = - (self.token.supply - self.token.free_supply) * self.token.price / volatility
        max_value = self.token.free_supply * self.token.price / volatility
        a, b = ((min_value - self.amount_mean) / self.amount_variance, (max_value - self.amount_mean) /
                self.amount_variance)

        dollars_trade_amount = truncnorm.rvs(a, b, loc=self.amount_mean, scale=self.amount_variance) * volatility
        trade_amount = dollars_trade_amount / self.token.price

        if trade_amount < 0:
            trade_amount *= 1 - self.pool_fee       # Necessary to avoid amount distribution imbalances

        return trade_amount

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
            if len(self.amount_mean_variation) > 0:
                self.amount_mean = self.amount_mean_variation.pop()
            else:
                self.amount_mean = self._initial_mean
        else:
            # Market panic behaviour
            self.amount_mean = self._initial_mean + self.delta_variation(stablecoin.price)
