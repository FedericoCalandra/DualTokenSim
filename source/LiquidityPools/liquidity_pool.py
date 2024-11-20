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

    def swap(self, input_token, input_amount):
        """
        Executes a swap between token_a and token_b, adjusting the pool quantities accordingly.

        Args:
            input_token (Token): The token being provided to the pool (either token_a or token_b).
            input_amount (float): The amount of the input token to swap.

        Returns:
            tuple: The output token and the amount of the output token after swap and fee deduction.

        Raises:
            ValueError: If the input token is not recognized or if input_amount is invalid.
        """
        if input_token not in {self.token_a, self.token_b}:
            raise ValueError("Invalid input token for this liquidity pool.")
        if input_amount <= 0:
            raise ValueError("Input amount must be positive.")

        if input_token.is_equal(self.token_a):
            input_reserve, output_reserve = self.quantity_token_a, self.quantity_token_b
            output_token = self.token_b
        elif input_token.is_equal(self.token_b):
            input_reserve, output_reserve = self.quantity_token_b, self.quantity_token_a
            output_token = self.token_a
        else:
            raise ValueError("Invalid input token for this liquidity pool.")

        # Calculate output amount with fee applied and the swap commission
        output_amount = self.compute_swap_value(input_amount, input_reserve, output_reserve)

        # Update pool quantities based on the swap
        if input_token.is_equal(self.token_a):
            self.quantity_token_a += input_amount
            self.quantity_token_b -= output_amount
        else:
            self.quantity_token_b += input_amount
            self.quantity_token_a -= output_amount

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
