# 🚀 Aerospace Root-Finding Toolbox

**🌟 [Try the Live Web App Here!](INSERT_YOUR_LINK_HERE)**

## 📖 Overview
This project is a computational tool designed to solve complex, non-linear equations commonly found in aerospace engineering and thermodynamics. It implements numerical methods to find precise roots for critical flight, propulsion, and engine parameters.

## 🧮 Mathematical Models

### 1. Mach Number \( M \)
Solves for the flight Mach number using compressible flow and area-Mach relations. The solver finds the roots for subsonic and supersonic conditions:
\[ \frac{A}{A^*} = \frac{1}{M} \left( \frac{2 + (\gamma - 1)M^2}{\gamma + 1} \right)^{\frac{\gamma + 1}{2(\gamma - 1)}} \]

### 2. Heat Input \( Q_{in} \)
Calculates the required heat addition and energy transfer for thermodynamic engine cycles:
\[ Q_{in} = m \cdot c_p \cdot (T_3 - T_2) \]

## ⚙️ Features
- **Numerical Solvers:** Custom root-finding algorithms (e.g., Newton-Raphson, Bisection) optimized for engineering equations.
- **Aerospace Applications:** Built specifically for thermodynamics, fluid mechanics, and propulsion systems.
- **Interactive Interface:** Web-based GUI for entering variables and visualizing outputs instantly.

## 🚀 How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/Aerospace-Root-Finding-Toolbox.git
