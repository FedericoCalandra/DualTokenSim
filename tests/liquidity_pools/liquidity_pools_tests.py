import unittest
from source.liquidity_pools.constant_product_formula import ConstantProductFormula
from source.liquidity_pools.liquidity_pool import LiquidityPool
from source.tokens.generic_token import GenericToken


class TestLiquidityPool(unittest.TestCase):
    def setUp(self):
        """Initialize a standard liquidity pool before each test"""
        self.token_a = GenericToken("TOKENA", 100000, 5000, 1)
        self.token_b = GenericToken("TOKENB", 100000, 5000, 5)
        self.formula = ConstantProductFormula()
        self.standard_fee = 0.003

    def create_pool(self, qty_a: float, qty_b: float, fee: float) -> 'LiquidityPool':
        """Helper method to create a liquidity pool with specified parameters"""
        return LiquidityPool(
            self.token_a, self.token_b, qty_a, qty_b, fee, self.formula
        )

    def test_basic_swap(self):
        """Test a basic swap operation with standard parameters"""
        # Arrange
        pool = self.create_pool(1000.0, 1000.0, self.standard_fee)
        input_amount = 100.0

        # Act
        output_token, output_amount = pool.swap(self.token_a, input_amount)

        # Assert
        self.assertEqual(output_token, self.token_b)
        self.assertAlmostEqual(pool.quantity_token_a, 1100.0, places=6)
        expected_output = self.formula.apply(
            input_amount * (1 - self.standard_fee), 1000.0, 1000.0
        )
        self.assertAlmostEqual(pool.quantity_token_b, 1000.0 - expected_output, places=6)

    def test_negative_swap(self):
        """Test removing tokens from the pool using a negative amount"""
        # Arrange
        pool = self.create_pool(1000.0, 1000.0, self.standard_fee)
        output_amount = -50.0  # Request to remove this amount of output token

        # Act
        output_token, input_amount = pool.swap(self.token_b, output_amount)

        # Assert
        self.assertEqual(output_token, self.token_b)
        expected_input = self.formula.inverse_apply(
            -output_amount * (1 - self.standard_fee), 1000.0, 1000.0
        )
        self.assertAlmostEqual(input_amount, expected_input, places=6)
        self.assertAlmostEqual(pool.quantity_token_b, 1000.0 + output_amount, places=6)

    def test_fee_calculations(self):
        """Test different fee scenarios including zero fee"""
        fee_cases = [
            (0.0, 100.0),  # No fee
            (0.01, 100.0),  # 1% fee
            (0.1, 100.0),  # 10% fee
            (0.003, 1000.0)  # Standard fee with larger amount
        ]

        for fee, input_amount in fee_cases:
            with self.subTest(f"Testing with fee {fee} and input {input_amount}"):
                # Arrange
                pool = self.create_pool(1000.0, 1000.0, fee)
                initial_b = pool.quantity_token_b

                # Act
                _, output_amount = pool.swap(self.token_a, input_amount)

                # Assert
                effective_input = input_amount * (1 - fee)
                expected_output = self.formula.apply(
                    effective_input, 1000.0, 1000.0
                )
                self.assertAlmostEqual(output_amount, expected_output, places=6)
                self.assertAlmostEqual(
                    pool.quantity_token_b,
                    initial_b - expected_output,
                    places=6
                )

    def test_edge_case_liquidity(self):
        """Test pool behavior with extreme liquidity conditions"""
        test_cases = [
            (1e-6, 1000.0, 0.1),  # Very low token A liquidity
            (1000.0, 1e-6, 0.1),  # Very low token B liquidity
            (1e18, 1e18, 1000.0),  # Very high liquidity
            (1.0, 1.0, 0.0001)  # Small swap amount
        ]

        for qty_a, qty_b, input_amount in test_cases:
            with self.subTest(f"Testing with {qty_a}, {qty_b}, {input_amount}"):
                # Arrange
                pool = self.create_pool(qty_a, qty_b, 0)
                initial_k = qty_a * qty_b

                # Act
                _, _ = pool.swap(self.token_a, input_amount)

                # Assert
                final_k = pool.quantity_token_a * pool.quantity_token_b
                # Use relative tolerance for extreme values
                self.assertAlmostEqual(initial_k / final_k, 1.0, places=6)

    def test_invariant_multiple_swaps(self):
        """Test that the constant product invariant is maintained after multiple swaps"""
        # Arrange
        pool = self.create_pool(1000.0, 1000.0, 0)
        initial_k = pool.quantity_token_a * pool.quantity_token_b
        swaps = [
            (self.token_a, 100.0),
            (self.token_b, 50.0),
            (self.token_a, 200.0),
            (self.token_b, 150.0)
        ]

        # Act
        for token, amount in swaps:
            pool.swap(token, amount)

        # Assert
        final_k = pool.quantity_token_a * pool.quantity_token_b
        # The final k should be slightly less than initial k due to fees
        self.assertGreaterEqual(final_k, initial_k)
        self.assertLess(final_k, initial_k * 1.05)  # Arbitrary threshold

    def test_invalid_swaps(self):
        """Test error handling for invalid swap attempts"""
        pool = self.create_pool(1000.0, 1000.0, self.standard_fee)

        invalid_cases = [
            (GenericToken("INVALID", 1, 1, 1), 100.0),  # Invalid token
            (self.token_a, 0.0)  # Zero amount
        ]

        for token, amount in invalid_cases:
            with self.subTest(f"Testing invalid swap: {token.__repr__()}, {amount}"):
                with self.assertRaises(ValueError):
                    pool.swap(token, amount)


if __name__ == '__main__':
    unittest.main()
