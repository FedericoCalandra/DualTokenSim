from source.LiquidityPools.formula import Formula


class ConstantProductFormula(Formula):
    """
    Implements the constant product formula (CPF), which maintains the invariant k = x * y
    where x and y represent the reserves of two tokens in a liquidity pool.

    Methods:
        apply: Calculates the output token amount using the constant product formula.
    """

    def apply(self, input_quantity, input_reserve, output_reserve):
        """
        Applies the constant product formula to calculate the output amount of a token swap.

        Args:
            input_quantity (float): The amount of the input token being swapped.
            input_reserve (float): The current reserve of the input token in the pool.
            output_reserve (float): The current reserve of the output token in the pool.

        Returns:
            float: The calculated amount of the output token after the swap, maintaining
                   the constant product k = x * y.

        Formula:
            output_amount = (output_reserve * input_quantity) / (input_reserve + input_quantity)

        Explanation:
            The formula is derived from the invariant k = x * y. By adding input_quantity
            to input_reserve, we calculate the resulting output amount to satisfy the invariant.
        """
        if input_quantity <= 0:
            raise ValueError("Input quantity must be positive.")
        if input_reserve <= 0:
            raise ValueError("Input reserve must be positive.")
        if output_reserve <= 0:
            raise ValueError("Output reserve must be positive.")

        output_amount = (output_reserve * input_quantity) / (input_reserve + input_quantity)
        return output_amount
