import unittest
from source.LiquidityPools.constant_product_formula import ConstantProductFormula
from source.LiquidityPools.liquidity_pool import LiquidityPool


class MockToken:
    def __init__(self, symbol: str):
        self.symbol = symbol

    def is_equal(self, other) -> bool:
        return self.symbol == other.symbol


class TestConstantProductFormula(unittest.TestCase):
    def setUp(self):
        """Initialize the formula instance before each test"""
        self.formula = ConstantProductFormula()

    def test_basic_constant_product(self):
        """
        Test that the constant product formula maintains k = x * y
        for a standard swap scenario
        """
        # Arrange
        input_reserve = 1000.0
        output_reserve = 1000.0
        input_quantity = 100.0

        # Act
        output_amount = self.formula.apply(input_quantity, input_reserve, output_reserve)

        # Assert
        initial_k = input_reserve * output_reserve
        final_k = (input_reserve + input_quantity) * (output_reserve - output_amount)
        self.assertAlmostEqual(initial_k, final_k, places=6)

    def test_extreme_values(self):
        """Test the formula with very large and very small values"""
        test_cases = [
            # (input_quantity, input_reserve, output_reserve)
            (1e-18, 1000.0, 1000.0),  # Very small input
            (1e18, 1e20, 1e20),  # Very large values
            (0.0001, 1e-6, 1.0),  # Small reserves
            (1000.0, 1e18, 1e-18)  # Extreme reserve ratio
        ]

        for input_qty, in_reserve, out_reserve in test_cases:
            with self.subTest(f"Testing with {input_qty}, {in_reserve}, {out_reserve}"):
                # Act
                output = self.formula.apply(input_qty, in_reserve, out_reserve)

                # Assert
                self.assertGreater(output, 0)
                initial_k = in_reserve * out_reserve
                final_k = (in_reserve + input_qty) * (out_reserve - output)
                # Use relative tolerance for extreme values
                self.assertAlmostEqual(initial_k / final_k, 1.0, places=6)

    def test_near_zero_quantity(self):
        """Test behavior when one token has near-zero quantity"""
        # Arrange
        input_reserve = 1000.0
        output_reserve = 1e-10
        input_quantity = 10.0

        # Act
        output_amount = self.formula.apply(input_quantity, input_reserve, output_reserve)

        # Assert
        self.assertLess(output_amount, output_reserve)
        self.assertGreater(output_amount, 0)

    def test_invalid_inputs(self):
        """Test that the formula properly handles invalid inputs"""
        invalid_cases = [
            (-100.0, 1000.0, 1000.0),  # Negative input quantity
            (100.0, -1000.0, 1000.0),  # Negative input reserve
            (100.0, 1000.0, -1000.0),  # Negative output reserve
            (100.0, 0.0, 1000.0),  # Zero input reserve
        ]

        for input_qty, in_reserve, out_reserve in invalid_cases:
            with self.subTest(f"Testing invalid inputs: {input_qty}, {in_reserve}, {out_reserve}"):
                with self.assertRaises(ValueError):
                    self.formula.apply(input_qty, in_reserve, out_reserve)


class TestLiquidityPool(unittest.TestCase):
    def setUp(self):
        """Initialize a standard liquidity pool before each test"""
        self.token_a = MockToken("TOKENA")
        self.token_b = MockToken("TOKENB")
        self.formula = ConstantProductFormula()
        self.standard_fee = 0.003  # 0.3% fee

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
        self.assertEqual(pool.quantity_token_a, 1100.0)
        expected_output = self.formula.apply(
            input_amount * (1 - self.standard_fee), 1000.0, 1000.0
        )
        self.assertAlmostEqual(pool.quantity_token_b, 1000.0 - expected_output)

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
            (MockToken("INVALID"), 100.0),  # Invalid token
            (self.token_a, -100.0),  # Negative amount
            (self.token_b, 0.0)  # Zero amount
        ]

        for token, amount in invalid_cases:
            with self.subTest(f"Testing invalid swap: {token.symbol}, {amount}"):
                with self.assertRaises(ValueError):
                    pool.swap(token, amount)


if __name__ == '__main__':
    unittest.main()