from abc import ABC, abstractmethod


class Formula(ABC):
    """
    An abstract base class for defining formulas that calculate token swap values
    within a liquidity pool.

    Methods:
        apply: An abstract method that calculates the swap amount based on input and output
               token quantities. Must be implemented by subclasses.
    """

    @abstractmethod
    def apply(self, input_quantity, input_reserve, output_reserve):
        """
        Calculates the output amount of a token swap based on the provided token quantities
        in the pool and the swap algorithm.

        Args:
            input_quantity (float): The amount of the input token to be swapped.
            input_reserve (float): The current reserve of the input token in the pool.
            output_reserve (float): The current reserve of the output token in the pool.

        Returns:
            float: The calculated amount of the output token after the swap.

        Note:
            This method must be implemented by subclasses, each defining a specific
            swap calculation formula.
        """
        pass
