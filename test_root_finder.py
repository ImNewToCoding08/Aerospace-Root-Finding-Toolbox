import pytest
from root_finder import RootFinder

# --- Analytical Setup ---
# Equation: f(x) = x^2 - 4 (The positive root is exactly 2.0)
def f_test(x):
    return x**2 - 4.0

# Derivative: f'(x) = 2x
def df_test(x):
    return 2.0 * x

# --- Unit Tests ---

def test_bisection_accuracy():
    """Validates Bisection against an analytical solution."""
    root, hist = RootFinder.bisection(f_test, 0.0, 5.0, tol=1e-5)
    assert abs(root - 2.0) < 1e-4, f"Bisection failed: got {root} instead of 2.0"

def test_newton_raphson_accuracy():
    """Validates Newton-Raphson against an analytical solution."""
    root, hist = RootFinder.newton_raphson(f_test, df_test, 5.0, tol=1e-5)
    assert abs(root - 2.0) < 1e-4, f"Newton failed: got {root} instead of 2.0"

def test_secant_accuracy():
    """Validates Secant against an analytical solution."""
    root, hist = RootFinder.secant(f_test, 4.0, 5.0, tol=1e-5)
    assert abs(root - 2.0) < 1e-4, f"Secant failed: got {root} instead of 2.0"

def test_bisection_failure_mode():
    """Tests failure mode: Bisection should raise ValueError if root isn't bracketed."""
    # f(3) = 5 and f(5) = 21 (Both positive, no root between them)
    with pytest.raises(ValueError):
        RootFinder.bisection(f_test, 3.0, 5.0)

def test_newton_failure_mode():
    """Tests failure mode: Newton should raise ZeroDivisionError if derivative is 0."""
    # At x=0, the derivative 2(0) = 0.
    with pytest.raises(ZeroDivisionError):
        RootFinder.newton_raphson(f_test, df_test, 0.0)
