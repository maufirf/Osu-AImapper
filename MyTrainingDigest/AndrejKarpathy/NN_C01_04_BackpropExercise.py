import numpy as np

def sig(x):
    return 1/(1+np.exp(-x))
def sig_deriv(x):
    return sig(x)*(1-sig(x))

a = 1; b = 2; c = -3; x = -1; y = 3

q = a*x + b*y + c
f = sig(q)

df = 1.0
dq = (f * (1.0 - f)) * df

da = x * dq
dx = a * dq
db = y * dq
dy = b * dq
dc = 1.0 * dq