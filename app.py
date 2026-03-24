import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math
from root_finder import RootFinder

# --- Page Configuration ---
st.set_page_config(page_title="Aerospace Root-Finding Toolbox", page_icon="🚀", layout="centered")

st.markdown("""
<style>
/* Base Modern Typography */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
html, body, [class*="css"]  {
    font-family: 'Inter', sans-serif;
}

/* Glassmorphism Metric Cards */
[data-testid="stMetricValue"] {
    font-size: 2.2rem !important;
    font-weight: 700 !important;
    color: #00d2ff !important;
}
[data-testid="stMetricLabel"] {
    font-size: 1rem !important;
    color: #94a3b8 !important;
    font-weight: 500 !important;
    margin-bottom: 0.5rem;
}
div[data-testid="metric-container"] {
    background: rgba(17, 24, 39, 0.7);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2), 0 2px 4px -1px rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(12px);
    transition: all 0.3s ease;
}
div[data-testid="metric-container"]:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 20px -3px rgba(0, 210, 255, 0.15), 0 4px 6px -2px rgba(0, 210, 255, 0.05);
    border: 1px solid rgba(0, 210, 255, 0.3);
}

/* Beautiful Gradients for Headers */
h1, h2, h3 {
    background: linear-gradient(135deg, #00d2ff 0%, #3a7bd5 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 800 !important;
    letter-spacing: -0.5px;
}

/* Premium Buttons */
.stButton > button {
    background: linear-gradient(135deg, #00d2ff 0%, #3a7bd5 100%);
    color: white !important;
    border-radius: 8px;
    border: none;
    padding: 0.6rem 1.5rem;
    font-weight: 600;
    transition: all 0.3s ease;
    width: 100%;
}
.stButton > button:hover {
    transform: scale(1.02);
    box-shadow: 0 0 20px rgba(0, 210, 255, 0.4);
}
</style>
""", unsafe_allow_html=True)

st.title("🚀 Aerospace Root-Finding Toolbox")
st.markdown("A numerical methods library comparing **Newton-Raphson**, **Secant**, and **Bisection** algorithms on implicit aerospace equations.")

# --- Sidebar Menu ---
st.sidebar.header("⚙️ Select a Module")
module = st.sidebar.radio("Choose a Test Case:", ["Compressible Flow (Area-Mach)", "Satellite Thermal Balance", "Airfoil Aerodynamics"])

# --- Helper Function for Plotting ---
def plot_convergence(hist_b, hist_n, hist_s, title):
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(hist_b['iteration'], hist_b['error'], marker='o', label='Bisection', linestyle='--')
    ax.plot(hist_n['iteration'], hist_n['error'], marker='s', label='Newton-Raphson', linewidth=2)
    ax.plot(hist_s['iteration'], hist_s['error'], marker='^', label='Secant', linestyle='-.')
    
    ax.set_yscale('log')
    ax.set_xlabel('Iteration Number')
    ax.set_ylabel('Absolute Error (log scale)')
    ax.set_title(title)
    ax.grid(True, which="both", ls="--", alpha=0.6)
    ax.legend()
    st.pyplot(fig) # Streamlit command to draw the plot!

# --- Module 1: Compressible Flow ---
if module == "Compressible Flow (Area-Mach)":
    st.header("💨 Isentropic Compressible Flow")
    st.markdown("Calculates the supersonic Mach number of a gas expanding through a nozzle given an Area Ratio ($A/A^*$).")
    
    # UI Inputs
    col1, col2 = st.columns(2)
    gamma = col1.number_input("Specific Heat Ratio (gamma)", value=1.4, step=0.1)
    A_ratio = col2.number_input("Target Area Ratio (A/A*)", value=2.0, min_value=1.01, step=0.5)
    
    def f(M):
        if M <= 1.0: return -1.0
        return (1/M) * ((2 + (gamma - 1) * M**2) / (gamma + 1)) ** ((gamma + 1) / (2 * (gamma - 1))) - A_ratio
    def df(M):
        h = 1e-5
        return (f(M + h) - f(M - h)) / (2 * h)

    if st.button("Calculate Mach Number"):
        try:
            root_b, hist_b = RootFinder.bisection(f, 1.01, 1000.0)
            root_n, hist_n = RootFinder.newton_raphson(f, df, 2.5)
            root_s, hist_s = RootFinder.secant(f, 2.0, 3.0)
            
            # Display Results nicely
            st.success(f"**Result:** The supersonic Mach number is **{root_n:.4f}**")
            
            st.subheader("Convergence Diagnostics")
            m1, m2, m3 = st.columns(3)
            m1.metric(label="Newton-Raphson", value=f"{len(hist_n)} iters", delta="Fastest", delta_color="normal")
            m2.metric(label="Secant", value=f"{len(hist_s)} iters")
            m3.metric(label="Bisection", value=f"{len(hist_b)} iters", delta="Slowest", delta_color="inverse")
            
            plot_convergence(hist_b, hist_n, hist_s, f"Algorithm Convergence (A/A* = {A_ratio})")
        except Exception as e:
            st.error(f"Calculation Error: {e}")

