class Underlying:
    """Market data for a single underlying asset.

    Stores the static inputs that a pricing model needs to simulate the
    asset under the risk-neutral measure: current price, volatility and
    continuous dividend yield. Inputs are validated on construction so
    that inconsistent market data is rejected as early as possible.

    Parameters
    ----------
    name : str
        Identifier of the asset, e.g. a ticker such as ``"SX5E"``.
    spot : float
        Current price of the asset, in the asset's currency units.
        Must be strictly positive.
    vol : float
        Annualised volatility of log-returns, expressed as a decimal
        (``0.20`` means 20 %). Must be non-negative.
    div : float, default 0.0
        Annualised, continuously compounded dividend yield, expressed
        as a decimal (``0.03`` means 3 %).

    Raises
    ------
    ValueError
        If ``spot`` is not strictly positive or ``volatility`` is negative.

    Notes
    -----
    Volatility and dividend yield are assumed constant over time,
    consistent with the geometric Brownian motion (Black-Scholes)
    framework used throughout the library.

    Example
    --------
    >>> Underlying("SX5E", spot=100.0, vol=0.20, div=0.03)
    """
    def __init__(self, name : str, spot : float, vol :float, div :float = 0.00) -> None:
        if type(name) != str:
                raise TypeError(f"Name must be a string")
        if spot <= 0:
                raise ValueError (f"Spot price must be strictly positive")
        if vol <0:
                raise ValueError(f"Volatility must be non-negative")
        self.name = name
        self.spot = spot
        self.vol = vol
        self.div = div

    def __repr__(self):
        return f"Underlying({self.name!r}, spot={self.spot}, vol={self.vol}, div={self.div})"


