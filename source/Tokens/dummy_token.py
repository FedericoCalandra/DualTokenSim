from source.Tokens.token import Token

class DummyToken(Token):
    def __init__(self, name: str):
        """
        Initializes a DummyToken instance.
        
        Args:
            name (str): The name of the DummyToken.
        """
        # Call the parent constructor with a constant price of 1.0 and an undefined supply
        super().__init__(name=name, initial_supply=float('inf'), initial_price=1.0)

    def set_new_price(self, new_price: float):
        """
        Overrides the set_new_price method to prevent changing the price.
        
        Raises:
            ValueError: Always, because the price of DummyToken is fixed at 1.0.
        """
        raise ValueError("The price of DummyToken is fixed at 1.0 and cannot be changed.")

    def increase_supply(self, amount: int):
        """
        Overrides the increase_supply method to do nothing,
        since supply is considered infinite.
        """
        pass  # Do nothing, as the supply is infinite

    def reduce_supply(self, amount: int):
        """
        Overrides the reduce_supply method to do nothing,
        since supply is considered infinite.
        """
        pass  # Do nothing, as the supply is infinite

    def __repr__(self) -> str:
        """
        Represents the DummyToken object as a string for debugging.
        """
        return f"DummyToken(name={self.name}, price={self.price})"
