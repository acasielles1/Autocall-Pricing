"""Unit test for the Product class"""

import pytest
import numpy as np

from autocall.products.base import Product

class DummyProduct(Product):

    def payoff(self, final_prices):
        """Pay nothing in every scenario"""
        return np.zeros_like(final_prices)

class IncompleteProduct(Product):
    """Subclass that forgets to implement payoff."""    




# ---------------------------------------------------------------------------
# Valid construction
# ---------------------------------------------------------------------------


def test_valid_creation_stores_attributes():
    """A valid Dummy Product stores all attributes correctly"""

    dp = DummyProduct(2,5)

    assert dp.maturity == 2
    assert dp.notional == 5

def test_default_notional_is_hundred():
    """If no notional is given, it defaults to 100"""

    dp = DummyProduct(2)

    assert dp.notional == 100

def test_product_cannot_be_instantiated():
    """Product is abstract: creating it directly must raise TypeError."""

    with pytest.raises(TypeError):
        Product(maturity=1.0)


# ---------------------------------------------------------------------------
# Invalid inputs
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("bad_maturity", [0,-1, float("inf"), float("-inf"), float("nan")])
def test_non_positive_maturity_raises(bad_maturity):
    """A maturity that is non positive or non bounded is rejected"""
    with pytest.raises(ValueError, match= "The maturity must be a positive, finite float"):
        DummyProduct(bad_maturity, 2)

@pytest.mark.parametrize("bad_notional", [0,-1, float("inf"), float("-inf"), float("nan")])
def test_non_positive_notional_raises(bad_notional):
    """A notional that is non positive or non bounded is rejected"""
    with pytest.raises(ValueError, match= "The notional must be a positive, finite float"):
        DummyProduct (2, bad_notional)


# ---------------------------------------------------------------------------
# Invalid instantiation
# ---------------------------------------------------------------------------


def test_subclass_without_payoff_cannot_be_instantiated():
    """A subclass that does not implement payoff must raise TypeError."""
    with pytest.raises(TypeError):
        IncompleteProduct(maturity=1.0)