# 🚀 Aerospace Root-Finding Toolbox

**[🔗 Try the Live Web App Here!](INSERT_YOUR_APP_LINK_HERE)**

## 📖 Project Overview
This repository contains a computational tool designed to solve complex, non-linear equations found in **thermodynamics, gas dynamics, and aerospace propulsion**. 

Many fundamental aerospace equations cannot be solved algebraically and require numerical root-finding methods (such as Newton-Raphson or Bisection). This tool automates those calculations, providing a clean interface for rapid design iteration without relying on manual trial-and-error.

---

## 🧮 Mathematical Models & Physics

To ensure this project is easy to understand later, here are the exact equations being solved and what they represent in aerospace engineering.

### 1. Isentropic Flow & Mach Number (M)
Used in the design of converging-diverging nozzles (like rocket engine exhaust nozzles). A single cross-sectional area ratio (A/A*) can result in either subsonic or supersonic flow, so numerical solvers are used to find the correct root (Mach number) for the chosen flight regime.

**Equation:**
`A / A* = (1 / M) * [ (2 + (γ - 1)M²) / (γ + 1) ] ^ [ (γ + 1) / 2(γ - 1) ]`

*Where:*
* `A/A*` = Area ratio
* `M` = Mach number
* `γ` (Gamma) = Specific heat ratio (1.4 for standard air)

### 2. Thermodynamic Heat Transfer (Q_in)
Evaluates the heat energy added to a system. This is specifically modeled for the combustion chamber phase of a gas turbine engine (Brayton Cycle).

**Equation:**
`Q_in = ṁ * c_p * (T3 - T2)`

*Where:*
* `Q_in` = Total heat input
* `ṁ` = Mass flow rate
* `c_p` = Specific heat at constant pressure
* `T2` = Compressor exit temperature
* `T3` = Turbine inlet temperature

---

## ⚙️ Core Features
- **Numerical Solvers:** Implements robust root-finding algorithms (SciPy/NumPy) optimized for non-linear engineering equations.
- **Aerospace Specific:** Tailored for BEng Aerospace Engineering coursework in thermodynamics and fluid mechanics.
- **Interactive Interface:** A web-based Graphical User Interface (GUI) built with Streamlit for instant variable input and visualization.

---

## 🚀 How to Run Locally

If you need to run this on your own machine, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/Aerospace-Root-Finding-Toolbox.git
   cd Aerospace-Root-Finding-Toolbox

