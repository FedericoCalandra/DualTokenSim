from source.Tokens.token import Token

class VolatileCoin(Token):
    """
    A standard token whose price and supply can vary freely.
    Inherits all functionality from the Token class without modification.
    """

    def __repr__(self) -> str:
        """
        Represents the VolatileCoin object as a string for debugging.
        """
        return f"VolatileToken(name={self.name}, price={self.price}, supply={self.supply})"
