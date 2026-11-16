"""European products whose payoff depends only on the price at maturity.

This module defines Call, Put, Digital, Forward and Bond. Each of them
pays a single cash flow at maturity that is a function of the terminal
price S_T alone, so they can all be priced from simulated terminal
prices without full paths.

Conventions
-----------
- Maturities are expressed in years.
- Strikes are absolute levels, in the same units as the underlying price.
- ``payoff`` takes a NumPy array of terminal prices and returns an array
  of the same shape.
- Call, Put, Digital and Forward payoffs are per one unit of the
  underlying; the ``notional`` inherited from Product is not applied.
- Bond pays its fixed ``payment`` amount regardless of S_T.
- Digital pays when S_T >= K, so the boundary S_T = K is in the money.
"""

from autocall.products.base import Product

import numpy as np

class Call(Product):
    """European call option.

    Pays max(S_T - K, 0) at maturity, per one unit of the underlying.

    Parameters
    ----------
    maturity : float
        Time to maturity in years. Must be positive.
    strike : float
        Absolute strike level K. Must be positive.
    """

    def __init__(self, maturity, strike):
        super().__init__(maturity)
        if not np.isfinite(strike) or strike <= 0:
            raise ValueError("The strike must be a positive, finite float")

        self.strike = strike

    def payoff(self, final_prices : np.ndarray) -> np.ndarray:
        diff = final_prices - self.strike
        return np.maximum(diff, 0)

class Put(Product):
    """European put option.

    Pays max(K - S_T, 0) at maturity, per one unit of the underlying.

    Parameters
    ----------
    maturity : float
        Time to maturity in years. Must be positive.
    strike : float
        Absolute strike level K. Must be positive.
    """

    def __init__(self, maturity, strike):
        super().__init__(maturity)
        if not np.isfinite(strike) or strike <= 0:
            raise ValueError("The strike must be a positive, finite float")

        self.strike = strike

    def payoff(self, final_prices : np.ndarray) -> np.ndarray:
        diff = self.strike - final_prices
        return np.maximum(diff, 0)
 
if __name__ == "__main__":
    call = Call(1.0, 100.0)
    print(call.payoff(np.array([80.0, 100.0, 120.0])))

    put = Put(1.0, 100.0)
    print(put.payoff(np.array([80.0, 100.0, 120.0])))
