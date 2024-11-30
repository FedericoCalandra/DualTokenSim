from typing import Callable
from source.wallets_generators.wallets_generator import WalletsGenerator
from source.purchase_generators.purchase_generator import PurchaseGenerator
from source.Tokens.seignorage_model_token import SeignorageModelToken
from source.Tokens.algorithmic_stablecoin import AlgorithmicStablecoin
from source.Tokens.collateral_token import CollateralToken
import numpy as np

class SeignorageModelPurchaseGenerator(PurchaseGenerator):
    """
    A concrete implementation of the PurchaseGenerator abstract class for generating
    random purchase events within a seigniorage model. In this context, the token 
    whose quantity is bought or sold must be an instance of either
    AlgorithmicStablecoin or CollateralToken.

    The nature of the purchase or sale is influenced by the price of an 
    algorithmic stablecoin within the seigniorage model.

    Attributes:
        token (AlgorithmicStablecoin or CollateralToken): The token whose quantity 
        is being simulated for purchase or sale.
        wallets_generator (WalletsGenerator): Provides wallet balances for the 
        simulation.
        threshold (float): The price level below which market panic is triggered.
        For instance, a threshold of 0.05 indicates a normal market situation 
        if the stablecoin's price is between 0.95 and 1.05.
        volatility (int): A factor that influences the trade amount, providing
        additional scaling based on market volatility.
        sigma (float): The variance of the Gaussian distribution from which 
        the sale quantity is drawn.
        mean (float): The mean of the Gaussian distribution from which the sale
        quantity is drawn.
        delta_variation (function): A mathematical function that describes how
        the mean of the Gaussian varies as a function of the stablecoin's price.
    """
    
    def __init__(self, token: SeignorageModelToken, wallets_generator: WalletsGenerator, 
                sigma: float = 1,
                mean: float = 0, 
                volatility: int = 1000,
                delta_variation: Callable[[float], float] = lambda x: 1/x, 
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
            volatility (int): A scaling factor applied to the trade size based on
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
        
        if not isinstance(token, (AlgorithmicStablecoin, CollateralToken)):
            raise TypeError("token must be an instance of AlgorithmicStablecoin or CollateralToken.")
        # Check that threshold, sigma, and mean are floats
        if not all(isinstance(x, float) for x in [threshold, sigma, mean]):
            raise ValueError("threshold, sigma, and mean must be floats.") 
        # Check that volatility is int.
        if not isinstance(volatility, int):
            raise TypeError("volatility must be an integer.")  
        # Check that delta_variation is a function
        if not callable(delta_variation):
            raise ValueError("delta_variation must be a function.")   

        # Initialization of arguments.   
        self.volatility = volatility
        self._initial_mean = mean
        self.token = token
        self.wallets_generator = wallets_generator
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
        # Update the Gaussian mean based on the stablecoin information.
        if isinstance(self.token, AlgorithmicStablecoin):
            self.compute_mean_variation(self.token)
        else:
            self.compute_mean_variation(self.token.stablecoin)
        # Determine the trade size in dollars using a Gaussian distribution.
        dollars_trade_amount = np.random.normal(self.mean, self.sigma) * self.volatility
        # Convert the trade size from dollars to tokens using the token's current price.
        trade_amount = dollars_trade_amount / self.token.price
        # A user's wallet balance is chosen randomly. 
        if isinstance(self.token, AlgorithmicStablecoin):
            random_wallet_balance = self.wallets_generator.get_random_wallet(self.token.free_supply)
        else:
            random_wallet_balance = self.wallets_generator.get_random_wallet(self.token.stablecoin.free_supply)
        # Return the smaller of the calculated trade amount and the available wallet 
        # balance. This ensures that the user cannot trade more tokens than 
        # they possess.
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
        if not isinstance(stablecoin):
            raise TypeError("Input of 'compute_mean_variation' must be an instance of AlgorithmicStablecoin.")
        if stablecoin.price > stablecoin.peg - self.threshold:
            self.mean = 0
        else:
            self.mean = self._initial_mean + self.delta_variation(stablecoin.price)
   
        


