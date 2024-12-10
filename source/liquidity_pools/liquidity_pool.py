class LiquidityPool:
    """
    Represents a liquidity pool for two tokens, facilitating swaps between them with a specified fee
    and a formula-based computation method.

    Attributes:
        token_a (Token): The first token in the pool.
        token_b (Token): The second token in the pool.
        quantity_token_a (float): Quantity of token_a in the pool.
        quantity_token_b (float): Quantity of token_b in the pool.
        fee (float): Transaction fee percentage applied to each swap.
        formula (Formula): An instance of Formula to define how swap values are computed.

    Methods:
        swap: Executes a swap between token_a and token_b, updating the pool quantities and applying the fee.
        compute_swap_value: Uses the formula to calculate the swap value based on current quantities,
                            adjusted for transaction fee.
    """

    def __init__(self, token_a, token_b, quantity_token_a, quantity_token_b, fee, formula):
        """
        Initializes the LiquidityPool with two tokens, their quantities, a transaction fee,
        and a swap calculation formula.

        Args:
            token_a (Token): The first token in the pool.
            token_b (Token): The second token in the pool.
            quantity_token_a (float): Initial quantity of token_a in the pool.
            quantity_token_b (float): Initial quantity of token_b in the pool.
            fee (float): Transaction fee percentage (e.g., 0.003 for 0.3% fee).
            formula (Formula): A formula instance that implements the swap computation logic.
        """
        self.token_a = token_a
        self.token_b = token_b
        self.quantity_token_a = quantity_token_a
        self.quantity_token_b = quantity_token_b
        self.fee = fee
        self.formula = formula

    def swap(self, token, amount):
        """
        Executes a swap between token_a and token_b, adjusting the pool quantities accordingly.

        Args:
            token (Token): The token considered for the swap in the pool (either token_a or token_b).
            amount (float): The amount of the input token to swap. Positive to add to the pool,
                            negative to remove from the pool (using inverse computation).

        Returns:
            tuple: The output token and the amount of the output token after swap and fee deduction.

        Raises:
            ValueError: If the input token is not recognized.
        """
        if token not in {self.token_a, self.token_b}:
            raise ValueError("Invalid input token for this liquidity pool.")

        if token.is_equal(self.token_a):
            input_reserve, output_reserve = self.quantity_token_a, self.quantity_token_b
            input_token, output_token = self.token_a, self.token_b
        else:
            input_reserve, output_reserve = self.quantity_token_b, self.quantity_token_a
            input_token, output_token = self.token_b, self.token_a

        if amount > 0:
            output_amount = self.compute_swap_value(amount, input_reserve, output_reserve)
            input_reserve += amount
            output_reserve -= output_amount
            input_token.free_supply = input_token.free_supply - amount
            output_token.free_supply = output_token.free_supply + output_amount
        else:
            output_amount = -amount
            input_amount = self.compute_inverse_swap_value(output_amount, input_reserve, output_reserve)
            input_reserve -= input_amount
            output_reserve += output_amount
            input_token.free_supply = input_token.free_supply + input_amount
            output_token.free_supply = output_token.free_supply - output_amount

        if input_token.is_equal(self.token_a):
            self.quantity_token_a, self.quantity_token_b = input_reserve, output_reserve
        else:
            self.quantity_token_b, self.quantity_token_a = input_reserve, output_reserve

        self.token_a.price = self.quantity_token_b / self.quantity_token_a

        return output_token, output_amount

    def compute_swap_value(self, input_quantity, input_reserve, output_reserve):
        """
        Computes the amount of output token based on the input quantity, pool reserves,
        and transaction fee.

        Args:
            input_quantity (float): The amount of the input token being swapped.
            input_reserve (float): The current reserve of the input token in the pool.
            output_reserve (float): The current reserve of the output token in the pool.

        Returns:
            float: The computed amount of the output token after applying the fee.
        """
        # Apply the transaction fee
        effective_input = input_quantity * (1 - self.fee)

        # Use the provided formula to calculate swap amount
        output_amount = self.formula.apply(effective_input, input_reserve, output_reserve)

        return output_amount

    def compute_inverse_swap_value(self, output_quantity, input_reserve, output_reserve):
        """
        """
        # Use the provided formula to calculate swap amount
        input_amount = self.formula.inverse_apply(output_quantity, input_reserve, output_reserve)

        # Apply the transaction fee
        effective_input = input_amount / (1 - self.fee)

        return effective_input
