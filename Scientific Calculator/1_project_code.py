
import tkinter as tk
from tkinter import ttk, messagebox
import math

class ScientificCalculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Scientific Calculator")
        self.geometry("420x560")
        self.resizable(False, False)
        self.memory = 0.0
        self._build_ui()

    def _build_ui(self):
        # Entry
        self.entry = tk.Entry(self, font=("Segoe UI", 18), borderwidth=2, relief="groove", justify="right")
        self.entry.grid(row=0, column=0, columnspan=6, sticky="nsew", padx=8, pady=10, ipady=8)

        # Buttons layout (each tuple = row)
        btns = [
            ('7','8','9','/','sqrt','MC'),
            ('4','5','6','*','**','MR'),
            ('1','2','3','-','(', 'M+'),
            ('0','.','=','+',' )','M-'),
            ('sin','cos','tan','log','ln','fact'),
            ('C','CE','<-','±','exp','pi')
        ]

        for r, row in enumerate(btns, start=1):
            for c, label in enumerate(row):
                btn = ttk.Button(self, text=label, command=lambda x=label: self.on_button(x))
                btn.grid(row=r, column=c, sticky="nsew", padx=4, pady=4)

        # make grid expand evenly
        for i in range(len(btns)+1):
            self.rowconfigure(i, weight=1)
        for j in range(6):
            self.columnconfigure(j, weight=1)

    def on_button(self, label):
        try:
            if label == 'C':  # clear
                self.entry.delete(0, tk.END)
            elif label == 'CE': # same as clear (could be made to clear last entry)
                self.entry.delete(0, tk.END)
            elif label == '<-':  # backspace
                cur = self.entry.get()
                self.entry.delete(0, tk.END)
                self.entry.insert(0, cur[:-1])
            elif label == '=':
                expr = self.entry.get()
                result = self.safe_eval(expr)
                self.entry.delete(0, tk.END)
                self.entry.insert(0, str(result))
            elif label == '±':
                cur = self.entry.get()
                if cur:
                    if cur.startswith('-'):
                        self.entry.delete(0, tk.END)
                        self.entry.insert(0, cur[1:])
                    else:
                        self.entry.delete(0, tk.END)
                        self.entry.insert(0, '-' + cur)
            elif label == 'pi':
                self.entry.insert(tk.END, str(math.pi))
            elif label == 'exp':
                # scientific notation: insert 'e' and user can type exponent
                self.entry.insert(tk.END, 'e')
            elif label == 'sqrt':
                self.entry.insert(tk.END, 'sqrt(')
            elif label == 'sin':
                self.entry.insert(tk.END, 'sin(')
            elif label == 'cos':
                self.entry.insert(tk.END, 'cos(')
            elif label == 'tan':
                self.entry.insert(tk.END, 'tan(')
            elif label == 'log':
                self.entry.insert(tk.END, 'log10(')
            elif label == 'ln':
                self.entry.insert(tk.END, 'log(')
            elif label == 'fact':
                self.entry.insert(tk.END, 'fact(')
            elif label == '**':
                self.entry.insert(tk.END, '**')
            elif label == '(': 
                self.entry.insert(tk.END, '(')
            elif label == ' )':
                self.entry.insert(tk.END, ')')
            elif label == 'MC':
                self.memory = 0.0
            elif label == 'MR':
                self.entry.insert(tk.END, str(self.memory))
            elif label == 'M+':
                val = self.safe_eval(self.entry.get())
                self.memory += float(val)
            elif label == 'M-':
                val = self.safe_eval(self.entry.get())
                self.memory -= float(val)
            else:
                # digits, dot, operators
                self.entry.insert(tk.END, label)
        except Exception as e:
            messagebox.showerror("Error", f"Invalid operation: {e}")

    def safe_eval(self, expr):
        """
        Evaluate expression in a restricted environment.
        Supported names: sin, cos, tan, sqrt, log (natural), log10, pi, e, pow, fact
        Blocks obviously dangerous tokens.
        """
        if not expr:
            raise ValueError("Empty expression")
        banned = ['__','import','os','sys','subprocess','open','eval','exec']
        for b in banned:
            if b in expr:
                raise ValueError("Unsafe token in expression")

        # define allowed functions
        def fact(x):
            # allow factorial like fact(5) or fact(5.0)
            xi = int(float(x))
            if xi < 0:
                raise ValueError("Factorial of negative")
            return math.factorial(xi)

        allowed = {
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'sqrt': math.sqrt,
            'log': math.log,     # natural log
            'log10': math.log10,
            'pi': math.pi,
            'e': math.e,
            'pow': pow,
            'fact': fact,
        }

        # Evaluate using restricted globals/locals
        result = eval(expr, {"__builtins__": None}, allowed)

        # For float results that are very close to integer, show integer
        if isinstance(result, float) and abs(result - round(result)) < 1e-12:
            result = int(round(result))
        return result

if __name__ == "__main__":
    app = ScientificCalculator()
    app.mainloop()
