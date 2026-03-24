import pandas as pd
import matplotlib.pyplot as plt
from root_finder import RootFinder
from ode_solver import ODESolver

def plot_convergence(hist_b, hist_n, hist_s, title):
    """Helper function to visualize algorithm performance"""
    plt.figure(figsize=(10, 6))
    plt.plot(hist_b['iteration'], hist_b['error'], marker='o', label='Bisection', linestyle='--')
    plt.plot(hist_n['iteration'], hist_n['error'], marker='s', label='Newton-Raphson', linewidth=2)
    plt.plot(hist_s['iteration'], hist_s['error'], marker='^', label='Secant', linestyle='-.')

    plt.yscale('log')
    plt.xlabel('Iteration Number', fontsize=12)
    plt.ylabel('Absolute Error (log scale)', fontsize=12)
    plt.title(title, fontsize=14)
    plt.grid(True, which="both", ls="--", alpha=0.6)
    plt.legend(fontsize=11)
    plt.tight_layout()
    
    # block=False lets the graph open WITHOUT freezing the terminal!
    plt.show(block=False) 
    plt.pause(0.1)

def compare_methods_flow():
    """Test Case 1: Compressible Flow"""
    print("\n--- 💨 TEST CASE 1: COMPRESSIBLE FLOW ---")
    gamma = 1.4
    
    try:
        A_ratio = float(input("Enter target Area Ratio A/A* : "))
        if A_ratio < 1.0:
            print("❌ Error: Area ratio must be >= 1.0. Returning to menu...")
            return
    except ValueError:
        print("❌ Invalid input! Returning to menu...")
        return
    
    def f(M):
        if M <= 1.0: return -1.0
        return (1/M) * ((2 + (gamma - 1) * M**2) / (gamma + 1)) ** ((gamma + 1) / (2 * (gamma - 1))) - A_ratio
    
    def df(M):
        h = 1e-5
        return (f(M + h) - f(M - h)) / (2 * h)
    
    print("\n⚙️ Running Iterative Methods...")
    try:
        root_b, hist_b = RootFinder.bisection(f, 1.01, 1000.0)
        root_n, hist_n = RootFinder.newton_raphson(f, df, 2.5)
        root_s, hist_s = RootFinder.secant(f, 2.0, 3.0)
        
        print(f"\n✅ Root Found (Mach Number): {root_n:.4f}")
        print("--- Convergence Diagnostics ---")
        print(f"   Newton-Raphson: {len(hist_n)} iterations")
        print(f"   Secant:         {len(hist_s)} iterations")
        print(f"   Bisection:      {len(hist_b)} iterations")
        
        plot_convergence(hist_b, hist_n, hist_s, f"Algorithm Convergence: Area-Mach (A/A* = {A_ratio})")
    except Exception as e:
        print(f"❌ Calculation Error: {e}")

def compare_methods_heat():
    """Test Case 2: Implicit Heat Transfer"""
    print("\n--- 🛰️ TEST CASE 2: SATELLITE HEAT TRANSFER ---")
    sigma = 5.67e-8  
    emissivity = 0.8  
    
    try:
        solar_flux = float(input("Enter absorbed solar heat flux W/m^2 : "))
    except ValueError:
        print("❌ Invalid input! Returning to menu...")
        return
    
    def f(T):
        return (emissivity * sigma * T**4) - solar_flux
        
    def df(T):
        return 4 * emissivity * sigma * T**3
        
    print("\n⚙️ Running Iterative Methods...")
    try:
        root_b, hist_b = RootFinder.bisection(f, 1.0, 1e7)
        root_n, hist_n = RootFinder.newton_raphson(f, df, 300.0)
        root_s, hist_s = RootFinder.secant(f, 250.0, 350.0)
        
        print(f"\n✅ Root Found (Temperature): {root_n:.2f} K ({root_n - 273.15:.2f} °C)")
        print("--- Convergence Diagnostics ---")
        print(f" 🏎️  Newton-Raphson: {len(hist_n)} iterations")
        print(f" 🚗  Secant:         {len(hist_s)} iterations")
        print(f" 🚲  Bisection:      {len(hist_b)} iterations")
        
        plot_convergence(hist_b, hist_n, hist_s, f"Algorithm Convergence: Thermal Balance (Q = {solar_flux})")
    except Exception as e:
        print(f"❌ Calculation Error: {e}")

