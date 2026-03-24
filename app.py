import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math
from root_finder import RootFinder
from ode_solver import ODESolver

# --- Page Configuration ---
st.set_page_config(page_title="Aerospace Root-Finding Toolbox", page_icon="🚀", layout="centered")

st.markdown("""
<style>
/* Base Modern Typography */
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;700&family=Rajdhani:wght@400;500;600;700&display=swap');
html, body, [class*="css"]  {
    font-family: 'Rajdhani', sans-serif;
    font-size: 1.1rem;
}

/* Futuristic Sci-Fi Animated Background */
.stApp {
    background-color: #050914 !important;
}

/* Moving Cyber-Grid */
.stApp::before {
    content: "";
    position: fixed;
    top: -50%; left: -50%;
    width: 200%; height: 200%;
    background-image: 
        linear-gradient(rgba(0, 210, 255, 0.07) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0, 210, 255, 0.07) 1px, transparent 1px);
    background-size: 50px 50px;
    transform: perspective(600px) rotateX(60deg) translateY(-100px) translateZ(-200px);
    animation: cyber-grid 8s linear infinite;
    pointer-events: none;
    z-index: 0;
}

@keyframes cyber-grid {
    0% { background-position: 0 0; }
    100% { background-position: 50px 50px; }
}

/* Floating Energy Orbs */
.stApp::after {
    content: "";
    position: fixed;
    top: 10%; right: 10%;
    width: 50vw; height: 50vh;
    background: radial-gradient(circle, rgba(58, 123, 213, 0.15), transparent 70%);
    border-radius: 50%;
    filter: blur(50px);
    animation: float-orb 15s ease-in-out infinite alternate;
    pointer-events: none;
    z-index: 0;
}

@keyframes float-orb {
    0% { transform: translate(0, 0) scale(1); }
    100% { transform: translate(-100px, 150px) scale(1.3); }
}

/* Main Content Layering over Background */
.main {
    z-index: 1;
    position: relative;
    background: transparent !important;
}

/* Make Sidebar Glassy too */
[data-testid="stSidebar"] {
    background: rgba(5, 9, 20, 0.8) !important;
    backdrop-filter: blur(15px);
    border-right: 1px solid rgba(0, 210, 255, 0.1);
}

/* Glassmorphism Metric Cards */
[data-testid="stMetricValue"] {
    font-family: 'Orbitron', sans-serif !important;
    font-size: 2.2rem !important;
    font-weight: 700 !important;
    color: #00d2ff !important;
    text-shadow: 0 0 10px rgba(0, 210, 255, 0.6);
}
[data-testid="stMetricLabel"] {
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 1.1rem !important;
    color: #94a3b8 !important;
    font-weight: 600 !important;
    text-transform: uppercase;
    letter-spacing: 1px;
}
div[data-testid="metric-container"] {
    background: linear-gradient(135deg, rgba(10, 14, 23, 0.85), rgba(17, 24, 39, 0.7));
    border: 1px solid rgba(0, 210, 255, 0.2);
    border-radius: 16px;
    padding: 1.5rem;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5), inset 0 0 15px rgba(0, 210, 255, 0.05);
    backdrop-filter: blur(12px);
    transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}
div[data-testid="metric-container"]:hover {
    transform: translateY(-5px) scale(1.02);
    box-shadow: 0 15px 35px -5px rgba(0, 210, 255, 0.3), inset 0 0 20px rgba(0, 210, 255, 0.15);
    border: 1px solid rgba(0, 210, 255, 0.6);
}

/* Headings with Glowing Sci-Fi Text */
h1, h2, h3 {
    font-family: 'Orbitron', sans-serif !important;
    background: linear-gradient(135deg, #00d2ff 0%, #3a7bd5 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 800 !important;
    letter-spacing: 1px;
    text-shadow: 0 0 30px rgba(0, 210, 255, 0.3);
}

/* Premium Sci-Fi Buttons */
.stButton > button {
    background: linear-gradient(135deg, rgba(0, 210, 255, 0.05), rgba(58, 123, 213, 0.05));
    color: #00d2ff !important;
    border: 1px solid #00d2ff;
    border-radius: 8px;
    padding: 0.6rem 1.5rem;
    font-family: 'Orbitron', sans-serif !important;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    transition: all 0.3s ease;
    width: 100%;
    box-shadow: 0 0 15px rgba(0, 210, 255, 0.1);
}
.stButton > button:hover {
    background: linear-gradient(135deg, #00d2ff 0%, #3a7bd5 100%);
    color: #ffffff !important;
    transform: scale(1.02);
    box-shadow: 0 0 25px rgba(0, 210, 255, 0.5);
    border: 1px solid transparent;
}

/* Input Boxes - Futuristic Styling */
.stTextInput > div > div > input,
.stNumberInput > div > div > input {
    background: rgba(10, 14, 23, 0.6) !important;
    border: 1px solid rgba(0, 210, 255, 0.2) !important;
    color: #00d2ff !important;
    border-radius: 8px !important;
    font-family: 'Orbitron', sans-serif !important;
    font-weight: 500 !important;
    backdrop-filter: blur(10px);
    transition: all 0.3s ease;
}
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus {
    box-shadow: 0 0 20px rgba(0, 210, 255, 0.3) !important;
    border-color: #00d2ff !important;
}

/* Custom expander headers */
.streamlit-expanderHeader {
    font-family: 'Orbitron', sans-serif !important;
    color: #e2e8f0 !important;
}

/* Fancy Success/Warning Alerts */
[data-testid="stAlert"] {
    background: rgba(10, 14, 23, 0.8) !important;
    backdrop-filter: blur(10px) !important;
    border: 1px solid rgba(0, 210, 255, 0.3) !important;
    border-left: 4px solid #00d2ff !important;
    box-shadow: 0 0 15px rgba(0, 210, 255, 0.1) !important;
    border-radius: 8px !important;
    font-family: 'Rajdhani', sans-serif !important;
    color: #e2e8f0 !important;
}
</style>
""", unsafe_allow_html=True)

