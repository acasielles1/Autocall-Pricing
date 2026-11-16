"""Unit tests for the Underlying class."""

import pytest

from autocall.underlying import Underlying


# ---------------------------------------------------------------------------
# Valid construction
# ---------------------------------------------------------------------------


def test_valid_creation_stores_attributes():
    """A valid Underlying stores every input as an attribute."""

    u = Underlying("SX5E", spot=100.0, vol=0.20, div=0.03)

    assert u.name == "SX5E"
    assert u.spot == 100.0
    assert u.vol == 0.20
    assert u.div == 0.03


def test_default_dividend_is_zero():
    """If no dividend yield is given, it defaults to zero."""
    u = Underlying("SX5E", spot=100.0, vol=0.20)

    assert u.div == 0.0


def test_zero_volatility_is_accepted():
    """Boundary case: vol = 0 is valid (deterministic limit of the model)."""

    u = Underlying("SX5E", spot=100.0, vol=0.0)

    assert u.vol == 0.0


# ---------------------------------------------------------------------------
# Invalid inputs
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("bad_spot", [0.0, -1.0, -100.0])
def test_non_positive_spot_raises(bad_spot):
    """A spot price that is zero or negative is rejected."""
    with pytest.raises(ValueError, match="Spot price must be strictly positive"):
        Underlying("SX5E", spot=bad_spot, vol=0.20)


def test_negative_volatility_raises():
    """A negative volatility is rejected."""
    with pytest.raises(ValueError, match="Volatility must be non-negative"):
        Underlying("SX5E", spot=100.0, vol=-0.01)


@pytest.mark.parametrize("bad_name", [123, 1.5, None])
def test_non_string_name_raises(bad_name):
    """A name that is not a string is rejected with a TypeError."""
    with pytest.raises(TypeError, match="Name must be a string"):
        Underlying(bad_name, spot=100.0, vol=0.20)


# ---------------------------------------------------------------------------
# Representation
# ---------------------------------------------------------------------------


def test_repr():
    """repr() returns a readable string that looks like the constructor call."""
    u = Underlying("SX5E", spot=100.0, vol=0.20, div=0.03)

    assert repr(u) == "Underlying('SX5E', spot=100.0, vol=0.2, div=0.03)"
