# 🚀 Aerospace & Signal Integrity Toolbox

**[🔗 Try the Live Web App Here!](https://aerospace-toolbox-for-fun.streamlit.app/)**

## 📖 Project Overview
This repository contains a highly interactive computational suite designed to solve complex, non-linear equations found in **thermodynamics, gas dynamics, aerospace propulsion, and electromagnetics**. 

Many fundamental engineering equations cannot be solved algebraically and require numerical root-finding algorithms or ODE solvers. This toolbox automates those calculations, providing a premium, futuristic 3D GUI built on Streamlit for rapid design iteration and visualization without relying on manual trial-and-error.

---

## 🧮 Mathematical Models & Physics

To ensure this project serves as a reliable educational and engineering reference, the core equations driving each simulation module are detailed below.

### 1. Isentropic Flow & Mach Number ($M$)
Used in the design of converging-diverging nozzles (like rocket engine exhaust nozzles). A single cross-sectional area ratio can result in either subsonic or supersonic flow, so numerical root-finding algorithms (Newton-Raphson, Bisection, Secant) are used to find the right physical root.

**Equation:**
$$ \frac{A}{A^*} = \frac{1}{M} \left[ \frac{2 + (\gamma - 1)M^2}{\gamma + 1} \right]^{\frac{\gamma + 1}{2(\gamma - 1)}} $$
*Where:*
* $A/A^*$ = Area ratio
* $M$ = Mach number
* $\gamma$ = Specific heat ratio (1.4 for standard air)

### 2. Thermal Radiation & Emissivity ($T$)
Evaluates the equilibrium heat transfer rate of a surface via thermal radiation using the Stefan-Boltzmann law. Because temperature is raised to the fourth power, finding the surface temperature given a specific solar heat flux requires iterative solving.

**Equation:**
$$ Q = \varepsilon \sigma A T^4 $$
*Where:*
* $Q$ = Absorbed solar heat flux (Watts)
* $\varepsilon$ = Emissivity of the surface (0 to 1)
* $\sigma$ = Stefan-Boltzmann constant ($5.67 \times 10^{-8} \, \text{W/m}^2\text{K}^4$)
* $T$ = Surface temperature (Kelvin)

### 3. Airfoil Aerodynamics & Stability
Computes the fundamental 2D aerodynamic forces (Lift and Drag) acting on an airfoil using dynamic pressure, and evaluates longitudinal stability parameters like the Center of Pressure and Static Margin.

**Dynamic Pressure ($q$):**  $q = \frac{1}{2} \rho V^2$
**Lift ($L$):** $L = q S C_L$
**Drag ($D$):** $D = q S C_D$

**Center of Pressure ($X_{cp}$) & Static Margin ($SM$):**
$$ X_{cp} = c \left( 0.25 - \frac{C_{M,ac}}{C_L \cos\alpha + C_D \sin\alpha} \right) $$
$$ SM\% = \frac{X_{ac} - X_{cg}}{c} \times 100 $$
*Where:* $c$ is the chord length, $\alpha$ is angle of attack, $C_{M,ac}$ is the pitching moment coefficient, and $X_{cg}$ is the calculated physical center of gravity based on component weights.

### 4. Transient Heat Transfer (ODE)
Simulates the time-temperature history of a satellite using a lumped-capacitance mathematical model subject to deep-space thermal radiation. Solved strictly using **Euler's Method (1st Order)** and **Runge-Kutta (RK4)** numerical algorithms.

**Differential Equation:**
$$ \frac{dT}{dt} = \frac{Q_{in} - \varepsilon \sigma A T^4}{m c_p} $$
*Where:* $m$ = mass (kg), $c_p$ = Specific heat capacity (J/kg·K).

### 5. EMI & Faraday Signal Analysis
Designed for avionics signal integrity, evaluating path loss over long distances, high-frequency shielding effectiveness of conductive meshes, and the surface confinement of RF currents.

**Free-Space Path Loss (FSPL):**
$$ FSPL\text{(dB)} = 20 \log_{10}(d) + 20 \log_{10}(f) - 147.55 $$

**Faraday Shielding Effectiveness (Sum of Absorption $A$ + Reflection $R$):**
$$ A\text{(dB)} = 131.4 \cdot t \cdot \sqrt{f \cdot \mu_r \cdot \sigma_r} \quad \text{and} \quad R\text{(dB)} = 168 - 10 \log_{10}\left( \frac{\mu_r f}{\sigma_r} \right) $$

**Skin Effect Penetration Depth ($\delta$):**
$$ \delta = \frac{1}{\sqrt{\pi f \mu_0 \mu_r \sigma}} $$
*Where:* $t$ = Shield thickness, $f$ = Frequency (Hz), $\sigma$ = Material Conductivity (S/m), $\mu$ = Permeability.

---

## ⚙️ Core Features
- **Numerical Math Solvers:** Implements robust root-finding algorithms (Bisection, Newton-Raphson, Secant) and **ODE Solvers** (Euler, RK4) optimized for non-linear engineering equations.
- **Aerospace Scope:** Tailored for BEng/BSc Aerospace Engineering coursework in aerodynamics, flight stability, thermodynamics, and signal integrity.
- **Futuristic 3D GUI:** A highly polished, custom-injected Streamlit CSS theme featuring an interactive, moving 3D cyber-grid background, glowing glassmorphism metrics, floating energy fields, and a sleek cyberpunk/aerospace aesthetic.

---

## 🚀 How to Run Locally

If you need to run this on your own machine without using the live site:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ImNewToCoding08/Aerospace-Root-Finding-Toolbox.git
   cd Aerospace-Root-Finding-Toolbox
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Streamlit Web Application:**
   ```bash
   streamlit run app.py
   ```

4. **Run the Native CLI Tool (Terminal only):**
   ```bash
   python main.py
   ```
