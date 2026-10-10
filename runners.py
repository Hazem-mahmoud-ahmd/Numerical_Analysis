import subprocess
import os
import sympy as sp
from sympy.printing import sstr


def differentiate_fx(fx_str):
    """Symbolically differentiates f(x) using SymPy and returns the derivative
    in two formats: a display string (with parentheses) and a muParser-compatible
    string (^ instead of **). Returns (df_display, df_muparser, error_msg)."""
    try:
        x = sp.Symbol('x')
        f_expr  = sp.sympify(fx_str.replace('^', '**'))
        df_expr = sp.diff(f_expr, x)
        ordered = sstr(df_expr, order='grlex')
        df_muparser = ordered.replace('**', '^')
        df_display  = '(' + df_muparser + ')'
        return df_display, df_muparser, None
    except Exception as e:
        return None, None, str(e)


def _run(exe, input_str):
    """Launches a compiled C++ executable, pipes input_str to its stdin,
    and returns (stdout, stderr) as strings. Uses UTF-8 encoding to avoid
    \r\n line-ending translation on Windows."""
    result = subprocess.run(
        [exe],
        input=input_str,
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='replace'
    )
    return result.stdout, result.stderr


def run_bisection(fx, xl, xu, mode, value):
    """Runs bisection.exe with the given f(x), bracket [xl, xu],
    stopping mode ('e' for epsilon, 'i' for iterations), and stop value."""
    return _run('bisection.exe',          f"{fx}\n{xl}\n{xu}\n{mode}\n{value}\n")

def run_false_position(fx, xl, xu, mode, value):
    """Runs false_position.exe with the given f(x), bracket [xl, xu],
    stopping mode, and stop value."""
    return _run('false_position.exe',     f"{fx}\n{xl}\n{xu}\n{mode}\n{value}\n")

def run_newton(fx, dfx, x0, mode, value):
    """Runs newton.exe with f(x), its derivative f'(x), initial guess x0,
    stopping mode, and stop value. f'(x) is pre-computed by differentiate_fx()."""
    return _run('newton.exe',             f"{fx}\n{dfx}\n{x0}\n{mode}\n{value}\n")

def run_secant(fx, xi_minus, xi, mode, value):
    """Runs secant.exe with f(x), two initial points (xi-1 and xi),
    stopping mode, and stop value."""
    return _run('secant.exe',             f"{fx}\n{xi_minus}\n{xi}\n{mode}\n{value}\n")

def run_fixed_point(gx, x0, mode, value):
    """Runs simple_fixed_point.exe with the iteration function g(x),
    initial guess x0, stopping mode, and stop value."""
    return _run('simple_fixed_point.exe', f"{gx}\n{x0}\n{mode}\n{value}\n")
