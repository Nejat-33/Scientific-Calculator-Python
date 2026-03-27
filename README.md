# Futuristic Scientific & Symbolic Calculator

A high-performance Python CLI calculator that combines standard arithmetic with powerful symbolic mathematics. Built using the **Shunting-Yard algorithm** for expression parsing and **SymPy** for solving complex algebraic equations and derivatives.

## Core Features

### Advanced Arithmetic
- **Order of Operations:** Full support for PEMDAS/BODMAS using a custom Shunting-Yard implementation.
- **Scientific Functions:** `sin`, `cos`, `tan`, `log` (base 10), `ln` (natural log), `sqrt`, and `factorial`.
- **Trigonometry Modes:** Easily toggle between **Radians** and **Degrees**.

### Symbolic & Algebraic Engine (via SymPy)
- **Equation Solver:** Solve complex equations automatically. 
  - *Example:* `solve x^2 + 5x + 6 = 0`
- **Calculus:** Compute derivatives of functions instantly.
  - *Example:* `diff x^3 + sin(x)`
- **Implicit Multiplication:** Supports natural math syntax like `2x` instead of `2*x`.

### Memory & Variables
- **Variable Assignment:** Store results for later use. 
  - *Example:* `radius = 10` then `pi * radius^2`
- **Result Persistence:** Use the `ans` keyword to reference your last calculated result.
- **History Logging:** All successful calculations are saved to `calculation_file.txt`.

## Tech Stack
- **Language:** Python 3.10+
- **Math Engine:** `math` (Numeric) & `sympy` (Symbolic)
- **Parsing:** Regular Expressions (Regex) & Shunting-Yard Algorithm

## Getting Started

### 1. Install Dependencies
pip install sympy
### 2. Run the Calculator
python main.py

## Example Commands
Basic Math    (10 + 5) * 2 / 3^2
Assignment    x =25
Solve Algebra   solve x^2 = 64
Derivatives    diff cos(x) * x^2
Trigonometry   sin(pi/2)

## Project Structure
.
├── main.py                # Core Calculator Class & Runner
├── calculation_file.txt   # Auto-generated history log
└── README.md              # Documentation
