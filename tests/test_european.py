"""Tests for the European products in autocall.products.european."""

import numpy as np
import pytest

from autocall.products.european import Call, Put

# Shared test data: one price below, at and above the strike.
PRICES = np.array([80.0, 100.0, 120.0])
STRIKE = 100.0
MATURITY = 1.0


# --- Value tests ---------------------------------------------------------


def test_call_payoff_values():
    call = Call(MATURITY, STRIKE)
    np.testing.assert_allclose(call.payoff(PRICES), [0.0, 0.0, 20.0])


def test_put_payoff_values():
    put = Put(MATURITY, STRIKE)
    np.testing.assert_allclose(put.payoff(PRICES), [20.0, 0.0, 0.0])


# --- Property tests ------------------------------------------------------


@pytest.mark.parametrize("product_cls", [Call, Put])
def test_payoff_preserves_shape(product_cls):
    product = product_cls(MATURITY, STRIKE)
    prices = np.linspace(50.0, 150.0, 1_000)
    assert product.payoff(prices).shape == prices.shape


@pytest.mark.parametrize("product_cls", [Call, Put])
def test_payoff_is_non_negative(product_cls):
    rng = np.random.default_rng(42)
    prices = rng.uniform(0.0, 200.0, size=1_000)
    assert np.all(product_cls(MATURITY, STRIKE).payoff(prices) >= 0.0)


@pytest.mark.parametrize("product_cls", [Call, Put])
def test_attributes_are_stored(product_cls):
    product = product_cls(MATURITY, STRIKE)
    assert product.maturity == MATURITY
    assert product.strike == STRIKE


# --- Validation tests ----------------------------------------------------


@pytest.mark.parametrize("product_cls", [Call, Put])
@pytest.mark.parametrize("bad_strike", [0.0, -10.0, np.nan, np.inf])
def test_invalid_strike_raises(product_cls, bad_strike):
    with pytest.raises(ValueError):
        product_cls(MATURITY, bad_strike)


@pytest.mark.parametrize("product_cls", [Call, Put])
@pytest.mark.parametrize("bad_maturity", [0.0, -1.0])
def test_invalid_maturity_raises(product_cls, bad_maturity):
    """Fails if the subclass forgets to call Product.__init__."""
    with pytest.raises(ValueError):
        product_cls(bad_maturity, STRIKE)
