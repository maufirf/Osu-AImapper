def list_rindex(li, x):
    for i in reversed(range(len(li))):
        if li[i] == x:
            return i
    raise ValueError("{} is not in list".format(x))

def np_max_elementwise(a,b):
    return (a*(a>=b))+((b>a)*b)