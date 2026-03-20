import pandas as pd
import matplotlib.pyplot as plt
from root_finder import RootFinder

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
        root_b, hist_b = RootFinder.bisection(f, 1.01, 10.0)
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
        root_b, hist_b = RootFinder.bisection(f, 100.0, 1000.0)
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

def main_menu():
    """The main interface for the toolbox."""
    while True:
        print("\n==================================================")
        print("   📐 ITERATIVE METHODS: ROOT-FINDING TOOLBOX 📐   ")
        print("==================================================")
        print("Select a test case to run convergence diagnostics:")
        print("1. Compare Methods on Compressible Flow")
        print("2. Compare Methods on Implicit Heat Transfer")
        print("3. Exit Toolbox")
        
        choice = input("\nSelect an option (1-3): ")
        
        if choice == '1': 
            compare_methods_flow()
        elif choice == '2': 
            compare_methods_heat()
        elif choice == '3': 
            print("\nExiting Toolbox. Goodbye! 👋")
            break
        else: 
            print("\n❌ Invalid choice. Please type 1, 2, or 3.")
            continue
            
        # The new prompt to keep the user in the app!
        print("\n" + "="*50)
        cont = input("Would you like to run another test? (y/n): ").lower()
        if cont != 'y':
            print("\nExiting Toolbox. Goodbye! 👋")
            break

if __name__ == "__main__":
    main_menu()
