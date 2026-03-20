# 🚀 Aerospace Root-Finding Toolbox

A comprehensive Python numerical methods library built from scratch to solve complex, implicit aerospace engineering equations where standard algebra fails.

---

## 🧠 The Core Concept: What is this actually doing?
In engineering, we often have equations where we cannot isolate the variable we want (e.g., we can't write `x = ...`). These are called **implicit equations**. 

To solve them, we move everything to one side of the equals sign so the equation looks like `f(x) = 0`. The value of `x` that makes the equation equal exactly zero is called the **"root"**. 

This Toolbox contains three custom-built algorithms that use different mathematical strategies to guess numbers, check the error, and automatically adjust their next guess until they find the exact root.

### The 3 Mathematical Engines:
1. **Bisection Method (The Safe Bet):** 
   * *How it works:* You give it a low guess and a high guess. It cuts the distance in half, checks which half the root is in, and repeats. 
   * *Pros/Cons:* It is slow (takes ~20 iterations), but it is mathematically guaranteed to never fail as long as your initial bounds are correct.
2. **Newton-Raphson Method (The Ferrari):** 
   * *How it works:* It uses pure calculus. It looks at the slope (the derivative) of the current guess and "slides" down the slope directly toward zero.
   * *Pros/Cons:* Blisteringly fast (usually finds the answer in 3-4 iterations), but it crashes if the slope ever hits exactly zero (a flatline).
3. **Secant Method (The Hybrid):** 
   * *How it works:* It works exactly like Newton-Raphson, but instead of requiring you to write out the complicated calculus derivative, it estimates the slope using its last two guesses.

---

## 🛠️ The Aerospace Applications

### Module 1: Compressible Flow (Area-Mach Relation)
When gas expands through a converging-diverging rocket nozzle, its speed (Mach number, $M$) is determined by how wide the nozzle is compared to the throat ($A/A^*$). 

**The Equation:**
$$ \frac{A}{A^*} = \frac{1}{M} \left[ \frac{2 + (\gamma - 1)M^2}{\gamma + 1} \right]^{\frac{\gamma + 1}{2(\gamma - 1)}} $$

Because the Mach number ($M$) is stuck inside and outside that massive exponent bracket, you cannot solve for $M$ with algebra. My code subtracts the Area Ratio from both sides and uses the algorithms to hunt down the exact Mach number that balances the equation to zero.

### Module 2: Satellite Thermal Balance
In the vacuum of space, there is no air to cool things down (no convection). Satellites only lose heat by radiating it away into space. 

**The Equation:**
$$ Q_{in} = \epsilon \sigma T^4 $$

We want to find the exact Surface Temperature ($T$) of the satellite based on how much heat from the sun ($Q_{in}$) it is absorbing. Because Temperature is raised to the 4th power (Stefan-Boltzmann law), it is a non-linear implicit equation that requires root-finding.

---

## 💻 Code Structure
* `root_finder.py` - The core mathematical engine containing the Bisection, Newton, and Secant classes.
* `main.py` - The interactive Command Line Interface (CLI) tool. It runs the user's inputs through all three algorithms simultaneously to race them against each other.
* `test_root_finder.py` - Pytest unit tests. This proves the algorithms work perfectly by testing them against known analytical solutions (like $x^2 - 4 = 0$).

## ⚙️ How to Run Locally
1. Clone this repository to your machine.
2. Install the required data science libraries:
   ```bash
   pip install pandas matplotlib pytest
