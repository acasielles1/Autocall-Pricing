from abc import ABC, abstractmethod
import numpy as np


class Product(ABC):
    """Abstract base class for all financial products in the library.

    A product is defined by its maturity, its notional and a payoff rule.
    Subclasses must implement :meth:`payoff`; this class cannot be
    instantiated directly.

    Payoffs are expressed from the holder's (long) perspective. The sign
    of a position (bought or sold) is handled outside the product.

    Parameters
    ----------
    maturity : float
        Time to maturity in years. Must be finite and strictly positive.
    notional : float, default 100.0
        Reference amount on which payments are computed. Must be finite
        and strictly positive. With the default of 100, amounts read as
        percentages of notional.

    Raises
    ------
    ValueError
        If ``maturity`` or ``notional`` is not finite and strictly positive.
    """
    
    def __init__(self, maturity : float, notional : float = 100.0) -> None: 
        if not np.isfinite(maturity) or maturity <= 0:
            raise ValueError("The maturity must be a positive, finite float")
        if not np.isfinite(notional) or notional <= 0:
            raise ValueError("The notional must be a positive, finite float")
        
        self.maturity = maturity
        self.notional = notional

    @abstractmethod
    def payoff(self, final_prices :np.ndarray) -> np.ndarray:
        """Compute the payoff at maturity in each simulated scenario.

        Parameters
        ----------
        final_prices : np.ndarray
            Prices of the underlying at maturity, shape ``(n,)``, one entry
            per scenario. Implementations must not modify it in place.

        Returns
        -------
        np.ndarray
            Payoff in each scenario, shape ``(n,)``, where entry ``i``
            corresponds to ``final_prices[i]``. Amounts are in the same
            currency units as the prices and the notional, from the
            holder's (long) perspective.
        """

    