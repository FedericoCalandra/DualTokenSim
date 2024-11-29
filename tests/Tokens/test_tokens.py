import unittest
from source.Tokens.token import Token
from source.Tokens.algorithmic_stablecoin import AlgorithmicStablecoin
from source.Tokens.collateral_token import CollateralToken
from source.Tokens.reference_token import ReferenceToken
from source.Tokens.generic_token import GenericToken


class TestTokenClasses(unittest.TestCase):

    def test_token_initialization(self):
        """Test base Token class initialization and validation"""
        # Valid initialization for GenericToken
        token = GenericToken("TestToken", 1000, 900, 10.0)
        self.assertEqual(token.name, "TestToken")
        self.assertEqual(token.supply, 1000)
        self.assertEqual(token.price, 10.0)
        self.assertEqual(token.free_supply, 900.0)

        # Test invalid name type
        with self.assertRaises(TypeError):
            GenericToken(123, 1000, 900, 10.0)  # Invalid name type

        # Test negative supply
        with self.assertRaises(ValueError):
            GenericToken("Test", -100, 900, 1.0)  # Negative supply

        # Test negative price
        with self.assertRaises(ValueError):
            GenericToken("Test", 1000, 900, -1.0)  # Negative price

        # Test free supply greater than supply.
        with self.assertRaises(ValueError):
            GenericToken("Test", 1000, 1100, 1.0)

    def test_token_price_setting(self):
        """Test setting new prices for tokens"""
        generic_token = GenericToken("TestToken", 1000, 900, 10.0)
        generic_token.price = 15.5  # Set new price using setter
        self.assertEqual(generic_token.price, 15.5)

        # Invalid price should raise error
        with self.assertRaises(ValueError):
            generic_token.price = -5  # Invalid price

    def test_reference_token(self):
        """Test Reference Token specific behaviors"""
        ref_token = ReferenceToken("USD")
        self.assertEqual(ref_token.price, 1.0)
        self.assertEqual(ref_token.supply, float('inf'))
        self.assertEqual(ref_token.free_supply, float('inf'))

        # Reference token price cannot be changed
        with self.assertRaises(AttributeError):
            ref_token.price = 2.0
        # Reference token supply cannot be changed
        with self.assertRaises(AttributeError):
            ref_token.supply = 500
        # Reference token free supply cannot be changed
        with self.assertRaises(AttributeError):
            ref_token.free_supply = 500
        
    def test_seignorage_model_token_minting(self):
        """Test minting tokens in seignorage model"""
        collateral_token = CollateralToken("LUNA", 1000, 900, 10.0)

        initial_supply = collateral_token.supply
        initial_free_supply = collateral_token.free_supply
        collateral_token.mint(500)
        self.assertEqual(collateral_token.supply, initial_supply + 500)
        self.assertEqual(collateral_token.free_supply, initial_free_supply + 500)

        with self.assertRaises(ValueError):
            collateral_token.mint(-100)  # Cannot mint negative amount

    def test_seignorage_model_token_burning(self):
        """Test burning tokens in seignorage model"""
        collateral_token = CollateralToken("LUNA", 1000, 900, 10.0)

        initial_supply = collateral_token.supply
        collateral_token.burn(300)
        self.assertEqual(collateral_token.supply, initial_supply - 300)

        with self.assertRaises(ValueError):
            collateral_token.burn(1500)  # Cannot burn more than supply

        collateral_token2 = CollateralToken("LUNA2", 1000, 900, 1)
        collateral_token2.free_supply = 300
        with self.assertRaises(ValueError):
            collateral_token2.burn(301)

    def test_algorithmic_stablecoin(self):
        """Test AlgorithmicStablecoin specific behaviors"""
        stablecoin = AlgorithmicStablecoin("UST", 10000, 900, 1.0, peg=1.0)
        
        self.assertEqual(stablecoin.peg, 1.0)
        self.assertEqual(stablecoin.price, 1.0)

        with self.assertRaises(ValueError):
            AlgorithmicStablecoin("BAD", 1000, 900, 1.0, peg=-1.0)  # Invalid peg

    def test_generic_token_supply_change(self):
        """Test changing supply for generic tokens"""
        generic_token = GenericToken("BTC", 1000, 900, 50000.0)
        
        generic_token.supply += 500  # Increase supply
        self.assertEqual(generic_token.supply, 1500)
        self.assertEqual(generic_token.free_supply, 1400)

        generic_token.supply -= 200  # Decrease supply
        self.assertEqual(generic_token.supply, 1300)
        self.assertEqual(generic_token.free_supply, 1200)

        with self.assertRaises(ValueError):
            generic_token.supply = -1500  # Cannot set negative supply

        genericToken2 = GenericToken("Ether", 1000, 300, 10)
        with self.assertRaises(ValueError):
            genericToken2.supply = 699

    def test_token_equality(self):
        """Test token object identity comparison"""
        token1 = GenericToken("TEST1", 1000, 900, 10.0)
        token2 = token1
        
        self.assertTrue(token1.is_equal(token2))  # Same object should be equal

    def test_algorithmic_stablecoin_price_adjustment(self):
        """Test price adjustment behavior in Algorithmic Stablecoin"""
        stablecoin = AlgorithmicStablecoin("UST", 10000, 900, 1.0, peg=1.0)
        
        # Adjust price up or down
        stablecoin.price = 1.05  # Slight increase
        self.assertEqual(stablecoin.price, 1.05)

        stablecoin.price = 0.95  # Slight decrease
        self.assertEqual(stablecoin.price, 0.95)

        # Test invalid price change
        with self.assertRaises(ValueError):
            stablecoin.price = -1.0  # Price cannot be negative

    def test_collateral_token_mint_burn_limit(self):
        """Test minting and burning limits in CollateralToken"""
        collateral_token = CollateralToken("ETH", 1000, 900, 2000.0)
        
        # Minting more tokens should increase supply
        collateral_token.mint(1000)
        self.assertEqual(collateral_token.supply, 2000)
        self.assertEqual(collateral_token.free_supply, 1900)

        # Burning tokens should decrease supply
        collateral_token.burn(500)
        self.assertEqual(collateral_token.supply, 1500)
        self.assertEqual(collateral_token.free_supply, 1400)

        # Ensure that burning more than available tokens raises an error
        with self.assertRaises(ValueError):
            collateral_token.burn(3000)  # Can't burn more than supply

    def test_reference_token_immutable_price(self):
        """Test that ReferenceToken's price cannot be changed"""
        ref_token = ReferenceToken("EUR")
        with self.assertRaises(AttributeError):
            ref_token.price = 10.0  # Should not allow price changes

    def test_seignorage_model_burn_after_mint(self):
        """Test minting and burning sequence"""
        collateral_token = CollateralToken("USDT", 1000, 900, 1.0)
        collateral_token.mint(500)
        self.assertEqual(collateral_token.supply, 1500)
        collateral_token.burn(200)
        self.assertEqual(collateral_token.supply, 1300)
        self.assertEqual(collateral_token.free_supply, 1200)


    def test_generic_token_to_string(self):
        """Test GenericToken string representation"""
        generic_token = GenericToken("GEN", 1000, 900, 50.0)
        self.assertEqual(repr(generic_token), \
                         "GenericToken(name=GEN, price=50.0, supply=1000.0, free_supply=900.0)")

    def test_algorithmic_stablecoin_peg_violation(self):
        """Test AlgorithmicStablecoin peg change"""
        stablecoin = AlgorithmicStablecoin("UST", 10000, 900, 1.0, peg=1.0)
        with self.assertRaises(AttributeError):
            stablecoin.peg = 1.2  

    def test_invalid_token_type(self):
        """Test invalid token type assignment"""
        with self.assertRaises(TypeError):
            Token("InvalidToken", 1000, 900, 10.0)  # Cannot instantiate Token directly

   
if __name__ == '__main__':
    unittest.main()

