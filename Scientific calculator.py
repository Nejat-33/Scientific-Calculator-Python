
import math
import sympy
import re
from pathlib import Path
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, \
    convert_xor

transformations = (standard_transformations + (implicit_multiplication_application, convert_xor))


class FuturisticCalculator:
    def __init__(self):
        self.history_file = Path("calculation_file.txt")
        self.mode = 'radian'
        self.variables = {"pi": math.pi, "e": math.e, "ans": 0}

        # Scientific functions
        self.scientific_ops = {
            "sin": math.sin, "cos": math.cos, "tan": math.tan,
            "asin": math.asin, "acos": math.acos, "atan": math.atan,
            "log": math.log10, "ln": math.log, "sqrt": math.sqrt, "factorial": math.factorial
        }

        # Precedence Level
        self.precedence = {
            "sin": 4, "cos": 4, "tan": 4, "log": 4, "ln": 4, "sqrt": 4,
            "^": 3, "*": 2, "/": 2, "%": 2, "+": 1, "-": 1, "(": 0
        }

    def tokenize(self, expr):
        # Regex to handle numbers, decimals, words, and operators
        return re.findall(r'\d*\.\d+|\d+|[a-zA-Z]+|[+\-*/%^()!]', expr)

    def handle_variables(self, tokens):
        # Replace variable names with their stored numeric values
        return [str(self.variables[t]) if t in self.variables else t for t in tokens]

    def solve_eq(self, userinput):
        try:
            equ = userinput.replace("solve", "").strip()
            if "=" not in equ: return "Error: Missing '='"
            lhs_str, rhs_str = equ.split("=")

            x = sympy.Symbol('x')
            lhs = parse_expr(lhs_str, transformations=transformations)
            rhs = parse_expr(rhs_str, transformations=transformations)

            result = sympy.solve(lhs - rhs, x)
            return f"Solution: x = {result}"
        except Exception as e:
            return f"Error in solver: {e}"

    def solve_derivative(self, userinput):
        try:
            expr_str = userinput.replace("diff", "").strip()
            x = sympy.Symbol('x')
            expr = parse_expr(expr_str, transformations=transformations)
            result = sympy.diff(expr, x)
            return f"Derivative: {result}"
        except Exception as e:
            return f"Error in derivative: {e}"

    def shunting_yard(self, tokens):
        output = []
        stack = []
        for t in tokens:
            # If it's a number (handling decimals and integers)
            if t.replace('.', '', 1).isdigit():
                output.append(t)
            elif t in self.scientific_ops:
                stack.append(t)
            elif t == '(':
                stack.append(t)
            elif t == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                if stack: stack.pop()  # Remove '('
                if stack and stack[-1] in self.scientific_ops:
                    output.append(stack.pop())
            else:
                while stack and self.precedence.get(stack[-1], 0) >= self.precedence.get(t, 0):
                    output.append(stack.pop())
                stack.append(t)
        while stack:
            output.append(stack.pop())
        return output

    def evaluate_postfix(self, postfix_tokens):
        num_stack = []
        for token in postfix_tokens:
            # Check if token is a number
            if token.replace('.', '', 1).isdigit() or (token.startswith('-') and len(token) > 1):
                num_stack.append(float(token))
            elif token in self.scientific_ops:
                if not num_stack: continue
                val = num_stack.pop()
                if token in ['sin', 'cos', 'tan'] and self.mode == 'degree':
                    val = math.radians(val)
                res = self.scientific_ops[token](val)
                if token in ['asin', 'acos', 'atan'] and self.mode == 'degree':
                    res = math.degrees(res)
                num_stack.append(res)
            else:
                # Binary Operators
                if len(num_stack) < 2: continue
                n1 = num_stack.pop()
                n2 = num_stack.pop()
                if token == '+':
                    num_stack.append(n2 + n1)
                elif token == '-':
                    num_stack.append(n2 - n1)
                elif token == '*':
                    num_stack.append(n2 * n1)
                elif token == '/':
                    num_stack.append(n2 / n1)
                elif token == '%':
                    num_stack.append(n2 % n1)
                elif token == '^':
                    num_stack.append(n2 ** n1)

        return num_stack[0] if num_stack else 0

    def process_input(self, user_input):
        raw_input = user_input.lower().strip()

        # 1. Symbolic Commands (SymPy)
        if raw_input.startswith('solve'):
            print(self.solve_eq(raw_input))
            return
        elif raw_input.startswith('diff'):
            print(self.solve_derivative(raw_input))
            return

        # 2. Variable Assignment (e.g., radius = 10)
        if "=" in raw_input and "==" not in raw_input:
            var_name, expr = raw_input.split("=")
            var_name = var_name.strip()

            # Solve the expression on the right
            tokens = self.tokenize(expr)
            tokens = self.handle_variables(tokens)
            postfix = self.shunting_yard(tokens)
            result = self.evaluate_postfix(postfix)

            self.variables[var_name] = result
            print(f"Stored: {var_name} = {result}")
            return

        # 3. Standard Calculation
        tokens = self.tokenize(raw_input)
        tokens = self.handle_variables(tokens)
        postfix = self.shunting_yard(tokens)

        try:
            result = self.evaluate_postfix(postfix)
            print(f"Result: {result}")
            self.variables["ans"] = result
            # Log to file
            with open(self.history_file, "a") as f:
                f.write(f"{raw_input} = {result}\n")
        except Exception as e:
            print(f"Math Error: {e}")


# --- RUNNER ---
if __name__ == "__main__":
    calc = FuturisticCalculator()
    print("---  Futuristic Calculator ---")
    print("Commands: 'solve x^2=4', 'diff x^3', 'radius = 10', 'pi * radius^2'")
    print("Type 'exit' to quit. Mode: RADIAN")

    while True:
        try:
            user_in = input("\n>>> ").strip()
            if user_in.lower() in ['exit', 'quit']:
                break
            if not user_in:
                continue

            calc.process_input(user_in)
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Global Error: {e}")