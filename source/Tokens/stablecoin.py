from source.Tokens.token import Token

class Stablecoin(Token):
    def __init__(self, name: str, initial_supply: int, initial_price: float, peg: float = 1.0):
        """
        Initializes a Stablecoin instance.
        
        Args:
            name (str): The name of the stablecoin.
            initial_supply (int): The initial supply of the stablecoin.
            initial_price (float): The initial price of the stablecoin.
            peg (float): The value the stablecoin is pegged to, defaults to 1.0 (USD).
        
        Raises:
            ValueError: If the peg value is non-positive.
        """
        # Call the parent class constructor.
        super().__init__(name, initial_supply, initial_price)

        # Validate the peg value.
        if peg <= 0:
            raise ValueError("The peg value must be positive.")
          
        self.peg = peg

        def __repr__(self) -> str:
            """
            Represents the Stablecoin object as a string.
            """
            return f"Stablecoin(name={self.name}, supply={self.supply}, price={self.price}, peg={self.peg})"
