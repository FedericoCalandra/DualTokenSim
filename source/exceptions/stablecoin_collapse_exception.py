class StablecoinCollapseException(Exception):
    """
    Raised when the algorithmic stablecoin system collapses due to insufficient collateral backing.
    """
    def __init__(self, message="The algorithmic stablecoin system has collapsed. Simulation terminated."):
        super().__init__(message)