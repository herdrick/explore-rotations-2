"""
Module for formatting numeric values as fractions of π when appropriate.
"""
import numpy as np
from math import gcd


def format_value(value, epsilon=2e-2):
    """
    Format a numeric value, showing it as a fraction of π if it's close to n*π/d.

    Parameters:
    -----------
    value : float
        The numeric value to format
    epsilon : float
        Tolerance for considering a value equal to n*π/d (default: 1e-3)

    Returns:
    --------
    str
        Formatted string, either as a π fraction or a decimal number
    """
    # Check if value is close to zero
    if abs(value) < epsilon:
        return "0"

    # Check all combinations of n*π/d
    denominators = [1, 2, 4, 8]
    numerators = range(-16, 17)

    for d in denominators:
        for n in numerators:
            target = n * np.pi / d
            if abs(value - target) < epsilon:
                # Found a match! Now simplify and format
                return _format_pi_fraction(n, d)

    # No match found, return as decimal
    return f"{value: .3f}"


def _format_pi_fraction(n, d):
    """
    Format n/d as a fraction of π with proper simplification.

    Examples:
    - _format_pi_fraction(0, 1) → "0"
    - _format_pi_fraction(1, 1) → "π"
    - _format_pi_fraction(-1, 1) → "-π"
    - _format_pi_fraction(2, 1) → "2π"
    - _format_pi_fraction(1, 2) → "π/2"
    - _format_pi_fraction(-1, 2) → "-π/2"
    - _format_pi_fraction(3, 4) → "3π/4"
    """
    # Handle zero
    if n == 0:
        return "0"

    # Simplify the fraction
    g = gcd(abs(n), d)
    n_simplified = n // g
    d_simplified = d // g

    # Handle sign
    sign = "-" if n_simplified < 0 else ""
    n_abs = abs(n_simplified)

    # Format based on numerator and denominator
    if d_simplified == 1:
        # Cases like π, 2π, -π, -2π
        if n_abs == 1:
            return f"{sign}π"
        else:
            return f"{sign}{n_abs}π"
    else:
        # Cases like π/2, 3π/4, -π/2
        if n_abs == 1:
            return f"{sign}π/{d_simplified}"
        else:
            return f"{sign}{n_abs}π/{d_simplified}"


def format_matrix_2x2(matrix, epsilon=2e-2):
    """
    Format a 2x2 matrix with π fractions where appropriate.

    Parameters:
    -----------
    matrix : ndarray
        2x2 numpy array
    epsilon : float
        Tolerance for π fraction detection

    Returns:
    --------
    str
        Formatted matrix string
    """
    v00 = format_value(matrix[0, 0], epsilon)
    v01 = format_value(matrix[0, 1], epsilon)
    v10 = format_value(matrix[1, 0], epsilon)
    v11 = format_value(matrix[1, 1], epsilon)

    return f"[{v00}  {v01}]\n    [{v10}  {v11}]"
