import pandas as pd

class ODESolver:
    """Numerical methods for solving ordinary differential equations (IVPs)."""
    
    @staticmethod
    def euler(f, y0, t0, t_end, dt):
        """
        Solves dy/dt = f(t, y) using Euler's Method (First Order).
        Returns a DataFrame with time history.
        """
        t = t0
        y = y0
        history = [{'time': t, 'Temperature': y}]
        
        while t < t_end:
            # Prevent going over t_end by exactly dt if step sizes don't perfectly divide
            step = dt if (t + dt) <= t_end else (t_end - t)
            
            y += f(t, y) * step
            t += step
            history.append({'time': t, 'Temperature': y})
            
        return pd.DataFrame(history)

    @staticmethod
    def rk4(f, y0, t0, t_end, dt):
        """
        Solves dy/dt = f(t, y) using Runge-Kutta 4th Order Method (RK4).
        Returns a DataFrame with time history.
        """
        t = t0
        y = y0
        history = [{'time': t, 'Temperature': y}]
        
        while t < t_end:
            step = dt if (t + dt) <= t_end else (t_end - t)
            
            k1 = f(t, y)
            k2 = f(t + step/2, y + k1 * step/2)
            k3 = f(t + step/2, y + k2 * step/2)
            k4 = f(t + step, y + k3 * step)
            
            y += (k1 + 2*k2 + 2*k3 + k4) * (step / 6)
            t += step
            history.append({'time': t, 'Temperature': y})
            
        return pd.DataFrame(history)
