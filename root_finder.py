import pandas as pd

class RootFinder:
    """A comprehensive numerical methods library for root-finding."""
    
    @staticmethod
    def bisection(f, a, b, tol=1e-6, max_iter=100):
        """Finds root of f(x) between a and b using the Bisection method."""
        if f(a) * f(b) > 0:
            raise ValueError(f"Root not bracketed. f({a})={f(a):.4f}, f({b})={f(b):.4f}")
            
        history = []
        for i in range(max_iter):
            c = (a + b) / 2
            fc = f(c)
            error = abs(b - a) / 2
            history.append({'iteration': i+1, 'x': c, 'f(x)': fc, 'error': error})
            
            if error < tol or abs(fc) < tol:
                return c, pd.DataFrame(history)
                
            if f(a) * fc < 0:
                b = c
            else:
                a = c
                
        raise TimeoutError("Maximum iterations reached without convergence.")

    @staticmethod
    def newton_raphson(f, df, x0, tol=1e-6, max_iter=100):
        """Finds root of f(x) given derivative df(x) and initial guess x0."""
        x = x0
        history = []
        for i in range(max_iter):
            fx = f(x)
            dfx = df(x)
            
            if dfx == 0:
                raise ZeroDivisionError("Derivative is zero. Newton-Raphson failed.")
                
            x_new = x - fx / dfx
            error = abs(x_new - x)
            history.append({'iteration': i+1, 'x': x_new, 'f(x)': f(x_new), 'error': error})
            
            if error < tol or abs(f(x_new)) < tol:
                return x_new, pd.DataFrame(history)
                
            x = x_new
            
        raise TimeoutError("Maximum iterations reached without convergence.")

    @staticmethod
    def secant(f, x0, x1, tol=1e-6, max_iter=100):
        """Finds root of f(x) using Secant method with initial guesses x0 and x1."""
        history = []
        for i in range(max_iter):
            f0 = f(x0)
            f1 = f(x1)
            
            if f1 - f0 == 0:
                raise ZeroDivisionError("Denominator is zero. Secant method failed.")
                
            x_new = x1 - f1 * (x1 - x0) / (f1 - f0)
            error = abs(x_new - x1)
            history.append({'iteration': i+1, 'x': x_new, 'f(x)': f(x_new), 'error': error})
            
            if error < tol or abs(f(x_new)) < tol:
                return x_new, pd.DataFrame(history)
                
            x0 = x1
            x1 = x_new
            
        raise TimeoutError("Maximum iterations reached without convergence.")


