import unittest
from source.Tokens.token import Token
from source.Tokens.seignorage_model_token import SeignorageModelToken
from source.Tokens.algorithmic_stablecoin import AlgorithmicStablecoin
from source.Tokens.collateral_token import CollateralToken
from source.Tokens.reference_token import ReferenceToken
from source.Tokens.generic_token import GenericToken

class TestTokenClasses(unittest.TestCase):
    def test_token_initialization(self):
        """Test base Token class initialization and validation"""
        with self.assertRaises(TypeError):
            Token(123, 100, 1.0)  # Invalid name type
        
        with self.assertRaises(ValueError):
            Token("Test", -100, 1.0)  # Negative supply
        
        with self.assertRaises(ValueError):
            Token("Test", 100, -1.0)  # Negative price

    def test_token_price_setting(self):
        """Test setting new prices for tokens"""
        generic_token = GenericToken("TestToken", 1000, 10.0)
        generic_token.set_new_price(15.5)
        self.assertEqual(generic_token.price, 15.5)

        with self.assertRaises(ValueError):
            generic_token.set_new_price(-5)

    def test_reference_token(self):
        """Test Reference Token specific behaviors"""
        ref_token = ReferenceToken("USD")
        self.assertEqual(ref_token.price, 1.0)
        self.assertEqual(ref_token.supply, float('inf'))

        with self.assertRaises(ValueError):
            ref_token.set_new_price(2.0)  # Should not allow price changes

    def test_seignorage_model_token_minting(self):
        """Test minting and burning tokens in seignorage model"""
        collateral_token = CollateralToken("LUNA", 1000, 10.0)
        
        initial_supply = collateral_token.supply
        collateral_token.mint(500)
        self.assertEqual(collateral_token.supply, initial_supply + 500)

        with self.assertRaises(ValueError):
            collateral_token.mint(-100)  # Cannot mint negative amount

    def test_seignorage_model_token_burning(self):
        """Test burning tokens in seignorage model"""
        collateral_token = CollateralToken("LUNA", 1000, 10.0)
        
        initial_supply = collateral_token.supply
        collateral_token.burn(300)
        self.assertEqual(collateral_token.supply, initial_supply - 300)

        with self.assertRaises(ValueError):
            collateral_token.burn(1500)  # Cannot burn more than supply

    def test_algorithmic_stablecoin(self):
        """Test AlgorithmicStablecoin specific behaviors"""
        stablecoin = AlgorithmicStablecoin("UST", 10000, 1.0, peg=1.0)
        
        self.assertEqual(stablecoin.peg, 1.0)
        self.assertEqual(stablecoin.price, 1.0)

        with self.assertRaises(ValueError):
            AlgorithmicStablecoin("BAD", 1000, 1.0, peg=-1.0)  # Invalid peg

    def test_generic_token_supply_change(self):
        """Test changing supply for generic tokens"""
        generic_token = GenericToken("BTC", 1000, 50000.0)
        
        generic_token.change_supply(500)
        self.assertEqual(generic_token.supply, 1500)

        generic_token.change_supply(-200)
        self.assertEqual(generic_token.supply, 1300)

        with self.assertRaises(ValueError):
            generic_token.change_supply(-1500)  # Cannot create negative supply

    def test_token_equality(self):
        """Test token object identity comparison"""
        token1 = GenericToken("TEST1", 1000, 10.0)
        token2 = GenericToken("TEST1", 1000, 10.0)
        
        self.assertTrue(token1.is_equal(token1))
        self.assertFalse(token1.is_equal(token2))  # Different instances

if __name__ == '__main__':
    unittest.main()