def airfoil_analysis():
    """Test Case 3: Airfoil Aerodynamics"""
    print("\n--- 🛩️ TEST CASE 3: AIRFOIL AERODYNAMICS ---")
    import math
    try:
        def get_input(prompt, default_val):
            val = input(prompt)
            return float(val) if val.strip() else default_val
            
        velocity = get_input("Enter Free-stream Velocity [m/s] (default 100.0): ", 100.0)
        density = get_input("Enter Air Density [kg/m^3] (default 1.225): ", 1.225)
        area = get_input("Enter Wing Area [m^2] (default 10.0): ", 10.0)
        chord = get_input("Enter Chord Length [m] (default 1.0): ", 1.0)
        Cl = get_input("Enter Coefficient of Lift (default 0.5): ", 0.5)
        Cd = get_input("Enter Coefficient of Drag (default 0.02): ", 0.02)
        Cm_ac = get_input("Enter Moment Coefficient at AC (default -0.05): ", -0.05)
        alpha_deg = get_input("Enter Angle of Attack [degrees] (default 5.0): ", 5.0)
    except ValueError:
        print("❌ Invalid input! Returning to menu...")
        return
        
    q = 0.5 * density * velocity**2
    lift = q * area * Cl
    drag = q * area * Cd
    total_force = math.sqrt(lift**2 + drag**2)
    
    alpha_rad = math.radians(alpha_deg)
    denom = (Cl * math.cos(alpha_rad) + Cd * math.sin(alpha_rad))
    
    print("\n✅ Results:")
    print(f"  Lift Force:                {lift:.2f} N")
    print(f"  Drag Force:                {drag:.2f} N")
    print(f"  Total Aerodynamic Force:   {total_force:.2f} N")
    
    if denom == 0:
        print("  Center of Pressure:        Undefined (Net normal force is zero)")
    else:
        xcp_chord_ratio = 0.25 - (Cm_ac / denom)
        xcp_position = chord * xcp_chord_ratio
        print(f"  Center of Pressure (x_cp): {xcp_position:.3f} m from LE ({xcp_chord_ratio*100:.1f}% c)")
        
    print("\n--- ⚖️ CENTER OF GRAVITY (CG) LOCATOR ---")
    calc_cg = input("Do you want to locate the CG and find Static Margin? (y/n): ").strip().lower() == 'y'
    if calc_cg:
        try:
            w_empty = get_input("  Enter Empty Weight [kg] (default 1200.0): ", 1200.0)
            arm_empty = get_input("  Enter Empty Weight Arm from LE [m] (default 1.0): ", 1.0)
            w_payload = get_input("  Enter Payload Weight [kg] (default 300.0): ", 300.0)
            arm_payload = get_input("  Enter Payload Arm from LE [m] (default 1.5): ", 1.5)
            w_fuel = get_input("  Enter Fuel Weight [kg] (default 150.0): ", 150.0)
            arm_fuel = get_input("  Enter Fuel Arm from LE [m] (default 0.8): ", 0.8)
            
            total_w = w_empty + w_payload + w_fuel
            cg_loc = ((w_empty*arm_empty) + (w_payload*arm_payload) + (w_fuel*arm_fuel)) / total_w
            sm = ((0.25*chord) - cg_loc) / chord * 100
            
            print(f"\n⚖️ CG Locator Results:")
            print(f"  Total Weight:              {total_w:.2f} kg")
            print(f"  CG Location (x_cg):        {cg_loc:.3f} m from LE")
            print(f"  Static Margin:             {sm:.1f}%")
            if sm < 0:
                print("  ⚠️ WARNING: Negative Static Margin. Aircraft is longitudinally UNSTABLE.")
            else:
                print("  ✅ Aircraft is longitudinally STABLE.")
        except ValueError:
            print("❌ Invalid input inside CG Locator!")

def transient_heating():
    """Test Case 4: Transient Heat Transfer (ODE)"""
    print("\n--- 🕰️ TEST CASE 4: TRANSIENT HEAT TRANSFER (ODE) ---")
    try:
        def get_input(prompt, default_val):
            val = input(prompt)
            return float(val) if val.strip() else default_val
            
        mass = get_input("Enter Mass [kg] (default 50.0): ", 50.0)
        cp = get_input("Enter Specific Heat [J/kg.K] (default 900.0): ", 900.0)
        area = get_input("Enter Surface Area [m^2] (default 2.0): ", 2.0)
        emissivity = get_input("Enter Emissivity (default 0.8): ", 0.8)
        solar_flux = get_input("Enter Absorbed Solar Flux [W] (default 500.0): ", 500.0)
        t0_temp = get_input("Enter Initial Temp [K] (default 200.0): ", 200.0)
        t_span = get_input("Enter Simulation Time [s] (default 10000.0): ", 10000.0)
        dt = get_input("Enter Time Step [s] (default 50.0): ", 50.0)
    except ValueError:
        print("❌ Invalid input! Returning to menu...")
        return
        
    sigma = 5.67e-8
    
    def dT_dt(t, T):
        return (solar_flux - emissivity * sigma * area * (T**4)) / (mass * cp)
        
    print("\n⚙️ Running Numerical ODE Solvers...")
    
    hist_euler = ODESolver.euler(dT_dt, t0_temp, 0, t_span, dt)
    hist_rk4 = ODESolver.rk4(dT_dt, t0_temp, 0, t_span, dt)
    
    final_euler = hist_euler.iloc[-1]['Temperature']
    final_rk4 = hist_rk4.iloc[-1]['Temperature']
    
    print("\n✅ Simulation Complete:")
    print(f"  Final Temp (Euler 1st Order):       {final_euler:.2f} K")
    print(f"  Final Temp (Runge-Kutta 4th Order): {final_rk4:.2f} K")

def main_menu():
    """The main interface for the toolbox."""
    while True:
        print("\n==================================================")
        print("   📐 ITERATIVE METHODS: ROOT-FINDING TOOLBOX 📐   ")
        print("==================================================")
        print("Select a test case to run convergence diagnostics:")
        print("1. Compare Methods on Compressible Flow")
        print("2. Compare Methods on Implicit Heat Transfer")
        print("3. Airfoil Aerodynamics Analysis")
        print("4. Transient Heat Transfer (ODE)")
        print("5. Exit Toolbox")
        
        choice = input("\nSelect an option (1-5): ")
        
        if choice == '1': 
            compare_methods_flow()
        elif choice == '2': 
            compare_methods_heat()
        elif choice == '3':
            airfoil_analysis()
        elif choice == '4':
            transient_heating()
        elif choice == '5': 
            print("\nExiting Toolbox. Goodbye! 👋")
            break
        else: 
            print("\n❌ Invalid choice. Please type 1, 2, 3, 4, or 5.")
            continue
            
        # The new prompt to keep the user in the app!
        print("\n" + "="*50)
        cont = input("Would you like to run another test? (y/n): ").lower()
        if cont != 'y':
            print("\nExiting Toolbox. Goodbye! 👋")
            break

if __name__ == "__main__":
    main_menu()
