import sympy
import numpy as np

t = 4.76
ng = 1.518
beta_in = 60.1765
Rp = 7095.248
Rv = 904.752
Y = 2 * t / (Rp + Rv)
x = sympy.Symbol('x')

f_a = x / ng

# print(sympy.solve(f_a + 3, x))

f_sin = np.sin(beta_in * np.pi / 180)
f_cos = np.cos(beta_in * np.pi / 180)
f_numerator = f_sin - f_cos * x / (sympy.sqrt(1 - x ** 2))
f_denominator = f_a / sympy.sqrt(1 - f_a ** 2)
fun = f_numerator / f_denominator - Y
rootX = sympy.solveset(fun, x, domain=sympy.S.Reals)
rootX = next(iter(rootX))
# print(rootX)
beta_out = np.arcsin(rootX)
beta_out = np.degrees(beta_out)
deta_beta = beta_in - beta_out
z = np.tan(deta_beta * np.pi / 180) * (Rp + Rv)

# m = int(round(z / ps))
# print("m2: {}".format(m))