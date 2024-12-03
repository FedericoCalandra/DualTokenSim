from abc import ABC, abstractmethod


class Formula(ABC):
    """
    An abstract base class for defining formulas that calculate token swap values
    within a liquidity pool.

    Methods:
        apply: An abstract method that calculates the swap amount based on input and output
               token quantities. Must be implemented by subclasses.
        compute_reserve: An abstract method that calculates the reserve of a given token.
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

    @abstractmethod
    def inverse_apply(self, output_quantity, input_reserve, output_reserve):
        """
        Calculates the input amount of a token swap based on the provided output and token quantities
        in the pool and the swap algorithm.

        Args:
            output_quantity (float): The amount of the output token obtained after the swap.
            input_reserve (float): The reserve of the input token in the pool before the swap.
            output_reserve (float): The reserve of the output token in the pool before the swap.

        Returns:
            float: The calculated amount of the input token that generated the swap.

        Note:
            This method must be implemented by subclasses, each defining a specific
            swap calculation formula.
        """
        pass

    def compute_reserve(self, input_reserve, output_reserve, new_input_reserve):
        """
        Calculates the current reserve of the other token in the pool with respect to input_reserve.

        Args:
            input_reserve (float): The current reserve of the input token in the pool.
            output_reserve (float): The current reserve of the output token in the pool.
            new_input_reserve (float): The new reserve of the input token in the pool.

        Returns:
            float: The calculated amount of the new output reserve.
        """
        if input_reserve > new_input_reserve:
            obtained_quantity = input_reserve - new_input_reserve
            new_output_quantity = output_reserve + self.inverse_apply(obtained_quantity, output_reserve, input_reserve)
        else:
            obtained_quantity = new_input_reserve - input_reserve
            new_output_quantity = output_reserve - self.apply(obtained_quantity, input_reserve, output_reserve)

        return new_output_quantity
