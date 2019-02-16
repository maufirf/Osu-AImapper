import pickle
import gzip
import numpy as np

def load_gz(path='mnist.pkl.gz'):
    f = gzip.open(path,'rb')
    out = pickle.load(f,encoding='latin1')
    f.close()
    return out

def load_gz_data_wrapper(path='mnist.pkl.gz'):
    tr_d, va_d, te_d = load_gz(path)
    training_inputs = [np.reshape(x, (784, 1)) for x in tr_d[0]]
    training_results = [vectorized_result(y) for y in tr_d[1]]
    training_data = (training_inputs, training_results)
    validation_inputs = [np.reshape(x, (784, 1)) for x in va_d[0]]
    validation_data = (validation_inputs, va_d[1])
    test_inputs = [np.reshape(x, (784, 1)) for x in te_d[0]]
    test_data = (test_inputs, te_d[1])
    return (training_data, validation_data, test_data)

def zip_data_tuple(tup):
    return zip(tup[0],tup[1])

def vectorized_result(j):
    e = np.zeros((10, 1))
    e[j] = 1.0
    return e