st.title("🚀 Aerospace Root-Finding Toolbox")
st.markdown("A numerical methods library comparing **Newton-Raphson**, **Secant**, and **Bisection** algorithms on implicit aerospace equations.")

# --- Sidebar Menu ---
st.sidebar.header("⚙️ Select a Module")
module = st.sidebar.radio("Choose a Test Case:", ["Compressible Flow (Area-Mach)", "Satellite Thermal Balance", "Airfoil Aerodynamics", "Transient Heat Transfer (ODE)"])

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
        
    with st.expander("⚖️ Center of Gravity (CG) Locator", expanded=False):
        st.markdown("Calculate the physical CG and **Static Margin** based on component weights and arms (distance from Leading Edge).")
        w1, a1 = st.columns(2)
        w_empty = w1.number_input("Empty Weight (kg)", value=1200.0, step=100.0)
        arm_empty = a1.number_input("Empty Weight Arm (m)", value=1.0, step=0.1)
        
        w2, a2 = st.columns(2)
        w_payload = w2.number_input("Payload Weight (kg)", value=300.0, step=50.0)
        arm_payload = a2.number_input("Payload Arm (m)", value=1.5, step=0.1)
        
        w3, a3 = st.columns(2)
        w_fuel = w3.number_input("Fuel Weight (kg)", value=150.0, step=10.0)
        arm_fuel = a3.number_input("Fuel Arm (m)", value=0.8, step=0.1)
        
        total_weight = w_empty + w_payload + w_fuel
        if total_weight > 0:
            cg_location = ((w_empty * arm_empty) + (w_payload * arm_payload) + (w_fuel * arm_fuel)) / total_weight
            static_margin = ((0.25 * chord) - cg_location) / chord * 100 # AC assumed at c/4
            
            cgm1, cgm2 = st.columns(2)
            cgm1.metric("CG Location (from LE)", f"{cg_location:.3f} m")
            cgm2.metric("Static Margin", f"{static_margin:.1f}%")
            if static_margin < 0:
                st.error("⚠️ Negative Static Margin! Aircraft is longitudinally unstable.")
            else:
                st.success("✅ Aircraft is longitudinally stable.")
    
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