# --- Module 2: Satellite Thermal Balance ---
elif module == "Satellite Thermal Balance":
    st.header("🛰️ Satellite Thermal Balance")
    st.markdown("Calculates the equilibrium surface temperature of a satellite in a vacuum based on absorbed solar heat flux.")
    
    sigma = 5.67e-8  
    emissivity = st.slider("Surface Emissivity (0 to 1)", min_value=0.1, max_value=1.0, value=0.8, step=0.05)
    solar_flux = st.number_input("Absorbed Solar Heat Flux (W/m²)", value=1000.0, step=100.0)
    
    def f(T): return (emissivity * sigma * T**4) - solar_flux
    def df(T): return 4 * emissivity * sigma * T**3

    if st.button("Calculate Equilibrium Temperature"):
        try:
            root_b, hist_b = RootFinder.bisection(f, 1.0, 1e7)
            root_n, hist_n = RootFinder.newton_raphson(f, df, 300.0)
            root_s, hist_s = RootFinder.secant(f, 250.0, 350.0)
            
            celsius = root_n - 273.15
            st.success(f"**Result:** Surface Temperature is **{root_n:.2f} K** ({celsius:.2f} °C)")
            
            st.subheader("Convergence Diagnostics")
            m1, m2, m3 = st.columns(3)
            m1.metric(label="Newton-Raphson", value=f"{len(hist_n)} iters")
            m2.metric(label="Secant", value=f"{len(hist_s)} iters")
            m3.metric(label="Bisection", value=f"{len(hist_b)} iters")
            
            plot_convergence(hist_b, hist_n, hist_s, f"Algorithm Convergence (Q = {solar_flux} W/m²)")
        except Exception as e:
            st.error(f"Calculation Error: {e}")

# --- Module 3: Airfoil Analysis ---
elif module == "Airfoil Aerodynamics":
    st.header("🛩️ Airfoil Aerodynamics")
    st.markdown("Calculates the Lift, Drag, Total Aerodynamic Force, and Center of Pressure based on airfoil characteristics.")
    
    col1, col2 = st.columns(2)
    velocity = col1.number_input("Free-stream Velocity (v) [m/s]", value=100.0, step=10.0)
    density = col2.number_input("Air Density (rho) [kg/m³]", value=1.225, step=0.1)
    
    col3, col4 = st.columns(2)
    area = col3.number_input("Wing Area (S) [m²]", value=10.0, min_value=0.1, step=1.0)
    chord = col4.number_input("Chord Length (c) [m]", value=1.0, min_value=0.01, step=0.1)
    
    alpha_deg = st.number_input("Angle of Attack (alpha) [degrees]", value=5.0, step=1.0)
    
    with st.expander("⚙️ Advanced Aerodynamic Coefficients", expanded=False):
        col5, col6, col7 = st.columns(3)
        Cl = col5.number_input("Coefficient of Lift (Cl)", value=0.5, step=0.1)
        Cd = col6.number_input("Coefficient of Drag (Cd)", value=0.02, step=0.01)
        Cm_ac = col7.number_input("Moment Coeff at AC (Cm_ac)", value=-0.05, step=0.01)
    
    st.markdown("<br>", unsafe_allow_html=True) # Adds a little spacing before the button
    
    if st.button("Calculate Aerodynamic Characteristics"):
        q = 0.5 * density * velocity**2
        lift = q * area * Cl
        drag = q * area * Cd
        total_force = math.sqrt(lift**2 + drag**2)
        
        alpha_rad = math.radians(alpha_deg)
        denom = (Cl * math.cos(alpha_rad) + Cd * math.sin(alpha_rad))
        
        st.success("Analysis Complete!")
        m1, m2 = st.columns(2)
        m1.metric(label="Lift Force (N)", value=f"{lift:.2f}")
        m2.metric(label="Drag Force (N)", value=f"{drag:.2f}")
        
        m3, m4 = st.columns(2)
        m3.metric(label="Total Aerodynamic Force (N)", value=f"{total_force:.2f}")
        
        if denom == 0:
            st.warning("Cannot calculate Center of Pressure: Net normal force implies division by zero.")
        else:
            xcp_chord_ratio = 0.25 - (Cm_ac / denom)
            xcp_position = chord * xcp_chord_ratio
            m4.metric(label="Center of Pressure (from LE)", value=f"{xcp_position:.3f} m ({xcp_chord_ratio*100:.1f}% c)")
