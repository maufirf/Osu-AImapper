import numpy as np

def forwardMultiplyGate(a,b):
    return a*b

def forwardAddGate(a,b):
    return a+b

#def forwardCircuit(x,y,z):
#    q = forwardAddGate(x,y)
#    f = forwardMultiplyGate(q,z)
#    return f

#Initial Conditions
x = -2; y = 5; z = -4
q = forwardAddGate(x,y)
f = forwardMultiplyGate(q,z)

#Gradient of he MULTIPLY gate with respect to its inputs
#wrt is short for "with respect to"
derivative_f_wrt_z = q
derivative_f_wrt_q = z

#derivative of the ADD gate with respect to its inputs
derivative_q_wrt_x = 1.0
derivative_q_wrt_y = 1.0

#chain rule, calculus
derivative_f_wrt_x = derivative_q_wrt_x * derivative_f_wrt_q
derivative_f_wrt_y = derivative_q_wrt_y * derivative_f_wrt_q

#print(derivative_f_wrt_z,derivative_f_wrt_q,derivative_f_wrt_x,derivative_f_wrt_y)

#final gradient; from above: [-4,-4,3]
gradient_f_wrt_xyz = [derivative_f_wrt_x,derivative_f_wrt_y,derivative_f_wrt_z]

#let the inputs respond to the force/tug
step_size = 0.01
x = x + step_size * derivative_f_wrt_x
y = y + step_size * derivative_f_wrt_y
z = z + step_size * derivative_f_wrt_z

#Our circuit now better give higher output:
q = forwardAddGate(x,y)
f = forwardMultiplyGate(q,z)

print(q,f,gradient_f_wrt_xyz)