# --- Module 4: Transient Heat Transfer (ODE) ---
elif module == "Transient Heat Transfer (ODE)":
    st.header("🕰️ Transient Heat Transfer (ODE)")
    st.markdown("Simulates the time-temperature history of a satellite using the lumped-capacitance model numerical evaluation.")
    
    col1, col2, col3 = st.columns(3)
    mass = col1.number_input("Mass (kg)", value=50.0, min_value=1.0)
    cp = col2.number_input("Specific Heat (J/kg·K)", value=900.0, min_value=1.0)
    area = col3.number_input("Surface Area (m²)", value=2.0, min_value=0.1)
    
    with st.expander("⚙️ Thermal Environment & Initial Conditions", expanded=True):
        c4, c5, c6 = st.columns(3)
        emissivity = c4.number_input("Emissivity (ε)", value=0.8, step=0.05, min_value=0.01, max_value=1.0)
        solar_flux = c5.number_input("Absorbed Solar Flux (W)", value=500.0, step=50.0)
        t0_temp = c6.number_input("Initial Temp (K)", value=200.0, step=10.0)
        
        c7, c8 = st.columns(2)
        t_span = c7.number_input("Simulate for (seconds)", value=10000.0, step=1000.0)
        dt = c8.number_input("Time Step Δt (seconds)", value=50.0, step=10.0)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("Run Numerical Simulation"):
        sigma = 5.67e-8
        
        # ODE function: dT/dt = (Qin - eps * sigma * A * T^4) / (m * cp)
        def dT_dt(t, T):
            return (solar_flux - emissivity * sigma * area * (T**4)) / (mass * cp)
            
        with st.spinner("Simulating..."):
            hist_euler = ODESolver.euler(dT_dt, t0_temp, 0, t_span, dt)
            hist_rk4 = ODESolver.rk4(dT_dt, t0_temp, 0, t_span, dt)
        
        st.success("Simulation Complete!")
        
        final_euler = hist_euler.iloc[-1]['Temperature']
        final_rk4 = hist_rk4.iloc[-1]['Temperature']
        
        m1, m2 = st.columns(2)
        m1.metric("Final Temp (Euler 1st Order)", f"{final_euler:.2f} K")
        m2.metric("Final Temp (Runge-Kutta 4th Order)", f"{final_rk4:.2f} K")
        
        # Custom matplotlib theme for dark mode
        fig, ax = plt.subplots(figsize=(10, 5))
        fig.patch.set_facecolor('#0a0e17')
        ax.set_facecolor('#111827')
        ax.plot(hist_euler['time'], hist_euler['Temperature'], label='Euler Method', linestyle='--', color='#ff4b4b')
        ax.plot(hist_rk4['time'], hist_rk4['Temperature'], label='RK4 Method', linewidth=2, color='#00d2ff')
        
        ax.tick_params(colors='#e2e8f0')
        ax.xaxis.label.set_color('#e2e8f0')
        ax.yaxis.label.set_color('#e2e8f0')
        ax.title.set_color('#e2e8f0')
        
        for spine in ax.spines.values():
            spine.set_color('#334155')
            
        ax.set_xlabel("Time (seconds)")
        ax.set_ylabel("Temperature (K)")
        ax.set_title(f"Satellite Transient Cooling / Heating")
        ax.grid(True, which="both", ls="--", alpha=0.2, color='#e2e8f0')
        
        legend = ax.legend(facecolor='#111827', edgecolor='#334155')
        for text in legend.get_texts():
            text.set_color("#e2e8f0")
            
        st.pyplot(fig)
