import numpy as np
import numpy.random as rd

# The idea is to find a way to make output has a
# higher value by finding the required force to
# the inputs.

# We think the neural nets are just a gate of functions.

def forwardMultiplyGate(x,y):
    return x*y
x=-2;y=3

'''
#The goal is to find the best tweak in each of x and y to pull output to postitive
tweak_amount = 0.01
best_out = -np.inf
best_x = x; best_y = y
for k in range(100):
    x_try = x + tweak_amount * (rd.rand() * 2 - 1)
    y_try = y + tweak_amount * (rd.rand() * 2 - 1)
    out = forwardMultiplyGate(x_try,y_try)
    if out>best_out:
        best_out = out
        best_x = x_try; best_y = y_try

print(best_out, best_x, best_y)
'''

'''
#The goal is the same but using derivative
out = forwardMultiplyGate(x,y)
h = 0.0001

xph = x+h
out2 = forwardMultiplyGate(xph,y)
x_derivative = (out2-out)/h

yph = y+h
out3 = forwardMultiplyGate(x,yph)
y_derivative = (out3-out)/h

step_size = 0.01
x = x + step_size * x_derivative
y = y + step_size * y_derivative
out_new = forwardMultiplyGate(x,y)

print(out_new)
'''

#With derivative too, but the final form
#if f(x,y) = xy, then df(x,y)/dx is y and df(x,y)/dy is x
x_gradient = y; y_gradient = x

step_size = 0.01
x += step_size * x_gradient
y += step_size * y_gradient
out_new = forwardMultiplyGate(x,y)

print(out_new)

'''
In summary:
Strat 1 : forwarding the circuit hundreds of times, result is approx
Strat 2 : forwarding the circuit only once, result is also approx
Strat 3 : No forward and the result is EXACT.
'''